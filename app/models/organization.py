"""
Data models for organization entities.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Organization:
    id: str
    name: str
    owner_id: str
    created_at: Optional[str] = None


@dataclass
class OrganizationMember:
    id: str
    organization_id: str
    user_id: str
    role: str
    invited_by: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class OrganizationInvite:
    id: str
    organization_id: str
    email: str
    role: str
    invited_by: Optional[str] = None
    status: str = "pending"
    created_at: Optional[str] = None
    expires_at: Optional[str] = None
