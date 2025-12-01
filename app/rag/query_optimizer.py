"""
Query optimizer to expand user queries.
"""
from typing import List


def generate(message: str) -> List[str]:
    """
    Produce multiple query variants for retrieval.
    """
    words = [w.strip(".,!?") for w in message.split() if len(w) > 2]
    base = " ".join(words[:12])
    tail = " ".join(words[-12:])
    reversed_terms = " ".join(reversed(words[:12]))
    queries = [message]
    if base:
        queries.append(base)
    if tail and tail not in queries:
        queries.append(tail)
    if reversed_terms and reversed_terms not in queries:
        queries.append(reversed_terms)
    return queries[:4]
