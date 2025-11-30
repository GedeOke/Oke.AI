# OkeAI - Project Setup

Setup awal untuk platform OkeAI sebagai fondasi backend FastAPI dengan dukungan multi-LLM dan embedding modular.

## Tujuan
- Menyediakan kerangka produksi awal (struktur folder, konfigurasi, middleware dasar).
- Menyiapkan entrypoint FastAPI, handler error global, dan placeholder rate limit.
- Menyusun arsitektur modular untuk LLM provider dan embedding provider.
- Menghubungkan konfigurasi ke environment agar aman dari hard-coded secrets.

## Struktur Folder
```
OkeAI/
  app/
    ai/                      # LLM engines & embedding engines
      embedding/             # Embedding providers
    core/                    # Config & security helpers
    middlewares/             # Global error handler, rate limiting stub, logging
    utils/                   # Helper utilities (logging, rate limiting)
    db/                      # Supabase client
    routers/                 # API routers registry
    services/                # Business logic layer (placeholder)
    schemas/                 # Pydantic schemas (placeholder)
    models/                  # ORM/data models (placeholder)
  docs/                      # Dokumentasi tambahan (placeholder)
  tests/                     # Test suite (placeholder)
  main.py                    # FastAPI entrypoint
  requirements.txt           # Dependencies
  .env.example               # Contoh environment variables
  .gitignore                 # Ignore rules
  LICENSE
  README.md
```

## Environment
- Semua secrets hanya dibaca via `os.getenv`/`BaseSettings`.
- Salin `.env.example` menjadi `.env` lalu isi nilai yang sesuai.
- Pastikan `.env` tidak di-commit (sudah di-ignore).

## Multi-LLM & Embedding
- LLM providers: OpenAI, Groq, Gemini (pilih via `LLM_PROVIDER`).
- Embedding providers: OpenAI, Hugging Face Inference, Voyage, Local SentenceTransformer (pilih via `EMBED_MODEL_PROVIDER`).
- Factory pattern digunakan untuk memuat provider sesuai ENV agar mudah diperluas.

## Apa yang Belum Dibuat
- Router/endpoint bisnis, schemas, services, dan models masih placeholder.
- Rate limiting masih stub (perlu diganti solusi terdistribusi/Redis).
- Integrasi RAG, storage, dan orchestrasi agent belum diimplementasi.
