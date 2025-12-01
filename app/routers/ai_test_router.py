"""
Test endpoints for AI/RAG.
"""
from fastapi import APIRouter, HTTPException

from app.rag.query_optimizer import generate as generate_queries
from app.rag.retriever import retrieve

router = APIRouter(prefix="/ai/test", tags=["ai-test"])


@router.post("/rag")
async def test_rag(payload: dict):
    org_id = payload.get("organization_id")
    query = payload.get("query", "")
    embed_provider = payload.get("embed_provider", "openai")
    if not org_id or not query:
        raise HTTPException(status_code=400, detail="organization_id and query are required")
    queries = generate_queries(query)
    try:
        chunks = retrieve(org_id, queries, embed_provider=embed_provider, top_k=6)
    except Exception:
        chunks = []
    formatted = "\n\n".join([f"- {c.get('content')}" for c in chunks]) if chunks else "Tidak ada informasi relevan."
    return {"queries": queries, "chunks": chunks, "formatted": formatted}
