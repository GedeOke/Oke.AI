"""
Validate WhatsApp webhook signature.
"""
import hmac
import os
from hashlib import sha256
from typing import Optional

from fastapi import HTTPException, status


def validate_signature(signature_header: Optional[str], body: bytes) -> None:
    app_secret = os.getenv("WHATSAPP_APP_SECRET")
    if not app_secret:
        # If not configured, skip validation but recommend setting it.
        return
    if not signature_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing signature header.",
        )
    expected = "sha256=" + hmac.new(app_secret.encode(), body, sha256).hexdigest()
    if not hmac.compare_digest(expected, signature_header):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid signature.",
        )
