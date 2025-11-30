"""
User profile endpoints.
"""
from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.db.supabase import get_supabase_client
from app.schemas.user_schema import (
    UpdateAvatarRequest,
    UpdateUserProfileRequest,
    UserProfileResponse,
)
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.put("/me", response_model=UserProfileResponse)
def update_me(
    payload: UpdateUserProfileRequest,
    client=Depends(get_supabase_client),
    current_user=Depends(get_current_user),
):
    return user_service.update_profile(current_user["id"], payload, client)


@router.post("/me/avatar", response_model=UserProfileResponse)
def upload_avatar(
    payload: UpdateAvatarRequest,
    client=Depends(get_supabase_client),
    current_user=Depends(get_current_user),
):
    return user_service.update_avatar(current_user["id"], payload, client)
