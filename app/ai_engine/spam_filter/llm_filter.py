"""
LLM-based spam filter using prompt.
"""
from typing import Any, Dict

from app.ai_engine.providers.provider_selector import chat_completion

PROMPT = """
Determine if the message is spam or noise. Respond with JSON: {"spam": true|false}.
"""


async def is_spam_llm(provider: str, message: str, metadata: Dict[str, Any] | None = None) -> bool:
    messages = [{"role": "system", "content": PROMPT}, {"role": "user", "content": message}]
    result = await chat_completion(provider, messages, {"temperature": 0.0, "max_tokens": 16})
    return "true" in result["content"].lower()
