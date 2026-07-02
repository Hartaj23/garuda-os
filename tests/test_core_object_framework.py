import unittest
from uuid import UUID

from packages.objects import CanonicalObject, GarudaObject, LifecycleState


class CoreObjectFrameworkTest(unittest.TestCase):
    def test_default_identity_is_uuid_and_immutable(self) -> None:
        obj = GarudaObject()
        self.assertIsInstance(obj.object_id, UUID)
        with self.assertRaises(AttributeError):
            obj.object_id = UUID(int=1)

    def test_object_type_schema_version_and_object_version_defaults(self) -> None:
        obj = GarudaObject()
        self.assertEqual(obj.object_type, "GarudaObject")
        self.assertEqual(obj.schema_version, "1.0")
        self.assertEqual(obj.object_version, 1)

    def test_metadata_and_tags_are_initialized(self) -> None:
        obj = GarudaObject(metadata={"owner": "ops"}, tags=["alpha", "beta"])
        self.assertEqual(obj.metadata.values["owner"], "ops")
        self.assertEqual(obj.tags, ("alpha", "beta"))

    def test_lifecycle_defaults_to_draft_and_transitions_to_active(self) -> None:
        obj = GarudaObject()
        self.assertEqual(obj.lifecycle_state, LifecycleState.DRAFT)
        obj.transition_to(LifecycleState.ACTIVE)
        self.assertEqual(obj.lifecycle_state, LifecycleState.ACTIVE)

    def test_invalid_lifecycle_transition_raises_value_error(self) -> None:
        obj = GarudaObject()
        with self.assertRaises(ValueError):
            obj.transition_to(LifecycleState.ARCHIVED)

    def test_audit_fields_are_initialised(self) -> None:
        obj = GarudaObject(created_by="alice", updated_by="alice")
        self.assertEqual(obj.created_by, "alice")
        self.assertEqual(obj.updated_by, "alice")
        self.assertIsNotNone(obj.created_at)
        self.assertIsNotNone(obj.updated_at)

    def test_validation_hooks_run(self) -> None:
        calls: list[str] = []

        def hook(obj: GarudaObject) -> None:
            calls.append(obj.object_type)

        obj = GarudaObject()
        obj.register_validation_hook(hook)
        obj.validate()
        self.assertEqual(calls, ["GarudaObject"])

    def test_subclass_inherits_core_behavior(self) -> None:
        class ExampleObject(CanonicalObject):
            pass

        obj = ExampleObject()
        self.assertEqual(obj.object_type, "ExampleObject")
        self.assertEqual(obj.lifecycle_state, LifecycleState.DRAFT)

    def test_behavior_section_is_available(self) -> None:
        obj = GarudaObject()
        obj.register_behavior("inspect", "enabled")
        self.assertEqual(obj.behaviors["inspect"], "enabled")


if __name__ == "__main__":
    unittest.main()
