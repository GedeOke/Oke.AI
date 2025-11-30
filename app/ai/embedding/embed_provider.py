"""
Embedding provider interface and loader.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from app.core.config import Settings, get_settings


class EmbeddingProviderError(Exception):
    """Custom exception for embedding provider issues."""


class BaseEmbeddingProvider(ABC):
    """
    Abstract base class for embedding providers.
    """

    provider_name: str = "base"

    def __init__(self, settings: Settings):
        self.settings = settings

    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """Embed the provided text into a vector space."""


def get_embedding_provider(
    provider_name: Optional[str] = None, settings: Optional[Settings] = None
) -> BaseEmbeddingProvider:
    """
    Factory to load the configured embedding provider.
    """
    settings = settings or get_settings()
    provider_key = (provider_name or settings.embed_model_provider or "openai").lower()

    if provider_key == "openai":
        from app.ai.embedding.openai_embed import OpenAIEmbeddingProvider

        return OpenAIEmbeddingProvider(settings)
    if provider_key == "hf":
        from app.ai.embedding.hf_embed import HuggingFaceEmbeddingProvider

        return HuggingFaceEmbeddingProvider(settings)
    if provider_key == "local":
        from app.ai.embedding.local_sentence_transformer import (
            LocalSentenceTransformerProvider,
        )

        return LocalSentenceTransformerProvider(settings)
    if provider_key == "voyage":
        from app.ai.embedding.voyage_embed import VoyageEmbeddingProvider

        return VoyageEmbeddingProvider(settings)

    raise EmbeddingProviderError(f"Unsupported embedding provider: {provider_key}")
