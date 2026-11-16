"""Structured exception hierarchy for FORGE."""

from typing import Any


class ForgeError(Exception):
    """Base exception for all FORGE domain errors."""

    def __init__(self, message: str, details: dict[str, Any] | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def to_dict(self) -> dict[str, Any]:
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "details": self.details,
        }


class ConfigurationError(ForgeError):
    """Raised when required configuration or environment settings are missing/invalid."""

    pass


class ModelProviderError(ForgeError):
    """Base exception for LLM provider errors."""

    pass


class ProviderAuthenticationError(ModelProviderError):
    """Raised when provider credentials are invalid or missing."""

    pass


class ProviderRateLimitError(ModelProviderError):
    """Raised when provider rate limits / quotas (e.g. 429) are exhausted."""

    pass


class ProviderTimeoutError(ModelProviderError):
    """Raised when provider call times out."""

    pass


class SchemaValidationError(ForgeError):
    """Raised when agent output cannot be parsed or validated against the Pydantic schema."""

    pass


class RevisionLimitExceededError(ForgeError):
    """Raised when maximum supervisory revision attempts have been exceeded."""

    pass


class ArchitectureValidationError(ForgeError):
    """Raised when architecture contains fatal integrity violations."""

    pass


class BenchmarkError(ForgeError):
    """Raised when benchmark dataset loading or execution fails."""

    pass


class StorageError(ForgeError):
    """Raised when database or cache operations fail."""

    pass
