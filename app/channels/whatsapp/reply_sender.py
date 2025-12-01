"""
Send replies to WhatsApp via Cloud API.
"""
import os
from typing import Dict

import httpx

from app.utils.logger import get_logger

logger = get_logger(__name__)


async def send_message(phone: str, text: str) -> Dict:
    token = os.getenv("WHATSAPP_TOKEN")
    phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    if not token or not phone_number_id:
        logger.warning("WhatsApp token/phone_number_id missing; skipping send")
        return {"status": "skipped"}

    url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": text},
    }
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            return resp.json()
    except Exception as exc:  # pragma: no cover
        logger.exception("Failed to send WhatsApp message", extra={"phone": phone})
        return {"status": "error", "detail": str(exc)}
