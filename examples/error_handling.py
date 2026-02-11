#!/usr/bin/env python3
"""
Error Handling Example for Zero CRM API

Demonstrates:
- Proper error handling patterns
- HTTP status code handling
- Retry logic with exponential backoff
- Validation before API calls
- Logging and debugging

Usage:
    python3 error_handling.py
"""

import requests
import os
import sys
import time
import logging
from dotenv import load_dotenv
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

API_KEY = os.getenv("ZERO_CRM_API_KEY")
BASE_URL = "https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws"

if not API_KEY:
    logger.error("ZERO_CRM_API_KEY not found in environment variables")
    sys.exit(1)

headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}


def make_request_with_retry(method, endpoint, max_retries=3, backoff_factor=2, **kwargs):
    """
    Make API request with exponential backoff retry logic.

    Args:
        method: HTTP method (GET, POST, PATCH, DELETE)
        endpoint: API endpoint path
        max_retries: Maximum number of retry attempts
        backoff_factor: Multiplier for exponential backoff
        **kwargs: Additional arguments for requests

    Returns:
        Response JSON or None on failure
    """
    url = f"{BASE_URL}{endpoint}"

    for attempt in range(max_retries):
        try:
            logger.info(f"{method} {endpoint} (attempt {attempt + 1}/{max_retries})")

            response = requests.request(
                method,
                url,
                headers=headers,
                timeout=10,  # 10 second timeout
                **kwargs
            )

            # Raise exception for 4xx/5xx status codes
            response.raise_for_status()

            logger.info(f"✅ Success: {method} {endpoint} - {response.status_code}")
            return response.json()

        except HTTPError as e:
            status_code = e.response.status_code

            if status_code == 401:
                logger.error("❌ Authentication failed - Invalid API key")
                logger.error("   Check your ZERO_CRM_API_KEY environment variable")
                return None  # Don't retry authentication errors

            elif status_code == 404:
                logger.error(f"❌ Resource not found: {endpoint}")
                return None  # Don't retry 404s

            elif status_code == 400:
                logger.error(f"❌ Bad request: {e.response.text}")
                return None  # Don't retry validation errors

            elif status_code >= 500:
                # Server errors - retry with backoff
                if attempt < max_retries - 1:
                    wait_time = backoff_factor ** attempt
                    logger.warning(f"⚠️  Server error {status_code} - retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"❌ Server error {status_code} after {max_retries} attempts")
                    return None
            else:
                logger.error(f"❌ HTTP error {status_code}: {e.response.text}")
                return None

        except ConnectionError:
            if attempt < max_retries - 1:
                wait_time = backoff_factor ** attempt
                logger.warning(f"⚠️  Connection error - retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                logger.error(f"❌ Connection failed after {max_retries} attempts")
                return None

        except Timeout:
            if attempt < max_retries - 1:
                wait_time = backoff_factor ** attempt
                logger.warning(f"⚠️  Request timeout - retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                logger.error(f"❌ Request timed out after {max_retries} attempts")
                return None

        except RequestException as e:
            logger.error(f"❌ Request error: {e}")
            return None

    return None


def validate_contact(contact):
    """
    Validate contact data before sending to API.

    Args:
        contact: Contact dictionary

    Returns:
        (is_valid, error_message)
    """
    # Required fields
    if not contact.get('name'):
        return False, "Missing required field: name"

    if not contact['name'].strip():
        return False, "Name cannot be empty"

    # Optional email validation
    email = contact.get('email', '')
    if email and '@' not in email:
        return False, f"Invalid email format: {email}"

    # Optional phone validation
    phone = contact.get('phone', '')
    if phone and len(phone) < 5:
        return False, f"Phone number too short: {phone}"

    return True, None


def validate_deal(deal):
    """
    Validate deal data before sending to API.

    Args:
        deal: Deal dictionary

    Returns:
        (is_valid, error_message)
    """
    # Required fields
    if not deal.get('title'):
        return False, "Missing required field: title"

    if not deal.get('stage'):
        return False, "Missing required field: stage"

    # Value validation
    value = deal.get('value', 0)
    if value < 0:
        return False, f"Deal value cannot be negative: {value}"

    # Priority validation
    valid_priorities = ['Low', 'Medium', 'High']
    priority = deal.get('priority', '')
    if priority and priority not in valid_priorities:
        return False, f"Invalid priority: {priority} (must be one of {valid_priorities})"

    return True, None


def safe_create_contact(contact):
    """Safely create a contact with validation and error handling."""
    logger.info("Creating contact with validation...")

    # Validate before sending
    is_valid, error = validate_contact(contact)
    if not is_valid:
        logger.error(f"❌ Validation failed: {error}")
        return None

    # Make request with retry logic
    result = make_request_with_retry(
        "POST",
        "/api/contacts",
        json=contact
    )

    if result:
        created = result.get('created', [{}])[0]
        logger.info(f"✅ Created contact: {created.get('name')} (ID: {created.get('id')})")
        return created

    return None


def safe_create_deal(deal):
    """Safely create a deal with validation and error handling."""
    logger.info("Creating deal with validation...")

    # Validate before sending
    is_valid, error = validate_deal(deal)
    if not is_valid:
        logger.error(f"❌ Validation failed: {error}")
        return None

    # Make request with retry logic
    result = make_request_with_retry(
        "POST",
        "/api/deals",
        json=deal
    )

    if result:
        created = result.get('created', [{}])[0]
        logger.info(f"✅ Created deal: {created.get('title')} (ID: {created.get('id')})")
        return created

    return None


def demonstrate_error_scenarios():
    """Demonstrate various error handling scenarios."""
    print("\n🔍 Zero CRM API - Error Handling Examples\n")

    # Scenario 1: Valid contact creation
    print("="*70)
    print("Scenario 1: Valid Contact Creation")
    print("="*70)
    valid_contact = {
        "name": "Test User",
        "email": "test@example.com",
        "company": "Test Corp"
    }
    created_contact = safe_create_contact(valid_contact)

    # Scenario 2: Missing required field
    print("\n" + "="*70)
    print("Scenario 2: Missing Required Field")
    print("="*70)
    invalid_contact = {
        "email": "missing-name@example.com",
        "company": "Test Corp"
    }
    safe_create_contact(invalid_contact)

    # Scenario 3: Invalid email
    print("\n" + "="*70)
    print("Scenario 3: Invalid Email Format")
    print("="*70)
    invalid_email_contact = {
        "name": "Invalid Email User",
        "email": "not-an-email",
        "company": "Test Corp"
    }
    safe_create_contact(invalid_email_contact)

    # Scenario 4: Valid deal creation
    if created_contact:
        print("\n" + "="*70)
        print("Scenario 4: Valid Deal Creation")
        print("="*70)
        valid_deal = {
            "title": "Test Deal",
            "stage": "Qualified",
            "value": 10000,
            "priority": "High",
            "contact_id": created_contact.get('id')
        }
        created_deal = safe_create_deal(valid_deal)

    # Scenario 5: Invalid deal priority
    print("\n" + "="*70)
    print("Scenario 5: Invalid Deal Priority")
    print("="*70)
    invalid_priority_deal = {
        "title": "Invalid Priority Deal",
        "stage": "Lead",
        "priority": "Urgent"  # Invalid - not in [Low, Medium, High]
    }
    safe_create_deal(invalid_priority_deal)

    # Scenario 6: Negative deal value
    print("\n" + "="*70)
    print("Scenario 6: Negative Deal Value")
    print("="*70)
    negative_value_deal = {
        "title": "Negative Value Deal",
        "stage": "Lead",
        "value": -5000
    }
    safe_create_deal(negative_value_deal)

    # Scenario 7: Fetch non-existent resource
    print("\n" + "="*70)
    print("Scenario 7: Fetch Non-Existent Resource")
    print("="*70)
    make_request_with_retry("GET", "/api/contacts/non-existent-id-12345")

    # Cleanup
    if created_contact:
        print("\n" + "="*70)
        print("Cleanup: Deleting Test Contact")
        print("="*70)
        make_request_with_retry("DELETE", f"/api/contacts/{created_contact['id']}")

    print("\n" + "="*70)
    print("✅ Error Handling Examples Completed")
    print("="*70)

    print("\n💡 Best Practices:")
    print("   • Always validate data before API calls")
    print("   • Implement retry logic for server errors")
    print("   • Don't retry authentication or validation errors")
    print("   • Use exponential backoff for retries")
    print("   • Log errors for debugging")
    print("   • Handle timeouts gracefully")


def main():
    """Run error handling demonstrations."""
    try:
        demonstrate_error_scenarios()
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
