from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class ContextScopeType(StrEnum):
    LOCAL = "local"
    SESSION = "session"
    TASK = "task"
    WORKFLOW = "workflow"
    GLOBAL = "global"


@dataclass(frozen=True, slots=True)
class ContextScope:
    scope_type: ContextScopeType
    boundary_identifier: str
    lifetime_metadata: dict[str, Any] | tuple[tuple[str, Any], ...] = field(default_factory=tuple)
    scope_metadata: dict[str, Any] | tuple[tuple[str, Any], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if isinstance(self.lifetime_metadata, dict):
            object.__setattr__(
                self,
                "lifetime_metadata",
                tuple(sorted(self.lifetime_metadata.items())),
            )
        elif isinstance(self.lifetime_metadata, tuple):
            object.__setattr__(
                self,
                "lifetime_metadata",
                tuple(sorted(self.lifetime_metadata)),
            )
        else:
            raise ValueError("lifetime_metadata must be a dictionary or tuple of key-value pairs")

        if isinstance(self.scope_metadata, dict):
            object.__setattr__(
                self,
                "scope_metadata",
                tuple(sorted(self.scope_metadata.items())),
            )
        elif isinstance(self.scope_metadata, tuple):
            object.__setattr__(
                self,
                "scope_metadata",
                tuple(sorted(self.scope_metadata)),
            )
        else:
            raise ValueError("scope_metadata must be a dictionary or tuple of key-value pairs")

    def to_dict(self) -> dict[str, object]:
        return {
            "scope_type": self.scope_type.value,
            "boundary_identifier": self.boundary_identifier,
            "lifetime_metadata": dict(self.lifetime_metadata),
            "scope_metadata": dict(self.scope_metadata),
        }
