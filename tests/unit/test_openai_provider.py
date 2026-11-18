"""Unit tests and mock suite for OpenAI provider adapter."""

import json
import urllib.error
from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from forge.core.exceptions import (
    ModelProviderError,
    ProviderAuthenticationError,
)
from forge.core.providers.openai import OpenAIProvider


class SampleModel(BaseModel):
    service: str
    port: int


@patch("urllib.request.urlopen")
def test_openai_generate_text_success(mock_urlopen: MagicMock) -> None:
    """Verify generate_text calls OpenAI and parses response."""
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({
        "choices": [{"message": {"content": "Use Redis cluster for distributed locking"}, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 50, "completion_tokens": 120, "total_tokens": 170},
    }).encode("utf-8")
    mock_urlopen.return_value.__enter__.return_value = mock_response

    provider = OpenAIProvider(api_key="sk-test", model_name="gpt-4o")
    resp = provider.generate_text("Distributed lock design")

    assert "Redis cluster" in resp.content
    assert resp.model_name == "gpt-4o"
    assert resp.total_tokens == 170
    assert resp.finish_reason == "stop"


@patch("urllib.request.urlopen")
def test_openai_generate_structured_success(mock_urlopen: MagicMock) -> None:
    """Verify generate_structured parses JSON payload into Pydantic model."""
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({
        "choices": [{"message": {"content": '{"service": "PaymentProcessor", "port": 8080}'}}],
    }).encode("utf-8")
    mock_urlopen.return_value.__enter__.return_value = mock_response

    provider = OpenAIProvider(api_key="sk-test")
    model = provider.generate_structured("Create payment service", SampleModel)

    assert model.service == "PaymentProcessor"
    assert model.port == 8080


@patch("urllib.request.urlopen")
def test_openai_authentication_error(mock_urlopen: MagicMock) -> None:
    """Verify 401 raises ProviderAuthenticationError."""
    mock_urlopen.side_effect = urllib.error.HTTPError(
        url="https://api.openai.com/v1/chat/completions",
        code=401,
        msg="Unauthorized",
        hdrs=MagicMock(),
        fp=MagicMock(),
    )

    provider = OpenAIProvider(api_key="invalid-key")
    with pytest.raises(ProviderAuthenticationError):
        provider.generate_text("Hello")


@patch("urllib.request.urlopen")
def test_openai_rate_limit_error(mock_urlopen: MagicMock) -> None:
    """Verify 429 raises ModelProviderError with rate limit note."""
    mock_urlopen.side_effect = urllib.error.HTTPError(
        url="https://api.openai.com/v1/chat/completions",
        code=429,
        msg="Too Many Requests",
        hdrs=MagicMock(),
        fp=MagicMock(),
    )

    provider = OpenAIProvider(api_key="sk-test")
    with pytest.raises(ModelProviderError, match="rate limit"):
        provider.generate_text("Hello")
