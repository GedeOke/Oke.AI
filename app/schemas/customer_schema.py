"""
Schemas for customer operations.
"""
from typing import Optional

from pydantic import BaseModel


class CustomerBase(BaseModel):
    external_id: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    source: Optional[str] = None  # whatsapp, instagram, telegram, webchat


class CustomerCreate(CustomerBase):
    organization_id: Optional[str] = None


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    source: Optional[str] = None


class CustomerResponse(CustomerBase):
    id: str
    organization_id: str
    created_at: Optional[str] = None
