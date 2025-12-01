"""
Rule-based spam filter using simple heuristics.
"""
import re
from typing import Any, Dict

SPAM_PATTERNS = [
    r"free money",
    r"visit this link",
    r"click here",
    r"win a prize",
]


def is_spam_rule(message: str, metadata: Dict[str, Any] | None = None) -> bool:
    text = (message or "").lower()
    for pattern in SPAM_PATTERNS:
        if re.search(pattern, text):
            return True
    if metadata and metadata.get("spam_score", 0) > 0.9:
        return True
    return False
