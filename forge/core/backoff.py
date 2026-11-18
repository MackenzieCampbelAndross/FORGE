"""Exponential backoff and randomized jitter utilities for API resilience."""

from __future__ import annotations

import random
import time
from collections.abc import Callable
from enum import Enum
from typing import Any, TypeVar

from forge.core.logging import logger

T = TypeVar("T")


class JitterMode(str, Enum):
    """Jitter strategies to avoid thundering herd problem on API clusters."""

    NONE = "none"
    FULL = "full"
    EQUAL = "equal"
    DECORRELATED = "decorrelated"


class ExponentialBackoff:
    """Calculates backoff delays with exponential scaling and stochastic jitter."""

    def __init__(
        self,
        base_delay: float = 1.0,
        max_delay: float = 30.0,
        factor: float = 2.0,
        jitter_mode: JitterMode = JitterMode.FULL,
    ) -> None:
        if base_delay <= 0:
            raise ValueError("base_delay must be positive")
        if max_delay < base_delay:
            raise ValueError("max_delay must be >= base_delay")
        if factor < 1.0:
            raise ValueError("factor must be >= 1.0")

        self.base_delay = base_delay
        self.max_delay = max_delay
        self.factor = factor
        self.jitter_mode = jitter_mode

    def compute_delay(self, attempt: int, previous_delay: float = 0.0) -> float:
        """Compute wait duration for a specific retry attempt (0-indexed)."""
        temp = min(self.max_delay, self.base_delay * (self.factor**attempt))

        if self.jitter_mode == JitterMode.NONE:
            return temp

        if self.jitter_mode == JitterMode.FULL:
            # Full Jitter: Uniform(0, min(max_delay, base * factor^attempt))
            return random.uniform(0, temp)

        if self.jitter_mode == JitterMode.EQUAL:
            # Equal Jitter: temp/2 + Uniform(0, temp/2)
            half = temp / 2.0
            return half + random.uniform(0, half)

        if self.jitter_mode == JitterMode.DECORRELATED:
            # Decorrelated Jitter: Uniform(base_delay, previous_delay * 3)
            high = max(self.base_delay, previous_delay * 3.0)
            return min(self.max_delay, random.uniform(self.base_delay, high))

        return temp

    def retry(
        self,
        func: Callable[..., T],
        max_retries: int = 3,
        retryable_exceptions: tuple[type[Exception], ...] = (Exception,),
        *args: Any,
        **kwargs: Any,
    ) -> T:
        """Execute callable with backoff retries on specified exceptions."""
        attempt = 0
        last_delay = 0.0
        while True:
            try:
                return func(*args, **kwargs)
            except retryable_exceptions as e:
                attempt += 1
                if attempt > max_retries:
                    logger.error(f"[ExponentialBackoff] Exhausted {max_retries} retries: {e}")
                    raise

                delay = self.compute_delay(attempt - 1, previous_delay=last_delay)
                last_delay = delay
                logger.warning(
                    f"[ExponentialBackoff] Attempt {attempt}/{max_retries} failed ({type(e).__name__}: {e}). "
                    f"Retrying in {delay:.2f}s..."
                )
                time.sleep(delay)
