"""
Local embedding provider using sentence-transformers.
"""
from typing import List

from app.ai.embedding.embed_provider import BaseEmbeddingProvider, EmbeddingProviderError
from app.utils.logger import get_logger

logger = get_logger(__name__)

try:
    from sentence_transformers import SentenceTransformer
except ImportError:  # pragma: no cover - optional dependency
    SentenceTransformer = None


class LocalSentenceTransformerProvider(BaseEmbeddingProvider):
    """
    Local embedding provider leveraging sentence-transformers.
    """

    provider_name = "local"

    def __init__(self, settings):
        super().__init__(settings)
        if SentenceTransformer is None:
            raise EmbeddingProviderError("sentence-transformers package is not installed.")
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> List[float]:
        try:
            vector = self.model.encode(text)
            return vector.tolist()
        except Exception as exc:  # pragma: no cover - external call
            logger.exception("Local sentence-transformer embedding failed")
            raise EmbeddingProviderError("Local embedding failed.") from exc
