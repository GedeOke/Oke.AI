"""
Logging utilities for structured application logs.
"""
import logging
from typing import Optional


def setup_logging(level: str = "INFO") -> logging.Logger:
    """
    Configure root logger with structured formatting.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    return logging.getLogger("okeai")


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Retrieve a configured logger instance.
    """
    return logging.getLogger(name or "okeai")
