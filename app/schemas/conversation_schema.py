"""
Schemas for conversation operations.
"""
from typing import Optional

from pydantic import BaseModel


class ConversationBase(BaseModel):
    channel: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[str] = None


class ConversationCreate(BaseModel):
    customer_id: str
    channel: str


class ConversationUpdateStatus(BaseModel):
    status: str


class ConversationAssign(BaseModel):
    assigned_to: Optional[str] = None


class ConversationResponse(ConversationBase):
    id: str
    organization_id: str
    customer_id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
