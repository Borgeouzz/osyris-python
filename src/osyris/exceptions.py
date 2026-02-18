"""Osyris SDK exceptions."""

from typing import Optional


class OsyrisError(Exception):
    """Base exception for all Osyris SDK errors."""

    pass


class AuthenticationError(OsyrisError):
    """Raised when authentication fails or API key is missing."""

    pass


class APIError(OsyrisError):
    """Raised when the API returns an error response."""

    def __init__(self, message: str, status_code: Optional[int] = None, response_body: Optional[str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body
