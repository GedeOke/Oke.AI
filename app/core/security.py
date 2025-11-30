"""
Security helpers for JWT verification via Supabase.
"""
from typing import Any, Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase import Client

from app.db.supabase import SupabaseClientError, get_supabase_client
from app.utils.logger import get_logger

logger = get_logger(__name__)
auth_scheme = HTTPBearer(auto_error=False)


def sanitize_input(value: str) -> str:
    """
    Perform simple input sanitization to reduce injection vectors.
    """
    return value.replace("\n", "").replace("\r", "").strip()


def verify_jwt(token: str, supabase_client: Client) -> Dict[str, Any]:
    """
    Validate JWT using Supabase Auth service.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token.",
        )

    try:
        user_response = supabase_client.auth.get_user(token)
    except Exception as exc:  # pragma: no cover - external call
        logger.warning("Supabase auth validation failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
        ) from exc

    user = getattr(user_response, "user", None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found for token.",
        )

    return {
        "id": getattr(user, "id", None),
        "email": getattr(user, "email", None),
        "metadata": getattr(user, "user_metadata", {}),
    }


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
    client: Client = Depends(get_supabase_client),
) -> Dict[str, Any]:
    """
    Dependency to retrieve the current user from the Authorization header.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing.",
        )

    token = sanitize_input(credentials.credentials)
    try:
        auth_user = verify_jwt(token, client)
        profile_response = (
            client.table("users_profile")
            .select("*")
            .eq("id", auth_user["id"])
            .maybe_single()
            .execute()
        )
        profile_data = getattr(profile_response, "data", None)
        if not profile_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User profile not found.",
            )
        profile_data["email"] = auth_user.get("email")
        return profile_data
    except SupabaseClientError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service unavailable.",
        ) from exc
