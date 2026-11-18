"""Unit and integration tests for model provider factory and FallbackModelProvider."""

from unittest.mock import MagicMock

from pydantic import BaseModel

from forge.core.exceptions import ModelProviderError
from forge.core.model_provider import (
    FallbackModelProvider,
    MockModelProvider,
    get_model_provider,
)
from forge.core.providers.anthropic import AnthropicProvider
from forge.core.providers.ollama import OllamaProvider
from forge.core.providers.openai import OpenAIProvider


class DummyModel(BaseModel):
    status: str


def test_get_model_provider_factory() -> None:
    """Verify get_model_provider instantiates appropriate adapter."""
    assert isinstance(get_model_provider("mock"), MockModelProvider)
    assert isinstance(get_model_provider("ollama"), OllamaProvider)
    assert isinstance(get_model_provider("openai"), OpenAIProvider)
    assert isinstance(get_model_provider("anthropic"), AnthropicProvider)


def test_fallback_provider_primary_healthy() -> None:
    """Verify primary provider is used when healthy."""
    primary = MockModelProvider(model_name="mock-primary")
    secondary = MockModelProvider(model_name="mock-secondary")
    fallback = FallbackModelProvider(primary, secondary)

    resp = fallback.generate_text("Test prompt")
    assert "mock-primary" in resp.model_name
    assert len(primary.call_history) == 1
    assert len(secondary.call_history) == 0


def test_fallback_provider_failover_text() -> None:
    """Verify failover to secondary when primary fails on generate_text."""
    primary = MagicMock()
    primary.model_name = "failing-primary"
    primary.generate_text.side_effect = ModelProviderError("Primary unavailable")

    secondary = MockModelProvider(model_name="backup-secondary")
    fallback = FallbackModelProvider(primary, secondary)

    resp = fallback.generate_text("Test prompt")
    assert "backup-secondary" in resp.model_name
    assert len(secondary.call_history) == 1


def test_fallback_provider_failover_structured() -> None:
    """Verify failover to secondary when primary fails on generate_structured."""
    primary = MagicMock()
    primary.model_name = "failing-primary"
    primary.generate_structured.side_effect = ModelProviderError("Structured fail")

    secondary = MagicMock()
    secondary.model_name = "backup-secondary"
    secondary.generate_structured.return_value = DummyModel(status="recovered")

    fallback = FallbackModelProvider(primary, secondary)
    result = fallback.generate_structured("Prompt", DummyModel)

    assert result.status == "recovered"
    secondary.generate_structured.assert_called_once()
