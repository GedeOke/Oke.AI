"""
Message endpoints.
"""
from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.db.supabase import get_supabase_client
from app.schemas.message_schema import MessageCreate, MessageResponse
from app.services import message_service

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("/conversations/{conversation_id}", response_model=list[MessageResponse])
def list_messages(
    conversation_id: str,
    client=Depends(get_supabase_client),
    current_user=Depends(get_current_user),
):
    return message_service.list_messages(current_user["organization_id"], conversation_id, client)


@router.post("/send", response_model=MessageResponse)
def send_message(
    payload: MessageCreate,
    client=Depends(get_supabase_client),
    current_user=Depends(get_current_user),
):
    return message_service.send_message(
        org_id=current_user["organization_id"],
        sender_id=current_user["id"],
        payload=payload,
        client=client,
        sender_type="agent",
    )
