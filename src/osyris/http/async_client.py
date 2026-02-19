"""Async HTTP client with auth, timeout, and optional retry."""

from typing import Any, Optional

import httpx
from httpx import Timeout

from osyris.exceptions import APIError, AuthenticationError
from osyris.http.retry import with_retry_async

from .client import DEFAULT_TIMEOUT, RETRYABLE_STATUS_CODES


class AsyncHttpClient:
    """Async HTTP client for the Osyris API."""

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = 3,
    ):
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key or ""
        self._timeout = Timeout(timeout)
        self._max_retries = max_retries
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            headers=self._headers(),
            timeout=self._timeout,
        )

    def _headers(self) -> dict:
        h = {"Content-Type": "application/json"}
        if self._api_key:
            h["Authorization"] = f"Bearer {self._api_key}"
        return h

    def _url(self, path: str) -> str:
        path = path.lstrip("/")
        return f"{self._base_url}/{path}"

    async def _request(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> Any:
        async def _do() -> Any:
            try:
                response = await self._client.request(
                    method, self._url(path), params=params, json=json
                )
                if response.status_code == 401:
                    raise AuthenticationError("Invalid or missing API key")
                if not response.is_success:
                    raise APIError(
                        f"API error: {response.status_code}",
                        status_code=response.status_code,
                        response_body=response.text,
                    )
                if response.status_code == 204 or not response.content:
                    return None
                return response.json()
            except httpx.HTTPError as e:
                raise APIError(str(e)) from e

        if self._max_retries > 0:
            return await with_retry_async(
                _do,
                max_retries=self._max_retries,
                retry_on=RETRYABLE_STATUS_CODES,
            )
        return await _do()

    async def get(self, path: str, params: Optional[dict] = None) -> Any:
        return await self._request("GET", path, params=params)

    async def post(self, path: str, json: Optional[dict] = None) -> Any:
        return await self._request("POST", path, json=json)

    async def put(self, path: str, json: Optional[dict] = None) -> Any:
        return await self._request("PUT", path, json=json)

    async def delete(self, path: str, json: Optional[dict] = None) -> Any:
        return await self._request("DELETE", path, json=json)

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> "AsyncHttpClient":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
