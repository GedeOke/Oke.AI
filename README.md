# Patch: Customers + Conversations + Messages

Foundational schema and APIs for multi-tenant inbox/AI messaging.

## ERD (ringkas)
- `customers`: {id, organization_id, external_id, name, phone, email, source}
- `conversations`: {id, organization_id, customer_id, channel, status, assigned_to}
- `messages`: {id, organization_id, conversation_id, sender_type, sender_id, content, metadata}

## Auto-Create Flows
- `find_or_create_customer(org_id, external_id, source)`
- `find_or_create_conversation(org_id, customer_id, channel)`
- Inbound handling (future webhook): create customer+conversation if not exists, then insert message.

## Endpoints
- Customers: `GET /customers`, `GET /customers/{id}`, `POST /customers`, `PUT /customers/{id}`, `DELETE /customers/{id}`
- Conversations: `GET /conversations`, `GET /conversations/{id}`, `PUT /conversations/{id}/close`, `PUT /conversations/{id}/assign`
- Messages: `GET /messages/conversations/{id}`, `POST /messages/send`

## Send Message Example
```
POST /messages/send
Authorization: Bearer <token>
{
  "conversation_id": "<uuid>",
  "content": "Hello from agent",
  "metadata": {"source": "webchat"}
}
```

## Multi-Tenancy & Security
- All queries filtered by `organization_id` from the authenticated user.
- No cross-org access; RLS-ready on Supabase.

## Webhook Integration (future)
- Inbound webhook → call `find_or_create_customer` and `find_or_create_conversation`, then append message via service.
