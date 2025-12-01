"""
Query optimizer to expand user queries.
"""
from typing import List


def optimize_query(message: str) -> List[str]:
    words = [w.strip(".,!?") for w in message.split() if len(w) > 3]
    base = " ".join(words[:8])
    return [message, base, " ".join(reversed(words[:8]))]
