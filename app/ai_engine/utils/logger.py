"""
Structured JSON logger for AI engine.
"""
import json
import logging
from typing import Any, Dict, Optional


def get_logger(name: Optional[str] = None) -> logging.Logger:
    logger = logging.getLogger(name or "ai_engine")
    if not logger.handlers:
        handler = logging.StreamHandler()

        class JsonFormatter(logging.Formatter):
            def format(self, record: logging.LogRecord) -> str:
                payload: Dict[str, Any] = {
                    "level": record.levelname,
                    "logger": record.name,
                    "message": record.getMessage(),
                }
                if record.exc_info:
                    payload["exc_info"] = self.formatException(record.exc_info)
                if hasattr(record, "extra") and isinstance(record.extra, dict):
                    payload.update(record.extra)
                return json.dumps(payload)

        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
