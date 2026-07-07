import unittest
from datetime import datetime
from uuid import UUID

from packages.objects import CanonicalObject, LifecycleState, ObjectSerializer, ValidationResult
from packages.runtime import (
    RuntimeArtifactLifecycle,
    RuntimeBoundaryDescriptor,
    RuntimeBoundaryExclusivity,
    RuntimeBoundaryModel,
    RuntimeBoundarySide,
    RuntimeLifecycleMetadata,
    RuntimeLifecycleState,
    validate_runtime_boundary_exclusivity,
    validate_runtime_lifecycle_transition,
)


TIMESTAMP = datetime.fromisoformat("2026-07-07T00:00:00+00:00")


def build_boundary_model() -> RuntimeBoundaryModel:
    return RuntimeBoundaryModel(
        object_id=UUID("00000000-0000-0000-0000-000000005001"),
        boundary_identifier="runtime-stack-traversal",
        boundary_side=RuntimeBoundarySide.STACK_TRAVERSAL,
        exclusivity=RuntimeBoundaryExclusivity(
            traverses_integration_foundation=True,
            traverses_interface_foundation=True,
        ),
        boundary_metadata=RuntimeLifecycleMetadata(values={"scope": "runtime"}),
        metadata={"owner": "runtime"},
        tags=["runtime", "charlie"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_artifact_lifecycle() -> RuntimeArtifactLifecycle:
    boundary = build_boundary_model()
    return RuntimeArtifactLifecycle(
        object_id=UUID("00000000-0000-0000-0000-000000005002"),
        runtime_lifecycle_state=RuntimeLifecycleState.ACTIVE,
        boundary_descriptor=boundary.to_descriptor(),
        artifact_reference="artifact:00000000-0000-0000-0000-000000005003",
        lifecycle_metadata=RuntimeLifecycleMetadata(values={"phase": "charlie"}),
        lifecycle_state=LifecycleState.DRAFT,
        metadata={"owner": "runtime"},
        tags=["runtime", "charlie"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


class RuntimeLifecycleTest(unittest.TestCase):
    def test_package_exports_import_cleanly(self) -> None:
        import packages.runtime as runtime_pkg

        for symbol in (
            "RuntimeArtifactLifecycle",
            "RuntimeBoundaryModel",
            "RuntimeBoundarySide",
            "RuntimeLifecycleState",
            "validate_runtime_lifecycle_transition",
        ):
            self.assertIn(symbol, runtime_pkg.__all__)
            self.assertTrue(hasattr(runtime_pkg, symbol))

    def test_lifecycle_artifacts_inherit_platform_core(self) -> None:
        boundary = build_boundary_model()
        lifecycle = build_artifact_lifecycle()

        self.assertIsInstance(boundary, CanonicalObject)
        self.assertIsInstance(lifecycle, CanonicalObject)
        self.assertEqual(boundary.object_type, "RuntimeBoundaryModel")
        self.assertEqual(lifecycle.object_type, "RuntimeArtifactLifecycle")

    def test_canonical_serialization_without_custom_adapters(self) -> None:
        boundary = build_boundary_model()
        lifecycle = build_artifact_lifecycle()

        boundary_core = ObjectSerializer.serialize(boundary)
        lifecycle_core = ObjectSerializer.serialize(lifecycle)

        self.assertEqual(boundary_core["object_type"], "RuntimeBoundaryModel")
        self.assertEqual(lifecycle_core["object_type"], "RuntimeArtifactLifecycle")
        self.assertEqual(
            boundary.to_dict()["boundary_identifier"],
            "runtime-stack-traversal",
        )
        self.assertEqual(
            lifecycle.to_dict()["runtime_lifecycle_state"],
            "active",
        )

    def test_platform_validation_passes(self) -> None:
        self.assertTrue(build_boundary_model().validate().is_valid)
        self.assertTrue(build_artifact_lifecycle().validate().is_valid)

    def test_identity_preserved_through_serialization_cycle(self) -> None:
        boundary = build_boundary_model()
        lifecycle = build_artifact_lifecycle()

        self.assertEqual(boundary.to_dict()["object_id"], str(boundary.object_id))
        self.assertEqual(
            ObjectSerializer.serialize(lifecycle)["object_id"],
            str(lifecycle.object_id),
        )

    def test_no_cognitive_foundation_imports_in_lifecycle_modules(self) -> None:
        import packages.runtime.lifecycle.artifact as artifact_module
        import packages.runtime.lifecycle.boundary as boundary_module
        import packages.runtime.lifecycle.states as states_module
        import packages.runtime.lifecycle.transitions as transitions_module

        forbidden_prefixes = (
            "packages.memory",
            "packages.knowledge",
            "packages.context",
            "packages.reasoning",
            "packages.decision",
            "packages.action",
            "packages.execution",
        )

        for module in (states_module, transitions_module, boundary_module, artifact_module):
            with open(module.__file__, encoding="utf-8") as module_file:
                source = module_file.read()
            for prefix in forbidden_prefixes:
                self.assertNotIn(prefix, source)

    def test_boundary_exclusivity_requires_stack_traversal(self) -> None:
        boundary = build_boundary_model()
        boundary._exclusivity = RuntimeBoundaryExclusivity(
            traverses_integration_foundation=False,
            traverses_interface_foundation=True,
        )

        result = boundary.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(
            result.errors[0].field,
            "exclusivity.traverses_integration_foundation",
        )

    def test_boundary_exclusivity_requires_interface_foundation_traversal(self) -> None:
        boundary = build_boundary_model()
        boundary._exclusivity = RuntimeBoundaryExclusivity(
            traverses_integration_foundation=True,
            traverses_interface_foundation=False,
        )

        result = boundary.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(
            result.errors[0].field,
            "exclusivity.traverses_interface_foundation",
        )

    def test_boundary_exclusivity_certification(self) -> None:
        exclusivity = RuntimeBoundaryExclusivity(
            traverses_integration_foundation=True,
            traverses_interface_foundation=True,
        )

        result = validate_runtime_boundary_exclusivity(exclusivity)

        self.assertTrue(result.is_valid)
        self.assertTrue(exclusivity.traverses_integration_foundation)
        self.assertTrue(exclusivity.traverses_interface_foundation)

    def test_lifecycle_states_are_descriptive_metadata_only(self) -> None:
        lifecycle = build_artifact_lifecycle()

        self.assertEqual(lifecycle.runtime_lifecycle_state, RuntimeLifecycleState.ACTIVE)
        self.assertEqual(lifecycle.lifecycle_state, LifecycleState.DRAFT)
        self.assertNotIn("transition", dir(lifecycle.runtime_lifecycle_state))

    def test_boundary_model_is_declarative_only(self) -> None:
        boundary = build_boundary_model()

        self.assertEqual(boundary.boundary_side, RuntimeBoundarySide.STACK_TRAVERSAL)
        self.assertNotIn("route", dir(boundary))
        self.assertNotIn("dispatch", dir(boundary))
        self.assertNotIn("schedule", dir(boundary))

    def test_artifact_reference_remains_opaque(self) -> None:
        lifecycle = build_artifact_lifecycle()

        self.assertEqual(
            lifecycle.artifact_reference,
            "artifact:00000000-0000-0000-0000-000000005003",
        )
        self.assertNotIn("resolve", dir(lifecycle))

    def test_lifecycle_state_enum_values_are_deterministic_and_serializable(self) -> None:
        metadata = RuntimeLifecycleMetadata(values={"z": "last", "a": "first"})

        self.assertEqual(metadata.to_dict(), {"a": "first", "z": "last"})
        self.assertEqual(RuntimeLifecycleState.ACTIVE.value, "active")

    def test_boundary_descriptor_rejects_empty_identifier(self) -> None:
        boundary = build_boundary_model()
        boundary._boundary_identifier = ""

        result = boundary.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "boundary_identifier")

    def test_artifact_lifecycle_validation_reports_invalid_state(self) -> None:
        lifecycle = build_artifact_lifecycle()
        lifecycle._runtime_lifecycle_state = "active"

        result = lifecycle.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "runtime_lifecycle_state")

    def test_validate_helpers_return_validation_result(self) -> None:
        boundary = build_boundary_model()
        boundary._boundary_side = "stack_traversal"

        result = boundary.validate()

        self.assertIsInstance(result, ValidationResult)
        self.assertFalse(result.is_valid)

    def test_lifecycle_transition_validation_allows_permitted_transition(self) -> None:
        result = validate_runtime_lifecycle_transition(
            RuntimeLifecycleState.DRAFT,
            RuntimeLifecycleState.ACTIVE,
        )

        self.assertTrue(result.is_valid)

    def test_lifecycle_transition_validation_rejects_invalid_transition(self) -> None:
        result = validate_runtime_lifecycle_transition(
            RuntimeLifecycleState.ARCHIVED,
            RuntimeLifecycleState.ACTIVE,
        )

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "invalid_lifecycle_transition")

    def test_lifecycle_to_dict_is_deterministic(self) -> None:
        lifecycle = build_artifact_lifecycle()

        first = lifecycle.to_dict()
        second = lifecycle.to_dict()

        self.assertEqual(first, second)
        self.assertEqual(first["runtime_lifecycle_state"], "active")
        self.assertTrue(
            first["boundary_descriptor"]["exclusivity"]["traverses_integration_foundation"]
        )
        self.assertTrue(
            first["boundary_descriptor"]["exclusivity"]["traverses_interface_foundation"]
        )


if __name__ == "__main__":
    unittest.main()
