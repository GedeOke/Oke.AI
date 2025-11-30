"""
Organization endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user
from app.db.supabase import get_supabase_client
from app.schemas.organization_schema import (
    AcceptInviteRequest,
    AcceptInviteResponse,
    InviteRequest,
    InviteResponse,
    OrganizationMembersResponse,
    OrganizationResponse,
    OrganizationMemberResponse,
)
from app.services import organization_service

router = APIRouter(prefix="/organization", tags=["organization"])


@router.get("", response_model=OrganizationResponse)
def get_my_organization(
    client=Depends(get_supabase_client), current_user=Depends(get_current_user)
):
    org = organization_service.get_user_organization(current_user["id"], client)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found."
        )
    return org


@router.get("/members", response_model=OrganizationMembersResponse)
def get_members(
    client=Depends(get_supabase_client), current_user=Depends(get_current_user)
):
    org = organization_service.get_user_organization(current_user["id"], client)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found."
        )
    return organization_service.list_members(org.id, client)


@router.post("/invite", response_model=InviteResponse)
def invite_member(
    payload: InviteRequest,
    client=Depends(get_supabase_client),
    current_user=Depends(get_current_user),
):
    return organization_service.invite_member_by_email(payload, current_user, client)


@router.post("/accept", response_model=AcceptInviteResponse)
def accept_invite(
    payload: AcceptInviteRequest,
    client=Depends(get_supabase_client),
    current_user=Depends(get_current_user),
):
    return organization_service.accept_invite(payload, current_user, client)
