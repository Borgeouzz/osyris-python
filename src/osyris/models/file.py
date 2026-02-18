"""File model."""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class File:
    """Represents a file in a workspace."""

    id: Optional[str] = None
    path: Optional[str] = None
    content: Optional[str] = None
    raw: Optional[dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "File":
        return cls(
            id=data.get("id"),
            path=data.get("path"),
            content=data.get("content"),
            raw=data,
        )
