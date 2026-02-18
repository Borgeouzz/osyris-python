"""Conversation model."""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Conversation:
    """Represents a conversation in a workspace."""

    id: str
    workspace_id: str
    title: Optional[str] = None
    raw: Optional[dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Conversation":
        return cls(
            id=data.get("id", ""),
            workspace_id=data.get("workspace_id", ""),
            title=data.get("title"),
            raw=data,
        )
