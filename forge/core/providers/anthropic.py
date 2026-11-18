"""Anthropic Claude API provider adapter."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any, TypeVar

from pydantic import BaseModel

from forge.core.backoff import ExponentialBackoff, JitterMode
from forge.core.exceptions import (
    ModelProviderError,
    ProviderAuthenticationError,
    ProviderTimeoutError,
    SchemaValidationError,
)
from forge.core.logging import logger
from forge.core.model_provider import ModelProvider, ProviderResponse

T = TypeVar("T", bound=BaseModel)


class AnthropicProvider(ModelProvider):
    """Provider adapter for Anthropic Claude Messages API."""

    ANTHROPIC_VERSION = "2023-06-01"

    def __init__(
        self,
        api_key: str = "",
        model_name: str = "claude-3-5-sonnet-20241022",
        base_url: str = "https://api.anthropic.com/v1",
        temperature: float = 0.2,
        max_tokens: int = 4096,
        timeout: int = 60,
        max_retries: int = 3,
    ) -> None:
        super().__init__(model_name=model_name, temperature=temperature, timeout=timeout, max_retries=max_retries)
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.max_tokens = max_tokens
        self.backoff = ExponentialBackoff(base_delay=1.0, max_delay=10.0, jitter_mode=JitterMode.FULL)

    def _post(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Execute HTTPS request to Anthropic endpoint."""
        url = f"{self.base_url}{endpoint}"
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": self.ANTHROPIC_VERSION,
        }
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")

        def _call() -> dict[str, Any]:
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    raw = json.loads(response.read().decode("utf-8"))
                    return dict(raw) if isinstance(raw, dict) else {}
            except urllib.error.HTTPError as e:
                if e.code == 401:
                    raise ProviderAuthenticationError(f"Anthropic authentication failed: {e.reason}") from e
                if e.code == 429:
                    raise ModelProviderError(f"Anthropic rate limit exceeded: {e.reason}") from e
                raise ModelProviderError(f"Anthropic HTTP error {e.code}: {e.reason}") from e
            except urllib.error.URLError as e:
                if "timed out" in str(e).lower():
                    raise ProviderTimeoutError(f"Anthropic request timed out: {e}") from e
                raise ModelProviderError(f"Anthropic connection error: {e}") from e

        return self.backoff.retry(
            _call,
            max_retries=self.max_retries,
            retryable_exceptions=(urllib.error.URLError, ProviderTimeoutError),
        )

    def generate_text(self, prompt: str, system_instruction: str | None = None) -> ProviderResponse:
        """Call /messages endpoint."""
        payload: dict[str, Any] = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }
        if system_instruction:
            payload["system"] = system_instruction

        start = time.monotonic()
        data = self._post("/messages", payload)
        latency = time.monotonic() - start

        # Extract text content from content blocks
        content_blocks = data.get("content", [])
        text_parts = [b.get("text", "") for b in content_blocks if b.get("type") == "text"]
        full_text = "".join(text_parts)

        usage = data.get("usage", {})
        prompt_tokens = usage.get("input_tokens")
        completion_tokens = usage.get("output_tokens")
        total_tokens = (prompt_tokens or 0) + (completion_tokens or 0)

        return ProviderResponse(
            content=full_text,
            model_name=self.model_name,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            latency_seconds=round(latency, 3),
            finish_reason=data.get("stop_reason"),
        )

    def generate_structured(
        self, prompt: str, response_schema: type[T], system_instruction: str | None = None
    ) -> T:
        """Generate structured JSON adhering to response_schema."""
        schema_json = json.dumps(response_schema.model_json_schema())
        system_text = (
            f"{system_instruction or ''}\n\n"
            f"CRITICAL: Output must be strictly valid JSON conforming to this schema:\n{schema_json}\n"
            f"Respond with raw JSON only. Do not wrap in markdown quotes."
        ).strip()

        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "system": system_text,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }

        data = self._post("/messages", payload)
        content_blocks = data.get("content", [])
        raw_text = "".join(b.get("text", "") for b in content_blocks if b.get("type") == "text").strip()

        if raw_text.startswith("```"):
            raw_text = raw_text.split("\n", 1)[-1]
        if raw_text.endswith("```"):
            raw_text = raw_text.rsplit("\n", 1)[0]
        raw_text = raw_text.strip()

        try:
            parsed = json.loads(raw_text)
            return response_schema.model_validate(parsed)
        except Exception as e:
            logger.error(f"[AnthropicProvider] Schema validation error: {e}")
            raise SchemaValidationError(f"Anthropic output failed schema validation: {e}") from e
