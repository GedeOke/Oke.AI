"""
RAG API router.
"""
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.core.security import get_current_user
from app.db.supabase import get_supabase_client
from app.rag.document_service import ingest_file, ingest_text, list_documents
from app.rag.retriever import retrieve
from app.services.organization_service import get_user_organization

router = APIRouter(prefix="/rag", tags=["rag"])


def _org_id(current_user: dict) -> str:
    client = get_supabase_client()
    org = get_user_organization(current_user["id"], client)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found for user.",
        )
    return org.id if hasattr(org, "id") else org["id"]


@router.post("/upload")
async def upload_file(
    embed_provider: str = "openai",
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
):
    org_id = _org_id(current_user)
    return ingest_file(org_id, file, embed_provider)


@router.post("/text")
async def upload_text(
    payload: dict,
    current_user=Depends(get_current_user),
):
    org_id = _org_id(current_user)
    text = payload.get("text", "")
    title = payload.get("title", "text")
    source = payload.get("source", "text")
    embed_provider = payload.get("embed_provider", "openai")
    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="text is required",
        )
    return ingest_text(org_id, text, title, source, embed_provider)


@router.get("/documents")
async def get_documents(current_user=Depends(get_current_user)):
    org_id = _org_id(current_user)
    return list_documents(org_id)


@router.get("/search")
async def search_chunks(
    query: str,
    top_k: int = 6,
    embed_provider: str = "openai",
    current_user=Depends(get_current_user),
):
    org_id = _org_id(current_user)
    chunks = retrieve(org_id, [query], embed_provider=embed_provider, top_k=top_k)
    return {"chunks": chunks}
