"""
Autopilot decision helper.
"""
from datetime import datetime
from typing import Any, Dict


def should_auto_reply(intent: str, org_rules: Dict[str, Any], agent_online: bool = False) -> Dict[str, bool]:
    working_hours = org_rules.get("working_hours", {"start": 9, "end": 17})
    now_hour = datetime.utcnow().hour
    within_hours = working_hours["start"] <= now_hour < working_hours["end"]
    auto_reply = not agent_online or not within_hours or intent in {"faq", "greeting"}
    return {"should_auto_reply": auto_reply}
