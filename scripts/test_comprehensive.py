#!/usr/bin/env python3
"""
Comprehensive Test Suite for Zero CRM API

Tests all major functionality:
- Health check
- Contact CRUD operations
- Deal CRUD operations
- Bulk operations
- User profile
- Error handling

Usage:
    python3 test_comprehensive.py
"""

import requests
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("ZERO_CRM_API_KEY")
BASE_URL = "https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws"

if not API_KEY:
    print("❌ Error: ZERO_CRM_API_KEY not found in environment variables")
    print("Set it in .env file or export ZERO_CRM_API_KEY=your_key_here")
    sys.exit(1)

headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}

# Test results tracking
tests_passed = 0
tests_failed = 0


def print_test(name):
    """Print test name."""
    print(f"\n{'='*70}")
    print(f"TEST: {name}")
    print(f"{'='*70}")


def pass_test(message=""):
    """Mark test as passed."""
    global tests_passed
    tests_passed += 1
    print(f"✅ PASSED {f'- {message}' if message else ''}")


def fail_test(message=""):
    """Mark test as failed."""
    global tests_failed
    tests_failed += 1
    print(f"❌ FAILED {f'- {message}' if message else ''}")


def test_health_check():
    """Test health check endpoint."""
    print_test("Health Check (No Auth)")

    try:
        response = requests.get(f"{BASE_URL}/api/health")

        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'ok' and data.get('platform') == 'Zero CRM':
                pass_test(f"Health check successful: {data}")
            else:
                fail_test(f"Unexpected response: {data}")
        else:
            fail_test(f"Status code {response.status_code}")

    except Exception as e:
        fail_test(f"Exception: {e}")


def test_user_profile():
    """Test user profile endpoint."""
    print_test("Get User Profile")

    try:
        response = requests.get(
            f"{BASE_URL}/api/user/profile",
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            if 'id' in data and 'email' in data and 'apiKey' in data:
                pass_test(f"Profile retrieved: {data['email']}")
                return data
            else:
                fail_test(f"Missing fields in response: {data}")
        else:
            fail_test(f"Status code {response.status_code}: {response.text}")

    except Exception as e:
        fail_test(f"Exception: {e}")

    return None


def test_create_contact():
    """Test creating a single contact."""
    print_test("Create Single Contact")

    contact = {
        "name": "Test Contact",
        "email": "test@example.com",
        "phone": "+1-555-9999",
        "company": "Test Company",
        "role": "Test Role",
        "location": "Test City",
        "notes": "Created by test suite"
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/contacts",
            headers=headers,
            json=contact
        )

        if response.status_code == 201:
            data = response.json()
            created = data.get('created', [])

            if created and created[0].get('name') == contact['name']:
                contact_id = created[0]['id']
                pass_test(f"Contact created with ID: {contact_id}")
                return contact_id
            else:
                fail_test(f"Unexpected response: {data}")
        else:
            fail_test(f"Status code {response.status_code}: {response.text}")

    except Exception as e:
        fail_test(f"Exception: {e}")

    return None


def test_list_contacts():
    """Test listing all contacts."""
    print_test("List All Contacts")

    try:
        response = requests.get(
            f"{BASE_URL}/api/contacts",
            headers=headers
        )

        if response.status_code == 200:
            contacts = response.json()
            if isinstance(contacts, list):
                pass_test(f"Retrieved {len(contacts)} contact(s)")
                return contacts
            else:
                fail_test(f"Expected array, got: {type(contacts)}")
        else:
            fail_test(f"Status code {response.status_code}: {response.text}")

    except Exception as e:
        fail_test(f"Exception: {e}")

    return []


def test_update_contact(contact_id):
    """Test updating a contact."""
    print_test("Update Contact")

    if not contact_id:
        fail_test("No contact ID provided")
        return

    updates = {
        "role": "Updated Role",
        "notes": "Updated by test suite"
    }

    try:
        response = requests.patch(
            f"{BASE_URL}/api/contacts/{contact_id}",
            headers=headers,
            json=updates
        )

        if response.status_code == 200:
            data = response.json()
            if data.get('role') == updates['role']:
                pass_test(f"Contact updated successfully")
            else:
                fail_test(f"Update not reflected: {data}")
        else:
            fail_test(f"Status code {response.status_code}: {response.text}")

    except Exception as e:
        fail_test(f"Exception: {e}")


def test_bulk_create_contacts():
    """Test creating multiple contacts."""
    print_test("Bulk Create Contacts")

    contacts = [
        {"name": "Bulk Contact 1", "email": "bulk1@example.com"},
        {"name": "Bulk Contact 2", "email": "bulk2@example.com"},
        {"name": "Bulk Contact 3", "email": "bulk3@example.com"}
    ]

    try:
        response = requests.post(
            f"{BASE_URL}/api/contacts",
            headers=headers,
            json=contacts
        )

        if response.status_code == 201:
            data = response.json()
            created = data.get('created', [])

            if len(created) == len(contacts):
                pass_test(f"Created {len(created)} contacts in bulk")
                return [c['id'] for c in created]
            else:
                fail_test(f"Expected {len(contacts)} contacts, created {len(created)}")
        else:
            fail_test(f"Status code {response.status_code}: {response.text}")

    except Exception as e:
        fail_test(f"Exception: {e}")

    return []


def test_create_deal(contact_id):
    """Test creating a deal."""
    print_test("Create Deal")

    deal = {
        "title": "Test Deal",
        "value": 50000,
        "stage": "Qualified",
        "priority": "High",
        "contact_id": contact_id,
        "notes": "Created by test suite"
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/deals",
            headers=headers,
            json=deal
        )

        if response.status_code == 201:
            data = response.json()
            created = data.get('created', [])

            if created and created[0].get('title') == deal['title']:
                deal_id = created[0]['id']
                pass_test(f"Deal created with ID: {deal_id}")
                return deal_id
            else:
                fail_test(f"Unexpected response: {data}")
        else:
            fail_test(f"Status code {response.status_code}: {response.text}")

    except Exception as e:
        fail_test(f"Exception: {e}")

    return None


def test_list_deals():
    """Test listing all deals."""
    print_test("List All Deals")

    try:
        response = requests.get(
            f"{BASE_URL}/api/deals",
            headers=headers
        )

        if response.status_code == 200:
            deals = response.json()
            if isinstance(deals, list):
                pass_test(f"Retrieved {len(deals)} deal(s)")
                return deals
            else:
                fail_test(f"Expected array, got: {type(deals)}")
        else:
            fail_test(f"Status code {response.status_code}: {response.text}")

    except Exception as e:
        fail_test(f"Exception: {e}")

    return []


def test_update_deal(deal_id):
    """Test updating a deal."""
    print_test("Update Deal")

    if not deal_id:
        fail_test("No deal ID provided")
        return

    updates = {
        "stage": "Negotiation",
        "notes": "Updated by test suite"
    }

    try:
        response = requests.patch(
            f"{BASE_URL}/api/deals/{deal_id}",
            headers=headers,
            json=updates
        )

        if response.status_code == 200:
            data = response.json()
            if data.get('stage') == updates['stage']:
                pass_test(f"Deal updated successfully")
            else:
                fail_test(f"Update not reflected: {data}")
        else:
            fail_test(f"Status code {response.status_code}: {response.text}")

    except Exception as e:
        fail_test(f"Exception: {e}")


def test_delete_deal(deal_id):
    """Test deleting a deal."""
    print_test("Delete Deal")

    if not deal_id:
        fail_test("No deal ID provided")
        return

    try:
        response = requests.delete(
            f"{BASE_URL}/api/deals/{deal_id}",
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            if 'message' in data:
                pass_test(f"Deal deleted successfully")
            else:
                fail_test(f"Unexpected response: {data}")
        else:
            fail_test(f"Status code {response.status_code}: {response.text}")

    except Exception as e:
        fail_test(f"Exception: {e}")


def test_delete_contact(contact_id):
    """Test deleting a contact."""
    print_test("Delete Contact")

    if not contact_id:
        fail_test("No contact ID provided")
        return

    try:
        response = requests.delete(
            f"{BASE_URL}/api/contacts/{contact_id}",
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            if 'message' in data:
                pass_test(f"Contact deleted successfully")
            else:
                fail_test(f"Unexpected response: {data}")
        else:
            fail_test(f"Status code {response.status_code}: {response.text}")

    except Exception as e:
        fail_test(f"Exception: {e}")


def test_error_handling():
    """Test error handling for invalid requests."""
    print_test("Error Handling - Invalid API Key")

    bad_headers = {"x-api-key": "invalid_key", "Content-Type": "application/json"}

    try:
        response = requests.get(
            f"{BASE_URL}/api/contacts",
            headers=bad_headers
        )

        if response.status_code == 401:
            pass_test("Correctly rejected invalid API key")
        else:
            fail_test(f"Expected 401, got {response.status_code}")

    except Exception as e:
        fail_test(f"Exception: {e}")


def test_404_handling():
    """Test 404 error handling."""
    print_test("Error Handling - 404 Not Found")

    try:
        response = requests.get(
            f"{BASE_URL}/api/contacts/nonexistent-id-12345",
            headers=headers
        )

        if response.status_code == 404:
            pass_test("Correctly returned 404 for missing resource")
        else:
            fail_test(f"Expected 404, got {response.status_code}")

    except Exception as e:
        fail_test(f"Exception: {e}")


def run_all_tests():
    """Run complete test suite."""
    print("\n" + "="*70)
    print("ZERO CRM API - COMPREHENSIVE TEST SUITE")
    print("="*70)

    # Test 1: Health check
    test_health_check()

    # Test 2: User profile
    test_user_profile()

    # Test 3: Create contact
    contact_id = test_create_contact()

    # Test 4: List contacts
    test_list_contacts()

    # Test 5: Update contact
    test_update_contact(contact_id)

    # Test 6: Bulk create contacts
    bulk_contact_ids = test_bulk_create_contacts()

    # Test 7: Create deal
    deal_id = test_create_deal(contact_id)

    # Test 8: List deals
    test_list_deals()

    # Test 9: Update deal
    test_update_deal(deal_id)

    # Test 10: Delete deal
    test_delete_deal(deal_id)

    # Test 11: Delete contacts
    test_delete_contact(contact_id)
    for bulk_id in bulk_contact_ids:
        test_delete_contact(bulk_id)

    # Test 12: Error handling
    test_error_handling()
    test_404_handling()

    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Passed: {tests_passed}")
    print(f"Failed: {tests_failed}")
    print(f"Total:  {tests_passed + tests_failed}")
    print("="*70)

    if tests_failed == 0:
        print("\n✅ ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n❌ {tests_failed} TEST(S) FAILED")
        return 1


def main():
    """Main entry point."""
    try:
        exit_code = run_all_tests()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
