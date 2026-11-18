"""Unit tests and mock suite for Anthropic Claude provider adapter."""

import json
import urllib.error
from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from forge.core.exceptions import (
    ModelProviderError,
    ProviderAuthenticationError,
)
from forge.core.providers.anthropic import AnthropicProvider


class SecurityPolicy(BaseModel):
    mfa_required: bool
    session_timeout_minutes: int


@patch("urllib.request.urlopen")
def test_anthropic_generate_text_success(mock_urlopen: MagicMock) -> None:
    """Verify generate_text calls Anthropic /messages and extracts tokens and content."""
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({
        "content": [{"type": "text", "text": "Zero-trust network segmentation blueprint"}],
        "usage": {"input_tokens": 120, "output_tokens": 340},
        "stop_reason": "end_turn",
    }).encode("utf-8")
    mock_urlopen.return_value.__enter__.return_value = mock_response

    provider = AnthropicProvider(api_key="sk-ant-test", model_name="claude-3-5-sonnet-20241022")
    resp = provider.generate_text("Design network policy")

    assert "Zero-trust" in resp.content
    assert resp.model_name == "claude-3-5-sonnet-20241022"
    assert resp.prompt_tokens == 120
    assert resp.completion_tokens == 340
    assert resp.total_tokens == 460
    assert resp.finish_reason == "end_turn"


@patch("urllib.request.urlopen")
def test_anthropic_generate_structured_success(mock_urlopen: MagicMock) -> None:
    """Verify generate_structured parses JSON payload into Pydantic model."""
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({
        "content": [{"type": "text", "text": '{"mfa_required": true, "session_timeout_minutes": 15}'}],
    }).encode("utf-8")
    mock_urlopen.return_value.__enter__.return_value = mock_response

    provider = AnthropicProvider(api_key="sk-ant-test")
    policy = provider.generate_structured("Generate policy", SecurityPolicy)

    assert policy.mfa_required is True
    assert policy.session_timeout_minutes == 15


@patch("urllib.request.urlopen")
def test_anthropic_auth_failure(mock_urlopen: MagicMock) -> None:
    """Verify 401 raises ProviderAuthenticationError."""
    mock_urlopen.side_effect = urllib.error.HTTPError(
        url="https://api.anthropic.com/v1/messages",
        code=401,
        msg="Unauthorized",
        hdrs=MagicMock(),
        fp=MagicMock(),
    )

    provider = AnthropicProvider(api_key="bad-key")
    with pytest.raises(ProviderAuthenticationError):
        provider.generate_text("Hello")


@patch("urllib.request.urlopen")
def test_anthropic_rate_limit(mock_urlopen: MagicMock) -> None:
    """Verify 429 raises ModelProviderError."""
    mock_urlopen.side_effect = urllib.error.HTTPError(
        url="https://api.anthropic.com/v1/messages",
        code=429,
        msg="Too Many Requests",
        hdrs=MagicMock(),
        fp=MagicMock(),
    )

    provider = AnthropicProvider(api_key="sk-ant-test")
    with pytest.raises(ModelProviderError, match="rate limit"):
        provider.generate_text("Hello")
