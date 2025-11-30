"""
Organization service logic.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import HTTPException, status
from supabase import Client

from app.schemas.organization_schema import (
    AcceptInviteRequest,
    AcceptInviteResponse,
    InviteRequest,
    InviteResponse,
    OrganizationMembersResponse,
    OrganizationMemberResponse,
    OrganizationResponse,
)
from app.utils.logger import get_logger

logger = get_logger(__name__)
ROLE_OPTIONS = {"owner", "admin", "agent"}


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
    org_result = client.table("organizations").select("*").eq("id", org_id).limit(1).execute()
    org_data_list = getattr(org_result, "data", None) or []
    org_data = org_data_list[0] if org_data_list else None
    if not org_data:
        return None
    return _map_org(org_data)


def list_members(organization_id: str, client: Client) -> OrganizationMembersResponse:
    org_result = (
        client.table("organizations")
        .select("*")
        .eq("id", organization_id)
        .limit(1)
        .execute()
    )
    org_data_list = getattr(org_result, "data", None) or []
    org_data = org_data_list[0] if org_data_list else None
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


def _ensure_inviter_role(inviter: Dict) -> None:
    role = (inviter.get("role") or "").lower()
    if role not in {"owner", "admin"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owner or admin can invite members.",
        )


def _validate_role(role: str) -> str:
    normalized = role.lower()
    if normalized not in ROLE_OPTIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role.",
        )
    return normalized


def _check_expiry(expires_at: Optional[str]) -> None:
    if not expires_at:
        return
    try:
        expires_dt = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
    except Exception:
        return
    if expires_dt < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invite expired.",
        )


def _error(code: str, message: str, status_code: int) -> HTTPException:
    return HTTPException(status_code=status_code, detail={"code": code, "message": message})


def invite_member_by_email(payload: InviteRequest, inviter: Dict, client: Client) -> InviteResponse:
    _ensure_inviter_role(inviter)
    role = _validate_role(payload.role)

    organization = get_user_organization(inviter["id"], client)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found.",
        )

    email = payload.email.lower().strip()

    existing_invite_resp = (
        client.table("organization_invites")
        .select("*")
        .eq("organization_id", organization.id)
        .eq("email", email)
        .eq("status", "pending")
        .limit(1)
        .execute()
    )
    existing_invite_data = getattr(existing_invite_resp, "data", None) or []
    if existing_invite_data:
        existing = existing_invite_data[0]
        return InviteResponse(invite_token=existing["id"], status=existing.get("status", "pending"))

    record = {
        "id": str(uuid4()),
        "organization_id": organization.id,
        "email": email,
        "role": role,
        "invited_by": inviter["id"],
        "status": "pending",
    }
    try:
        response = client.table("organization_invites").insert(record).execute()
    except Exception as exc:  # pragma: no cover - external service
        logger.exception("Failed to create invite")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create invite.",
        ) from exc

    data = getattr(response, "data", None) or [record]
    invite = data[0]
    return InviteResponse(invite_token=invite["id"], status=invite.get("status", "pending"))


def accept_invite(payload: AcceptInviteRequest, current_user: Dict, client: Client) -> AcceptInviteResponse:
    invite_resp = (
        client.table("organization_invites")
        .select("*")
        .eq("id", str(payload.invite_token))
        .limit(1)
        .execute()
    )
    invite_data_list = getattr(invite_resp, "data", None) or []
    invite = invite_data_list[0] if invite_data_list else None
    if not invite:
        raise _error("ERR_INVITE_NOT_FOUND", "Invite not found.", status.HTTP_404_NOT_FOUND)

    if invite.get("status") != "pending":
        raise _error("ERR_INVITE_INVALID_STATUS", "Invite is not pending.", status.HTTP_400_BAD_REQUEST)

    try:
        _check_expiry(invite.get("expires_at"))
    except HTTPException:
        raise _error("ERR_INVITE_EXPIRED", "Invite expired.", status.HTTP_400_BAD_REQUEST)

    invite_email = (invite.get("email") or "").lower()
    current_email = (current_user.get("email") or "").lower()
    if invite_email != current_email:
        raise _error(
            "ERR_INVITE_EMAIL_MISMATCH",
            "Invite email does not match current user.",
            status.HTTP_403_FORBIDDEN,
        )

    try:
        role = _validate_role(invite.get("role", "agent"))
    except HTTPException:
        raise _error("ERR_INVITE_INVALID_STATUS", "Invalid invite role.", status.HTTP_400_BAD_REQUEST)

    org_result = (
        client.table("organizations").select("*").eq("id", invite["organization_id"]).limit(1).execute()
    )
    org_data_list = getattr(org_result, "data", None) or []
    org_data = org_data_list[0] if org_data_list else None
    if not org_data:
        raise _error("ERR_INVITE_NOT_FOUND", "Organization not found for invite.", status.HTTP_404_NOT_FOUND)

    membership_result = (
        client.table("organization_members")
        .select("id")
        .eq("organization_id", invite["organization_id"])
        .eq("user_id", current_user["id"])
        .limit(1)
        .execute()
    )
    membership_data = getattr(membership_result, "data", None) or []
    if membership_data:
        raise _error("ERR_ALREADY_MEMBER", "User already a member.", status.HTTP_400_BAD_REQUEST)

    member_record = {
        "id": str(uuid4()),
        "organization_id": invite["organization_id"],
        "user_id": current_user["id"],
        "role": role,
        "invited_by": invite.get("invited_by"),
    }

    try:
        insert_resp = client.table("organization_members").insert(member_record).execute()
        client.table("organization_invites").update({"status": "accepted"}).eq("id", invite["id"]).execute()
    except Exception as exc:  # pragma: no cover - external service
        logger.exception("Failed to accept invite")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to accept invite.",
        ) from exc

    member_data = getattr(insert_resp, "data", None) or [member_record]
    member = _map_member(member_data[0])
    return AcceptInviteResponse(
        organization_id=invite["organization_id"],
        role=member.role,
    )
