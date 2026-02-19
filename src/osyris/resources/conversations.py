"""Conversations API resource (sync and async)."""

from typing import List, Optional

from osyris.http.client import HttpClient
from osyris.http.async_client import AsyncHttpClient
from osyris.models.conversation import Conversation


class ConversationsResource:
    """Sync operations on conversations within a workspace."""

    def __init__(self, http: HttpClient):
        self._http = http

    def list(self, workspace_id: str) -> List[Conversation]:
        """List conversations in a workspace."""
        data = self._http.get(f"workspaces/{workspace_id}/conversations")
        items = data if isinstance(data, list) else (data.get("conversations") or [])
        return [Conversation.from_dict(item) for item in items]

    def get(self, workspace_id: str, conversation_id: str) -> Conversation:
        """Get a conversation by ID."""
        data = self._http.get(
            f"workspaces/{workspace_id}/conversations/{conversation_id}"
        )
        return Conversation.from_dict(data)

    def create(self, workspace_id: str, title: Optional[str] = None) -> Conversation:
        """Create a new conversation."""
        payload = {} if not title else {"title": title}
        data = self._http.post(
            f"workspaces/{workspace_id}/conversations",
            json=payload,
        )
        return Conversation.from_dict(data)


class AsyncConversationsResource:
    """Async operations on conversations within a workspace."""

    def __init__(self, http: AsyncHttpClient):
        self._http = http

    async def list(self, workspace_id: str) -> List[Conversation]:
        """List conversations in a workspace."""
        data = await self._http.get(f"workspaces/{workspace_id}/conversations")
        items = data if isinstance(data, list) else (data.get("conversations") or [])
        return [Conversation.from_dict(item) for item in items]

    async def get(self, workspace_id: str, conversation_id: str) -> Conversation:
        """Get a conversation by ID."""
        data = await self._http.get(
            f"workspaces/{workspace_id}/conversations/{conversation_id}"
        )
        return Conversation.from_dict(data)

    async def create(
        self, workspace_id: str, title: Optional[str] = None
    ) -> Conversation:
        """Create a new conversation."""
        payload = {} if not title else {"title": title}
        data = await self._http.post(
            f"workspaces/{workspace_id}/conversations",
            json=payload,
        )
        return Conversation.from_dict(data)
