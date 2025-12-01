"""
Custom exceptions for AI engine.
"""


class AIEngineError(Exception):
    """Base AI engine error."""


class ProviderError(AIEngineError):
    """LLM provider failure."""


class ValidationError(AIEngineError):
    """Validation error inside AI engine."""


class SafetyError(AIEngineError):
    """Raised when safety checks fail."""


class SpamDetected(AIEngineError):
    """Raised when spam detection triggers."""
