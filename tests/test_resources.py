"""Tests for API resources (with mocked HTTP)."""

import pytest
from unittest.mock import MagicMock

from osyris.http.client import HttpClient
from osyris.resources.workspaces import WorkspacesResource
from osyris.resources.files import FilesResource
from osyris.models.workspace import Workspace


def test_workspaces_resource_list():
    http = MagicMock(spec=HttpClient)
    http.get.return_value = [
        {"id": "w1", "name": "Workspace 1"},
        {"id": "w2", "name": "Workspace 2"},
    ]
    resource = WorkspacesResource(http)
    workspaces = resource.list()
    assert len(workspaces) == 2
    assert workspaces[0].id == "w1"
    assert workspaces[0].name == "Workspace 1"
    http.get.assert_called_once_with("workspaces")


def test_workspaces_resource_get():
    http = MagicMock(spec=HttpClient)
    http.get.return_value = {"id": "w1", "name": "My Workspace"}
    resource = WorkspacesResource(http)
    ws = resource.get("w1")
    assert ws.id == "w1"
    assert ws.name == "My Workspace"
    http.get.assert_called_once_with("workspaces/w1")


def test_files_resource_upload():
    http = MagicMock(spec=HttpClient)
    http.post.return_value = {"id": "f1", "path": "doc.txt"}
    resource = FilesResource(http)
    result = resource.upload("wid", "doc.txt", "content")
    assert result["path"] == "doc.txt"
    http.post.assert_called_once_with(
        "files",
        json={"workspace_id": "wid", "path": "doc.txt", "content": "content"},
    )
