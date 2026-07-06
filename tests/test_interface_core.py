import unittest
from datetime import datetime
from uuid import UUID

from packages.interface import (
    InterfaceFoundation,
    InterfaceFoundationCategory,
    InterfaceFoundationMetadata,
    validate_interface_foundation,
)
from packages.objects import CanonicalObject, LifecycleState, ValidationResult


TIMESTAMP = datetime.fromisoformat("2026-07-06T00:00:00+00:00")


class InterfaceCoreTest(unittest.TestCase):
    def test_package_exports_import_cleanly(self) -> None:
        import packages.interface as interface_pkg

        for symbol in (
            "InterfaceFoundation",
            "InterfaceFoundationCategory",
            "InterfaceFoundationMetadata",
            "validate_interface_foundation",
            "CanonicalInterfaceRequest",
            "CanonicalInterfaceResponse",
            "InterfaceBoundaryModel",
            "InterfaceArtifactLifecycle",
            "CanonicalTranslationContract",
            "normalize_to_canonical_payload",
        ):
            self.assertIn(symbol, interface_pkg.__all__)
            self.assertTrue(hasattr(interface_pkg, symbol))

    def test_interface_foundation_inherits_platform_core_object_behavior(self) -> None:
        foundation = InterfaceFoundation(
            metadata={"owner": "platform"},
            tags=["interface", "alpha"],
            created_by="codex",
        )

        self.assertIsInstance(foundation, CanonicalObject)
        self.assertIsInstance(foundation.object_id, UUID)
        self.assertEqual(foundation.object_type, "InterfaceFoundation")
        self.assertEqual(foundation.metadata.values["owner"], "platform")
        self.assertEqual(foundation.tags, ("interface", "alpha"))
        self.assertEqual(foundation.lifecycle_state, LifecycleState.DRAFT)
        self.assertEqual(foundation.created_by, "codex")

    def test_explicit_object_id_is_preserved(self) -> None:
        object_id = UUID("00000000-0000-0000-0000-000000001001")
        foundation = InterfaceFoundation(object_id=object_id)

        self.assertEqual(foundation.object_id, object_id)
        self.assertEqual(foundation.object_type, "InterfaceFoundation")

    def test_foundation_primitives_are_available(self) -> None:
        metadata = InterfaceFoundationMetadata(values={"domain": "interface"})
        foundation = InterfaceFoundation(
            foundation_category=InterfaceFoundationCategory.CORE,
            foundation_metadata=metadata,
        )

        self.assertEqual(foundation.foundation_category, InterfaceFoundationCategory.CORE)
        self.assertEqual(foundation.foundation_metadata.values, (("domain", "interface"),))

    def test_valid_foundation_passes_platform_validation(self) -> None:
        foundation = InterfaceFoundation()

        result = foundation.validate()

        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_foundation_validation_reports_invalid_category(self) -> None:
        foundation = InterfaceFoundation()
        foundation._foundation_category = "core"

        result = foundation.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "foundation_category")

    def test_foundation_validation_reports_invalid_metadata(self) -> None:
        foundation = InterfaceFoundation()
        foundation._foundation_metadata = {"domain": "interface"}

        result = foundation.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "foundation_metadata")

    def test_validate_interface_foundation_returns_validation_result(self) -> None:
        foundation = InterfaceFoundation()
        foundation._foundation_category = "core"

        result = validate_interface_foundation(foundation)

        self.assertIsInstance(result, ValidationResult)
        self.assertFalse(result.is_valid)

    def test_foundation_lifecycle_transitions_use_existing_platform_rules(self) -> None:
        foundation = InterfaceFoundation()

        foundation.transition_to(LifecycleState.ACTIVE)

        self.assertEqual(foundation.lifecycle_state, LifecycleState.ACTIVE)

    def test_to_dict_returns_deterministic_foundation_payload(self) -> None:
        foundation = InterfaceFoundation(
            object_id=UUID("00000000-0000-0000-0000-000000001002"),
            foundation_metadata=InterfaceFoundationMetadata(values={"z": "last", "a": "first"}),
            metadata={"b": 2, "a": 1},
            tags=["interface"],
            lifecycle_state=LifecycleState.DRAFT,
            created_by="codex",
            updated_by="codex",
            created_at=TIMESTAMP,
            updated_at=TIMESTAMP,
        )

        payload = foundation.to_dict()

        self.assertEqual(payload["object_type"], "InterfaceFoundation")
        self.assertEqual(payload["object_id"], "00000000-0000-0000-0000-000000001002")
        self.assertEqual(payload["foundation_category"], "core")
        self.assertEqual(payload["foundation_metadata"], {"a": "first", "z": "last"})
        self.assertEqual(payload["metadata"], {"a": 1, "b": 2})
        self.assertNotIn("contracts", payload)
        self.assertNotIn("registry", payload)


if __name__ == "__main__":
    unittest.main()
