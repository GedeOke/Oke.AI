"""
User profile business logic.
"""
from typing import Dict, Optional

from fastapi import HTTPException, status
from supabase import Client

from app.schemas.user_schema import UpdateAvatarRequest, UpdateUserProfileRequest, UserProfileResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)


def get_profile(user_id: str, client: Client) -> Optional[Dict]:
    result = (
        client.table("users_profile")
        .select("*")
        .eq("id", user_id)
        .maybe_single()
        .execute()
    )
    return getattr(result, "data", None)


def update_profile(user_id: str, payload: UpdateUserProfileRequest, client: Client) -> UserProfileResponse:
    updates = {k: v for k, v in payload.dict().items() if v is not None}
    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update.",
        )
    try:
        response = (
            client.table("users_profile")
            .update(updates)
            .eq("id", user_id)
            .maybe_single()
            .execute()
        )
    except Exception as exc:  # pragma: no cover - external service
        logger.exception("Failed to update user profile")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update profile.",
        ) from exc

    data = getattr(response, "data", None)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found.",
        )
    return UserProfileResponse(**data)


def update_avatar(user_id: str, payload: UpdateAvatarRequest, client: Client) -> UserProfileResponse:
    try:
        response = (
            client.table("users_profile")
            .update({"avatar_url": payload.avatar_url})
            .eq("id", user_id)
            .maybe_single()
            .execute()
        )
    except Exception as exc:  # pragma: no cover - external service
        logger.exception("Failed to update avatar")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update avatar.",
        ) from exc

    data = getattr(response, "data", None)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found.",
        )
    return UserProfileResponse(**data)
