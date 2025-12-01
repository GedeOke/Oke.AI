"""
Safety checks for AI responses.
"""
from typing import Dict

from app.ai_engine.utils.logger import get_logger

logger = get_logger(__name__)


def check_safety(response: str) -> Dict[str, str]:
    unsafe_keywords = ["hate", "violence"]
    for kw in unsafe_keywords:
        if kw in response.lower():
            return {"safe": False, "reason": f"Contains unsafe content: {kw}"}
    return {"safe": True, "reason": ""}
