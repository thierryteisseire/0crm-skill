#!/usr/bin/env python3
import requests
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("ZERO_CRM_API_KEY")
BASE_URL = "https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws"

if not API_KEY:
    print("❌ Error: ZERO_CRM_API_KEY not found")
    sys.exit(1)

headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}

def create_demo_data():
    print("🚀 Creating Mockup Contacts...")
    
    contacts_data = [
        {
            "name": "Alice Freeman",
            "email": "alice@ecoflow.com",
            "company": "EcoFlow",
            "role": "CEO",
            "location": "Bristol, UK",
            "notes": "Early adopter of green energy. Interested in bulk licensing."
        },
        {
            "name": "Bob Miller",
            "email": "bob@megamart.com",
            "company": "MegaMart",
            "role": "Head of Procurement",
            "location": "Chicago, IL",
            "notes": "High volume potential. Key decision maker for Retail vertical."
        },
        {
            "name": "Charlie Zhang",
            "email": "charlie@zenith.sg",
            "company": "Zenith Systems",
            "role": "Sales Director",
            "location": "Singapore",
            "notes": "Looking for CRM migration. Referral from J. Smith."
        },
        {
            "name": "Diana Prince",
            "email": "diana@wonderworks.com",
            "company": "WonderWorks",
            "role": "Founder",
            "location": "London, UK",
            "notes": "Expanding to European markets. Highly interested in automation."
        },
        {
            "name": "Edward Norton",
            "email": "edward@skylinedesigns.com",
            "company": "Skyline Designs",
            "role": "Lead Architect",
            "location": "New York, NY",
            "notes": "Strategic partner for Urban planning projects."
        }
    ]

    response = requests.post(f"{BASE_URL}/api/contacts", headers=headers, json=contacts_data)
    if response.status_code != 201:
        print(f"❌ Failed to create contacts: {response.text}")
        return

    created_contacts = response.json().get('created', [])
    print(f"✅ Created {len(created_contacts)} contacts.")

    # Sort contacts by name to map correctly to deals
    created_contacts.sort(key=lambda x: x['name'])
    
    # Map names to IDs
    contact_map = {c['name']: c['id'] for c in created_contacts}

    print("\n🚀 Creating Mockup Deals (Linked to Contacts)...")
    
    deals_data = [
        {
            "title": "EcoFlow Enterprise Suite",
            "value": 45000,
            "stage": "Negotiation",
            "priority": "High",
            "contact_id": contact_map.get("Alice Freeman"),
            "notes": "Annual subscription for UK and EU teams."
        },
        {
            "title": "MegaMart Global Rollout",
            "value": 120000,
            "stage": "Qualified",
            "priority": "High",
            "contact_id": contact_map.get("Bob Miller"),
            "notes": "Target for Q3 implementation."
        },
        {
            "title": "Zenith CRM Integration",
            "value": 15000,
            "stage": "Proposal Sent",
            "priority": "Medium",
            "contact_id": contact_map.get("Charlie Zhang"),
            "notes": "Technical assessment in progress."
        },
        {
            "title": "WonderWorks Supply Chain",
            "value": 60000,
            "stage": "Lead",
            "priority": "High",
            "contact_id": contact_map.get("Diana Prince"),
            "notes": "Initial discovery call scheduled."
        },
        {
            "title": "Skyline Office Design",
            "value": 25000,
            "stage": "Closed Won",
            "priority": "Medium",
            "contact_id": contact_map.get("Edward Norton"),
            "notes": "Contract signed on 2024-02-05."
        }
    ]

    response = requests.post(f"{BASE_URL}/api/deals", headers=headers, json=deals_data)
    if response.status_code != 201:
        print(f"❌ Failed to create deals: {response.text}")
        return

    created_deals = response.json().get('created', [])
    print(f"✅ Created {len(created_deals)} deals.")
    
    print("\n🎉 Demo data created successfully!")
    print("Run '0crm contacts list' or '0crm deals list' to verify.")

if __name__ == "__main__":
    create_demo_data()
