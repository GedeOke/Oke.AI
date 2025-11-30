"""
Hugging Face hosted embedding provider implementation.
"""
import os
from typing import List

from app.ai.embedding.embed_provider import BaseEmbeddingProvider, EmbeddingProviderError
from app.utils.logger import get_logger

logger = get_logger(__name__)

try:
    from huggingface_hub import InferenceClient
except ImportError:  # pragma: no cover - optional dependency
    InferenceClient = None


class HuggingFaceEmbeddingProvider(BaseEmbeddingProvider):
    """
    Hugging Face Inference API embedding provider.
    """

    provider_name = "hf"

    def __init__(self, settings):
        super().__init__(settings)
        token = settings.huggingface_api_key or os.getenv("HUGGINGFACE_API_KEY")
        if InferenceClient is None:
            raise EmbeddingProviderError("huggingface_hub package is not installed.")

        self.model = "sentence-transformers/all-MiniLM-L6-v2"
        self.client = InferenceClient(model=self.model, token=token)

    def embed_text(self, text: str) -> List[float]:
        try:
            result = self.client.feature_extraction(text)
            # feature_extraction returns List[List[float]]; use first embedding vector.
            return result[0] if result and isinstance(result[0], list) else result
        except Exception as exc:  # pragma: no cover - external call
            logger.exception("Hugging Face embedding failed")
            raise EmbeddingProviderError("Hugging Face embedding failed.") from exc
