"""Main Osyris SDK client (sync)."""

from typing import Optional

from osyris.config import Config
from osyris.exceptions import AuthenticationError
from osyris.http.client import HttpClient
from osyris.resources.workspaces import WorkspacesResource
from osyris.resources.conversations import ConversationsResource
from osyris.resources.files import FilesResource


class Osyris:
    """Sync client for the Osyris API."""

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
        self._http = HttpClient(
            base_url=self._config.api_base_url,
            api_key=self._config.api_key,
            timeout=self._config.timeout,
            max_retries=self._config.max_retries,
        )
        self._workspaces = WorkspacesResource(self._http)
        self._conversations = ConversationsResource(self._http)
        self._files = FilesResource(self._http)

    @property
    def workspaces(self) -> WorkspacesResource:
        return self._workspaces

    @property
    def conversations(self) -> ConversationsResource:
        return self._conversations

    @property
    def files(self) -> FilesResource:
        return self._files

    def upload_file(self, path: str, content: str, workspace_id: Optional[str] = None) -> dict:
        """Upload a file. If workspace_id is omitted, uses default workspace context."""
        return self._files.upload(
            workspace_id=workspace_id or "",
            path=path,
            content=content,
        )

    def delete_file(self, path: str, workspace_id: Optional[str] = None) -> None:
        """Delete a file by path."""
        self._files.delete(path=path, workspace_id=workspace_id)

    def close(self) -> None:
        """Close the underlying HTTP client. Optional for short-lived usage."""
        self._http.close()
