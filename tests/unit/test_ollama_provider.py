"""Unit tests and mock suite for local Ollama provider adapter."""

import json
import urllib.error
from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from forge.core.exceptions import ModelProviderError, SchemaValidationError
from forge.core.providers.ollama import OllamaProvider


class DummySchema(BaseModel):
    name: str
    active: bool


@patch("urllib.request.urlopen")
def test_ollama_generate_text_success(mock_urlopen: MagicMock) -> None:
    """Verify generate_text calls Ollama and extracts text and token counts."""
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({
        "response": "Architectural recommendation: use Redis",
        "prompt_eval_count": 42,
        "eval_count": 88,
    }).encode("utf-8")
    mock_urlopen.return_value.__enter__.return_value = mock_response

    provider = OllamaProvider(model_name="mistral:latest")
    resp = provider.generate_text("Suggest caching strategy")

    assert resp.content == "Architectural recommendation: use Redis"
    assert resp.model_name == "mistral:latest"
    assert resp.prompt_tokens == 42
    assert resp.completion_tokens == 88
    assert resp.total_tokens == 130


@patch("urllib.request.urlopen")
def test_ollama_generate_structured_success(mock_urlopen: MagicMock) -> None:
    """Verify generate_structured parses JSON payload correctly."""
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({
        "response": '```json\n{"name": "Auth Gateway", "active": true}\n```'
    }).encode("utf-8")
    mock_urlopen.return_value.__enter__.return_value = mock_response

    provider = OllamaProvider(model_name="llama3:latest")
    obj = provider.generate_structured("Create component", DummySchema)

    assert obj.name == "Auth Gateway"
    assert obj.active is True


@patch("urllib.request.urlopen")
def test_ollama_generate_structured_invalid_schema_raises(mock_urlopen: MagicMock) -> None:
    """Verify invalid JSON raises SchemaValidationError."""
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({
        "response": "Not valid json at all!"
    }).encode("utf-8")
    mock_urlopen.return_value.__enter__.return_value = mock_response

    provider = OllamaProvider()
    with pytest.raises(SchemaValidationError):
        provider.generate_structured("Create component", DummySchema)


@patch("urllib.request.urlopen")
def test_ollama_http_error_raises(mock_urlopen: MagicMock) -> None:
    """Verify HTTP error raises ModelProviderError."""
    mock_urlopen.side_effect = urllib.error.HTTPError(
        url="http://localhost:11434/api/generate",
        code=500,
        msg="Internal Error",
        hdrs=MagicMock(),
        fp=MagicMock(),
    )

    provider = OllamaProvider()
    with pytest.raises(ModelProviderError, match="Ollama HTTP error 500"):
        provider.generate_text("Hello")
