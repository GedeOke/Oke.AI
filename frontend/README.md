# OkeAI Dashboard (Frontend)

React + Vite + Tailwind dashboard untuk AI Playground dan Inbox dasar.

## Setup
```bash
cd frontend
npm install
npm run dev
```
Env optional: set `VITE_API_BASE` untuk URL backend (default `http://localhost:8000`).

## Struktur
- `src/components/ui`: Button, Card, Input, Textarea.
- `src/components/layout`: Sidebar, Topbar.
- `src/components/ai`: Model selector, result panel, payload viewer.
- `src/components/inbox`: Conversation list, message list, message input/item.
- `src/pages`: `AiPlayground`, `Inbox`.
- `src/lib`: `axios` instance, API wrapper.
- `src/hooks`: `useAi`, `useConversations`.
- `src/context`: `OrganizationContext`.
- `src/styles`: `globals.css`.

## AI Playground
Form prompt + dropdown provider/model. Panggil `POST /ai/run` dengan payload:
```json
{
  "organization_id": "<org>",
  "message": "...",
  "model_provider": "openai",
  "model": "gpt-4o-mini"
}
```
Hasil yang ditampilkan: reply, intent, sentiment, RAG chunks, planner, safety, payload request.

## Inbox
- List conversations: `GET /conversations`
- List messages: `GET /messages/conversations/{id}`
- Kirim pesan: `POST /messages/send`

## Test Cepat
1. Set `VITE_API_BASE` jika backend bukan localhost:8000.
2. Set Organization ID di topbar (UUID org).
3. Buka AI Playground, isi prompt, klik Run.
4. Buka Inbox, pilih conversation, kirim pesan.

## Auth (Login/Register)
- Pages: `/login`, `/register`.
- API: Supabase Auth (`/auth/v1/signup`, `/auth/v1/token?grant_type=password`) via `VITE_SUPABASE_URL` dan `VITE_SUPABASE_KEY`.
- Token disimpan di localStorage, dipakai untuk request backend via Axios interceptor.
- Protected routes: `/ai`, `/inbox` redirect ke login jika belum login.
