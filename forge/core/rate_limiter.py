"""Token bucket rate limiter for LLM provider throttling and quota protection."""

from __future__ import annotations

import threading
import time

from forge.core.exceptions import ModelProviderError


class RateLimitExceededError(ModelProviderError):
    """Raised when token bucket capacity is exceeded in non-blocking mode."""


class TokenBucketRateLimiter:
    """Thread-safe token bucket algorithm enforcing rate limits (requests or tokens)."""

    def __init__(self, rate_per_second: float, capacity: float) -> None:
        if rate_per_second <= 0:
            raise ValueError("rate_per_second must be positive")
        if capacity <= 0:
            raise ValueError("capacity must be positive")

        self.rate_per_second = float(rate_per_second)
        self.capacity = float(capacity)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = threading.Lock()

    def _refill(self) -> None:
        """Add tokens proportional to elapsed time since last refill."""
        now = time.monotonic()
        elapsed = now - self.last_refill
        if elapsed > 0:
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate_per_second)
            self.last_refill = now

    def try_acquire(self, tokens: float = 1.0) -> bool:
        """Attempt to consume tokens immediately without waiting. Returns True if granted."""
        with self._lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

    def acquire(self, tokens: float = 1.0, timeout: float | None = 30.0) -> None:
        """Wait until requested tokens are available and consume them."""
        start = time.monotonic()
        while True:
            with self._lock:
                self._refill()
                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return
                # Calculate sleep duration needed for remaining tokens
                missing = tokens - self.tokens
                sleep_time = min(0.1, missing / self.rate_per_second)

            if timeout is not None and (time.monotonic() - start + sleep_time) > timeout:
                raise RateLimitExceededError(
                    f"Rate limit exceeded: could not acquire {tokens} tokens within {timeout}s"
                )

            time.sleep(sleep_time)

    def available_tokens(self) -> float:
        """Current available tokens in bucket."""
        with self._lock:
            self._refill()
            return self.tokens
