# AI Engine – OkeAI (FastAPI + Supabase)

Modular AI engine for OkeAI with multi-provider LLMs, prompt tuning, safety, RAG, memory, and orchestration.

## Arsitektur
- `providers/`: OpenAI, Groq, Gemini wrappers + selector.
- `tuning/`: AI settings loader (Supabase `ai_settings`), master prompt builder (BothINST, REIT, RIGHT, MOCK, INFO, NAME, POS).
- `classifiers/`: Intent & sentiment classification.
- `spam_filter/`: Rule, ML placeholder, LLM fallback with pipeline.
- `rag/`: Query optimizer + retriever (Supabase table `rag_chunks` placeholder).
- `memory/`: Summarizer + memory manager (store to `ai_memory`).
- `safety/`: Safety checker.
- `planner/`: Function calling planner.
- `autopilot/`: Auto-reply decider.
- `rewriter/`: Tone rewriter.
- `agent_assist/`: Suggestion generator.
- `orchestrator/`: Pipeline executor.
- `utils/`: Logger, exceptions, validation.

## Pipeline (simplified)
1. Spam check (rule → ML → optional LLM).
2. Intent classification.
3. Sentiment analysis.
4. Query optimization + RAG retrieval.
5. Load AI settings (persona, rules, style, examples, LLM params, tools).
6. Build prompt (system + history + RAG).
7. LLM chat (provider selector).
8. Safety check.
9. Function planner.
10. Autopilot decision.
11. Tone rewrite.
12. Agent suggestions.
13. Return reply/action/metadata.

## Contoh Penggunaan (pseudo)
```python
from app.ai_engine.orchestrator.ai_orchestrator import run_ai_pipeline

result = await run_ai_pipeline(
    org_id="org-uuid",
    user_message="Halo, saya butuh bantuan",
    conversation_context=[
        {"role": "user", "content": "Halo"},
        {"role": "assistant", "content": "Hai, ada yang bisa dibantu?"}
    ],
    provider="openai",
)
print(result["reply"])
```

## Contoh Request/Response (high level)
- Input: `org_id`, `user_message`, optional `conversation_context`, `provider`
- Output:
```json
{
  "reply": "...",
  "action": null,
  "classification": {"intent": "..."},
  "sentiment": "positive|neutral|negative",
  "rag_used": true,
  "should_auto_reply": true,
  "safety": {"safe": true, "reason": ""},
  "suggestions": ["..."]
}
```

## Webhook / Integrasi
- Inbound webhook → gunakan `message_service.ingest_message_auto` untuk membuat customer + conversation + message, lalu panggil `run_ai_pipeline`.
- RLS: pastikan `organization_id` selalu difilter dari konteks user.

## Tuning AI
- Atur tabel `ai_settings` per organisasi untuk persona, rules, style, examples, call_word, rag, llm_params, tools schema.
- Set env keys untuk provider: `OPENAI_API_KEY`, `GROQ_API_KEY`, `GEMINI_API_KEY` (+ optional model overrides).

---

# RAG Module

## Alur Upload → Chunk → Embed
1) Upload file via `POST /rag/upload` (pdf/docx/txt) atau teks via `POST /rag/text`.
2) Ekstrak teks → chunking (`chunk_size` default 500, overlap 50).
3) Embedding (OpenAI/Gemini/local ST) → simpan ke `ai_chunks` dengan metadata.
4) Dokumen tercatat di `ai_documents`.

## Vector Search
- `GET /rag/search?query=...` → embed query, panggil RPC `match_ai_chunks` (pgvector) → kembalikan chunks terbaik.
- Index: `create index on ai_chunks using ivfflat (embedding vector_cosine_ops);`

## Integrasi AI Engine
- Orchestrator memanggil `rag.retrieve(org_id, user_message, embed_provider=...)` sebelum build prompt.
- `rag_chunks` dikirim ke prompt builder sebagai konteks.

## Format Dokumen Didukung
- `.pdf` (butuh PyPDF2)
- `.docx` (butuh python-docx)
- `.txt` (plain text)

## Endpoint Ringkas
- `POST /rag/upload` (UploadFile)
- `POST /rag/text` (JSON text/title/source)
- `GET /rag/documents`
- `GET /rag/search?query=...`

## Prosedur SQL (Supabase)
```sql
create table if not exists public.ai_documents (
  id uuid primary key,
  organization_id uuid references public.organizations(id),
  title text,
  source text,
  created_at timestamp with time zone default now()
);

create table if not exists public.ai_chunks (
  id uuid primary key,
  organization_id uuid,
  document_id uuid references public.ai_documents(id),
  content text,
  embedding vector(1536),
  metadata jsonb,
  created_at timestamp with time zone default now()
);

create index on public.ai_chunks using ivfflat (embedding vector_cosine_ops);
```

# WhatsApp Webhook Channel

## Endpoint
- `GET /webhook/whatsapp/{organization_id}` untuk verification (hub.challenge). Env: `WHATSAPP_VERIFY_TOKEN`.
- `POST /webhook/whatsapp/{organization_id}` untuk event/pesan.
- Opsional: `POST /webhook/whatsapp/test/send` body `{ "organization_id": "...", "phone": "...", "text": "..." }`.

## Signature
- Header `X-Hub-Signature-256` divalidasi dengan HMAC SHA256 dan `WHATSAPP_APP_SECRET`.
- Jika secret tidak diset, validasi dilewati (direkomendasikan untuk diisi).

## Flow Inbound
1) Verify signature → normalize payload (text/image/audio minimal).
2) Dedup message_id via tabel `whatsapp_message_log`.
3) Spam filter.
4) Find/create customer (`source=whatsapp`) dan conversation (`channel=whatsapp`).
5) Simpan pesan customer ke `messages`.
6) Panggil `run_ai_pipeline` → simpan balasan AI ke `messages`.
7) Kirim balasan ke WhatsApp Cloud API (env `WHATSAPP_TOKEN`, `WHATSAPP_PHONE_NUMBER_ID`).
8) Logging structured.

## Tabel Dedup
```sql
create table if not exists public.whatsapp_message_log (
  message_id text,
  organization_id uuid,
  created_at timestamp with time zone default now()
);
create index if not exists idx_whatsapp_msg_log on public.whatsapp_message_log (organization_id, message_id);
```

## Contoh Payload WhatsApp (text)
```json
{
  "entry": [{
    "changes": [{
      "value": {
        "messages": [{
          "id": "wamid.ABCD",
          "from": "628123456789",
          "timestamp": "1700000000",
          "type": "text",
          "text": {"body": "Halo"}
        }]
      }
    }]
  }]
}
```

## Cara Tes (manual)
- GET verification: `curl -G "http://localhost:8000/webhook/whatsapp/<org_id>" --data-urlencode "hub.mode=subscribe" --data-urlencode "hub.verify_token=<token>" --data-urlencode "hub.challenge=123"`.
- POST event: kirim payload di atas ke endpoint POST dengan header signature sesuai `WHATSAPP_APP_SECRET`.
- Test send: `POST /webhook/whatsapp/test/send` untuk kirim pesan WA outbound (butuh token/phone_number_id).
