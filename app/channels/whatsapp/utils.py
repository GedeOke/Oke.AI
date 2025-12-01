"""
Utilities for WhatsApp channel.
"""
from typing import Any, Dict


def get_value(data: Dict[str, Any], path: str, default=None):
    ref = data
    for part in path.split("."):
        if isinstance(ref, list):
            try:
                part_int = int(part)
                ref = ref[part_int]
            except (ValueError, IndexError):
                return default
        elif isinstance(ref, dict):
            ref = ref.get(part, default)
        else:
            return default
    return ref
