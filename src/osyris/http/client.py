"""HTTP client with auth and base URL."""

import requests
from typing import Any, Optional

from osyris.exceptions import APIError, AuthenticationError


class HttpClient:
    """Low-level HTTP client for the Osyris API."""

    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key or ""
        self._session = requests.Session()
        if self._api_key:
            self._session.headers["Authorization"] = f"Bearer {self._api_key}"
        self._session.headers["Content-Type"] = "application/json"

    def _url(self, path: str) -> str:
        path = path.lstrip("/")
        return f"{self._base_url}/{path}"

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> Any:
        url = self._url(path)
        try:
            response = self._session.request(
                method, url, params=params, json=json, timeout=30
            )
            if response.status_code == 401:
                raise AuthenticationError("Invalid or missing API key")
            if not response.ok:
                raise APIError(
                    f"API error: {response.status_code}",
                    status_code=response.status_code,
                    response_body=response.text,
                )
            if response.status_code == 204 or not response.content:
                return None
            return response.json()
        except requests.RequestException as e:
            raise APIError(str(e)) from e

    def get(self, path: str, params: Optional[dict] = None) -> Any:
        return self._request("GET", path, params=params)

    def post(self, path: str, json: Optional[dict] = None) -> Any:
        return self._request("POST", path, json=json)

    def put(self, path: str, json: Optional[dict] = None) -> Any:
        return self._request("PUT", path, json=json)

    def delete(self, path: str, json: Optional[dict] = None) -> Any:
        return self._request("DELETE", path, json=json)
