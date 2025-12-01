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

# Integrasi RAG ke AI Engine
- Query optimizer menghasilkan beberapa varian query.
- Retriever meng-embed query, vector search via pgvector, lalu memberi chunk terformat ke prompt builder (INFO).
- Pipeline AI tetap jalan meski RAG kosong/error (fallback “Tidak ada informasi relevan.”).
- Endpoint test: `POST /ai/test/rag` dengan `organization_id` dan `query` untuk melihat queries/chunks yang dipakai.

# Cara Tes Cepat
- Jalankan `pytest tests/test_rag_chunker.py` untuk chunker.
- Panggil `POST /ai/test/rag` (pastikan tabel dan embeddings ada) untuk cek retrieval.
- Jalankan `run_ai_pipeline` seperti contoh sebelumnya; pastikan provider API key terisi.
