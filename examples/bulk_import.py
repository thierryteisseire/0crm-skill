#!/usr/bin/env python3
"""
Bulk Import Example for Zero CRM API

Demonstrates:
- Reading contacts from CSV
- Batch importing contacts
- Reading deals from CSV
- Batch importing deals
- Error handling for bulk operations

Usage:
    python3 bulk_import.py contacts.csv deals.csv
"""

import requests
import os
import csv
import sys
from dotenv import load_dotenv

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
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def read_contacts_csv(filename):
    """Read contacts from CSV file."""
    contacts = []

    if not os.path.exists(filename):
        print(f"❌ File not found: {filename}")
        return contacts

    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is 1)
            # Required field validation
            if not row.get("name"):
                print(f"⚠️  Skipping row {row_num}: Missing required field 'name'")
                continue

            contact = {
                "name": row["name"].strip(),
                "email": row.get("email", "").strip(),
                "phone": row.get("phone", "").strip(),
                "company": row.get("company", "").strip(),
                "role": row.get("role", "").strip(),
                "location": row.get("location", "").strip(),
                "notes": row.get("notes", "").strip()
            }

            # Remove empty fields
            contact = {k: v for k, v in contact.items() if v}
            contacts.append(contact)

    return contacts


def read_deals_csv(filename):
    """Read deals from CSV file."""
    deals = []

    if not os.path.exists(filename):
        print(f"❌ File not found: {filename}")
        return deals

    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row_num, row in enumerate(reader, start=2):
            # Required field validation
            if not row.get("title"):
                print(f"⚠️  Skipping row {row_num}: Missing required field 'title'")
                continue

            if not row.get("stage"):
                print(f"⚠️  Skipping row {row_num}: Missing required field 'stage'")
                continue

            deal = {
                "title": row["title"].strip(),
                "stage": row["stage"].strip(),
                "value": float(row.get("value", 0)) if row.get("value") else 0,
                "priority": row.get("priority", "").strip(),
                "notes": row.get("notes", "").strip()
            }

            # Remove empty fields
            deal = {k: v for k, v in deal.items() if v}
            deals.append(deal)

    return deals


def bulk_import_contacts(contacts):
    """Import contacts in bulk."""
    print_separator(f"Importing {len(contacts)} Contacts")

    if not contacts:
        print("⚠️  No contacts to import")
        return

    try:
        response = requests.post(
            f"{BASE_URL}/api/contacts",
            headers=headers,
            json=contacts
        )

        if response.status_code == 201:
            result = response.json()
            created = result.get("created", [])
            skipped = result.get("skipped", [])

            print(f"✅ Successfully imported {len(created)} contact(s)")

            if skipped:
                print(f"⚠️  Skipped {len(skipped)} contact(s)")

            # Show sample of created contacts
            if created:
                print("\n📇 Sample of created contacts:")
                for contact in created[:3]:  # Show first 3
                    print(f"   • {contact['name']} ({contact.get('email', 'No email')})")

                if len(created) > 3:
                    print(f"   ... and {len(created) - 3} more")

            return created
        else:
            print(f"❌ Import failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return []

    except Exception as e:
        print(f"❌ Error during import: {e}")
        return []


def bulk_import_deals(deals):
    """Import deals in bulk."""
    print_separator(f"Importing {len(deals)} Deals")

    if not deals:
        print("⚠️  No deals to import")
        return

    try:
        response = requests.post(
            f"{BASE_URL}/api/deals",
            headers=headers,
            json=deals
        )

        if response.status_code == 201:
            result = response.json()
            created = result.get("created", [])
            skipped = result.get("skipped", [])

            print(f"✅ Successfully imported {len(created)} deal(s)")

            if skipped:
                print(f"⚠️  Skipped {len(skipped)} deal(s)")

            # Show sample of created deals
            if created:
                print("\n💼 Sample of created deals:")
                total_value = 0
                for deal in created[:3]:  # Show first 3
                    value = deal.get('value', 0)
                    total_value += value
                    print(f"   • {deal['title']} - ${value:,} ({deal['stage']})")

                if len(created) > 3:
                    print(f"   ... and {len(created) - 3} more")

                # Calculate total value
                for deal in created[3:]:
                    total_value += deal.get('value', 0)

                print(f"\n💰 Total pipeline value: ${total_value:,}")

            return created
        else:
            print(f"❌ Import failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return []

    except Exception as e:
        print(f"❌ Error during import: {e}")
        return []


def create_sample_contacts_csv():
    """Create a sample contacts CSV file."""
    filename = "sample_contacts.csv"

    sample_data = [
        {
            "name": "John Smith",
            "email": "john.smith@techcorp.com",
            "phone": "+1-555-0101",
            "company": "TechCorp",
            "role": "CEO",
            "location": "New York, NY",
            "notes": "Interested in enterprise plan"
        },
        {
            "name": "Sarah Johnson",
            "email": "sarah@startup.io",
            "phone": "+1-555-0102",
            "company": "Startup Inc",
            "role": "CTO",
            "location": "San Francisco, CA",
            "notes": "Met at conference"
        },
        {
            "name": "Michael Chen",
            "email": "mchen@innovate.com",
            "phone": "+1-555-0103",
            "company": "Innovate LLC",
            "role": "VP Sales",
            "location": "Austin, TX",
            "notes": "Referral from John"
        }
    ]

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ["name", "email", "phone", "company", "role", "location", "notes"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sample_data)

    print(f"✅ Created sample file: {filename}")
    return filename


def create_sample_deals_csv():
    """Create a sample deals CSV file."""
    filename = "sample_deals.csv"

    sample_data = [
        {
            "title": "Enterprise Contract - TechCorp",
            "value": "50000",
            "stage": "Proposal Sent",
            "priority": "High",
            "notes": "Annual subscription"
        },
        {
            "title": "Startup Package - Startup Inc",
            "value": "10000",
            "stage": "Qualified",
            "priority": "Medium",
            "notes": "Monthly plan"
        },
        {
            "title": "Growth Plan - Innovate LLC",
            "value": "25000",
            "stage": "Negotiation",
            "priority": "High",
            "notes": "Quarterly contract"
        }
    ]

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ["title", "value", "stage", "priority", "notes"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sample_data)

    print(f"✅ Created sample file: {filename}")
    return filename


def main():
    """Run bulk import operations."""
    print("\n🚀 Zero CRM API - Bulk Import Example")

    # Check command line arguments
    if len(sys.argv) > 1:
        contacts_file = sys.argv[1]
        deals_file = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        print("\n⚠️  No CSV files provided. Creating sample files...")
        contacts_file = create_sample_contacts_csv()
        deals_file = create_sample_deals_csv()
        print("\n💡 You can now run:")
        print(f"   python3 {sys.argv[0]} {contacts_file} {deals_file}")
        print("\nProceeding with sample files...\n")

    # Import contacts
    if contacts_file:
        print_separator(f"Reading Contacts from {contacts_file}")
        contacts = read_contacts_csv(contacts_file)
        print(f"Found {len(contacts)} valid contact(s)")

        if contacts:
            bulk_import_contacts(contacts)

    # Import deals
    if deals_file:
        print_separator(f"Reading Deals from {deals_file}")
        deals = read_deals_csv(deals_file)
        print(f"Found {len(deals)} valid deal(s)")

        if deals:
            bulk_import_deals(deals)

    print_separator("✅ Bulk Import Completed")
    print("\n💡 Tips:")
    print("   • Use bulk import for batches of 10-1000 records")
    print("   • Validate CSV data before import")
    print("   • Check the 'skipped' array for failed imports")


if __name__ == "__main__":
    main()
