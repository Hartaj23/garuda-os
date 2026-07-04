from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class ContextSourceType(StrEnum):
    MEMORY = "memory"
    KNOWLEDGE = "knowledge"
    USER_INPUT = "user_input"
    SYSTEM_STATE = "system_state"
    EXTERNAL_REFERENCE = "external_reference"


@dataclass(frozen=True, slots=True)
class ContextSource:
    source_type: ContextSourceType
    source_identifier: str
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))
    source_metadata: dict[str, Any] | tuple[tuple[str, Any], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if isinstance(self.source_metadata, dict):
            object.__setattr__(
                self,
                "source_metadata",
                tuple(sorted(self.source_metadata.items())),
            )
        elif isinstance(self.source_metadata, tuple):
            object.__setattr__(
                self,
                "source_metadata",
                tuple(sorted(self.source_metadata)),
            )
        else:
            raise ValueError("source_metadata must be a dictionary or tuple of key-value pairs")

    def to_dict(self) -> dict[str, object]:
        return {
            "source_type": self.source_type.value,
            "source_identifier": self.source_identifier,
            "created_at": self.created_at.isoformat(),
            "source_metadata": dict(self.source_metadata),
        }
