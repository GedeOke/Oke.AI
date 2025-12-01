"""
RAG retriever combining query optimization, embedding, and vector search.
"""
from typing import Any, Dict, List

from app.rag.embedder import Embedder
from app.rag.vector_store import search
from app.ai_engine.utils.logger import get_logger

logger = get_logger(__name__)


def retrieve(org_id: str, queries: List[str], embed_provider: str = "openai", top_k: int = 6) -> List[Dict[str, Any]]:
    """
    Retrieve relevant chunks for a list of optimized queries.
    """
    embedder = Embedder(embed_provider)
    embeddings = embedder.embed_batch(queries)

    results: List[Dict[str, Any]] = []
    for emb in embeddings:
        hits = search(org_id, emb, top_k=top_k)
        results.extend(hits)

    seen = set()
    chunks: List[Dict[str, Any]] = []
    for hit in results:
        cid = hit.get("id") or hit.get("chunk_id")
        if cid in seen:
            continue
        seen.add(cid)
        content = hit.get("content")
        if content:
            chunks.append(
                {
                    "id": cid,
                    "content": content,
                    "metadata": hit.get("metadata"),
                    "similarity": hit.get("similarity"),
                }
            )
    return chunks[:8]
