"""
Pydantic schemas for authentication workflows.
"""
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, UUID4

from app.schemas.user_schema import UserProfileResponse
from app.schemas.organization_schema import OrganizationResponse


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    full_name: str
    phone: Optional[str] = None
    invite_token: Optional[UUID4] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    profile: UserProfileResponse
    organization: Optional[OrganizationResponse] = None


class LogoutResponse(BaseModel):
    message: str = "Logged out"
