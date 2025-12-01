"""
Prompt builder using composite techniques (BothINST, REIT, RIGHT, MOCK, INFO, NAME, POS).
"""
from typing import Any, Dict, List, Optional

from app.ai_engine.utils.logger import get_logger

logger = get_logger(__name__)


def build_prompt(
    identity: str,
    persona: str,
    rules: List[str],
    style: str,
    examples: List[Dict[str, str]],
    rag_chunks: Optional[List[str]] = None,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    safety_rules: Optional[List[str]] = None,
    action_mode: str = "normal",
    call_word: str = "",
) -> List[Dict[str, str]]:
    """
    Construct system + context messages for chat completion.
    """
    rag_text = "\n".join(rag_chunks or [])
    rules_text = "\n".join(f"- {r}" for r in (rules or []))
    safety_text = "\n".join(f"- {r}" for r in (safety_rules or []))
    examples_text = "\n".join(f"{e.get('role', 'user')}: {e.get('content','')}" for e in (examples or []))

    system_prompt = f"""
You are {identity}.
Persona: {persona}
Style: {style}
Rules:
{rules_text}
Safety:
{safety_text}
Action mode: {action_mode}
RAG:
{rag_text}
Examples:
{examples_text}
Call word: {call_word}
Techniques: BothINST, REIT, RIGHT, MOCK, INFO, NAME, POS.
    """.strip()

    messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]
    if conversation_history:
        messages.extend(conversation_history)
    return messages
