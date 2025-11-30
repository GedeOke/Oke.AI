"""
Authentication service logic backed by Supabase.
"""
from __future__ import annotations

from typing import Dict, Optional
from uuid import uuid4

from fastapi import HTTPException, status
from supabase import Client

from app.schemas.auth_schema import LoginRequest, RegisterRequest
from app.schemas.user_schema import UserProfileResponse
from app.schemas.organization_schema import OrganizationResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)


def _map_profile(data: Dict, email: Optional[str] = None) -> UserProfileResponse:
    return UserProfileResponse(
        id=data["id"],
        full_name=data.get("full_name"),
        phone=data.get("phone"),
        avatar_url=data.get("avatar_url"),
        role=data.get("role"),
        email=email,
    )


def _map_org(data: Dict) -> OrganizationResponse:
    return OrganizationResponse(
        id=data["id"],
        name=data["name"],
        owner_id=data["owner_id"],
        created_at=data.get("created_at"),
    )


def register_user(payload: RegisterRequest, client: Client) -> Dict:
    """
    Register user via Supabase Auth and bootstrap organization.
    """
    try:
        auth_response = client.auth.sign_up(
            {"email": payload.email, "password": payload.password}
        )
    except Exception as exc:  # pragma: no cover - external service
        logger.exception("Supabase sign_up failed")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    user = getattr(auth_response, "user", None)
    session = getattr(auth_response, "session", None)

    if not session or not getattr(session, "access_token", None):
        # If email confirmation is required, Supabase returns no session.
        try:
            signin_response = client.auth.sign_in_with_password(
                {"email": payload.email, "password": payload.password}
            )
            session = getattr(signin_response, "session", None)
            user = user or getattr(signin_response, "user", None)
        except Exception as exc:  # pragma: no cover - external service
            logger.warning("Sign in after sign up failed", exc_info=exc)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email confirmation required. Please verify your email then login.",
            ) from exc

    if not user or not session or not getattr(session, "access_token", None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email confirmation required. Please verify your email then login.",
        )

    user_id = user.id
    profile_payload = {
        "id": user_id,
        "full_name": payload.full_name,
        "phone": payload.phone,
        "avatar_url": None,
        "role": "owner",
    }
    profile_result = client.table("users_profile").insert(profile_payload).execute()
    profile_data = (getattr(profile_result, "data", None) or [profile_payload])[0]

    org_id = str(uuid4())
    organization_payload = {
        "id": org_id,
        "name": f"{payload.full_name}'s Organization",
        "owner_id": user_id,
    }
    org_result = client.table("organizations").insert(organization_payload).execute()
    org_data = (getattr(org_result, "data", None) or [organization_payload])[0]

    member_payload = {
        "id": str(uuid4()),
        "organization_id": org_id,
        "user_id": user_id,
        "role": "owner",
        "invited_by": user_id,
    }
    client.table("organization_members").insert(member_payload).execute()

    return {
        "access_token": session.access_token,
        "token_type": "bearer",
        "profile": _map_profile(profile_data, email=user.email),
        "organization": _map_org(org_data),
    }


def login_user(payload: LoginRequest, client: Client) -> Dict:
    """
    Login user and return token plus profile.
    """
    try:
        auth_response = client.auth.sign_in_with_password(
            {"email": payload.email, "password": payload.password}
        )
    except Exception as exc:  # pragma: no cover - external service
        logger.exception("Supabase sign_in failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc

    user = getattr(auth_response, "user", None)
    session = getattr(auth_response, "session", None)
    if not user or not session or not session.access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )

    profile_result = (
        client.table("users_profile")
        .select("*")
        .eq("id", user.id)
        .maybe_single()
        .execute()
    )
    profile_data = getattr(profile_result, "data", None) or {}
    if not profile_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found.",
        )
    profile = _map_profile(profile_data, email=user.email)

    return {
        "access_token": session.access_token,
        "token_type": "bearer",
        "profile": profile,
    }


def logout_user(client: Client) -> Dict:
    """
    Logout by revoking current session.
    """
    try:
        client.auth.sign_out()
    except Exception as exc:  # pragma: no cover - external service
        logger.exception("Supabase sign_out failed")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Logout failed.",
        ) from exc
    return {"message": "Logged out"}
