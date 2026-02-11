#!/usr/bin/env python3
"""
Pipeline Report Example for Zero CRM API

Generates sales pipeline reports with:
- Total pipeline value by stage
- Win rate analysis
- Average deal size
- Priority breakdown
- Contact engagement metrics

Usage:
    python3 pipeline_report.py
"""

import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import sys

# Load environment variables
load_dotenv()

API_KEY = os.getenv("ZERO_CRM_API_KEY")
BASE_URL = "https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws"

if not API_KEY:
    print("❌ Error: ZERO_CRM_API_KEY not found in environment variables")
    sys.exit(1)

headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}


def print_separator(title):
    """Print a formatted section separator."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def fetch_deals():
    """Fetch all deals from the API."""
    try:
        response = requests.get(f"{BASE_URL}/api/deals", headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching deals: {e}")
        return []


def fetch_contacts():
    """Fetch all contacts from the API."""
    try:
        response = requests.get(f"{BASE_URL}/api/contacts", headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching contacts: {e}")
        return []


def pipeline_by_stage(deals):
    """Calculate pipeline value by stage."""
    print_separator("Pipeline Value by Stage")

    stages = {}
    for deal in deals:
        stage = deal.get('stage', 'Unknown')
        value = deal.get('value', 0)

        if stage not in stages:
            stages[stage] = {'count': 0, 'value': 0}

        stages[stage]['count'] += 1
        stages[stage]['value'] += value

    # Sort by value descending
    sorted_stages = sorted(stages.items(), key=lambda x: x[1]['value'], reverse=True)

    total_value = sum(s[1]['value'] for s in sorted_stages)
    total_count = sum(s[1]['count'] for s in sorted_stages)

    for stage, data in sorted_stages:
        percentage = (data['value'] / total_value * 100) if total_value > 0 else 0
        print(f"{stage:<20} {data['count']:>3} deals    ${data['value']:>12,}    {percentage:>5.1f}%")

    print(f"{'-'*70}")
    print(f"{'TOTAL':<20} {total_count:>3} deals    ${total_value:>12,}    100.0%")

    return stages


def win_rate_analysis(deals):
    """Calculate win rate metrics."""
    print_separator("Win Rate Analysis")

    total = len(deals)
    won = len([d for d in deals if d.get('stage') == 'Closed Won'])
    lost = len([d for d in deals if d.get('stage') == 'Closed Lost'])
    active = total - won - lost

    win_rate = (won / (won + lost) * 100) if (won + lost) > 0 else 0

    won_value = sum(d.get('value', 0) for d in deals if d.get('stage') == 'Closed Won')
    lost_value = sum(d.get('value', 0) for d in deals if d.get('stage') == 'Closed Lost')
    active_value = sum(d.get('value', 0) for d in deals if d.get('stage') not in ['Closed Won', 'Closed Lost'])

    print(f"Total Deals:        {total:>6}")
    print(f"Won:                {won:>6}    ${won_value:>12,}")
    print(f"Lost:               {lost:>6}    ${lost_value:>12,}")
    print(f"Active:             {active:>6}    ${active_value:>12,}")
    print(f"\n{'Win Rate:':<20} {win_rate:>6.1f}%")

    return {
        'total': total,
        'won': won,
        'lost': lost,
        'active': active,
        'win_rate': win_rate
    }


def priority_breakdown(deals):
    """Analyze deals by priority."""
    print_separator("Priority Breakdown")

    priorities = {}
    for deal in deals:
        priority = deal.get('priority', 'Not Set')
        value = deal.get('value', 0)

        if priority not in priorities:
            priorities[priority] = {'count': 0, 'value': 0}

        priorities[priority]['count'] += 1
        priorities[priority]['value'] += value

    # Define priority order
    priority_order = ['High', 'Medium', 'Low', 'Not Set']

    for priority in priority_order:
        if priority in priorities:
            data = priorities[priority]
            print(f"{priority:<15} {data['count']:>3} deals    ${data['value']:>12,}")


def average_deal_metrics(deals):
    """Calculate average deal metrics."""
    print_separator("Average Deal Metrics")

    if not deals:
        print("No deals found")
        return

    total_value = sum(d.get('value', 0) for d in deals)
    avg_value = total_value / len(deals) if deals else 0

    # Median deal value
    values = sorted([d.get('value', 0) for d in deals])
    median_idx = len(values) // 2
    median_value = values[median_idx] if values else 0

    # Largest deal
    max_deal = max(deals, key=lambda x: x.get('value', 0), default=None)

    print(f"Average Deal Size:  ${avg_value:>12,.2f}")
    print(f"Median Deal Size:   ${median_value:>12,}")

    if max_deal:
        print(f"\nLargest Deal:")
        print(f"  {max_deal['title']}")
        print(f"  Value: ${max_deal.get('value', 0):,}")
        print(f"  Stage: {max_deal.get('stage', 'Unknown')}")


def contact_engagement(contacts, deals):
    """Analyze contact engagement metrics."""
    print_separator("Contact Engagement")

    total_contacts = len(contacts)

    # Count contacts with deals
    contact_ids_with_deals = set(d.get('contact_id') for d in deals if d.get('contact_id'))
    engaged_contacts = len(contact_ids_with_deals)

    engagement_rate = (engaged_contacts / total_contacts * 100) if total_contacts > 0 else 0

    print(f"Total Contacts:     {total_contacts:>6}")
    print(f"With Active Deals:  {engaged_contacts:>6}")
    print(f"Engagement Rate:    {engagement_rate:>6.1f}%")

    # Top companies by deal count
    companies = {}
    for contact in contacts:
        company = contact.get('company', 'Unknown')
        if company not in companies:
            companies[company] = 0
        companies[company] += 1

    print(f"\nTop Companies by Contact Count:")
    sorted_companies = sorted(companies.items(), key=lambda x: x[1], reverse=True)
    for company, count in sorted_companies[:5]:
        print(f"  {company:<30} {count:>3} contacts")


def forecast_analysis(deals):
    """Forecast upcoming revenue."""
    print_separator("Revenue Forecast")

    # Calculate revenue by stage probability
    stage_probability = {
        'Lead': 0.1,
        'Qualified': 0.25,
        'Proposal Sent': 0.5,
        'Negotiation': 0.75,
        'Closed Won': 1.0,
        'Closed Lost': 0.0
    }

    weighted_pipeline = 0
    active_pipeline = 0

    for deal in deals:
        stage = deal.get('stage', 'Unknown')
        value = deal.get('value', 0)

        if stage not in ['Closed Won', 'Closed Lost']:
            active_pipeline += value
            probability = stage_probability.get(stage, 0.3)  # Default 30%
            weighted_pipeline += value * probability

    print(f"Active Pipeline:         ${active_pipeline:>12,}")
    print(f"Weighted Forecast:       ${weighted_pipeline:>12,.2f}")
    print(f"\n(Based on stage-weighted probability)")


def generate_report():
    """Generate complete pipeline report."""
    print("\n" + "="*70)
    print(f"{'ZERO CRM PIPELINE REPORT':^70}")
    print(f"{'Generated: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'):^70}")
    print("="*70)

    # Fetch data
    deals = fetch_deals()
    contacts = fetch_contacts()

    if not deals and not contacts:
        print("\n⚠️  No data found in CRM")
        return

    # Generate report sections
    pipeline_by_stage(deals)
    win_rate_analysis(deals)
    priority_breakdown(deals)
    average_deal_metrics(deals)
    forecast_analysis(deals)
    contact_engagement(contacts, deals)

    print_separator("✅ Report Generated Successfully")

    print("\n💡 Tips:")
    print("   • Review high-priority deals in Negotiation stage")
    print("   • Follow up with engaged contacts")
    print("   • Focus on stages with highest conversion rates")


def main():
    """Run the pipeline report."""
    try:
        generate_report()
    except Exception as e:
        print(f"\n❌ Error generating report: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
