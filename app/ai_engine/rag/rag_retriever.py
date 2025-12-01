"""
RAG retriever using Supabase (placeholder).
"""
from typing import Dict, List

from app.db.supabase import get_supabase_client
from app.utils.logger import get_logger

logger = get_logger(__name__)


def retrieve_chunks(org_id: str, query: str, top_k: int = 3) -> List[str]:
    """
    Retrieve top_k chunks from vector store (placeholder).
    """
    try:
        client = get_supabase_client()
        # Placeholder: adjust table/column names as needed.
        result = (
            client.table("rag_chunks")
            .select("content")
            .eq("organization_id", org_id)
            .limit(top_k)
            .execute()
        )
        data = getattr(result, "data", None) or []
        return [row["content"] for row in data if "content" in row]
    except Exception:  # pragma: no cover
        logger.info("RAG lookup skipped or failed", extra={"query": query})
        return []
