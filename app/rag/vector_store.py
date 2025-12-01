"""
Vector store operations using Supabase/pgvector.
"""
from typing import Any, Dict, List
from uuid import uuid4

from fastapi import HTTPException, status

from app.db.supabase import get_supabase_client
from app.utils.logger import get_logger

logger = get_logger(__name__)


def insert_chunk(org_id: str, doc_id: str, content: str, embedding: List[float], metadata: Dict[str, Any] | None) -> str:
    client = get_supabase_client()
    chunk_id = str(uuid4())
    record = {
        "id": chunk_id,
        "organization_id": org_id,
        "document_id": doc_id,
        "content": content,
        "embedding": embedding,
        "metadata": metadata or {},
    }
    try:
        client.table("ai_chunks").insert(record).execute()
    except Exception as exc:  # pragma: no cover - external call
        logger.exception("Failed to insert chunk")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to insert chunk.",
        ) from exc
    return chunk_id


def search(org_id: str, embedding: List[float], top_k: int = 6) -> List[Dict[str, Any]]:
    """
    Vector search using a Supabase RPC function match_ai_chunks (needs to be created).
    Falls back to empty result on failure.
    """
    client = get_supabase_client()
    try:
        resp = client.rpc(
            "match_ai_chunks",
            {"query_embedding": embedding, "match_count": top_k, "match_org": org_id},
        ).execute()
        return getattr(resp, "data", None) or []
    except Exception:  # pragma: no cover - external call
        logger.warning("Vector search failed or RPC missing", extra={"org_id": org_id})
        return []
