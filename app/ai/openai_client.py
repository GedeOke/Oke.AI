"""
OpenAI provider implementation.
"""
import asyncio
import os
from typing import AsyncGenerator, Dict, List

from app.ai.llm_provider import BaseLLMProvider, LLMProviderError
from app.utils.logger import get_logger

logger = get_logger(__name__)

try:
    from openai import AsyncOpenAI, OpenAI
except ImportError:  # pragma: no cover - optional dependency
    AsyncOpenAI = None
    OpenAI = None


class OpenAIClient(BaseLLMProvider):
    """
    OpenAI LLM provider.
    """

    provider_name = "openai"

    def __init__(self, settings):
        super().__init__(settings)
        api_key = settings.openai_api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise LLMProviderError("OPENAI_API_KEY is not configured.")

        if AsyncOpenAI:
            self.client = AsyncOpenAI(api_key=api_key)
            self._async_client = True
        elif OpenAI:
            self.client = OpenAI(api_key=api_key)
            self._async_client = False
        else:
            raise LLMProviderError("openai package is not installed.")

        self.model = "gpt-4o-mini"

    async def generate_text(self, prompt: str, **kwargs) -> str:
        messages = [{"role": "user", "content": prompt}]
        return await self.generate_chat(messages, **kwargs)

    async def generate_chat(
        self, messages: List[Dict[str, str]], **kwargs
    ) -> str:
        try:
            if self._async_client:
                response = await self.client.chat.completions.create(
                    model=self.model, messages=messages, **kwargs
                )
            else:
                response = await asyncio.to_thread(
                    self.client.chat.completions.create,
                    model=self.model,
                    messages=messages,
                    **kwargs,
                )
            return response.choices[0].message.content or ""
        except Exception as exc:  # pragma: no cover - external call
            logger.exception("OpenAI chat generation failed")
            raise LLMProviderError("OpenAI chat generation failed.") from exc

    async def stream_chat(
        self, messages: List[Dict[str, str]], **kwargs
    ) -> AsyncGenerator[str, None]:
        try:
            if self._async_client:
                stream = await self.client.chat.completions.create(
                    model=self.model, messages=messages, stream=True, **kwargs
                )
                async for chunk in stream:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        yield delta
            else:
                # Fallback: yield full response once when async client is unavailable.
                result = await self.generate_chat(messages, **kwargs)
                yield result
        except Exception as exc:  # pragma: no cover - external call
            logger.exception("OpenAI stream failed")
            raise LLMProviderError("OpenAI streaming failed.") from exc
