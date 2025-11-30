"""
Voyage embedding provider implementation.
"""
import os
from typing import List

from app.ai.embedding.embed_provider import BaseEmbeddingProvider, EmbeddingProviderError
from app.utils.logger import get_logger

logger = get_logger(__name__)

try:
    import voyageai
except ImportError:  # pragma: no cover - optional dependency
    voyageai = None


class VoyageEmbeddingProvider(BaseEmbeddingProvider):
    """
    Voyage AI embedding provider.
    """

    provider_name = "voyage"

    def __init__(self, settings):
        super().__init__(settings)
        api_key = getattr(settings, "voyage_api_key", None) or os.getenv("VOYAGE_API_KEY")
        if not api_key:
            raise EmbeddingProviderError("VOYAGE_API_KEY is not configured.")
        if voyageai is None:
            raise EmbeddingProviderError("voyageai package is not installed.")

        self.client = voyageai.Client(api_key)
        self.model = "voyage-3"

    def embed_text(self, text: str) -> List[float]:
        try:
            response = self.client.embed([text], model=self.model)
            embeddings = getattr(response, "embeddings", None)
            return embeddings[0] if embeddings else []
        except Exception as exc:  # pragma: no cover - external call
            logger.exception("Voyage embedding failed")
            raise EmbeddingProviderError("Voyage embedding failed.") from exc
