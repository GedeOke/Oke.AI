"""
Conversation service logic with org scoping and auto-create support.
"""
from typing import Dict, List
from uuid import uuid4

from fastapi import HTTPException, status
from supabase import Client

from app.schemas.conversation_schema import (
    ConversationAssign,
    ConversationCreate,
    ConversationResponse,
    ConversationUpdateStatus,
)
from app.services.customer_service import find_or_create_customer
from app.utils.logger import get_logger

logger = get_logger(__name__)


def _map_conversation(data: Dict) -> ConversationResponse:
    return ConversationResponse(
        id=data["id"],
        organization_id=data["organization_id"],
        customer_id=data["customer_id"],
        channel=data.get("channel"),
        status=data.get("status"),
        assigned_to=data.get("assigned_to"),
        created_at=data.get("created_at"),
        updated_at=data.get("updated_at"),
    )


def list_conversations(org_id: str, client: Client) -> List[ConversationResponse]:
    result = client.table("conversations").select("*").eq("organization_id", org_id).execute()
    data = getattr(result, "data", None) or []
    return [_map_conversation(item) for item in data]


def get_conversation(org_id: str, conversation_id: str, client: Client) -> ConversationResponse:
    result = (
        client.table("conversations")
        .select("*")
        .eq("organization_id", org_id)
        .eq("id", conversation_id)
        .limit(1)
        .execute()
    )
    data = getattr(result, "data", None) or []
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found.",
        )
    return _map_conversation(data[0])


def create_conversation(org_id: str, payload: ConversationCreate, client: Client) -> ConversationResponse:
    record = {
        "id": str(uuid4()),
        "organization_id": org_id,
        "customer_id": payload.customer_id,
        "channel": payload.channel,
        "status": "open",
    }
    try:
        result = client.table("conversations").insert(record).execute()
    except Exception as exc:  # pragma: no cover - external service
        logger.exception("Failed to create conversation")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create conversation.",
        ) from exc
    data = getattr(result, "data", None) or [record]
    return _map_conversation(data[0])


def update_status(org_id: str, conversation_id: str, payload: ConversationUpdateStatus, client: Client) -> ConversationResponse:
    try:
        result = (
            client.table("conversations")
            .update({"status": payload.status})
            .eq("organization_id", org_id)
            .eq("id", conversation_id)
            .execute()
        )
    except Exception as exc:  # pragma: no cover - external service
        logger.exception("Failed to update conversation status")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update conversation.",
        ) from exc
    data = getattr(result, "data", None) or []
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found.",
        )
    return _map_conversation(data[0])


def assign_conversation(org_id: str, conversation_id: str, payload: ConversationAssign, client: Client) -> ConversationResponse:
    try:
        result = (
            client.table("conversations")
            .update({"assigned_to": payload.assigned_to})
            .eq("organization_id", org_id)
            .eq("id", conversation_id)
            .execute()
        )
    except Exception as exc:  # pragma: no cover - external service
        logger.exception("Failed to assign conversation")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to assign conversation.",
        ) from exc
    data = getattr(result, "data", None) or []
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found.",
        )
    return _map_conversation(data[0])


def find_or_create_conversation(org_id: str, customer_id: str, channel: str, client: Client) -> ConversationResponse:
    result = (
        client.table("conversations")
        .select("*")
        .eq("organization_id", org_id)
        .eq("customer_id", customer_id)
        .eq("channel", channel)
        .eq("status", "open")
        .limit(1)
        .execute()
    )
    data = getattr(result, "data", None) or []
    if data:
        return _map_conversation(data[0])
    return create_conversation(
        org_id,
        ConversationCreate(customer_id=customer_id, channel=channel),
        client,
    )
