"""
WhatsApp message handler pipeline.
"""
from typing import Dict, List
from uuid import uuid4

from fastapi import HTTPException, status

from app.ai_engine.orchestrator.ai_orchestrator import run_ai_pipeline
from app.ai_engine.spam_filter.spam_pipeline import is_spam
from app.channels.whatsapp.reply_sender import send_message
from app.channels.whatsapp.whatsapp_normalizer import normalize
from app.db.supabase import get_supabase_client
from app.services import customer_service, conversation_service
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def _is_duplicate(org_id: str, message_id: str) -> bool:
    client = get_supabase_client()
    resp = (
        client.table("whatsapp_message_log")
        .select("message_id")
        .eq("organization_id", org_id)
        .eq("message_id", message_id)
        .limit(1)
        .execute()
    )
    data = getattr(resp, "data", None) or []
    return bool(data)


def _log_message(org_id: str, message_id: str) -> None:
    client = get_supabase_client()
    client.table("whatsapp_message_log").insert(
        {"organization_id": org_id, "message_id": message_id}
    ).execute()


async def handle(payload: Dict, organization_id: str) -> Dict:
    normalized = normalize(payload, organization_id)
    if not normalized:
        return {"status": "ignored"}

    if normalized["message_id"] and await _is_duplicate(organization_id, normalized["message_id"]):
        logger.info("Duplicate WA message ignored", extra={"message_id": normalized["message_id"]})
        return {"status": "duplicate"}

    if await is_spam(normalized["content"], {}, None):
        logger.info("Spam detected, skipping", extra={"message_id": normalized["message_id"]})
        return {"status": "spam"}

    client = get_supabase_client()
    customer = customer_service.find_or_create_customer(
        organization_id, normalized["external_id"], source="whatsapp", client=client
    )
    conversation = conversation_service.find_or_create_conversation(
        organization_id, customer.id if hasattr(customer, "id") else customer["id"], "whatsapp", client=client
    )

    # Save incoming message
    msg_record = {
        "id": str(uuid4()),
        "organization_id": organization_id,
        "conversation_id": conversation.id if hasattr(conversation, "id") else conversation["id"],
        "sender_type": "customer",
        "sender_id": None,
        "content": normalized["content"],
        "metadata": normalized,
    }
    client.table("messages").insert(msg_record).execute()

    # Build conversation history context (last 10)
    history_resp = (
        client.table("messages")
        .select("sender_type,content")
        .eq("conversation_id", msg_record["conversation_id"])
        .order("created_at", desc=True)
        .limit(10)
        .execute()
    )
    history_data = list(reversed(getattr(history_resp, "data", None) or []))
    history: List[Dict[str, str]] = []
    for item in history_data:
        role = "assistant" if item["sender_type"] != "customer" else "user"
        history.append({"role": role, "content": item["content"]})

    # Run AI pipeline
    ai_reply = await run_ai_pipeline(
        org_id=organization_id,
        user_message=normalized["content"],
        conversation_context=history,
        provider="openai",
    )

    ai_text = ai_reply.get("reply", "")
    if ai_text:
        ai_msg_record = {
            "id": str(uuid4()),
            "organization_id": organization_id,
            "conversation_id": msg_record["conversation_id"],
            "sender_type": "ai",
            "sender_id": None,
            "content": ai_text,
            "metadata": {"source": "ai_engine"},
        }
        client.table("messages").insert(ai_msg_record).execute()
        await send_message(normalized["external_id"], ai_text)

    if normalized["message_id"]:
        _log_message(organization_id, normalized["message_id"])

    return {"status": "processed", "ai_reply": ai_text}
