---
name: 0crm-skill
description: Interaction with the Zero CRM application via its REST API. Use this skill when you need to programmatically manage contacts, deals, or user profile information within the Zero CRM ecosystem. It supports listing, creating, updating, and deleting records using the 'x-api-key' authentication method.
---

# Zero CRM API Interaction

This skill enables programmatic interaction with the Zero CRM application.

## Core Operations

1. **Information Retrieval**:
   - List contacts and deals to understand the current state of the CRM.
   - Fetch the user profile to verify identity and API configuration.

2. **Data Ingestion**:
   - Create single contacts or deals.
   - Perform bulk imports by sending arrays of records to the POST endpoints.

3. **Lifecycle Management**:
   - Update existing records via PATCH.
   - Remove records via DELETE (supports cascade deletion of associated entities).

## Usage Guidelines

- Always check the [API Reference](references/api_reference.md) for exact endpoint paths and payload schemas.
- **Authentication**: Use the `x-api-key` header. The key can be found in the user's Settings page or retrieved from the [User Profile] endpoint if you have a valid session token.
- **Error Handling**: The API returns standard HTTP status codes. `401` indicates an authentication failure.

## Workflow Patterns

### Bulk Importing Contacts
When task entails importing data from external sources (CSV, JSON), use the bulk POST capability:
1. Parse the source data.
2. Format as an array of objects matching the schema.
3. Post to `/api/contacts`.

### Syncing Performance Data
To generate external reports or sync with dashboards:
1. Fetch all deals from `/api/deals`.
2. Process metrics (Win Rate, Total Revenue) locally.
3. Optionally fetch associated contacts for enriched reporting.
