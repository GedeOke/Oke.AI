"""
RAG retriever combining query optimization, embedding, and vector search.
"""
from typing import Any, Dict, List

from fastapi import HTTPException, status

from app.rag.embedder import Embedder
from app.rag.vector_store import search
from app.rag.chunker import chunk_text
from app.ai_engine.utils.logger import get_logger

logger = get_logger(__name__)


def optimize_queries(message: str) -> List[str]:
    parts = [message]
    words = message.split()
    if len(words) > 6:
        parts.append(" ".join(words[:6]))
        parts.append(" ".join(words[-6:]))
    return parts


def retrieve(org_id: str, message: str, embed_provider: str = "openai", top_k: int = 6) -> List[str]:
    embedder = Embedder(embed_provider)
    queries = optimize_queries(message)
    embeddings = embedder.embed_batch(queries)

    results: List[Dict[str, Any]] = []
    for emb in embeddings:
        hits = search(org_id, emb, top_k=top_k)
        results.extend(hits)

    # Deduplicate by chunk id, preserve order
    seen = set()
    chunks: List[str] = []
    for hit in results:
        cid = hit.get("id") or hit.get("chunk_id")
        if cid in seen:
            continue
        seen.add(cid)
        content = hit.get("content")
        if content:
            chunks.append(content)
    return chunks[:8]
