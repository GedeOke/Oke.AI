"""
Schemas for organization operations.
"""
from typing import List, Optional

from pydantic import BaseModel


class OrganizationResponse(BaseModel):
    id: str
    name: str
    owner_id: str
    created_at: Optional[str] = None

    class Config:
        orm_mode = True


class OrganizationMemberResponse(BaseModel):
    id: str
    organization_id: str
    user_id: str
    role: str
    invited_by: Optional[str] = None
    created_at: Optional[str] = None
    profile: Optional[dict] = None


class InviteMemberRequest(BaseModel):
    organization_id: str
    user_id: str
    role: str = "agent"


class AcceptInviteRequest(BaseModel):
    organization_id: str


class OrganizationMembersResponse(BaseModel):
    organization: OrganizationResponse
    members: List[OrganizationMemberResponse]
