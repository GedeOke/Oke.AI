"""
Lightweight in-memory rate limit placeholder.
Replace with a robust store-backed limiter (Redis) in production.
"""
import time
from typing import Dict, Tuple


class RateLimiter:
    """
    Very naive rate limiter placeholder using in-memory counters.
    """

    def __init__(self, limit: int = 100, window_seconds: int = 60):
        self.limit = limit
        self.window_seconds = window_seconds
        self._requests: Dict[str, Tuple[int, int]] = {}

    def allow(self, key: str) -> bool:
        """
        Determine if the provided key can perform the request.
        """
        now = int(time.time())
        window_start = now - self.window_seconds
        count, timestamp = self._requests.get(key, (0, now))

        if timestamp < window_start:
            # Reset window
            self._requests[key] = (1, now)
            return True

        if count >= self.limit:
            return False

        self._requests[key] = (count + 1, timestamp)
        return True
