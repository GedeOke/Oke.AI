"""
Prompt builder using composite techniques (BothINST, REIT, RIGHT, MOCK, INFO, NAME, POS).
"""
from typing import Any, Dict, List, Optional

from app.ai_engine.utils.logger import get_logger

logger = get_logger(__name__)


def build(
    ai_settings: Dict[str, Any],
    rag_chunks: str,
    history: Optional[List[Dict[str, str]]] = None,
) -> List[Dict[str, str]]:
    persona = ai_settings.get("persona") or "Helpful assistant"
    rules = ai_settings.get("rules") or []
    style = ai_settings.get("style") or ""
    examples = ai_settings.get("examples") or []
    call_word = ai_settings.get("call_word", "")
    safety_rules = ai_settings.get("safety_rules", [])
    action_mode = ai_settings.get("action_mode", "normal")

    rules_text = "\n".join(f"- {r}" for r in rules)
    safety_text = "\n".join(f"- {r}" for r in safety_rules)
    examples_text = "\n".join(f"{e.get('role', 'user')}: {e.get('content','')}" for e in examples)
    info_text = rag_chunks or "Tidak ada informasi relevan."

    system_prompt = f"""
NAME: OkeAI Agent
IDENTITY: AI assistant untuk organisasi.
PERSONA: {persona}
STYLE: {style}
RULES:
{rules_text}
SAFETY:
{safety_text}
INFO (RAG):
{info_text}
EXAMPLES:
{examples_text}
CALL WORD: {call_word}
ACTION MODE: {action_mode}
TECHNIQUES: BothINST, REIT, RIGHT, MOCK, INFO, NAME, POS.
""".strip()

    messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]
    if history:
        messages.extend(history)
    return messages
