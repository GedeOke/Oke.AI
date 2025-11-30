"""
Conversation endpoints.
"""
from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.db.supabase import get_supabase_client
from app.schemas.conversation_schema import (
    ConversationAssign,
    ConversationCreate,
    ConversationResponse,
    ConversationUpdateStatus,
)
from app.services import conversation_service

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.get("", response_model=list[ConversationResponse])
def list_conversations(client=Depends(get_supabase_client), current_user=Depends(get_current_user)):
    return conversation_service.list_conversations(current_user["organization_id"], client)


@router.get("/{conversation_id}", response_model=ConversationResponse)
def get_conversation(
    conversation_id: str,
    client=Depends(get_supabase_client),
    current_user=Depends(get_current_user),
):
    return conversation_service.get_conversation(current_user["organization_id"], conversation_id, client)


@router.post("", response_model=ConversationResponse)
def create_conversation(
    payload: ConversationCreate,
    client=Depends(get_supabase_client),
    current_user=Depends(get_current_user),
):
    return conversation_service.create_conversation(current_user["organization_id"], payload, client)


@router.put("/{conversation_id}/close", response_model=ConversationResponse)
def close_conversation(
    conversation_id: str,
    client=Depends(get_supabase_client),
    current_user=Depends(get_current_user),
):
    return conversation_service.update_status(
        current_user["organization_id"], conversation_id, ConversationUpdateStatus(status="closed"), client
    )


@router.put("/{conversation_id}/assign", response_model=ConversationResponse)
def assign_conversation(
    conversation_id: str,
    payload: ConversationAssign,
    client=Depends(get_supabase_client),
    current_user=Depends(get_current_user),
):
    return conversation_service.assign_conversation(current_user["organization_id"], conversation_id, payload, client)
