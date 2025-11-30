"""
LLM provider interface and loader.
"""
from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, List, Optional

from app.core.config import Settings, get_settings


class LLMProviderError(Exception):
    """Custom exception for LLM provider issues."""


class BaseLLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    """

    provider_name: str = "base"

    def __init__(self, settings: Settings):
        self.settings = settings

    @abstractmethod
    async def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text completion from a prompt."""

    @abstractmethod
    async def generate_chat(
        self, messages: List[Dict[str, str]], **kwargs
    ) -> str:
        """Generate a chat-style response."""

    @abstractmethod
    async def stream_chat(
        self, messages: List[Dict[str, str]], **kwargs
    ) -> AsyncGenerator[str, None]:
        """Stream chat responses incrementally."""


def get_llm_provider(
    provider_name: Optional[str] = None, settings: Optional[Settings] = None
) -> BaseLLMProvider:
    """
    Factory to load the correct LLM provider implementation.
    """
    settings = settings or get_settings()
    provider_key = (provider_name or settings.llm_provider or "openai").lower()

    if provider_key == "openai":
        from app.ai.openai_client import OpenAIClient

        return OpenAIClient(settings)
    if provider_key == "groq":
        from app.ai.groq_client import GroqClient

        return GroqClient(settings)
    if provider_key == "gemini":
        from app.ai.gemini_client import GeminiClient

        return GeminiClient(settings)

    raise LLMProviderError(f"Unsupported LLM provider: {provider_key}")
