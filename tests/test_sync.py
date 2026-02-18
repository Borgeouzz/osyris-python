"""Tests for the sync engine."""

import os
import tempfile
import json
import pytest

from osyris.sync.engine import SyncEngine
from osyris.sync.state import LocalState
from osyris.sync.hasher import hash_file


def test_sync_engine_ignores_dotfiles(tmp_path):
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / ".hidden").write_text("hidden")
    state_dir = tmp_path / ".osyris"
    state_dir.mkdir()
    state_path = state_dir / "state.json"

    engine = SyncEngine(client=None, root_path=str(tmp_path))
    engine.initial_sync()

    state = LocalState(str(state_path))
    assert state.get_file_hash("a.txt") is not None
    assert state.get_file_hash(".hidden") is None


def test_sync_engine_ignores_osyris_folder(tmp_path):
    (tmp_path / "a.txt").write_text("a")
    state_dir = tmp_path / ".osyris"
    state_dir.mkdir()
    (state_dir / "state.json").write_text("{}")

    engine = SyncEngine(client=None, root_path=str(tmp_path))
    engine.initial_sync()

    data = json.loads((state_dir / "state.json").read_text())
    # .osyris/state.json must not appear in files
    assert "state.json" not in str(data.get("files", {}))
    assert ".osyris/state.json" not in data.get("files", {})


def test_local_state_save_and_load(tmp_path):
    state_path = tmp_path / "state.json"
    state = LocalState(str(state_path))
    state.update_file("foo.txt", "abc123")
    state.save()

    state2 = LocalState(str(state_path))
    assert state2.get_file_hash("foo.txt") == "abc123"
