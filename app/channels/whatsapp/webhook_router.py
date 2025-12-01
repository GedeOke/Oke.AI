"""
WhatsApp webhook router.
"""
import json
import os
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, Request

from app.channels.whatsapp.message_handler import handle
from app.channels.whatsapp.signature_validator import validate_signature
from app.utils.logger import get_logger

router = APIRouter(prefix="/webhook/whatsapp", tags=["webhook-whatsapp"])
logger = get_logger(__name__)


@router.get("/{organization_id}")
async def verify_webhook(organization_id: str, hub_mode: str = "", hub_challenge: str = "", hub_verify_token: str = ""):
    verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN", "")
    if hub_mode == "subscribe" and hub_verify_token == verify_token:
        return int(hub_challenge or 0)
    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/{organization_id}")
async def receive_webhook(
    organization_id: str,
    request: Request,
):
    raw_body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256")
    try:
        validate_signature(signature, raw_body)
        payload: Dict = json.loads(raw_body.decode("utf-8"))
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid payload")

    logger.info("WA message received", extra={"org": organization_id})
    try:
        result = await handle(payload, organization_id)
    except Exception as exc:
        logger.exception("Failed to handle WA webhook", extra={"org": organization_id})
        # Do not fail webhook to avoid retries storm; return 200
        return {"status": "error", "detail": str(exc)}
    return result


@router.post("/test/send")
async def test_send(payload: Dict):
    from app.channels.whatsapp.reply_sender import send_message

    org_id = payload.get("organization_id")
    phone = payload.get("phone")
    text = payload.get("text", "tes dari backend")
    if not org_id or not phone:
        raise HTTPException(status_code=400, detail="organization_id and phone required")
    resp = await send_message(phone, text)
    return {"status": "sent", "detail": resp}
