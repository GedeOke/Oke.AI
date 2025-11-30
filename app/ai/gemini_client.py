"""
Gemini provider implementation.
"""
import asyncio
import os
from typing import AsyncGenerator, Dict, List

from app.ai.llm_provider import BaseLLMProvider, LLMProviderError
from app.utils.logger import get_logger

logger = get_logger(__name__)

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover - optional dependency
    genai = None


class GeminiClient(BaseLLMProvider):
    """
    Gemini (Google Generative AI) provider implementation.
    """

    provider_name = "gemini"

    def __init__(self, settings):
        super().__init__(settings)
        api_key = settings.gemini_api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise LLMProviderError("GEMINI_API_KEY is not configured.")
        if genai is None:
            raise LLMProviderError("google-generativeai package is not installed.")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def generate_text(self, prompt: str, **kwargs) -> str:
        try:
            response = await asyncio.to_thread(
                self.model.generate_content, prompt, **kwargs
            )
            return getattr(response, "text", "") or ""
        except Exception as exc:  # pragma: no cover - external call
            logger.exception("Gemini text generation failed")
            raise LLMProviderError("Gemini text generation failed.") from exc

    async def generate_chat(
        self, messages: List[Dict[str, str]], **kwargs
    ) -> str:
        prompt = "\n".join(f"{item['role']}: {item['content']}" for item in messages)
        return await self.generate_text(prompt, **kwargs)

    async def stream_chat(
        self, messages: List[Dict[str, str]], **kwargs
    ) -> AsyncGenerator[str, None]:
        try:
            prompt = "\n".join(f"{item['role']}: {item['content']}" for item in messages)
            stream = await asyncio.to_thread(
                self.model.generate_content, prompt, stream=True, **kwargs
            )
            for chunk in stream:
                text = getattr(chunk, "text", "") or ""
                if text:
                    yield text
        except Exception as exc:  # pragma: no cover - external call
            logger.exception("Gemini streaming failed")
            raise LLMProviderError("Gemini streaming failed.") from exc
