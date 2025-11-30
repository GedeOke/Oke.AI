"""
Groq provider implementation.
"""
import asyncio
import os
from typing import AsyncGenerator, Dict, List

from app.ai.llm_provider import BaseLLMProvider, LLMProviderError
from app.utils.logger import get_logger

logger = get_logger(__name__)

try:
    from groq import Groq
except ImportError:  # pragma: no cover - optional dependency
    Groq = None


class GroqClient(BaseLLMProvider):
    """
    Groq LLM provider implementation.
    """

    provider_name = "groq"

    def __init__(self, settings):
        super().__init__(settings)
        api_key = settings.groq_api_key or os.getenv("GROQ_API_KEY")
        if not api_key:
            raise LLMProviderError("GROQ_API_KEY is not configured.")
        if Groq is None:
            raise LLMProviderError("groq package is not installed.")

        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-70b-versatile"

    async def generate_text(self, prompt: str, **kwargs) -> str:
        messages = [{"role": "user", "content": prompt}]
        return await self.generate_chat(messages, **kwargs)

    async def generate_chat(
        self, messages: List[Dict[str, str]], **kwargs
    ) -> str:
        try:
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=messages,
                **kwargs,
            )
            return response.choices[0].message.content or ""
        except Exception as exc:  # pragma: no cover - external call
            logger.exception("Groq chat generation failed")
            raise LLMProviderError("Groq chat generation failed.") from exc

    async def stream_chat(
        self, messages: List[Dict[str, str]], **kwargs
    ) -> AsyncGenerator[str, None]:
        try:
            stream = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=messages,
                stream=True,
                **kwargs,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    yield delta
        except Exception as exc:  # pragma: no cover - external call
            logger.exception("Groq streaming failed")
            raise LLMProviderError("Groq streaming failed.") from exc
