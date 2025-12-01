"""
Tone rewriter to align with persona/style.
"""
from typing import Dict

from app.ai_engine.providers.provider_selector import chat_completion

PROMPT = """
Rewrite the assistant reply to match the persona and style provided.
Reply with the rewritten text only.
"""


async def rewrite_tone(provider: str, reply: str, persona: str, style: str) -> str:
    messages = [
        {"role": "system", "content": PROMPT + f"\nPersona: {persona}\nStyle: {style}"},
        {"role": "user", "content": reply},
    ]
    result = await chat_completion(provider, messages, {"temperature": 0.4, "max_tokens": 256})
    return result["content"]
