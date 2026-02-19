"""Tests for the main Osyris client."""

import os
import pytest

from osyris import Osyris
from osyris.exceptions import AuthenticationError


def test_client_requires_api_key(monkeypatch):
    monkeypatch.delenv("OSYRIS_API_KEY", raising=False)
    with pytest.raises(AuthenticationError):
        Osyris()


def test_client_uses_env_api_key(monkeypatch):
    monkeypatch.setenv("OSYRIS_API_KEY", "test-key")
    client = Osyris()
    assert client.workspaces is not None
    assert client.conversations is not None
    assert client.files is not None


def test_client_uses_explicit_api_key(monkeypatch):
    monkeypatch.delenv("OSYRIS_API_KEY", raising=False)
    client = Osyris(api_key="explicit-key")
    assert client.workspaces is not None


def test_async_client_has_resources(monkeypatch):
    monkeypatch.delenv("OSYRIS_API_KEY", raising=False)
    from osyris import AsyncOsyris

    client = AsyncOsyris(api_key="test-key")
    assert client.workspaces is not None
    assert client.conversations is not None
    assert client.files is not None
