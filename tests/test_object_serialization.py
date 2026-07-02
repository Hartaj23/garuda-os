import json
import unittest
from datetime import datetime
from uuid import UUID

from packages.objects import GarudaObject, LifecycleState, ObjectSerializer


class ObjectSerializationTest(unittest.TestCase):
    def test_serializes_object_state_with_header(self) -> None:
        obj = GarudaObject(
            metadata={"owner": "ops"},
            tags=["alpha", "beta"],
            lifecycle_state=LifecycleState.ACTIVE,
            created_by="alice",
            updated_by="alice",
        )
        payload = ObjectSerializer.serialize(obj)
        self.assertIn("serialization_version", payload)
        self.assertIn("schema_version", payload)
        self.assertIn("object_version", payload)
        self.assertIn("object_type", payload)
        self.assertEqual(payload["object_type"], "GarudaObject")

    def test_deterministic_output_for_equivalent_objects(self) -> None:
        first = GarudaObject(
            object_id=UUID("00000000-0000-0000-0000-000000000001"),
            metadata={"owner": "ops"},
            tags=["alpha", "beta"],
            created_at=datetime.fromisoformat("2024-01-01T00:00:00+00:00"),
            updated_at=datetime.fromisoformat("2024-01-01T00:00:00+00:00"),
        )
        second = GarudaObject(
            object_id=UUID("00000000-0000-0000-0000-000000000001"),
            metadata={"owner": "ops"},
            tags=["alpha", "beta"],
            created_at=datetime.fromisoformat("2024-01-01T00:00:00+00:00"),
            updated_at=datetime.fromisoformat("2024-01-01T00:00:00+00:00"),
        )
        self.assertEqual(ObjectSerializer.serialize(first), ObjectSerializer.serialize(second))

    def test_deserializer_ignores_unknown_fields(self) -> None:
        payload = {
            "serialization_version": 1,
            "schema_version": "1.0",
            "object_version": 1,
            "object_type": "GarudaObject",
            "object_id": "00000000-0000-0000-0000-000000000001",
            "metadata": {"owner": "ops"},
            "tags": ["alpha"],
            "lifecycle_state": "active",
            "created_by": "alice",
            "updated_by": "alice",
            "created_at": "2024-01-01T00:00:00+00:00",
            "updated_at": "2024-01-01T00:00:00+00:00",
            "behaviors": {"inspect": "enabled"},
            "unknown_field": "ignored",
        }
        obj = ObjectSerializer.deserialize(payload)
        self.assertEqual(obj.metadata.values["owner"], "ops")
        self.assertEqual(obj.lifecycle_state, LifecycleState.ACTIVE)
        self.assertEqual(obj.behaviors["inspect"], "enabled")

    def test_round_trip_preserves_core_fields(self) -> None:
        obj = GarudaObject(
            metadata={"owner": "ops"},
            tags=["alpha", "beta"],
            lifecycle_state=LifecycleState.ACTIVE,
            created_by="alice",
            updated_by="alice",
        )
        payload = ObjectSerializer.serialize(obj)
        restored = ObjectSerializer.deserialize(payload)
        self.assertEqual(restored.object_id, obj.object_id)
        self.assertEqual(restored.object_type, obj.object_type)
        self.assertEqual(restored.schema_version, obj.schema_version)
        self.assertEqual(restored.object_version, obj.object_version)
        self.assertEqual(restored.metadata.values, obj.metadata.values)
        self.assertEqual(restored.tags, obj.tags)
        self.assertEqual(restored.lifecycle_state, obj.lifecycle_state)
        self.assertEqual(restored.created_by, obj.created_by)
        self.assertEqual(restored.updated_by, obj.updated_by)
        self.assertEqual(restored.behaviors, obj.behaviors)


if __name__ == "__main__":
    unittest.main()
