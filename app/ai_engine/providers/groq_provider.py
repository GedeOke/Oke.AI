"""
Groq provider wrapper.
"""
import os
from typing import Any, Dict, List

from app.ai_engine.utils.exceptions import ProviderError
from app.ai_engine.utils.logger import get_logger

logger = get_logger(__name__)

try:
    from groq import Groq
except ImportError:  # pragma: no cover
    Groq = None


class GroqProvider:
    def __init__(self) -> None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or Groq is None:
            raise ProviderError("Groq not configured or package missing.")
        self.client = Groq(api_key=api_key)
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")

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
            logger.exception("Groq chat failed")
            raise ProviderError("Groq chat failed") from exc
