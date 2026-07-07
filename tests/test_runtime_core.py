import ast
import unittest
from datetime import datetime
from pathlib import Path
from uuid import UUID

from packages.execution import ExecutionType, UniversalExecution
from packages.integration import IntegrationFoundation
from packages.interface import InterfaceFoundation
from packages.runtime import (
    RuntimeFoundation,
    RuntimeFoundationCategory,
    RuntimeFoundationMetadata,
    RuntimeIntegrationDependency,
    RuntimeInterfaceDependency,
    resolve_integration_foundation_type,
    resolve_interface_foundation_type,
    validate_runtime_foundation,
)
from packages.objects import CanonicalObject, LifecycleState, ValidationResult


TIMESTAMP = datetime.fromisoformat("2026-07-07T00:00:00+00:00")
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_PACKAGE_ROOT = REPOSITORY_ROOT / "packages" / "runtime"
FORBIDDEN_COGNITIVE_PREFIXES = (
    "packages.memory",
    "packages.knowledge",
    "packages.context",
    "packages.reasoning",
    "packages.decision",
    "packages.action",
    "packages.execution",
)


class RuntimeCoreTest(unittest.TestCase):
    def test_package_exports_import_cleanly(self) -> None:
        import packages.runtime as runtime_pkg

        for symbol in (
            "RuntimeFoundation",
            "RuntimeFoundationCategory",
            "RuntimeFoundationMetadata",
            "RuntimeIntegrationDependency",
            "RuntimeInterfaceDependency",
            "resolve_integration_foundation_type",
            "resolve_interface_foundation_type",
            "validate_runtime_foundation",
        ):
            self.assertIn(symbol, runtime_pkg.__all__)
            self.assertTrue(hasattr(runtime_pkg, symbol))

    def test_runtime_foundation_inherits_platform_core_object_behavior(self) -> None:
        foundation = RuntimeFoundation(
            metadata={"owner": "platform"},
            tags=["runtime", "alpha"],
            created_by="codex",
        )

        self.assertIsInstance(foundation, CanonicalObject)
        self.assertIsInstance(foundation.object_id, UUID)
        self.assertEqual(foundation.object_type, "RuntimeFoundation")
        self.assertEqual(foundation.metadata.values["owner"], "platform")
        self.assertEqual(foundation.tags, ("runtime", "alpha"))
        self.assertEqual(foundation.lifecycle_state, LifecycleState.DRAFT)
        self.assertEqual(foundation.created_by, "codex")

    def test_explicit_object_id_is_preserved(self) -> None:
        object_id = UUID("00000000-0000-0000-0000-000000003001")
        foundation = RuntimeFoundation(object_id=object_id)

        self.assertEqual(foundation.object_id, object_id)
        self.assertEqual(foundation.object_type, "RuntimeFoundation")

    def test_foundation_primitives_are_available(self) -> None:
        metadata = RuntimeFoundationMetadata(values={"domain": "runtime"})
        foundation = RuntimeFoundation(
            foundation_category=RuntimeFoundationCategory.CORE,
            foundation_metadata=metadata,
        )

        self.assertEqual(foundation.foundation_category, RuntimeFoundationCategory.CORE)
        self.assertEqual(foundation.foundation_metadata.values, (("domain", "runtime"),))

    def test_valid_foundation_passes_platform_validation(self) -> None:
        foundation = RuntimeFoundation()

        result = foundation.validate()

        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_foundation_validation_reports_invalid_category(self) -> None:
        foundation = RuntimeFoundation()
        foundation._foundation_category = "core"

        result = foundation.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "foundation_category")

    def test_foundation_validation_reports_invalid_metadata(self) -> None:
        foundation = RuntimeFoundation()
        foundation._foundation_metadata = {"domain": "runtime"}

        result = foundation.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "foundation_metadata")

    def test_validate_runtime_foundation_returns_validation_result(self) -> None:
        foundation = RuntimeFoundation()
        foundation._foundation_category = "core"

        result = validate_runtime_foundation(foundation)

        self.assertIsInstance(result, ValidationResult)
        self.assertFalse(result.is_valid)

    def test_foundation_lifecycle_transitions_use_existing_platform_rules(self) -> None:
        foundation = RuntimeFoundation()

        foundation.transition_to(LifecycleState.ACTIVE)

        self.assertEqual(foundation.lifecycle_state, LifecycleState.ACTIVE)

    def test_to_dict_returns_deterministic_foundation_payload(self) -> None:
        foundation = RuntimeFoundation(
            object_id=UUID("00000000-0000-0000-0000-000000003002"),
            foundation_metadata=RuntimeFoundationMetadata(values={"z": "last", "a": "first"}),
            metadata={"b": 2, "a": 1},
            tags=["runtime"],
            lifecycle_state=LifecycleState.DRAFT,
            created_by="codex",
            updated_by="codex",
            created_at=TIMESTAMP,
            updated_at=TIMESTAMP,
        )

        payload = foundation.to_dict()

        self.assertEqual(payload["object_type"], "RuntimeFoundation")
        self.assertEqual(payload["object_id"], "00000000-0000-0000-0000-000000003002")
        self.assertEqual(payload["foundation_category"], "core")
        self.assertEqual(payload["foundation_metadata"], {"a": "first", "z": "last"})
        self.assertEqual(payload["metadata"], {"a": 1, "b": 2})
        self.assertNotIn("contracts", payload)
        self.assertNotIn("registry", payload)

    def test_interface_foundation_coexistence(self) -> None:
        interface_foundation = InterfaceFoundation(
            object_id=UUID("00000000-0000-0000-0000-000000001001"),
        )
        dependency = RuntimeInterfaceDependency()

        self.assertTrue(dependency.is_compatible(interface_foundation))
        self.assertEqual(resolve_interface_foundation_type(), InterfaceFoundation)

    def test_integration_foundation_coexistence(self) -> None:
        integration_foundation = IntegrationFoundation(
            object_id=UUID("00000000-0000-0000-0000-000000002001"),
        )
        dependency = RuntimeIntegrationDependency()

        self.assertTrue(dependency.is_compatible(integration_foundation))
        self.assertEqual(resolve_integration_foundation_type(), IntegrationFoundation)

    def test_stack_foundation_coexistence(self) -> None:
        interface_foundation = InterfaceFoundation(
            object_id=UUID("00000000-0000-0000-0000-000000001002"),
        )
        integration_foundation = IntegrationFoundation(
            object_id=UUID("00000000-0000-0000-0000-000000002002"),
        )
        runtime_foundation = RuntimeFoundation(
            object_id=UUID("00000000-0000-0000-0000-000000003003"),
        )

        self.assertIsInstance(interface_foundation, CanonicalObject)
        self.assertIsInstance(integration_foundation, CanonicalObject)
        self.assertIsInstance(runtime_foundation, CanonicalObject)
        self.assertEqual(interface_foundation.object_type, "InterfaceFoundation")
        self.assertEqual(integration_foundation.object_type, "IntegrationFoundation")
        self.assertEqual(runtime_foundation.object_type, "RuntimeFoundation")

    def test_runtime_foundation_is_not_universal_execution(self) -> None:
        runtime_foundation = RuntimeFoundation()
        execution = UniversalExecution(execution_type=ExecutionType.ACTION)

        self.assertNotIsInstance(runtime_foundation, UniversalExecution)
        self.assertNotEqual(runtime_foundation.object_type, execution.object_type)
        self.assertEqual(runtime_foundation.object_type, "RuntimeFoundation")
        self.assertEqual(execution.object_type, "UniversalExecution")

    def test_runtime_package_does_not_import_cognitive_foundations(self) -> None:
        for path in RUNTIME_PACKAGE_ROOT.rglob("*.py"):
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
