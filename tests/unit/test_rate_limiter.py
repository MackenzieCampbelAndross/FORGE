"""Unit tests for token bucket rate limiter."""

import time

import pytest

from forge.core.rate_limiter import RateLimitExceededError, TokenBucketRateLimiter


def test_invalid_parameters() -> None:
    """Verify negative or zero rate/capacity raises ValueError."""
    with pytest.raises(ValueError):
        TokenBucketRateLimiter(rate_per_second=0, capacity=10)
    with pytest.raises(ValueError):
        TokenBucketRateLimiter(rate_per_second=10, capacity=-1)


def test_try_acquire() -> None:
    """Verify immediate non-blocking token consumption."""
    limiter = TokenBucketRateLimiter(rate_per_second=10, capacity=5)
    assert limiter.try_acquire(3) is True
    assert limiter.try_acquire(2) is True
    # Now empty
    assert limiter.try_acquire(1) is False


def test_acquire_blocking_refill() -> None:
    """Verify blocking acquire waits for replenishment."""
    limiter = TokenBucketRateLimiter(rate_per_second=20, capacity=2)
    assert limiter.try_acquire(2) is True

    start = time.monotonic()
    # Need 1 token: at 20/sec, takes ~0.05s
    limiter.acquire(1, timeout=2.0)
    elapsed = time.monotonic() - start
    assert elapsed >= 0.03


def test_acquire_timeout() -> None:
    """Verify acquire raises RateLimitExceededError if timeout expires."""
    limiter = TokenBucketRateLimiter(rate_per_second=1, capacity=1)
    limiter.try_acquire(1)

    with pytest.raises(RateLimitExceededError):
        limiter.acquire(10, timeout=0.05)
