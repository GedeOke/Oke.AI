"""
Message service logic with auto-create hooks.
"""
from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import HTTPException, status
from supabase import Client

from app.schemas.message_schema import MessageCreate, MessageResponse
from app.services.conversation_service import find_or_create_conversation
from app.services.customer_service import find_or_create_customer
from app.utils.logger import get_logger

logger = get_logger(__name__)


def _map_message(data: Dict) -> MessageResponse:
    return MessageResponse(
        id=data["id"],
        organization_id=data["organization_id"],
        conversation_id=data["conversation_id"],
        sender_type=data.get("sender_type"),
        sender_id=data.get("sender_id"),
        content=data.get("content"),
        metadata=data.get("metadata"),
        created_at=data.get("created_at"),
    )


def list_messages(org_id: str, conversation_id: str, client: Client) -> List[MessageResponse]:
    result = (
        client.table("messages")
        .select("*")
        .eq("organization_id", org_id)
        .eq("conversation_id", conversation_id)
        .order("created_at", desc=False)
        .execute()
    )
    data = getattr(result, "data", None) or []
    return [_map_message(item) for item in data]


def send_message(
    org_id: str,
    sender_id: Optional[str],
    payload: MessageCreate,
    client: Client,
    sender_type: str = "agent",
) -> MessageResponse:
    # Ensure conversation belongs to org
    conv_result = (
        client.table("conversations")
        .select("*")
        .eq("id", payload.conversation_id)
        .eq("organization_id", org_id)
        .limit(1)
        .execute()
    )
    conv_data = getattr(conv_result, "data", None) or []
    if not conv_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found.",
        )
    conversation = conv_data[0]

    record = {
        "id": str(uuid4()),
        "organization_id": org_id,
        "conversation_id": payload.conversation_id,
        "sender_type": sender_type,
        "sender_id": sender_id,
        "content": payload.content,
        "metadata": payload.metadata,
    }
    try:
        result = client.table("messages").insert(record).execute()
        # bump conversation updated_at
        client.table("conversations").update({"updated_at": "now()"}).eq("id", payload.conversation_id).execute()
    except Exception as exc:  # pragma: no cover - external service
        logger.exception("Failed to send message")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to send message.",
        ) from exc
    data = getattr(result, "data", None) or [record]
    return _map_message(data[0])


def ingest_message_auto(
    org_id: str,
    external_id: str,
    source: str,
    channel: str,
    content: str,
    client: Client,
    metadata: Optional[dict] = None,
) -> MessageResponse:
    customer = find_or_create_customer(org_id, external_id, source, client)
    conversation = find_or_create_conversation(org_id, customer.id, channel, client)
    message_payload = MessageCreate(conversation_id=conversation.id, content=content, metadata=metadata)
    return send_message(org_id, None, message_payload, client, sender_type="customer")
