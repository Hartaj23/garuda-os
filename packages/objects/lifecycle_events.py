from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4


class LifecycleEventType(str, Enum):
    OBJECT_CREATED = "object_created"
    OBJECT_UPDATED = "object_updated"
    OBJECT_ACTIVATED = "object_activated"
    OBJECT_SUSPENDED = "object_suspended"
    OBJECT_ARCHIVED = "object_archived"
    OBJECT_DELETED = "object_deleted"
    VALIDATION_FAILED = "validation_failed"
    RELATIONSHIP_ADDED = "relationship_added"
    RELATIONSHIP_REMOVED = "relationship_removed"
    BEHAVIOR_CHANGED = "behavior_changed"
    VERSION_CHANGED = "version_changed"


@dataclass(slots=True)
class LifecycleEvent:
    """Minimal lifecycle event definition for Universal Objects."""

    related_object_id: UUID | None = None
    event_type: LifecycleEventType | None = None
    event_timestamp: datetime | None = None
    event_actor: str | None = None
    event_metadata: dict[str, Any] = field(default_factory=dict)
    event_version: int = 1
    event_id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        if self.related_object_id is None:
            raise ValueError("related_object_id is required")
        if self.event_type is None:
            raise ValueError("event_type is required")
        if self.event_timestamp is None:
            self.event_timestamp = datetime.now(tz=UTC)
        if not isinstance(self.event_metadata, dict):
            raise ValueError("event_metadata must be a dictionary")
        if self.event_version < 1:
            raise ValueError("event_version must be at least 1")

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": str(self.event_id),
            "related_object_id": str(self.related_object_id),
            "event_type": self.event_type.value,
            "event_timestamp": self.event_timestamp.isoformat(),
            "event_actor": self.event_actor,
            "event_metadata": dict(sorted(self.event_metadata.items())),
            "event_version": self.event_version,
        }
