"""
Testing endpoints for AI/RAG.
"""
from fastapi import APIRouter, Depends, HTTPException

from app.core.security import get_current_user
from app.rag import query_optimizer, retriever

router = APIRouter(prefix="/ai/test", tags=["ai-test"])


@router.post("/rag")
async def test_rag(payload: dict, current_user=Depends(get_current_user)):
    org_id = payload.get("organization_id")
    query = payload.get("query", "")
    embed_provider = payload.get("embed_provider", "openai")
    if not org_id or not query:
        raise HTTPException(status_code=400, detail="organization_id and query are required")
    queries = query_optimizer.generate(query)
    try:
        chunks = retriever.retrieve(org_id, queries, embed_provider=embed_provider, top_k=6)
    except Exception:
        chunks = []
    formatted = "\n\n".join([f"- {c.get('content')}" for c in chunks]) if chunks else "Tidak ada informasi relevan."
    return {"queries": queries, "chunks": chunks, "formatted": formatted}
