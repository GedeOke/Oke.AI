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
