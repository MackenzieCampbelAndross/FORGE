"""OpenAI and OpenAI-compatible API provider adapter."""

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


class OpenAIProvider(ModelProvider):
    """Provider adapter for OpenAI chat completions API and compatible gateways."""

    def __init__(
        self,
        api_key: str = "",
        model_name: str = "gpt-4o",
        base_url: str = "https://api.openai.com/v1",
        temperature: float = 0.2,
        timeout: int = 60,
        max_retries: int = 3,
    ) -> None:
        super().__init__(model_name=model_name, temperature=temperature, timeout=timeout, max_retries=max_retries)
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.backoff = ExponentialBackoff(base_delay=1.0, max_delay=10.0, jitter_mode=JitterMode.FULL)

    def _post(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Execute HTTPS request to OpenAI endpoint."""
        url = f"{self.base_url}{endpoint}"
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")

        def _call() -> dict[str, Any]:
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    raw_data = json.loads(response.read().decode("utf-8"))
                    return dict(raw_data) if isinstance(raw_data, dict) else {}
            except urllib.error.HTTPError as e:
                if e.code == 401:
                    raise ProviderAuthenticationError(f"OpenAI authentication failed: {e.reason}") from e
                if e.code == 429:
                    raise ModelProviderError(f"OpenAI rate limit exceeded: {e.reason}") from e
                raise ModelProviderError(f"OpenAI HTTP error {e.code}: {e.reason}") from e
            except urllib.error.URLError as e:
                if "timed out" in str(e).lower():
                    raise ProviderTimeoutError(f"OpenAI request timed out: {e}") from e
                raise ModelProviderError(f"OpenAI connection error: {e}") from e

        return self.backoff.retry(
            _call,
            max_retries=self.max_retries,
            retryable_exceptions=(urllib.error.URLError, ProviderTimeoutError),
        )

    def generate_text(self, prompt: str, system_instruction: str | None = None) -> ProviderResponse:
        """Call chat/completions endpoint."""
        messages: list[dict[str, str]] = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
        }

        start = time.monotonic()
        data = self._post("/chat/completions", payload)
        latency = time.monotonic() - start

        choices = data.get("choices", [])
        content = choices[0]["message"]["content"] if choices else ""
        usage = data.get("usage", {})

        return ProviderResponse(
            content=content,
            model_name=self.model_name,
            prompt_tokens=usage.get("prompt_tokens"),
            completion_tokens=usage.get("completion_tokens"),
            total_tokens=usage.get("total_tokens"),
            latency_seconds=round(latency, 3),
            finish_reason=choices[0].get("finish_reason") if choices else None,
        )

    def generate_structured(
        self, prompt: str, response_schema: type[T], system_instruction: str | None = None
    ) -> T:
        """Generate structured JSON adhering to response_schema."""
        schema_json = json.dumps(response_schema.model_json_schema())
        messages: list[dict[str, str]] = []

        system_text = (
            f"{system_instruction or ''}\n\n"
            f"You must produce JSON conforming strictly to this schema:\n{schema_json}"
        ).strip()
        messages.append({"role": "system", "content": system_text})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
            "response_format": {"type": "json_object"},
        }

        data = self._post("/chat/completions", payload)
        choices = data.get("choices", [])
        raw_text = choices[0]["message"]["content"].strip() if choices else "{}"

        try:
            parsed = json.loads(raw_text)
            return response_schema.model_validate(parsed)
        except Exception as e:
            logger.error(f"[OpenAIProvider] Schema validation error: {e}")
            raise SchemaValidationError(f"OpenAI output failed schema validation: {e}") from e
