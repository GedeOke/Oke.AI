"""
OpenAI provider wrapper.
"""
import os
from typing import Any, Dict, List

from app.ai_engine.utils.exceptions import ProviderError
from app.ai_engine.utils.logger import get_logger

logger = get_logger(__name__)

try:
    from openai import AsyncOpenAI
except ImportError:  # pragma: no cover
    AsyncOpenAI = None


class OpenAIProvider:
    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or AsyncOpenAI is None:
            raise ProviderError("OpenAI not configured or package missing.")
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    async def chat(self, messages: List[Dict[str, str]], params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            resp = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=params.get("temperature", 0.3),
                top_p=params.get("top_p"),
                max_tokens=params.get("max_tokens"),
                frequency_penalty=params.get("frequency_penalty"),
                presence_penalty=params.get("presence_penalty"),
            )
            content = resp.choices[0].message.content or ""
            return {"content": content, "raw": resp}
        except Exception as exc:  # pragma: no cover
            logger.exception("OpenAI chat failed")
            raise ProviderError("OpenAI chat failed") from exc
