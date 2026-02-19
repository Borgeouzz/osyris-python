"""Async Osyris SDK client."""

from typing import Optional

from osyris.config import Config
from osyris.exceptions import AuthenticationError
from osyris.http.async_client import AsyncHttpClient
from osyris.resources.workspaces import AsyncWorkspacesResource
from osyris.resources.conversations import AsyncConversationsResource
from osyris.resources.files import AsyncFilesResource


class AsyncOsyris:
    """Async client for the Osyris API. Use as an async context manager to ensure the HTTP client is closed."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = Config.DEFAULT_TIMEOUT,
        max_retries: int = Config.DEFAULT_MAX_RETRIES,
    ):
        self._config = Config(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )
        if not self._config.is_configured():
            raise AuthenticationError("OSYRIS_API_KEY is not set")
        self._http = AsyncHttpClient(
            base_url=self._config.api_base_url,
            api_key=self._config.api_key,
            timeout=self._config.timeout,
            max_retries=self._config.max_retries,
        )
        self._workspaces = AsyncWorkspacesResource(self._http)
        self._conversations = AsyncConversationsResource(self._http)
        self._files = AsyncFilesResource(self._http)

    @property
    def workspaces(self) -> AsyncWorkspacesResource:
        return self._workspaces

    @property
    def conversations(self) -> AsyncConversationsResource:
        return self._conversations

    @property
    def files(self) -> AsyncFilesResource:
        return self._files

    async def upload_file(
        self,
        path: str,
        content: str,
        workspace_id: Optional[str] = None,
    ) -> dict:
        """Upload a file. If workspace_id is omitted, uses default workspace context."""
        return await self._files.upload(
            workspace_id=workspace_id or "",
            path=path,
            content=content,
        )

    async def delete_file(
        self,
        path: str,
        workspace_id: Optional[str] = None,
    ) -> None:
        """Delete a file by path."""
        await self._files.delete(path=path, workspace_id=workspace_id)

    async def close(self) -> None:
        """Close the underlying HTTP client. Prefer using async with instead."""
        await self._http.close()

    async def __aenter__(self) -> "AsyncOsyris":
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
