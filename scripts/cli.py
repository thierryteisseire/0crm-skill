#!/usr/bin/env python3
"""
Zero CRM CLI Tool

Command-line interface for Zero CRM API operations.

Usage:
    0crm contacts list
    0crm contacts create --name "John Doe" --email "john@example.com"
    0crm deals list --stage "Negotiation"
    0crm profile
    0crm test

Commands:
    contacts    Manage contacts
    deals       Manage deals
    profile     Show user profile
    test        Test API connection
"""

import sys
import argparse
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = "https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws"

def get_headers():
    """Get authenticated headers."""
    api_key = os.getenv("ZERO_CRM_API_KEY")
    if not api_key:
        print("❌ Error: ZERO_CRM_API_KEY not found")
        print("Set it in .env file or:")
        print("  export ZERO_CRM_API_KEY=zero_your_key_here")
        sys.exit(1)
    return {"x-api-key": api_key, "Content-Type": "application/json"}


def format_contact(contact):
    """Format contact for display."""
    print(f"\n📇 {contact['name']}")
    print(f"   ID:       {contact['id']}")
    if contact.get('email'):
        print(f"   Email:    {contact['email']}")
    if contact.get('phone'):
        print(f"   Phone:    {contact['phone']}")
    if contact.get('company'):
        print(f"   Company:  {contact['company']}")
    if contact.get('role'):
        print(f"   Role:     {contact['role']}")
    if contact.get('location'):
        print(f"   Location: {contact['location']}")
    if contact.get('notes'):
        print(f"   Notes:    {contact['notes']}")


def format_deal(deal):
    """Format deal for display."""
    print(f"\n💼 {deal['title']}")
    print(f"   ID:       {deal['id']}")
    if deal.get('value'):
        print(f"   Value:    ${deal['value']:,}")
    print(f"   Stage:    {deal['stage']}")
    if deal.get('priority'):
        print(f"   Priority: {deal['priority']}")
    if deal.get('contact_id'):
        print(f"   Contact:  {deal['contact_id']}")
    if deal.get('notes'):
        print(f"   Notes:    {deal['notes']}")


def cmd_contacts_list(args):
    """List all contacts."""
    response = requests.get(f"{BASE_URL}/api/contacts", headers=get_headers())

    if response.status_code == 200:
        contacts = response.json()
        print(f"\nFound {len(contacts)} contact(s):")

        for contact in contacts:
            format_contact(contact)
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        sys.exit(1)


def cmd_contacts_create(args):
    """Create a new contact."""
    contact = {"name": args.name}

    if args.email:
        contact["email"] = args.email
    if args.phone:
        contact["phone"] = args.phone
    if args.company:
        contact["company"] = args.company
    if args.role:
        contact["role"] = args.role
    if args.location:
        contact["location"] = args.location
    if args.notes:
        contact["notes"] = args.notes

    response = requests.post(
        f"{BASE_URL}/api/contacts",
        headers=get_headers(),
        json=contact
    )

    if response.status_code == 201:
        result = response.json()
        created = result.get('created', [{}])[0]
        print("✅ Contact created successfully:")
        format_contact(created)
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        sys.exit(1)


def cmd_contacts_delete(args):
    """Delete a contact."""
    response = requests.delete(
        f"{BASE_URL}/api/contacts/{args.id}",
        headers=get_headers()
    )

    if response.status_code == 200:
        result = response.json()
        print(f"✅ {result['message']}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        sys.exit(1)


def cmd_deals_list(args):
    """List all deals."""
    response = requests.get(f"{BASE_URL}/api/deals", headers=get_headers())

    if response.status_code == 200:
        deals = response.json()

        # Filter by stage if provided
        if args.stage:
            deals = [d for d in deals if d.get('stage') == args.stage]

        print(f"\nFound {len(deals)} deal(s):")

        for deal in deals:
            format_deal(deal)

        # Show total value
        total_value = sum(d.get('value', 0) for d in deals)
        print(f"\n💰 Total value: ${total_value:,}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        sys.exit(1)


def cmd_deals_create(args):
    """Create a new deal."""
    deal = {
        "title": args.title,
        "stage": args.stage
    }

    if args.value:
        deal["value"] = args.value
    if args.priority:
        deal["priority"] = args.priority
    if args.contact_id:
        deal["contact_id"] = args.contact_id
    if args.notes:
        deal["notes"] = args.notes

    response = requests.post(
        f"{BASE_URL}/api/deals",
        headers=get_headers(),
        json=deal
    )

    if response.status_code == 201:
        result = response.json()
        created = result.get('created', [{}])[0]
        print("✅ Deal created successfully:")
        format_deal(created)
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        sys.exit(1)


def cmd_deals_update(args):
    """Update a deal."""
    updates = {}

    if args.title:
        updates["title"] = args.title
    if args.stage:
        updates["stage"] = args.stage
    if args.value is not None:
        updates["value"] = args.value
    if args.priority:
        updates["priority"] = args.priority
    if args.notes:
        updates["notes"] = args.notes

    if not updates:
        print("❌ No updates provided")
        sys.exit(1)

    response = requests.patch(
        f"{BASE_URL}/api/deals/{args.id}",
        headers=get_headers(),
        json=updates
    )

    if response.status_code == 200:
        updated = response.json()
        print("✅ Deal updated successfully:")
        format_deal(updated)
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        sys.exit(1)


def cmd_deals_delete(args):
    """Delete a deal."""
    response = requests.delete(
        f"{BASE_URL}/api/deals/{args.id}",
        headers=get_headers()
    )

    if response.status_code == 200:
        result = response.json()
        print(f"✅ {result['message']}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        sys.exit(1)


def cmd_profile(args):
    """Show user profile."""
    response = requests.get(f"{BASE_URL}/api/user/profile", headers=get_headers())

    if response.status_code == 200:
        profile = response.json()
        print("\n👤 User Profile")
        print(f"   ID:       {profile['id']}")
        print(f"   Email:    {profile['email']}")
        print(f"   API Key:  {profile['apiKey'][:10]}...{profile['apiKey'][-5:]}")
        print(f"   Created:  {profile.get('created_at', 'N/A')}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        sys.exit(1)


def cmd_test(args):
    """Test API connection."""
    print("\n🔍 Testing Zero CRM API Connection...\n")

    # Test 1: Health check
    print("1. Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/api/health")

    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Health check passed: {data}")
    else:
        print(f"   ❌ Health check failed: {response.status_code}")
        sys.exit(1)

    # Test 2: Authentication
    print("\n2. Testing authentication...")
    response = requests.get(f"{BASE_URL}/api/user/profile", headers=get_headers())

    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Authentication successful")
        print(f"      User: {data.get('email', 'N/A')}")
    else:
        print(f"   ❌ Authentication failed: {response.status_code}")
        sys.exit(1)

    print("\n✅ All tests passed! API is working correctly.")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Zero CRM CLI Tool",
        epilog="For more information, visit: https://github.com/thierryteisseire/0crm-skill"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Contacts commands
    contacts_parser = subparsers.add_parser("contacts", help="Manage contacts")
    contacts_sub = contacts_parser.add_subparsers(dest="subcommand")

    # contacts list
    contacts_sub.add_parser("list", help="List all contacts")

    # contacts create
    create_parser = contacts_sub.add_parser("create", help="Create a contact")
    create_parser.add_argument("--name", required=True, help="Contact name")
    create_parser.add_argument("--email", help="Email address")
    create_parser.add_argument("--phone", help="Phone number")
    create_parser.add_argument("--company", help="Company name")
    create_parser.add_argument("--role", help="Job role")
    create_parser.add_argument("--location", help="Location")
    create_parser.add_argument("--notes", help="Notes")

    # contacts delete
    delete_contact_parser = contacts_sub.add_parser("delete", help="Delete a contact")
    delete_contact_parser.add_argument("id", help="Contact ID")

    # Deals commands
    deals_parser = subparsers.add_parser("deals", help="Manage deals")
    deals_sub = deals_parser.add_subparsers(dest="subcommand")

    # deals list
    list_deals_parser = deals_sub.add_parser("list", help="List all deals")
    list_deals_parser.add_argument("--stage", help="Filter by stage")

    # deals create
    create_deal_parser = deals_sub.add_parser("create", help="Create a deal")
    create_deal_parser.add_argument("--title", required=True, help="Deal title")
    create_deal_parser.add_argument("--stage", required=True, help="Deal stage")
    create_deal_parser.add_argument("--value", type=float, help="Deal value")
    create_deal_parser.add_argument("--priority", help="Priority (Low/Medium/High)")
    create_deal_parser.add_argument("--contact-id", help="Associated contact ID")
    create_deal_parser.add_argument("--notes", help="Notes")

    # deals update
    update_deal_parser = deals_sub.add_parser("update", help="Update a deal")
    update_deal_parser.add_argument("id", help="Deal ID")
    update_deal_parser.add_argument("--title", help="New title")
    update_deal_parser.add_argument("--stage", help="New stage")
    update_deal_parser.add_argument("--value", type=float, help="New value")
    update_deal_parser.add_argument("--priority", help="New priority")
    update_deal_parser.add_argument("--notes", help="New notes")

    # deals delete
    delete_deal_parser = deals_sub.add_parser("delete", help="Delete a deal")
    delete_deal_parser.add_argument("id", help="Deal ID")

    # Other commands
    subparsers.add_parser("profile", help="Show user profile")
    subparsers.add_parser("test", help="Test API connection")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Route to command handlers
    try:
        if args.command == "contacts":
            if args.subcommand == "list":
                cmd_contacts_list(args)
            elif args.subcommand == "create":
                cmd_contacts_create(args)
            elif args.subcommand == "delete":
                cmd_contacts_delete(args)
            else:
                contacts_parser.print_help()

        elif args.command == "deals":
            if args.subcommand == "list":
                cmd_deals_list(args)
            elif args.subcommand == "create":
                cmd_deals_create(args)
            elif args.subcommand == "update":
                cmd_deals_update(args)
            elif args.subcommand == "delete":
                cmd_deals_delete(args)
            else:
                deals_parser.print_help()

        elif args.command == "profile":
            cmd_profile(args)

        elif args.command == "test":
            cmd_test(args)

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(130)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
