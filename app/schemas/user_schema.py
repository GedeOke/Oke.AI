"""
Schemas for user profile operations.
"""
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserProfileBase(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    role: Optional[str] = None


class UserProfileResponse(UserProfileBase):
    id: str
    email: Optional[EmailStr] = None

    class Config:
        orm_mode = True


class UpdateUserProfileRequest(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None


class UpdateAvatarRequest(BaseModel):
    avatar_url: str
