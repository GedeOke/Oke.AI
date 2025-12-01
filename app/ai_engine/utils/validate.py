"""
Validation helpers.
"""
from typing import Any

from app.ai_engine.utils.exceptions import ValidationError


def require(value: Any, message: str) -> Any:
    if value is None:
        raise ValidationError(message)
    return value
