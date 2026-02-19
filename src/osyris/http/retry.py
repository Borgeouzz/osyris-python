"""Retry logic for HTTP requests (sync and async)."""

import asyncio
import time
from typing import Awaitable, Callable, Optional, TypeVar

from osyris.exceptions import APIError

T = TypeVar("T")

DEFAULT_RETRY_ON = (429, 500, 502, 503)


def with_retry(
    fn: Callable[[], T],
    max_retries: int = 3,
    backoff_factor: float = 1.0,
    retry_on: tuple = DEFAULT_RETRY_ON,
) -> T:
    """Execute a callable with exponential backoff on retryable errors."""
    last_error: Optional[Exception] = None
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except APIError as e:
            last_error = e
            code = getattr(e, "status_code", None)
            if code not in retry_on or attempt == max_retries:
                raise
            time.sleep(backoff_factor * (2**attempt))
    raise last_error  # type: ignore[misc]


async def with_retry_async(
    fn: Callable[[], Awaitable[T]],
    max_retries: int = 3,
    backoff_factor: float = 1.0,
    retry_on: tuple = DEFAULT_RETRY_ON,
) -> T:
    """Execute an async callable with exponential backoff on retryable errors."""
    last_error: Optional[Exception] = None
    for attempt in range(max_retries + 1):
        try:
            return await fn()
        except APIError as e:
            last_error = e
            code = getattr(e, "status_code", None)
            if code not in retry_on or attempt == max_retries:
                raise
            await asyncio.sleep(backoff_factor * (2**attempt))
    raise last_error  # type: ignore[misc]
