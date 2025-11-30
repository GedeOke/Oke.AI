"""
Schemas for message operations.
"""
from typing import Any, Optional

from pydantic import BaseModel


class MessageCreate(BaseModel):
    conversation_id: str
    content: str
    metadata: Optional[dict[str, Any]] = None


class MessageResponse(BaseModel):
    id: str
    organization_id: str
    conversation_id: str
    sender_type: str
    sender_id: Optional[str] = None
    content: str
    metadata: Optional[dict[str, Any]] = None
    created_at: Optional[str] = None
