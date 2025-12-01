"""
Embedding utilities for RAG.
"""
import os
from typing import Any, List, Optional

from app.ai_engine.utils.logger import get_logger
from app.ai_engine.utils.exceptions import ProviderError

logger = get_logger(__name__)

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover
    genai = None

try:
    from sentence_transformers import SentenceTransformer
except ImportError:  # pragma: no cover
    SentenceTransformer = None


class Embedder:
    def __init__(self, provider: str = "openai") -> None:
        self.provider = provider.lower()
        self.client = None
        self.model_name = None
        if self.provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key or OpenAI is None:
                raise ProviderError("OpenAI embedding not configured.")
            self.client = OpenAI(api_key=api_key)
            self.model_name = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
        elif self.provider == "gemini":
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key or genai is None:
                raise ProviderError("Gemini embedding not configured.")
            genai.configure(api_key=api_key)
            self.model_name = os.getenv("GEMINI_EMBED_MODEL", "text-embedding-004")
        elif self.provider == "local":
            if SentenceTransformer is None:
                raise ProviderError("Local embedding model not installed.")
            self.model_name = os.getenv("LOCAL_EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
            self.client = SentenceTransformer(self.model_name)
        else:
            raise ProviderError(f"Unsupported embedder provider: {provider}")

    def embed_text(self, text: str) -> List[float]:
        if self.provider == "openai":
            resp = self.client.embeddings.create(input=text, model=self.model_name)
            return resp.data[0].embedding
        if self.provider == "gemini":
            model = genai.embed_content  # type: ignore
            resp = model(model=self.model_name, content=text)
            return resp["embedding"]
        if self.provider == "local":
            vector = self.client.encode(text)
            return vector.tolist()
        raise ProviderError("Unsupported embedder provider.")

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        if self.provider == "openai":
            resp = self.client.embeddings.create(input=texts, model=self.model_name)
            return [item.embedding for item in resp.data]
        if self.provider == "gemini":
            outputs = []
            for t in texts:
                outputs.append(self.embed_text(t))
            return outputs
        if self.provider == "local":
            vectors = self.client.encode(texts)
            return [vec.tolist() for vec in vectors]
        raise ProviderError("Unsupported embedder provider.")
