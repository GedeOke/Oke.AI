"""
Document ingestion service for RAG.
"""
import io
import os
from typing import Any, Dict, List, Optional
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status

from app.rag.chunker import chunk_text
from app.rag.embedder import Embedder
from app.rag.vector_store import insert_chunk
from app.db.supabase import get_supabase_client
from app.utils.logger import get_logger

logger = get_logger(__name__)

try:
    import PyPDF2
except ImportError:  # pragma: no cover
    PyPDF2 = None

try:
    import docx  # type: ignore
except ImportError:  # pragma: no cover
    docx = None


def _extract_text_from_pdf(file_bytes: bytes) -> str:
    if PyPDF2 is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PDF support not installed.",
        )
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def _extract_text_from_docx(file_bytes: bytes) -> str:
    if docx is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="DOCX support not installed.",
        )
    document = docx.Document(io.BytesIO(file_bytes))
    return "\n".join(p.text for p in document.paragraphs)


def _detect_and_extract(file: UploadFile) -> str:
    name = (file.filename or "").lower()
    content = file.file.read()
    if name.endswith(".pdf"):
        return _extract_text_from_pdf(content)
    if name.endswith(".docx"):
        return _extract_text_from_docx(content)
    # default plain text
    return content.decode("utf-8", errors="ignore")


def _create_document(org_id: str, title: str, source: str) -> str:
    client = get_supabase_client()
    doc_id = str(uuid4())
    payload = {
        "id": doc_id,
        "organization_id": org_id,
        "title": title,
        "source": source,
    }
    try:
        client.table("ai_documents").insert(payload).execute()
    except Exception as exc:  # pragma: no cover
        logger.exception("Failed to insert document")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to store document.",
        ) from exc
    return doc_id


def ingest_text(org_id: str, text: str, title: str, source: str, embed_provider: str = "openai") -> Dict[str, Any]:
    doc_id = _create_document(org_id, title, source)
    chunks = chunk_text(text)
    embedder = Embedder(embed_provider)
    embeddings = embedder.embed_batch(chunks) if chunks else []
    for content, emb in zip(chunks, embeddings):
        insert_chunk(org_id, doc_id, content, emb, metadata={"title": title, "source": source})
    return {"document_id": doc_id, "chunks": len(chunks)}


def ingest_file(org_id: str, file: UploadFile, embed_provider: str = "openai") -> Dict[str, Any]:
    text = _detect_and_extract(file)
    title = file.filename or "untitled"
    source = os.path.splitext(title)[1].strip(".") or "upload"
    return ingest_text(org_id, text, title, source, embed_provider)


def list_documents(org_id: str) -> List[Dict[str, str]]:
    client = get_supabase_client()
    try:
        resp = client.table("ai_documents").select("*").eq("organization_id", org_id).execute()
        return getattr(resp, "data", None) or []
    except Exception as exc:  # pragma: no cover
        logger.exception("Failed to list documents")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to list documents.",
        ) from exc
