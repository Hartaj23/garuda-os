import ast
import unittest
from datetime import datetime
from pathlib import Path
from uuid import UUID

from packages.integration import (
    IntegrationFoundation,
    IntegrationFoundationCategory,
    IntegrationFoundationMetadata,
    IntegrationInterfaceDependency,
    resolve_interface_foundation_type,
    validate_integration_foundation,
)
from packages.interface import InterfaceFoundation
from packages.objects import CanonicalObject, LifecycleState, ValidationResult


TIMESTAMP = datetime.fromisoformat("2026-07-07T00:00:00+00:00")
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
INTEGRATION_PACKAGE_ROOT = REPOSITORY_ROOT / "packages" / "integration"
FORBIDDEN_COGNITIVE_PREFIXES = (
    "packages.memory",
    "packages.knowledge",
    "packages.context",
    "packages.reasoning",
    "packages.decision",
    "packages.action",
    "packages.execution",
)


class IntegrationCoreTest(unittest.TestCase):
    def test_package_exports_import_cleanly(self) -> None:
        import packages.integration as integration_pkg

        for symbol in (
            "IntegrationFoundation",
            "IntegrationFoundationCategory",
            "IntegrationFoundationMetadata",
            "IntegrationInterfaceDependency",
            "resolve_interface_foundation_type",
            "validate_integration_foundation",
        ):
            self.assertIn(symbol, integration_pkg.__all__)
            self.assertTrue(hasattr(integration_pkg, symbol))

    def test_integration_foundation_inherits_platform_core_object_behavior(self) -> None:
        foundation = IntegrationFoundation(
            metadata={"owner": "platform"},
            tags=["integration", "alpha"],
            created_by="codex",
        )

        self.assertIsInstance(foundation, CanonicalObject)
        self.assertIsInstance(foundation.object_id, UUID)
        self.assertEqual(foundation.object_type, "IntegrationFoundation")
        self.assertEqual(foundation.metadata.values["owner"], "platform")
        self.assertEqual(foundation.tags, ("integration", "alpha"))
        self.assertEqual(foundation.lifecycle_state, LifecycleState.DRAFT)
        self.assertEqual(foundation.created_by, "codex")

    def test_explicit_object_id_is_preserved(self) -> None:
        object_id = UUID("00000000-0000-0000-0000-000000002001")
        foundation = IntegrationFoundation(object_id=object_id)

        self.assertEqual(foundation.object_id, object_id)
        self.assertEqual(foundation.object_type, "IntegrationFoundation")

    def test_foundation_primitives_are_available(self) -> None:
        metadata = IntegrationFoundationMetadata(values={"domain": "integration"})
        foundation = IntegrationFoundation(
            foundation_category=IntegrationFoundationCategory.CORE,
            foundation_metadata=metadata,
        )

        self.assertEqual(foundation.foundation_category, IntegrationFoundationCategory.CORE)
        self.assertEqual(foundation.foundation_metadata.values, (("domain", "integration"),))

    def test_valid_foundation_passes_platform_validation(self) -> None:
        foundation = IntegrationFoundation()

        result = foundation.validate()

        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_foundation_validation_reports_invalid_category(self) -> None:
        foundation = IntegrationFoundation()
        foundation._foundation_category = "core"

        result = foundation.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "foundation_category")

    def test_foundation_validation_reports_invalid_metadata(self) -> None:
        foundation = IntegrationFoundation()
        foundation._foundation_metadata = {"domain": "integration"}

        result = foundation.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "foundation_metadata")

    def test_validate_integration_foundation_returns_validation_result(self) -> None:
        foundation = IntegrationFoundation()
        foundation._foundation_category = "core"

        result = validate_integration_foundation(foundation)

        self.assertIsInstance(result, ValidationResult)
        self.assertFalse(result.is_valid)

    def test_foundation_lifecycle_transitions_use_existing_platform_rules(self) -> None:
        foundation = IntegrationFoundation()

        foundation.transition_to(LifecycleState.ACTIVE)

        self.assertEqual(foundation.lifecycle_state, LifecycleState.ACTIVE)

    def test_to_dict_returns_deterministic_foundation_payload(self) -> None:
        foundation = IntegrationFoundation(
            object_id=UUID("00000000-0000-0000-0000-000000002002"),
            foundation_metadata=IntegrationFoundationMetadata(values={"z": "last", "a": "first"}),
            metadata={"b": 2, "a": 1},
            tags=["integration"],
            lifecycle_state=LifecycleState.DRAFT,
            created_by="codex",
            updated_by="codex",
            created_at=TIMESTAMP,
            updated_at=TIMESTAMP,
        )

        payload = foundation.to_dict()

        self.assertEqual(payload["object_type"], "IntegrationFoundation")
        self.assertEqual(payload["object_id"], "00000000-0000-0000-0000-000000002002")
        self.assertEqual(payload["foundation_category"], "core")
        self.assertEqual(payload["foundation_metadata"], {"a": "first", "z": "last"})
        self.assertEqual(payload["metadata"], {"a": 1, "b": 2})
        self.assertNotIn("contracts", payload)
        self.assertNotIn("registry", payload)

    def test_interface_foundation_coexistence(self) -> None:
        interface_foundation = InterfaceFoundation(
            object_id=UUID("00000000-0000-0000-0000-000000001001"),
        )
        integration_foundation = IntegrationFoundation(
            object_id=UUID("00000000-0000-0000-0000-000000002003"),
        )
        dependency = IntegrationInterfaceDependency()

        self.assertTrue(dependency.is_compatible(interface_foundation))
        self.assertEqual(resolve_interface_foundation_type(), InterfaceFoundation)
        self.assertNotEqual(interface_foundation.object_type, integration_foundation.object_type)
        self.assertIsInstance(interface_foundation, CanonicalObject)
        self.assertIsInstance(integration_foundation, CanonicalObject)

    def test_integration_package_does_not_import_cognitive_foundations(self) -> None:
        for path in INTEGRATION_PACKAGE_ROOT.rglob("*.py"):
            module_path = path.relative_to(REPOSITORY_ROOT).with_suffix("")
            module_name = ".".join(module_path.parts)
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self.assertFalse(
                            alias.name.startswith(FORBIDDEN_COGNITIVE_PREFIXES),
                            msg=f"{module_name} imports forbidden module {alias.name}",
                        )
                elif isinstance(node, ast.ImportFrom) and node.module is not None:
                    self.assertFalse(
                        node.module.startswith(FORBIDDEN_COGNITIVE_PREFIXES),
                        msg=f"{module_name} imports forbidden module {node.module}",
                    )


if __name__ == "__main__":
    unittest.main()
