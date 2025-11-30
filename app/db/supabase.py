"""
Supabase client initialization and helper utilities.
"""
from functools import lru_cache
from typing import Any, Callable

from supabase import Client, create_client

from app.core.config import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SupabaseClientError(Exception):
    """Custom error for Supabase client failures."""


@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    """
    Initialize and cache a Supabase client using environment variables.
    """
    settings = get_settings()
    if not settings.supabase_url or not settings.supabase_key:
        raise SupabaseClientError("Supabase credentials are not configured.")

    try:
        client: Client = create_client(str(settings.supabase_url), settings.supabase_key)
        return client
    except Exception as exc:  # pragma: no cover - external client creation
        logger.exception("Failed to initialize Supabase client")
        raise SupabaseClientError("Failed to initialize Supabase client") from exc


def safe_query(query_fn: Callable[[Client], Any]) -> Any:
    """
    Execute a Supabase query with consistent error handling.
    """
    client = get_supabase_client()
    try:
        return query_fn(client)
    except Exception as exc:
        logger.exception("Supabase query failed")
        raise SupabaseClientError("Supabase query failed") from exc
