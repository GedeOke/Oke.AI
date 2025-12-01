"""
Gemini provider wrapper.
"""
import os
from typing import Any, Dict, List

from app.ai_engine.utils.exceptions import ProviderError
from app.ai_engine.utils.logger import get_logger

logger = get_logger(__name__)

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover
    genai = None


class GeminiProvider:
    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or genai is None:
            raise ProviderError("Gemini not configured or package missing.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-1.5-flash"))

    async def chat(self, messages: List[Dict[str, str]], params: Dict[str, Any]) -> Dict[str, Any]:
        prompt = "\n".join(f"{m['role']}: {m['content']}" for m in messages)
        try:
            resp = await self.model.generate_content_async(
                prompt,
                generation_config={
                    "temperature": params.get("temperature", 0.3),
                    "top_p": params.get("top_p"),
                    "max_output_tokens": params.get("max_tokens"),
                },
            )
            content = getattr(resp, "text", "") or ""
            return {"content": content, "raw": resp}
        except Exception as exc:  # pragma: no cover
            logger.exception("Gemini chat failed")
            raise ProviderError("Gemini chat failed") from exc
