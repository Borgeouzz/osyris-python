"""Workspaces API resource (sync and async)."""

from typing import List

from osyris.http.client import HttpClient
from osyris.http.async_client import AsyncHttpClient
from osyris.models.workspace import Workspace


class WorkspacesResource:
    """Sync operations on workspaces."""

    def __init__(self, http: HttpClient):
        self._http = http

    def list(self) -> List[Workspace]:
        """List all workspaces."""
        data = self._http.get("workspaces")
        items = data if isinstance(data, list) else (data.get("workspaces") or [])
        return [Workspace.from_dict(item) for item in items]

    def get(self, workspace_id: str) -> Workspace:
        """Get a workspace by ID."""
        data = self._http.get(f"workspaces/{workspace_id}")
        return Workspace.from_dict(data)


class AsyncWorkspacesResource:
    """Async operations on workspaces."""

    def __init__(self, http: AsyncHttpClient):
        self._http = http

    async def list(self) -> List[Workspace]:
        """List all workspaces."""
        data = await self._http.get("workspaces")
        items = data if isinstance(data, list) else (data.get("workspaces") or [])
        return [Workspace.from_dict(item) for item in items]

    async def get(self, workspace_id: str) -> Workspace:
        """Get a workspace by ID."""
        data = await self._http.get(f"workspaces/{workspace_id}")
        return Workspace.from_dict(data)
