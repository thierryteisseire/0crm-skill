---
name: 0crm-skill
description: Comprehensive Zero CRM API skill for managing contacts, deals, and user profiles via REST API. Supports CRUD operations, bulk imports, and automation workflows. Use for: contact management, deal tracking, sales automation, data migration, CRM integrations, bulk operations.
---

# Zero CRM API Skill

> **Production-ready CRM automation** — Programmatically manage contacts, deals, and user profiles with comprehensive documentation, examples, and best practices.

**Base URL:** `https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws`

---

## 🚀 Quick Start

### Authentication

All API requests require the `x-api-key` header with a valid API key.

```bash
# Get your API key from Zero CRM Settings
# Format: zero_<hash>

export ZERO_CRM_API_KEY="zero_your_key_here"
```

### Basic Usage

```python
import requests
import os

API_KEY = os.getenv("ZERO_CRM_API_KEY")
BASE_URL = "https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws"

headers = {"x-api-key": API_KEY}

# Test connection
response = requests.get(f"{BASE_URL}/api/health")
print(response.json())  # {"status": "ok", "platform": "Zero CRM"}
```

---

## 📦 Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Or install globally via npm
npm install -g @thierryteisseire/0crm-skill
```

**Dependencies:**
- `requests>=2.28.0`
- `python-dotenv>=0.19.0`

---

## 🔐 Authentication

### API Key Format

API keys follow the format: `zero_<hash>`

### Getting Your API Key

1. Log in to Zero CRM
2. Navigate to **Settings** → **API Keys**
3. Copy your existing key or generate a new one

### Using Environment Variables

```bash
# .env file (never commit this!)
ZERO_CRM_API_KEY=zero_abc123def456...
```

```python
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("ZERO_CRM_API_KEY")
```

### Programmatic Key Rotation

```python
import requests

# Regenerate API key (requires current key)
response = requests.post(
    f"{BASE_URL}/api/user/generate-api-key",
    headers={"x-api-key": current_key}
)

new_key = response.json()["apiKey"]
print(f"New API key: {new_key}")
```

---

## 📚 Core Operations

### Contacts

#### List All Contacts

```python
response = requests.get(f"{BASE_URL}/api/contacts", headers=headers)
contacts = response.json()

for contact in contacts:
    print(f"{contact['name']} - {contact['email']}")
```

**Response:**
```json
[
  {
    "id": "uuid",
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "+1-555-0100",
    "company": "Acme Corp",
    "role": "VP Sales",
    "location": "San Francisco, CA",
    "notes": "Met at conference 2024",
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:00:00Z",
    "user_id": "uuid"
  }
]
```

#### Create Single Contact

```python
new_contact = {
    "name": "John Smith",
    "email": "john@company.com",
    "phone": "+1-555-0200",
    "company": "Tech Inc",
    "role": "CTO",
    "location": "New York, NY",
    "notes": "Interested in enterprise plan"
}

response = requests.post(
    f"{BASE_URL}/api/contacts",
    headers=headers,
    json=new_contact
)

created = response.json()
print(f"Created contact: {created['id']}")
```

#### Create Multiple Contacts (Bulk)

```python
contacts = [
    {"name": "Alice", "email": "alice@example.com"},
    {"name": "Bob", "email": "bob@example.com"},
    {"name": "Charlie", "email": "charlie@example.com"}
]

response = requests.post(
    f"{BASE_URL}/api/contacts",
    headers=headers,
    json=contacts  # Send as array
)

result = response.json()
print(f"Created {len(result['created'])} contacts")
```

#### Update Contact

```python
contact_id = "uuid-here"
updates = {
    "role": "SVP Sales",
    "notes": "Promoted to SVP"
}

response = requests.patch(
    f"{BASE_URL}/api/contacts/{contact_id}",
    headers=headers,
    json=updates
)

updated = response.json()
print(f"Updated: {updated['name']}")
```

#### Delete Contact

```python
contact_id = "uuid-here"

response = requests.delete(
    f"{BASE_URL}/api/contacts/{contact_id}",
    headers=headers
)

if response.status_code == 200:
    print("Contact deleted successfully")
```

---

### Deals

#### List All Deals

```python
response = requests.get(f"{BASE_URL}/api/deals", headers=headers)
deals = response.json()

for deal in deals:
    print(f"{deal['title']} - ${deal['value']} - {deal['stage']}")
```

**Response:**
```json
[
  {
    "id": "uuid",
    "title": "Enterprise Contract - Acme Corp",
    "value": 50000,
    "stage": "Negotiation",
    "priority": "High",
    "contact_id": "uuid",
    "notes": "Q1 2024 target",
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:00:00Z",
    "user_id": "uuid"
  }
]
```

#### Create Deal

```python
new_deal = {
    "title": "Annual Subscription - Tech Inc",
    "value": 120000,
    "stage": "Proposal Sent",
    "priority": "High",
    "contact_id": "uuid-of-john-smith",
    "notes": "Decision expected by end of month"
}

response = requests.post(
    f"{BASE_URL}/api/deals",
    headers=headers,
    json=new_deal
)

created = response.json()
print(f"Created deal: {created['id']}")
```

#### Update Deal Stage

```python
deal_id = "uuid-here"
updates = {
    "stage": "Closed Won",
    "notes": "Signed contract on 2024-02-01"
}

response = requests.patch(
    f"{BASE_URL}/api/deals/{deal_id}",
    headers=headers,
    json=updates
)

updated = response.json()
print(f"Deal status: {updated['stage']}")
```

#### Delete Deal

```python
deal_id = "uuid-here"

response = requests.delete(
    f"{BASE_URL}/api/deals/{deal_id}",
    headers=headers
)

if response.status_code == 200:
    print("Deal deleted successfully")
```

---

### User Profile

#### Get Current User

```python
response = requests.get(
    f"{BASE_URL}/api/user/profile",
    headers=headers
)

profile = response.json()
print(f"User: {profile['email']}")
print(f"API Key: {profile['apiKey']}")
```

**Response:**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "apiKey": "zero_abc123...",
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

## 🔄 Bulk Operations

### Bulk Import from CSV

```python
import csv
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ZERO_CRM_API_KEY")
BASE_URL = "https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws"
headers = {"x-api-key": API_KEY}

# Read contacts from CSV
contacts = []
with open('contacts.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        contact = {
            "name": row["name"],
            "email": row.get("email", ""),
            "phone": row.get("phone", ""),
            "company": row.get("company", ""),
            "role": row.get("role", ""),
            "location": row.get("location", ""),
            "notes": row.get("notes", "")
        }
        # Remove empty fields
        contact = {k: v for k, v in contact.items() if v}
        contacts.append(contact)

# Bulk import (API accepts arrays)
response = requests.post(
    f"{BASE_URL}/api/contacts",
    headers=headers,
    json=contacts
)

result = response.json()
print(f"✅ Imported {len(result.get('created', []))} contacts")
print(f"⚠️ Skipped {len(result.get('skipped', []))} contacts")
```

**CSV Format:**
```csv
name,email,phone,company,role,location,notes
Jane Doe,jane@acme.com,+1-555-0100,Acme Corp,VP Sales,San Francisco,"Met at conference"
John Smith,john@tech.com,+1-555-0200,Tech Inc,CTO,New York,"Enterprise prospect"
```

### Bulk Import Deals

```python
deals = []
with open('deals.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        deal = {
            "title": row["title"],
            "value": float(row.get("value", 0)),
            "stage": row.get("stage", "Lead"),
            "priority": row.get("priority", "Medium"),
            "notes": row.get("notes", "")
        }
        deals.append(deal)

response = requests.post(
    f"{BASE_URL}/api/deals",
    headers=headers,
    json=deals
)

result = response.json()
print(f"✅ Imported {len(result.get('created', []))} deals")
```

---

## 🔧 Error Handling

### HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Continue processing |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Validate request payload |
| 401 | Unauthorized | Check API key |
| 404 | Not Found | Verify resource ID |
| 500 | Server Error | Retry with exponential backoff |

### Standard Error Response

```json
{
  "error": "Unauthorized",
  "message": "Invalid API key"
}
```

### Error Handling Pattern

```python
import requests
from requests.exceptions import HTTPError

def make_request(method, endpoint, **kwargs):
    """Make API request with error handling."""
    try:
        response = requests.request(
            method,
            f"{BASE_URL}{endpoint}",
            headers=headers,
            **kwargs
        )
        response.raise_for_status()
        return response.json()
    
    except HTTPError as e:
        if e.response.status_code == 401:
            print("❌ Authentication failed. Check your API key.")
        elif e.response.status_code == 404:
            print("❌ Resource not found.")
        elif e.response.status_code >= 500:
            print("❌ Server error. Please try again later.")
        else:
            print(f"❌ Error: {e.response.status_code} - {e.response.text}")
        raise
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise

# Usage
try:
    contacts = make_request("GET", "/api/contacts")
    print(f"Found {len(contacts)} contacts")
except Exception:
    pass
```

---

## 💡 Workflow Patterns

### 1. Bulk Import Workflow

**Use Case:** Import 500 contacts from a spreadsheet

```python
import pandas as pd
import requests
import os

# Step 1: Read data
df = pd.read_excel('contacts.xlsx')

# Step 2: Transform to API format
contacts = []
for _, row in df.iterrows():
    contacts.append({
        "name": row["Full Name"],
        "email": row["Email Address"],
        "company": row["Company"],
        "role": row["Title"]
    })

# Step 3: Bulk import
response = requests.post(
    f"{BASE_URL}/api/contacts",
    headers=headers,
    json=contacts
)

# Step 4: Verify
result = response.json()
print(f"✅ Created: {len(result['created'])}")
print(f"⚠️ Skipped: {len(result.get('skipped', []))}")
```

### 2. Deal Pipeline Report

**Use Case:** Generate weekly sales pipeline report

```python
# Fetch all deals
response = requests.get(f"{BASE_URL}/api/deals", headers=headers)
deals = response.json()

# Calculate metrics
stages = {}
for deal in deals:
    stage = deal['stage']
    stages[stage] = stages.get(stage, 0) + deal.get('value', 0)

# Print report
print("\n📊 Sales Pipeline Report")
print("=" * 40)
for stage, total in stages.items():
    print(f"{stage:<20} ${total:>15,.2f}")

total_pipeline = sum(stages.values())
print("=" * 40)
print(f"{'Total Pipeline':<20} ${total_pipeline:>15,.2f}")
```

### 3. Contact Enrichment

**Use Case:** Enrich contacts with company data from external API

```python
# Fetch all contacts
response = requests.get(f"{BASE_URL}/api/contacts", headers=headers)
contacts = response.json()

for contact in contacts:
    if contact.get('company') and not contact.get('notes'):
        # Fetch company data from external API
        # company_data = fetch_company_info(contact['company'])
        
        # Update contact with enriched data
        updates = {
            "notes": f"Company size: 500+\nIndustry: Technology"
        }
        
        requests.patch(
            f"{BASE_URL}/api/contacts/{contact['id']}",
            headers=headers,
            json=updates
        )
        
        print(f"✅ Enriched: {contact['name']}")
```

### 4. Win Rate Analysis

**Use Case:** Calculate win rate by stage

```python
# Fetch all deals
response = requests.get(f"{BASE_URL}/api/deals", headers=headers)
deals = response.json()

# Calculate win rate
total_deals = len(deals)
won_deals = len([d for d in deals if d['stage'] == 'Closed Won'])
lost_deals = len([d for d in deals if d['stage'] == 'Closed Lost'])

win_rate = (won_deals / (won_deals + lost_deals)) * 100 if (won_deals + lost_deals) > 0 else 0

print(f"\n📈 Win Rate Analysis")
print(f"Total Deals: {total_deals}")
print(f"Won: {won_deals}")
print(f"Lost: {lost_deals}")
print(f"Win Rate: {win_rate:.1f}%")
```

---

## 🔐 Security Best Practices

### 1. API Key Management

- ✅ **Never commit API keys** to version control
- ✅ **Use environment variables** (`.env` file)
- ✅ **Rotate keys regularly** via API
- ✅ **Use different keys** for dev/staging/production

### 2. Environment Variables

```python
# Bad ❌
API_KEY = "zero_abc123..."  # Hardcoded

# Good ✅
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("ZERO_CRM_API_KEY")
```

### 3. HTTPS Only

All API requests use HTTPS by default. Never use HTTP endpoints.

### 4. Error Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    response = requests.get(f"{BASE_URL}/api/contacts", headers=headers)
    response.raise_for_status()
except Exception as e:
    logger.error(f"API request failed: {e}")
    # Don't log the API key!
```

---

## 🧪 Testing

### Basic Test

```bash
# Using test script
python3 scripts/test_api.py $ZERO_CRM_API_KEY
```

### Comprehensive Test

```bash
# Run full test suite
python3 scripts/test_comprehensive.py
```

### Verify Installation

```bash
npm run verify
```

---

## 🔍 Troubleshooting

### Authentication Failed (401)

**Problem:** `{"error": "Unauthorized"}`

**Solution:**
```bash
# Verify API key format
echo $ZERO_CRM_API_KEY  # Should start with "zero_"

# Test with curl
curl -H "x-api-key: $ZERO_CRM_API_KEY" \
  https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws/api/user/profile
```

### Resource Not Found (404)

**Problem:** `{"error": "Not found"}`

**Solution:**
- Verify the resource ID is correct
- Check if the resource was deleted
- Ensure you're using the correct endpoint

### Server Error (500)

**Problem:** Internal server error

**Solution:**
- Wait and retry with exponential backoff
- Check API status page
- Contact support if persists

---

## 📖 Reference Documentation

- **[API Reference](references/api_reference.md)** — Complete endpoint documentation
- **[Examples](examples/)** — Code samples and use cases
- **[README](README.md)** — Quickstart guide

---

## 🔗 Links

- **GitHub Repository**: https://github.com/thierryteisseire/0crm-skill
- **Zero CRM Application**: https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws/
- **Issue Tracker**: https://github.com/thierryteisseire/0crm-skill/issues

---

**Version:** 1.0.0  
**License:** MIT  
**Author:** Thierry Teisseire

For questions or issues, visit [GitHub Issues](https://github.com/thierryteisseire/0crm-skill/issues).
