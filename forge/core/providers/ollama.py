"""Ollama local model provider adapter for offline and sovereign execution."""

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
    ProviderTimeoutError,
    SchemaValidationError,
)
from forge.core.logging import logger
from forge.core.model_provider import ModelProvider, ProviderResponse

T = TypeVar("T", bound=BaseModel)


class OllamaProvider(ModelProvider):
    """Provider adapter for local Ollama instances (Llama 3, Mistral, DeepSeek, Qwen)."""

    def __init__(
        self,
        model_name: str = "llama3:latest",
        base_url: str = "http://localhost:11434",
        temperature: float = 0.2,
        timeout: int = 60,
        max_retries: int = 3,
    ) -> None:
        super().__init__(model_name=model_name, temperature=temperature, timeout=timeout, max_retries=max_retries)
        self.base_url = base_url.rstrip("/")
        self.backoff = ExponentialBackoff(base_delay=0.5, max_delay=5.0, jitter_mode=JitterMode.FULL)

    def _post(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Send POST request to local Ollama server with backoff."""
        url = f"{self.base_url}{endpoint}"
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        def _call() -> dict[str, Any]:
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    raw_data = json.loads(response.read().decode("utf-8"))
                    return dict(raw_data) if isinstance(raw_data, dict) else {}
            except urllib.error.HTTPError as e:
                raise ModelProviderError(f"Ollama HTTP error {e.code}: {e.reason}") from e
            except urllib.error.URLError as e:
                if "timed out" in str(e).lower():
                    raise ProviderTimeoutError(f"Ollama request timed out after {self.timeout}s: {e}") from e
                raise ModelProviderError(f"Ollama connection error: {e}") from e

        return self.backoff.retry(
            _call,
            max_retries=self.max_retries,
            retryable_exceptions=(urllib.error.URLError, ProviderTimeoutError),
        )

    def generate_text(self, prompt: str, system_instruction: str | None = None) -> ProviderResponse:
        """Call Ollama /api/generate endpoint."""
        payload: dict[str, Any] = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": self.temperature},
        }
        if system_instruction:
            payload["system"] = system_instruction

        start_time = time.monotonic()
        data = self._post("/api/generate", payload)
        latency = time.monotonic() - start_time

        return ProviderResponse(
            content=data.get("response", ""),
            model_name=self.model_name,
            prompt_tokens=data.get("prompt_eval_count"),
            completion_tokens=data.get("eval_count"),
            total_tokens=(data.get("prompt_eval_count") or 0) + (data.get("eval_count") or 0),
            latency_seconds=round(latency, 3),
        )

    def generate_structured(
        self, prompt: str, response_schema: type[T], system_instruction: str | None = None
    ) -> T:
        """Request JSON schema conforming generation from Ollama."""
        schema_json = json.dumps(response_schema.model_json_schema())
        guided_prompt = (
            f"{prompt}\n\n"
            f"CRITICAL: Output must be strictly valid JSON conforming to this schema:\n"
            f"```json\n{schema_json}\n```\n"
            f"Respond ONLY with raw JSON. No conversational preamble, markdown fences, or explanations."
        )

        payload: dict[str, Any] = {
            "model": self.model_name,
            "prompt": guided_prompt,
            "format": "json",
            "stream": False,
            "options": {"temperature": self.temperature},
        }
        if system_instruction:
            payload["system"] = system_instruction

        data = self._post("/api/generate", payload)
        raw_text = data.get("response", "").strip()

        # Clean potential fences if present
        if raw_text.startswith("```"):
            raw_text = raw_text.split("\n", 1)[-1]
        if raw_text.endswith("```"):
            raw_text = raw_text.rsplit("\n", 1)[0]
        raw_text = raw_text.strip()

        try:
            parsed_dict = json.loads(raw_text)
            return response_schema.model_validate(parsed_dict)
        except Exception as e:
            logger.error(f"[OllamaProvider] Failed validating schema {response_schema.__name__}: {e}")
            raise SchemaValidationError(f"Ollama response failed schema validation: {e}") from e
