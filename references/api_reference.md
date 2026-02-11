# Zero CRM API Reference

## Authentication
All requests must include the `x-api-key` header with a valid API key.
Key format: `zero_<hash>`

**Base URL**: `https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws/`

## Endpoints

### Health Check
- **GET** `/api/health`
- Returns status and platform info.

### Contacts
- **GET** `/api/contacts` - List all contacts for the authenticated user.
- **POST** `/api/contacts` - Create a contact.
  - Body: `{ name: string, email?: string, phone?: string, role?: string, company?: string, location?: string, notes?: string }`
  - Accepts a single object or an array of objects for bulk import.
- **PATCH** `/api/contacts/:id` - Update a contact.
- **DELETE** `/api/contacts/:id` - Delete a contact.

### Deals
- **GET** `/api/deals` - List all deals.
- **POST** `/api/deals` - Create a deal.
  - Body: `{ title: string, value?: number, stage: string, priority?: string, contact_id?: uuid, notes?: string }`
  - Accepts a single object or an array of objects for bulk import.
- **PATCH** `/api/deals/:id` - Update a deal.
- **DELETE** `/api/deals/:id` - Delete a deal.

### User Profile
- **GET** `/api/user/profile` - Get current user profile and API key.
- **POST** `/api/user/generate-api-key` - Regenerate the API key.
