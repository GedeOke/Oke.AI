"""
AI settings loader from Supabase.
"""
from typing import Any, Dict, Optional

from fastapi import HTTPException, status

from app.db.supabase import get_supabase_client
from app.utils.logger import get_logger

logger = get_logger(__name__)


def load_ai_settings(org_id: str) -> Dict[str, Any]:
    """
    Load AI settings (persona, rules, style, examples, rag params, llm params, tools schema).
    Falls back to defaults if not found.
    """
    client = get_supabase_client()
    try:
        result = (
            client.table("ai_settings")
            .select("*")
            .eq("organization_id", org_id)
            .limit(1)
            .execute()
        )
    except Exception as exc:  # pragma: no cover - external call
        logger.exception("Failed to fetch ai_settings")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to load AI settings.",
        ) from exc

    data = getattr(result, "data", None) or []
    if not data:
        return {
            "persona": "Helpful assistant",
            "rules": [],
            "style": "",
            "examples": [],
            "call_word": "",
            "rag": {"top_k": 3},
            "llm_params": {"temperature": 0.3},
            "tools": [],
        }
    row = data[0]
    return {
        "persona": row.get("persona"),
        "rules": row.get("rules") or [],
        "style": row.get("style") or "",
        "examples": row.get("examples") or [],
        "call_word": row.get("call_word") or "",
        "rag": row.get("rag") or {},
        "llm_params": row.get("llm_params") or {},
        "tools": row.get("tools") or [],
    }
