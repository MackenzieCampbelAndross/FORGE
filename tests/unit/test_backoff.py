"""Unit tests for exponential backoff and jitter strategies."""

from unittest.mock import MagicMock

import pytest

from forge.core.backoff import ExponentialBackoff, JitterMode


def test_invalid_parameters() -> None:
    """Verify invalid base_delay, max_delay, or factor raises ValueError."""
    with pytest.raises(ValueError):
        ExponentialBackoff(base_delay=-1.0)
    with pytest.raises(ValueError):
        ExponentialBackoff(base_delay=10.0, max_delay=5.0)
    with pytest.raises(ValueError):
        ExponentialBackoff(factor=0.5)


def test_compute_delay_no_jitter() -> None:
    """Verify exact exponential progression without jitter."""
    backoff = ExponentialBackoff(base_delay=1.0, max_delay=10.0, factor=2.0, jitter_mode=JitterMode.NONE)

    # attempt 0: 1.0 * 2^0 = 1.0
    assert backoff.compute_delay(0) == 1.0
    # attempt 1: 1.0 * 2^1 = 2.0
    assert backoff.compute_delay(1) == 2.0
    # attempt 2: 1.0 * 2^2 = 4.0
    assert backoff.compute_delay(2) == 4.0
    # attempt 3: 1.0 * 2^3 = 8.0
    assert backoff.compute_delay(3) == 8.0
    # attempt 4: min(10.0, 16.0) = 10.0
    assert backoff.compute_delay(4) == 10.0


def test_compute_delay_full_jitter() -> None:
    """Verify delay is bounded within [0, min(max_delay, base * factor^attempt)]."""
    backoff = ExponentialBackoff(base_delay=2.0, max_delay=8.0, factor=2.0, jitter_mode=JitterMode.FULL)
    for _ in range(20):
        d = backoff.compute_delay(1)  # ceiling is 4.0
        assert 0.0 <= d <= 4.0


def test_compute_delay_equal_jitter() -> None:
    """Verify delay is bounded within [temp/2, temp]."""
    backoff = ExponentialBackoff(base_delay=2.0, max_delay=8.0, factor=2.0, jitter_mode=JitterMode.EQUAL)
    for _ in range(20):
        d = backoff.compute_delay(1)  # temp is 4.0, half is 2.0
        assert 2.0 <= d <= 4.0


def test_retry_successful_after_transient_failure() -> None:
    """Verify retry recovers after transient exception."""
    mock_func = MagicMock(side_effect=[ValueError("Transient fail"), "success"])
    backoff = ExponentialBackoff(base_delay=0.01, max_delay=0.05, jitter_mode=JitterMode.NONE)

    result = backoff.retry(mock_func, max_retries=2, retryable_exceptions=(ValueError,))
    assert result == "success"
    assert mock_func.call_count == 2


def test_retry_exhausted_raises() -> None:
    """Verify retry raises after exceeding max_retries."""
    mock_func = MagicMock(side_effect=RuntimeError("Permanent fail"))
    backoff = ExponentialBackoff(base_delay=0.01, max_delay=0.05, jitter_mode=JitterMode.NONE)

    with pytest.raises(RuntimeError, match="Permanent fail"):
        backoff.retry(mock_func, max_retries=2, retryable_exceptions=(RuntimeError,))
    assert mock_func.call_count == 3
