"""
Spam detection pipeline.
"""
from typing import Any, Dict

from app.ai_engine.spam_filter.rule_filter import is_spam_rule
from app.ai_engine.spam_filter.ml_filter import is_spam_ml
from app.ai_engine.spam_filter.llm_filter import is_spam_llm


async def is_spam(message: str, metadata: Dict[str, Any] | None, provider: str | None = None) -> bool:
    if is_spam_rule(message, metadata):
        return True
    if is_spam_ml(message, metadata):
        return True
    if provider:
        return await is_spam_llm(provider, message, metadata)
    return False
