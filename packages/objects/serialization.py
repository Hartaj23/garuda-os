from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from .core import GarudaObject, LifecycleState


class ObjectSerializer:
    """Serialize and deserialize GarudaObject state as deterministic JSON."""

    serialization_version = 1

    @classmethod
    def serialize(cls, obj: GarudaObject) -> dict[str, Any]:
        payload = {
            "serialization_version": cls.serialization_version,
            "schema_version": obj.schema_version,
            "object_version": obj.object_version,
            "object_type": obj.object_type,
            "object_id": str(obj.object_id),
            "metadata": dict(sorted(obj.metadata.values.items())),
            "tags": list(obj.tags),
            "lifecycle_state": obj.lifecycle_state.value,
            "created_by": obj.created_by,
            "updated_by": obj.updated_by,
            "created_at": obj.created_at.isoformat(),
            "updated_at": obj.updated_at.isoformat(),
            "behaviors": dict(sorted(obj.behaviors.items())),
        }
        return payload

    @classmethod
    def serialize_json(cls, obj: GarudaObject) -> str:
        return json.dumps(cls.serialize(obj), sort_keys=True, separators=(",", ":"))

    @classmethod
    def deserialize(cls, payload: dict[str, Any]) -> GarudaObject:
        object_type = payload.get("object_type", "GarudaObject")
        metadata = payload.get("metadata", {}) or {}
        tags = payload.get("tags", []) or []
        lifecycle_state = payload.get("lifecycle_state", "draft")
        created_by = payload.get("created_by")
        updated_by = payload.get("updated_by")
        created_at = payload.get("created_at")
        updated_at = payload.get("updated_at")
        behaviors = payload.get("behaviors", {}) or {}

        obj = GarudaObject(
            object_id=UUID(payload["object_id"]) if payload.get("object_id") else None,
            metadata=dict(metadata),
            tags=list(tags),
            lifecycle_state=LifecycleState(lifecycle_state),
            created_by=created_by,
            updated_by=updated_by,
            created_at=datetime.fromisoformat(created_at) if created_at else None,
            updated_at=datetime.fromisoformat(updated_at) if updated_at else None,
        )
        obj.object_type = object_type
        obj.object_version = payload.get("object_version", 1)
        obj.schema_version = payload.get("schema_version", "1.0")
        for name, value in behaviors.items():
            obj.register_behavior(name, value)
        return obj

    @classmethod
    def deserialize_json(cls, text: str) -> GarudaObject:
        return cls.deserialize(json.loads(text))
