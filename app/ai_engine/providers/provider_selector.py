"""
Provider selector for AI Engine.
"""
from typing import Any, Dict

from app.ai_engine.providers.gemini_provider import GeminiProvider
from app.ai_engine.providers.groq_provider import GroqProvider
from app.ai_engine.providers.openai_provider import OpenAIProvider
from app.ai_engine.utils.exceptions import ProviderError


def select_provider(provider_name: str) -> Any:
    name = (provider_name or "").lower()
    if name == "openai":
        return OpenAIProvider()
    if name == "groq":
        return GroqProvider()
    if name == "gemini":
        return GeminiProvider()
    raise ProviderError(f"Unsupported provider: {provider_name}")


async def chat_completion(
    provider_name: str,
    messages: list[Dict[str, str]],
    params: Dict[str, Any],
) -> Dict[str, Any]:
    provider = select_provider(provider_name)
    return await provider.chat(messages=messages, params=params)
