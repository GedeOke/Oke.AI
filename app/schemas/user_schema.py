"""
Schemas for user profile operations.
"""
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class UserProfileBase(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    role: Optional[str] = None


class UserProfileResponse(UserProfileBase):
    id: str
    email: Optional[EmailStr] = None

    model_config = ConfigDict(from_attributes=True)


class UpdateUserProfileRequest(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None


class UpdateAvatarRequest(BaseModel):
    avatar_url: str
