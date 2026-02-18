"""Retry logic for HTTP requests."""

import time
from typing import Callable, TypeVar

from osyris.exceptions import APIError

T = TypeVar("T")


def with_retry(
    fn: Callable[[], T],
    max_retries: int = 3,
    backoff_factor: float = 1.0,
    retry_on: tuple = (429, 500, 502, 503),
) -> T:
    """Execute a callable with exponential backoff on retryable errors."""
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except APIError as e:
            last_error = e
            if e.status_code not in retry_on or attempt == max_retries:
                raise
            time.sleep(backoff_factor * (2**attempt))
    raise last_error
