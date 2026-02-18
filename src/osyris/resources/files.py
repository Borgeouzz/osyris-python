"""Files API resource."""

from typing import List, Optional

from osyris.http.client import HttpClient
from osyris.models.file import File


class FilesResource:
    """Operations on files within a workspace."""

    def __init__(self, http: HttpClient):
        self._http = http

    def upload(self, workspace_id: str, path: str, content: str) -> dict:
        """Upload or update a file."""
        return self._http.post(
            "files",
            json={
                "workspace_id": workspace_id,
                "path": path,
                "content": content,
            },
        )

    def delete(self, path: str, workspace_id: Optional[str] = None) -> None:
        """Delete a file by path."""
        payload = {"path": path}
        if workspace_id:
            payload["workspace_id"] = workspace_id
        self._http.delete("files", json=payload)

    def list(self, workspace_id: str) -> List[File]:
        """List files in a workspace."""
        data = self._http.get(f"workspaces/{workspace_id}/files")
        items = data if isinstance(data, list) else (data.get("files") or [])
        return [File.from_dict(item) for item in items]
