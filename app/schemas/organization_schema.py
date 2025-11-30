"""
Schemas for organization operations.
"""
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class OrganizationResponse(BaseModel):
    id: str
    name: str
    owner_id: str
    created_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class OrganizationMemberResponse(BaseModel):
    id: str
    organization_id: str
    user_id: str
    role: str
    invited_by: Optional[str] = None
    created_at: Optional[str] = None
    profile: Optional[dict] = None


class InviteRequest(BaseModel):
    email: EmailStr
    role: str = Field(default="agent")


class InviteResponse(BaseModel):
    invite_token: str
    status: str


class InviteMemberRequest(BaseModel):
    organization_id: str
    user_id: str
    role: str = "agent"


class AcceptInviteRequest(BaseModel):
    invite_token: str


class AcceptInviteResponse(BaseModel):
    organization: OrganizationResponse
    member: OrganizationMemberResponse


class OrganizationMembersResponse(BaseModel):
    organization: OrganizationResponse
    members: List[OrganizationMemberResponse]
