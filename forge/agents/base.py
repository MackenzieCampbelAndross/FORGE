"""Base agent architecture for FORGE."""

import time
from abc import ABC, abstractmethod
from typing import Any, TypeVar

from pydantic import BaseModel

from forge.core.logging import logger
from forge.core.model_provider import ModelProvider, get_model_provider

T = TypeVar("T", bound=BaseModel)


class BaseAgent(ABC):
    """Abstract base agent providing model interactions, schema validation, and telemetry."""

    def __init__(self, name: str, role: str, provider: ModelProvider | None = None):
        self.name = name
        self.role = role
        self.provider = provider or get_model_provider()

    @abstractmethod
    def run(self, *args, **kwargs) -> Any:
        """Execute agent workflow."""
        pass

    def call_structured(
        self,
        prompt: str,
        response_schema: type[T],
        system_instruction: str | None = None,
    ) -> tuple[T, float]:
        """Invoke provider with schema validation and latency tracking."""
        start = time.time()
        logger.info(f"[{self.name}] Invoking model with schema {response_schema.__name__}...")
        result = self.provider.generate_structured(
            prompt=prompt,
            response_schema=response_schema,
            system_instruction=system_instruction
            or f"You are the {self.role} in the FORGE engineering platform.",
        )
        elapsed = time.time() - start
        logger.info(f"[{self.name}] Completed in {elapsed:.3f}s")
        return result, elapsed
