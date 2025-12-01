"""
Channel-related helpers.
"""
from typing import Dict

from app.db.supabase import get_supabase_client


def is_message_logged(org_id: str, message_id: str) -> bool:
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


def log_message(org_id: str, message_id: str) -> None:
    client = get_supabase_client()
    client.table("whatsapp_message_log").insert(
        {"organization_id": org_id, "message_id": message_id}
    ).execute()
