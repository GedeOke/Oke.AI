"""
Organization service logic.
"""
from __future__ import annotations

from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import HTTPException, status
from supabase import Client

from app.schemas.organization_schema import (
    AcceptInviteRequest,
    InviteMemberRequest,
    OrganizationMembersResponse,
    OrganizationMemberResponse,
    OrganizationResponse,
)
from app.utils.logger import get_logger

logger = get_logger(__name__)


def _map_org(data: Dict) -> OrganizationResponse:
    return OrganizationResponse(
        id=data["id"],
        name=data["name"],
        owner_id=data["owner_id"],
        created_at=data.get("created_at"),
    )


def _map_member(data: Dict, profile_lookup: Optional[Dict[str, Dict]] = None) -> OrganizationMemberResponse:
    profile = None
    if profile_lookup and data["user_id"] in profile_lookup:
        profile = profile_lookup[data["user_id"]]
    return OrganizationMemberResponse(
        id=data["id"],
        organization_id=data["organization_id"],
        user_id=data["user_id"],
        role=data.get("role", "agent"),
        invited_by=data.get("invited_by"),
        created_at=data.get("created_at"),
        profile=profile,
    )


def get_user_organization(user_id: str, client: Client) -> Optional[OrganizationResponse]:
    membership_result = (
        client.table("organization_members")
        .select("organization_id")
        .eq("user_id", user_id)
        .limit(1)
        .execute()
    )
    membership_data = getattr(membership_result, "data", None)
    if not membership_data:
        return None

    org_id = membership_data[0]["organization_id"]
    org_result = (
        client.table("organizations").select("*").eq("id", org_id).maybe_single().execute()
    )
    org_data = getattr(org_result, "data", None)
    if not org_data:
        return None
    return _map_org(org_data)


def list_members(organization_id: str, client: Client) -> OrganizationMembersResponse:
    org_result = (
        client.table("organizations")
        .select("*")
        .eq("id", organization_id)
        .maybe_single()
        .execute()
    )
    org_data = getattr(org_result, "data", None)
    if not org_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found.",
        )

    member_result = (
        client.table("organization_members")
        .select("*")
        .eq("organization_id", organization_id)
        .execute()
    )
    member_data: List[Dict] = getattr(member_result, "data", []) or []
    user_ids = [m["user_id"] for m in member_data]

    profile_lookup: Dict[str, Dict] = {}
    if user_ids:
        profiles_resp = (
            client.table("users_profile")
            .select("*")
            .in_("id", user_ids)
            .execute()
        )
        for item in getattr(profiles_resp, "data", []) or []:
            profile_lookup[item["id"]] = item

    members = [_map_member(m, profile_lookup) for m in member_data]
    return OrganizationMembersResponse(organization=_map_org(org_data), members=members)


def invite_member(payload: InviteMemberRequest, inviter_id: str, client: Client) -> OrganizationMemberResponse:
    record = {
        "id": str(uuid4()),
        "organization_id": payload.organization_id,
        "user_id": payload.user_id,
        "role": payload.role,
        "invited_by": inviter_id,
    }
    try:
        response = client.table("organization_members").insert(record).execute()
    except Exception as exc:  # pragma: no cover - external service
        logger.exception("Failed to invite member")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to invite member.",
        ) from exc

    data = getattr(response, "data", None) or [record]
    return _map_member(data[0])


def accept_invite(payload: AcceptInviteRequest, user_id: str, client: Client) -> OrganizationMemberResponse:
    member_result = (
        client.table("organization_members")
        .select("*")
        .eq("organization_id", payload.organization_id)
        .eq("user_id", user_id)
        .maybe_single()
        .execute()
    )
    existing = getattr(member_result, "data", None)

    if not existing:
        record = {
            "id": str(uuid4()),
            "organization_id": payload.organization_id,
            "user_id": user_id,
            "role": "agent",
            "invited_by": None,
        }
        response = client.table("organization_members").insert(record).execute()
        data = getattr(response, "data", None) or [record]
        return _map_member(data[0])

    # If invitation exists, simply return it (treated as accepted).
    return _map_member(existing)
