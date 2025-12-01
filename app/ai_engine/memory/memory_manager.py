"""
Memory manager for compressing conversation history.
"""
from typing import List

from app.ai_engine.memory.summarizer import summarize
from app.db.supabase import get_supabase_client
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def compress_and_store(provider: str, org_id: str, conversation_id: str, history: List[dict]) -> str:
    summary = await summarize(provider, history)
    try:
        client = get_supabase_client()
        client.table("ai_memory").insert(
            {
                "organization_id": org_id,
                "conversation_id": conversation_id,
                "summary": summary,
            }
        ).execute()
    except Exception:  # pragma: no cover
        logger.info("Failed to store memory", extra={"conversation_id": conversation_id})
    return summary
