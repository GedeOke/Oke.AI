"""
OpenAI embedding provider implementation.
"""
import os
from typing import List

from app.ai.embedding.embed_provider import BaseEmbeddingProvider, EmbeddingProviderError
from app.utils.logger import get_logger

logger = get_logger(__name__)

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - optional dependency
    OpenAI = None


class OpenAIEmbeddingProvider(BaseEmbeddingProvider):
    """
    OpenAI embedding provider using text-embedding-3-small by default.
    """

    provider_name = "openai"

    def __init__(self, settings):
        super().__init__(settings)
        api_key = settings.openai_api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise EmbeddingProviderError("OPENAI_API_KEY is not configured.")
        if OpenAI is None:
            raise EmbeddingProviderError("openai package is not installed.")

        self.client = OpenAI(api_key=api_key)
        self.model = "text-embedding-3-small"

    def embed_text(self, text: str) -> List[float]:
        try:
            response = self.client.embeddings.create(
                input=text, model=self.model, dimensions=None
            )
            return response.data[0].embedding
        except Exception as exc:  # pragma: no cover - external call
            logger.exception("OpenAI embedding failed")
            raise EmbeddingProviderError("OpenAI embedding failed.") from exc
