#!/usr/bin/env python3
"""
Basic Operations Example for Zero CRM API

Demonstrates:
- Creating contacts
- Listing contacts
- Updating contacts
- Deleting contacts
- Creating deals
- Updating deal stages

Usage:
    python3 basic_operations.py
"""

import requests
import os
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

API_KEY = os.getenv("ZERO_CRM_API_KEY")
BASE_URL = "https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws"

if not API_KEY:
    print("❌ Error: ZERO_CRM_API_KEY not found in environment variables")
    print("Please set it in your .env file or export it:")
    print("  export ZERO_CRM_API_KEY=zero_your_key_here")
    sys.exit(1)

headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}


def print_separator(title):
    """Print a formatted section separator."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def test_health():
    """Test API health check."""
    print_separator("1. Health Check")

    response = requests.get(f"{BASE_URL}/api/health")
    health = response.json()

    print(f"Status: {health['status']}")
    print(f"Platform: {health['platform']}")


def create_contact():
    """Create a new contact."""
    print_separator("2. Create Contact")

    new_contact = {
        "name": "Alice Johnson",
        "email": "alice@techstartup.com",
        "phone": "+1-555-0100",
        "company": "Tech Startup Inc",
        "role": "CTO",
        "location": "San Francisco, CA",
        "notes": "Met at TechCrunch Disrupt 2024"
    }

    response = requests.post(
        f"{BASE_URL}/api/contacts",
        headers=headers,
        json=new_contact
    )

    if response.status_code == 201:
        result = response.json()
        contact = result.get("created", [{}])[0]
        print(f"✅ Created contact: {contact['name']}")
        print(f"   ID: {contact['id']}")
        print(f"   Email: {contact['email']}")
        print(f"   Company: {contact['company']}")
        return contact['id']
    else:
        print(f"❌ Failed to create contact: {response.text}")
        return None


def list_contacts():
    """List all contacts."""
    print_separator("3. List All Contacts")

    response = requests.get(f"{BASE_URL}/api/contacts", headers=headers)

    if response.status_code == 200:
        contacts = response.json()
        print(f"Found {len(contacts)} contact(s):\n")

        for contact in contacts:
            print(f"📇 {contact['name']}")
            print(f"   Email: {contact.get('email', 'N/A')}")
            print(f"   Company: {contact.get('company', 'N/A')}")
            print(f"   Role: {contact.get('role', 'N/A')}")
            print()

        return contacts
    else:
        print(f"❌ Failed to list contacts: {response.text}")
        return []


def update_contact(contact_id):
    """Update a contact."""
    print_separator("4. Update Contact")

    updates = {
        "role": "VP Engineering",
        "notes": "Promoted to VP Engineering in Q1 2024"
    }

    response = requests.patch(
        f"{BASE_URL}/api/contacts/{contact_id}",
        headers=headers,
        json=updates
    )

    if response.status_code == 200:
        updated = response.json()
        print(f"✅ Updated contact: {updated['name']}")
        print(f"   New Role: {updated['role']}")
        print(f"   Notes: {updated['notes']}")
    else:
        print(f"❌ Failed to update contact: {response.text}")


def create_deal(contact_id):
    """Create a new deal."""
    print_separator("5. Create Deal")

    new_deal = {
        "title": "Enterprise License - Tech Startup Inc",
        "value": 75000,
        "stage": "Proposal Sent",
        "priority": "High",
        "contact_id": contact_id,
        "notes": "Annual contract, 50 seats"
    }

    response = requests.post(
        f"{BASE_URL}/api/deals",
        headers=headers,
        json=new_deal
    )

    if response.status_code == 201:
        result = response.json()
        deal = result.get("created", [{}])[0]
        print(f"✅ Created deal: {deal['title']}")
        print(f"   ID: {deal['id']}")
        print(f"   Value: ${deal['value']:,}")
        print(f"   Stage: {deal['stage']}")
        print(f"   Priority: {deal['priority']}")
        return deal['id']
    else:
        print(f"❌ Failed to create deal: {response.text}")
        return None


def update_deal_stage(deal_id):
    """Update a deal's stage."""
    print_separator("6. Update Deal Stage")

    updates = {
        "stage": "Negotiation",
        "notes": "Contract review in progress, legal approval pending"
    }

    response = requests.patch(
        f"{BASE_URL}/api/deals/{deal_id}",
        headers=headers,
        json=updates
    )

    if response.status_code == 200:
        updated = response.json()
        print(f"✅ Updated deal: {updated['title']}")
        print(f"   New Stage: {updated['stage']}")
        print(f"   Notes: {updated['notes']}")
    else:
        print(f"❌ Failed to update deal: {response.text}")


def list_deals():
    """List all deals."""
    print_separator("7. List All Deals")

    response = requests.get(f"{BASE_URL}/api/deals", headers=headers)

    if response.status_code == 200:
        deals = response.json()
        print(f"Found {len(deals)} deal(s):\n")

        for deal in deals:
            print(f"💼 {deal['title']}")
            print(f"   Value: ${deal.get('value', 0):,}")
            print(f"   Stage: {deal['stage']}")
            print(f"   Priority: {deal.get('priority', 'N/A')}")
            print()

        return deals
    else:
        print(f"❌ Failed to list deals: {response.text}")
        return []


def delete_contact(contact_id):
    """Delete a contact."""
    print_separator("8. Delete Contact")

    response = requests.delete(
        f"{BASE_URL}/api/contacts/{contact_id}",
        headers=headers
    )

    if response.status_code == 200:
        result = response.json()
        print(f"✅ {result['message']}")
    else:
        print(f"❌ Failed to delete contact: {response.text}")


def delete_deal(deal_id):
    """Delete a deal."""
    print_separator("9. Delete Deal")

    response = requests.delete(
        f"{BASE_URL}/api/deals/{deal_id}",
        headers=headers
    )

    if response.status_code == 200:
        result = response.json()
        print(f"✅ {result['message']}")
    else:
        print(f"❌ Failed to delete deal: {response.text}")


def main():
    """Run all basic operations."""
    print("\n🚀 Zero CRM API - Basic Operations Example")

    try:
        # 1. Health check
        test_health()

        # 2. Create a contact
        contact_id = create_contact()
        if not contact_id:
            print("❌ Stopping due to contact creation failure")
            return

        # 3. List contacts
        list_contacts()

        # 4. Update the contact
        update_contact(contact_id)

        # 5. Create a deal
        deal_id = create_deal(contact_id)
        if not deal_id:
            print("❌ Stopping due to deal creation failure")
            return

        # 6. Update deal stage
        update_deal_stage(deal_id)

        # 7. List deals
        list_deals()

        # 8. Cleanup: Delete deal
        delete_deal(deal_id)

        # 9. Cleanup: Delete contact
        delete_contact(contact_id)

        print_separator("✅ All Operations Completed Successfully")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
