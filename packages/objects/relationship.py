from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4


class RelationshipType(str, Enum):
    OWNS = "owns"
    CONTAINS = "contains"
    REFERENCES = "references"
    DEPENDS_ON = "depends_on"
    PARENT_OF = "parent_of"
    CHILD_OF = "child_of"
    RELATED_TO = "related_to"


class RelationshipDirection(str, Enum):
    DIRECTED = "directed"
    UNDIRECTED = "undirected"


class RelationshipStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"


@dataclass(slots=True)
class Relationship:
    """Minimal platform-level relationship object."""

    source_object_id: UUID
    target_object_id: UUID
    relationship_type: RelationshipType = RelationshipType.RELATED_TO
    relationship_direction: RelationshipDirection = RelationshipDirection.DIRECTED
    relationship_status: RelationshipStatus = RelationshipStatus.ACTIVE
    metadata: dict[str, Any] = field(default_factory=dict)
    created_by: str | None = None
    updated_by: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    relationship_id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        if self.created_at is None:
            self.created_at = datetime.now(tz=UTC)
        if self.updated_at is None:
            self.updated_at = self.created_at

    def to_dict(self) -> dict[str, Any]:
        return {
            "relationship_id": str(self.relationship_id),
            "source_object_id": str(self.source_object_id),
            "target_object_id": str(self.target_object_id),
            "relationship_type": self.relationship_type.value,
            "relationship_direction": self.relationship_direction.value,
            "relationship_status": self.relationship_status.value,
            "metadata": dict(sorted(self.metadata.items())),
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
