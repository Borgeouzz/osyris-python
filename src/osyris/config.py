"""SDK configuration."""

import os
from typing import Optional


class Config:
    """Configuration for the Osyris client."""

    DEFAULT_BASE_URL = "https://api.osyris.dev"
    API_VERSION = "v1"
    DEFAULT_TIMEOUT = 30.0
    DEFAULT_MAX_RETRIES = 3

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ):
        self.api_key = api_key or os.getenv("OSYRIS_API_KEY")
        self.base_url = (base_url or os.getenv("OSYRIS_BASE_URL") or self.DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        self.max_retries = max(0, max_retries)

    @property
    def api_base_url(self) -> str:
        return f"{self.base_url}/api/{self.API_VERSION}"

    def is_configured(self) -> bool:
        return bool(self.api_key)
