# Zero CRM API Skill

> **Simple, fast, and powerful CRM automation** — Programmatically manage contacts, deals, and user profiles with the Zero CRM REST API.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.2-blue.svg)](https://github.com/thierryteisseire/0crm-skill)

Interact with the Zero CRM application to automate contact management, deal tracking, and bulk data operations. Perfect for sales automation, data migration, and CRM integrations.

---

## 🚀 Quick Start

### 1. Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Or install globally via npm
npm install -g @thierryteisseire/0crm-skill
```

### 2. Get Your API Key

1. Log in to [Zero CRM](https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws/)
2. Navigate to **Settings** → **API Keys**
3. Copy your API key (format: `zero_<hash>`)

### 3. Set Up Environment

```bash
# Create .env file
echo "ZERO_CRM_API_KEY=zero_your_api_key_here" > .env
```

### 4. Test Connection

```bash
# Using Python
python3 scripts/test_api.py $ZERO_CRM_API_KEY

# Using CLI (after npm install)
0crm test
```

---

## 📦 Features

- ✅ **Contact Management** — Create, read, update, delete contacts
- ✅ **Deal Tracking** — Manage sales pipeline with stages and priorities
- ✅ **Bulk Operations** — Import hundreds of contacts/deals in one request
- ✅ **User Profile** — Retrieve and manage user settings
- ✅ **API Key Management** — Generate and rotate keys programmatically
- ✅ **Simple Authentication** — Single header (`x-api-key`) authentication
- ✅ **RESTful Design** — Standard HTTP methods and status codes

---

## 📚 Usage Examples

### Python SDK

```python
import requests
import os

API_KEY = os.getenv("ZERO_CRM_API_KEY")
BASE_URL = "https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws"

headers = {"x-api-key": API_KEY}

# List all contacts
response = requests.get(f"{BASE_URL}/api/contacts", headers=headers)
contacts = response.json()

# Create a contact
new_contact = {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "company": "Acme Corp",
    "role": "VP Sales"
}
response = requests.post(f"{BASE_URL}/api/contacts", headers=headers, json=new_contact)
created = response.json()

print(f"Created contact: {created['id']}")
```

### Bulk Import from CSV

```python
import csv
import requests
import os

API_KEY = os.getenv("ZERO_CRM_API_KEY")
BASE_URL = "https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws"
headers = {"x-api-key": API_KEY}

# Read CSV
contacts = []
with open('contacts.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        contacts.append({
            "name": row["name"],
            "email": row["email"],
            "company": row.get("company", ""),
            "role": row.get("role", "")
        })

# Bulk import (API accepts arrays)
response = requests.post(f"{BASE_URL}/api/contacts", headers=headers, json=contacts)
result = response.json()

print(f"Imported {len(result['created'])} contacts")
```

### CLI Usage

```bash
# List contacts
0crm contacts list

# Create contact
0crm contacts create --name "John Doe" --email "john@example.com"

# Bulk import
0crm contacts import contacts.csv

# List deals
0crm deals list --stage "Negotiation"

# Get user profile
0crm profile
```

---

## 🛠️ API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/contacts` | GET | List all contacts |
| `/api/contacts` | POST | Create contact(s) |
| `/api/contacts/:id` | PATCH | Update contact |
| `/api/contacts/:id` | DELETE | Delete contact |
| `/api/deals` | GET | List all deals |
| `/api/deals` | POST | Create deal(s) |
| `/api/deals/:id` | PATCH | Update deal |
| `/api/deals/:id` | DELETE | Delete deal |
| `/api/user/profile` | GET | Get user profile |
| `/api/user/generate-api-key` | POST | Regenerate API key |

---

## 📖 Documentation

- **[SKILL.md](SKILL.md)** — Comprehensive documentation for Claude Code
- **[API Reference](references/api_reference.md)** — Detailed endpoint documentation
- **[Examples](examples/)** — Code samples and use cases

---

## 🔐 Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for API keys (`.env` file)
3. **Rotate keys regularly** via `/api/user/generate-api-key`
4. **Use HTTPS only** (enforced by default)
5. **Monitor API usage** for unusual patterns

---

## 🧪 Testing

```bash
# Run basic tests
python3 scripts/test_api.py $ZERO_CRM_API_KEY

# Run comprehensive tests
python3 scripts/test_comprehensive.py

# Verify skill configuration
npm run verify
```

---

## 📊 Use Cases

### 1. Sales Automation
Automatically create contacts from form submissions, web scraping, or enrichment services.

### 2. Data Migration
Bulk import contacts and deals from spreadsheets, legacy CRMs, or databases.

### 3. Reporting & Analytics
Export deals and contacts for external dashboards, BI tools, or custom reports.

### 4. Integration Workflows
Connect Zero CRM with Zapier, Make.com, or custom webhooks for automation.

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or pull request on [GitHub](https://github.com/thierryteisseire/0crm-skill).

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🔗 Links

- **GitHub Repository**: https://github.com/thierryteisseire/0crm-skill
- **Zero CRM Application**: https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws/
- **Issue Tracker**: https://github.com/thierryteisseire/0crm-skill/issues

---

**Questions?** Check the [API Reference](references/api_reference.md) or open an issue on GitHub.
