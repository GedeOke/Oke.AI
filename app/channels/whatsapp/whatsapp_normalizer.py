"""
Normalize WhatsApp Cloud API payloads.
"""
from typing import Any, Dict, Optional

from app.channels.whatsapp.utils import get_value


def normalize(payload: Dict[str, Any], organization_id: str) -> Optional[Dict[str, Any]]:
    """
    Extract a single message from WhatsApp webhook payload.
    """
    message = get_value(payload, "entry.0.changes.0.value.messages.0")
    if not message:
        return None

    msg_type = message.get("type", "text")
    text = ""
    if msg_type == "text":
        text = get_value(message, "text.body", "")
    elif msg_type == "image":
        text = message.get("image", {}).get("caption", "")
    elif msg_type == "audio":
        text = "[audio message]"
    else:
        text = "[unsupported message]"

    phone = get_value(message, "from", "")
    message_id = message.get("id")
    timestamp = message.get("timestamp")

    return {
        "external_id": phone,
        "message_id": message_id,
        "type": msg_type,
        "content": text,
        "raw": message,
        "timestamp": timestamp,
        "organization_id": organization_id,
    }
