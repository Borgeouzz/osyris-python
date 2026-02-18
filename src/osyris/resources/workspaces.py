"""Workspaces API resource."""

from typing import List

from osyris.http.client import HttpClient
from osyris.models.workspace import Workspace


class WorkspacesResource:
    """Operations on workspaces."""

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
