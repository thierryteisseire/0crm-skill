# Zero CRM API Reference

Complete reference for the Zero CRM REST API v1.0

**Base URL:** `https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws`

---

## Table of Contents

1. [Authentication](#authentication)
2. [HTTP Status Codes](#http-status-codes)
3. [Error Responses](#error-responses)
4. [Health & Status](#health--status)
5. [Contacts API](#contacts-api)
6. [Deals API](#deals-api)
7. [User Profile API](#user-profile-api)
8. [Best Practices](#best-practices)

---

## Authentication

All API requests (except health check) require authentication via the `x-api-key` header.

### API Key Format

```
zero_<hash>
```

Example: `zero_abc123def456ghi789...`

### Headers

```http
x-api-key: zero_your_api_key_here
Content-Type: application/json
```

### Getting Your API Key

1. Log in to Zero CRM
2. Navigate to **Settings** → **API Keys**
3. Copy your existing key or click "Generate New Key"

### Example Request

```bash
curl -H "x-api-key: zero_abc123..." \
     -H "Content-Type: application/json" \
     https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws/api/contacts
```

```python
import requests

headers = {
    "x-api-key": "zero_abc123...",
    "Content-Type": "application/json"
}

response = requests.get(
    "https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws/api/contacts",
    headers=headers
)
```

---

## HTTP Status Codes

| Code | Status | Description | Action |
|------|--------|-------------|--------|
| 200 | OK | Request successful | Continue processing |
| 201 | Created | Resource created | Capture returned ID |
| 400 | Bad Request | Invalid request payload | Validate request body |
| 401 | Unauthorized | Invalid or missing API key | Check authentication |
| 404 | Not Found | Resource doesn't exist | Verify resource ID |
| 500 | Internal Server Error | Server-side error | Retry with backoff |

---

## Error Responses

### Standard Error Format

```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

### Example Error Responses

**401 Unauthorized:**
```json
{
  "error": "Unauthorized",
  "message": "Invalid API key"
}
```

**404 Not Found:**
```json
{
  "error": "Not Found",
  "message": "Contact not found"
}
```

**400 Bad Request:**
```json
{
  "error": "Bad Request",
  "message": "Missing required field: name"
}
```

---

## Health & Status

### GET /api/health

Health check endpoint (no authentication required).

**Request:**
```bash
curl https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws/api/health
```

**Response (200):**
```json
{
  "status": "ok",
  "platform": "Zero CRM"
}
```

---

## Contacts API

### GET /api/contacts

List all contacts for the authenticated user.

**Request:**
```bash
curl -H "x-api-key: zero_abc123..." \
  https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws/api/contacts
```

**Response (200):**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "+1-555-0100",
    "company": "Acme Corp",
    "role": "VP Sales",
    "location": "San Francisco, CA",
    "notes": "Met at conference 2024",
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:00:00Z",
    "user_id": "user-uuid"
  }
]
```

### POST /api/contacts

Create one or more contacts.

**Supports both single object and array of objects.**

**Request (Single Contact):**
```json
{
  "name": "John Smith",
  "email": "john@company.com",
  "phone": "+1-555-0200",
  "company": "Tech Inc",
  "role": "CTO",
  "location": "New York, NY",
  "notes": "Interested in enterprise plan"
}
```

**Request (Multiple Contacts):**
```json
[
  {
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "company": "Startup Co"
  },
  {
    "name": "Bob Williams",
    "email": "bob@example.com",
    "company": "Big Corp"
  }
]
```

**Response (201):**
```json
{
  "created": [
    {
      "id": "new-uuid-1",
      "name": "John Smith",
      "email": "john@company.com",
      ...
    }
  ],
  "skipped": []
}
```

**Field Schema:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Contact's full name |
| `email` | string | No | Email address |
| `phone` | string | No | Phone number |
| `company` | string | No | Company name |
| `role` | string | No | Job title/role |
| `location` | string | No | City, state, country |
| `notes` | string | No | Additional notes |

### PATCH /api/contacts/:id

Update an existing contact.

**Request:**
```bash
curl -X PATCH \
  -H "x-api-key: zero_abc123..." \
  -H "Content-Type: application/json" \
  -d '{"role": "SVP Sales", "notes": "Promoted"}' \
  https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws/api/contacts/550e8400...
```

**Request Body:**
```json
{
  "role": "SVP Sales",
  "notes": "Promoted to SVP"
}
```

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Jane Doe",
  "email": "jane@example.com",
  "role": "SVP Sales",
  "notes": "Promoted to SVP",
  "updated_at": "2024-02-01T15:30:00Z",
  ...
}
```

### DELETE /api/contacts/:id

Delete a contact.

**Request:**
```bash
curl -X DELETE \
  -H "x-api-key: zero_abc123..." \
  https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws/api/contacts/550e8400...
```

**Response (200):**
```json
{
  "message": "Contact deleted successfully",
  "id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

## Deals API

### GET /api/deals

List all deals for the authenticated user.

**Request:**
```bash
curl -H "x-api-key: zero_abc123..." \
  https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws/api/deals
```

**Response (200):**
```json
[
  {
    "id": "deal-uuid",
    "title": "Enterprise Contract - Acme Corp",
    "value": 50000,
    "stage": "Negotiation",
    "priority": "High",
    "contact_id": "contact-uuid",
    "notes": "Q1 2024 target",
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:00:00Z",
    "user_id": "user-uuid"
  }
]
```

### POST /api/deals

Create one or more deals.

**Supports both single object and array of objects.**

**Request (Single Deal):**
```json
{
  "title": "Annual Subscription - Tech Inc",
  "value": 120000,
  "stage": "Proposal Sent",
  "priority": "High",
  "contact_id": "contact-uuid",
  "notes": "Decision expected by end of month"
}
```

**Request (Multiple Deals):**
```json
[
  {
    "title": "Deal 1",
    "value": 10000,
    "stage": "Lead"
  },
  {
    "title": "Deal 2",
    "value": 25000,
    "stage": "Qualified"
  }
]
```

**Response (201):**
```json
{
  "created": [
    {
      "id": "new-deal-uuid",
      "title": "Annual Subscription - Tech Inc",
      "value": 120000,
      ...
    }
  ],
  "skipped": []
}
```

**Field Schema:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | Deal title/name |
| `value` | number | No | Deal value in USD |
| `stage` | string | Yes | Pipeline stage |
| `priority` | string | No | Priority level (Low, Medium, High) |
| `contact_id` | UUID | No | Associated contact ID |
| `notes` | string | No | Additional notes |

**Common Stage Values:**
- Lead
- Qualified
- Proposal Sent
- Negotiation
- Closed Won
- Closed Lost

### PATCH /api/deals/:id

Update an existing deal.

**Request:**
```bash
curl -X PATCH \
  -H "x-api-key: zero_abc123..." \
  -H "Content-Type: application/json" \
  -d '{"stage": "Closed Won", "notes": "Signed!"}' \
  https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws/api/deals/deal-uuid
```

**Request Body:**
```json
{
  "stage": "Closed Won",
  "notes": "Signed contract on 2024-02-01"
}
```

**Response (200):**
```json
{
  "id": "deal-uuid",
  "title": "Annual Subscription - Tech Inc",
  "stage": "Closed Won",
  "notes": "Signed contract on 2024-02-01",
  "updated_at": "2024-02-01T16:00:00Z",
  ...
}
```

### DELETE /api/deals/:id

Delete a deal.

**Request:**
```bash
curl -X DELETE \
  -H "x-api-key: zero_abc123..." \
  https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws/api/deals/deal-uuid
```

**Response (200):**
```json
{
  "message": "Deal deleted successfully",
  "id": "deal-uuid"
}
```

---

## User Profile API

### GET /api/user/profile

Get current user profile and API key.

**Request:**
```bash
curl -H "x-api-key: zero_abc123..." \
  https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws/api/user/profile
```

**Response (200):**
```json
{
  "id": "user-uuid",
  "email": "user@example.com",
  "apiKey": "zero_abc123...",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### POST /api/user/generate-api-key

Regenerate API key (requires current valid key).

**Request:**
```bash
curl -X POST \
  -H "x-api-key: zero_current_key..." \
  https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws/api/user/generate-api-key
```

**Response (200):**
```json
{
  "apiKey": "zero_new_key_abc456...",
  "message": "API key regenerated successfully"
}
```

**⚠️ Warning:** The old API key will be invalidated immediately upon generating a new one.

---

## Best Practices

### 1. Error Handling

Always implement proper error handling:

```python
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        print("Authentication failed")
    elif e.response.status_code == 404:
        print("Resource not found")
    else:
        print(f"HTTP error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### 2. Rate Limiting

While there are no explicit rate limits, be respectful:
- Use bulk operations for importing multiple records
- Implement reasonable delays between requests
- Avoid unnecessary polling

### 3. Data Validation

Validate data before sending to API:
- Ensure required fields are present
- Format phone/email correctly
- Handle special characters in names/notes

### 4. API Key Security

- Never commit API keys to version control
- Use environment variables
- Rotate keys periodically
- Use different keys for dev/prod

---

## Code Examples

See [../examples/](../examples/) for comprehensive code samples:
- `basic_operations.py` — CRUD operations
- `bulk_import.py` — CSV import example
- `pipeline_report.py` — Sales metrics
- `error_handling.py` — Robust error handling

---

## Support

- **GitHub Issues:** https://github.com/thierryteisseire/0crm-skill/issues
- **Documentation:** [SKILL.md](../SKILL.md)

---

**API Version:** 1.0  
**Last Updated:** 2024-02-11
