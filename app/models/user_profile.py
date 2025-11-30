"""
Data model for user profiles.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class UserProfile:
    id: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    email: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
