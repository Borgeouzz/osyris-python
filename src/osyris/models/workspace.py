"""Workspace model."""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Workspace:
    """Represents an Osyris workspace."""

    id: str
    name: str
    raw: Optional[dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Workspace":
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            raw=data,
        )
