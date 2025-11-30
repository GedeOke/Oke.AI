"""
Authentication endpoints.
"""
from fastapi import APIRouter, Depends

from app.db.supabase import get_supabase_client
from app.schemas.auth_schema import (
    AuthResponse,
    LoginRequest,
    LogoutResponse,
    RegisterRequest,
    TokenResponse,
)
from app.schemas.user_schema import UserProfileResponse
from app.services import auth_service
from app.core.security import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse)
def register(payload: RegisterRequest, client=Depends(get_supabase_client)):
    return auth_service.register_user(payload, client)


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, client=Depends(get_supabase_client)):
    data = auth_service.login_user(payload, client)
    return {
        "access_token": data["access_token"],
        "token_type": "bearer",
        "profile": data["profile"],
        "organization": None,
    }


@router.post("/logout", response_model=LogoutResponse)
def logout(client=Depends(get_supabase_client), current_user=Depends(get_current_user)):
    return auth_service.logout_user(client)


@router.get("/me", response_model=UserProfileResponse)
def me(current_user=Depends(get_current_user)):
    return current_user
