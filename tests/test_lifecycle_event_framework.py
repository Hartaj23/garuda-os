import unittest
from datetime import datetime
from uuid import UUID

from packages.objects import (
    LifecycleEvent,
    LifecycleEventType,
)


class LifecycleEventFrameworkTest(unittest.TestCase):
    def test_lifecycle_event_uses_required_fields_and_defaults(self) -> None:
        event = LifecycleEvent(
            related_object_id=UUID("00000000-0000-0000-0000-000000000001"),
            event_type=LifecycleEventType.OBJECT_CREATED,
        )
        self.assertIsNotNone(event.event_id)
        self.assertEqual(event.related_object_id, UUID("00000000-0000-0000-0000-000000000001"))
        self.assertEqual(event.event_type, LifecycleEventType.OBJECT_CREATED)
        self.assertIsNotNone(event.event_timestamp)
        self.assertEqual(event.event_version, 1)
        self.assertEqual(event.event_actor, None)
        self.assertEqual(event.event_metadata, {})

    def test_standard_lifecycle_event_types_exist(self) -> None:
        expected = {
            "object_created",
            "object_updated",
            "object_activated",
            "object_suspended",
            "object_archived",
            "object_deleted",
            "validation_failed",
            "relationship_added",
            "relationship_removed",
            "behavior_changed",
            "version_changed",
        }
        actual = {item.value for item in LifecycleEventType}
        self.assertEqual(actual, expected)

    def test_validation_rejects_missing_required_fields(self) -> None:
        with self.assertRaises(ValueError):
            LifecycleEvent(event_type=LifecycleEventType.OBJECT_CREATED)

        with self.assertRaises(ValueError):
            LifecycleEvent(related_object_id=UUID("00000000-0000-0000-0000-000000000001"))

    def test_deterministic_payload_representation(self) -> None:
        created = datetime.fromisoformat("2024-01-01T00:00:00+00:00")
        event = LifecycleEvent(
            event_id=UUID("00000000-0000-0000-0000-000000000010"),
            related_object_id=UUID("00000000-0000-0000-0000-000000000001"),
            event_type=LifecycleEventType.OBJECT_UPDATED,
            event_timestamp=created,
            event_actor="alice",
            event_metadata={"reason": "revision", "source": "cli"},
            event_version=2,
        )
        payload = event.to_dict()
        self.assertEqual(payload["event_id"], "00000000-0000-0000-0000-000000000010")
        self.assertEqual(payload["related_object_id"], "00000000-0000-0000-0000-000000000001")
        self.assertEqual(payload["event_type"], "object_updated")
        self.assertEqual(payload["event_timestamp"], created.isoformat())
        self.assertEqual(payload["event_actor"], "alice")
        self.assertEqual(payload["event_metadata"], {"reason": "revision", "source": "cli"})
        self.assertEqual(payload["event_version"], 2)

    def test_payload_metadata_is_sorted_for_determinism(self) -> None:
        event = LifecycleEvent(
            related_object_id=UUID("00000000-0000-0000-0000-000000000001"),
            event_type=LifecycleEventType.OBJECT_CREATED,
            event_metadata={"zeta": 1, "alpha": 2},
        )
        payload = event.to_dict()
        self.assertEqual(payload["event_metadata"], {"alpha": 2, "zeta": 1})


if __name__ == "__main__":
    unittest.main()
