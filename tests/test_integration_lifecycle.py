import unittest
from datetime import datetime
from uuid import UUID

from packages.integration import (
    IntegrationArtifactLifecycle,
    IntegrationBoundaryDescriptor,
    IntegrationBoundaryExclusivity,
    IntegrationBoundaryModel,
    IntegrationBoundarySide,
    IntegrationLifecycleMetadata,
    IntegrationLifecycleState,
    validate_integration_boundary_exclusivity,
    validate_integration_lifecycle_transition,
)
from packages.objects import CanonicalObject, LifecycleState, ObjectSerializer, ValidationResult


TIMESTAMP = datetime.fromisoformat("2026-07-07T00:00:00+00:00")


def build_boundary_model() -> IntegrationBoundaryModel:
    return IntegrationBoundaryModel(
        object_id=UUID("00000000-0000-0000-0000-000000004001"),
        boundary_identifier="integration-membrane-traversal",
        boundary_side=IntegrationBoundarySide.MEMBRANE_TRAVERSAL,
        exclusivity=IntegrationBoundaryExclusivity(traverses_membrane=True),
        boundary_metadata=IntegrationLifecycleMetadata(values={"scope": "integration"}),
        metadata={"owner": "integration"},
        tags=["integration", "charlie"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_artifact_lifecycle() -> IntegrationArtifactLifecycle:
    boundary = build_boundary_model()
    return IntegrationArtifactLifecycle(
        object_id=UUID("00000000-0000-0000-0000-000000004002"),
        integration_lifecycle_state=IntegrationLifecycleState.ACTIVE,
        boundary_descriptor=boundary.to_descriptor(),
        artifact_reference="artifact:00000000-0000-0000-0000-000000004003",
        lifecycle_metadata=IntegrationLifecycleMetadata(values={"phase": "charlie"}),
        lifecycle_state=LifecycleState.DRAFT,
        metadata={"owner": "integration"},
        tags=["integration", "charlie"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


class IntegrationLifecycleTest(unittest.TestCase):
    def test_lifecycle_artifacts_inherit_platform_core(self) -> None:
        boundary = build_boundary_model()
        lifecycle = build_artifact_lifecycle()

        self.assertIsInstance(boundary, CanonicalObject)
        self.assertIsInstance(lifecycle, CanonicalObject)
        self.assertEqual(boundary.object_type, "IntegrationBoundaryModel")
        self.assertEqual(lifecycle.object_type, "IntegrationArtifactLifecycle")

    def test_canonical_serialization_without_custom_adapters(self) -> None:
        boundary = build_boundary_model()
        lifecycle = build_artifact_lifecycle()

        boundary_core = ObjectSerializer.serialize(boundary)
        lifecycle_core = ObjectSerializer.serialize(lifecycle)

        self.assertEqual(boundary_core["object_type"], "IntegrationBoundaryModel")
        self.assertEqual(lifecycle_core["object_type"], "IntegrationArtifactLifecycle")
        self.assertEqual(
            boundary.to_dict()["boundary_identifier"],
            "integration-membrane-traversal",
        )
        self.assertEqual(
            lifecycle.to_dict()["integration_lifecycle_state"],
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
        import packages.integration.lifecycle.artifact as artifact_module
        import packages.integration.lifecycle.boundary as boundary_module
        import packages.integration.lifecycle.states as states_module
        import packages.integration.lifecycle.transitions as transitions_module

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

    def test_boundary_exclusivity_requires_membrane_traversal(self) -> None:
        boundary = build_boundary_model()
        boundary._exclusivity = IntegrationBoundaryExclusivity(traverses_membrane=False)

        result = boundary.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "exclusivity.traverses_membrane")

    def test_boundary_exclusivity_certification(self) -> None:
        exclusivity = IntegrationBoundaryExclusivity(traverses_membrane=True)

        result = validate_integration_boundary_exclusivity(exclusivity)

        self.assertTrue(result.is_valid)
        self.assertTrue(exclusivity.traverses_membrane)

    def test_lifecycle_states_are_descriptive_metadata_only(self) -> None:
        lifecycle = build_artifact_lifecycle()

        self.assertEqual(lifecycle.integration_lifecycle_state, IntegrationLifecycleState.ACTIVE)
        self.assertEqual(lifecycle.lifecycle_state, LifecycleState.DRAFT)
        self.assertNotIn("transition", dir(lifecycle.integration_lifecycle_state))

    def test_boundary_model_is_declarative_only(self) -> None:
        boundary = build_boundary_model()

        self.assertEqual(boundary.boundary_side, IntegrationBoundarySide.MEMBRANE_TRAVERSAL)
        self.assertNotIn("route", dir(boundary))
        self.assertNotIn("dispatch", dir(boundary))

    def test_artifact_reference_remains_opaque(self) -> None:
        lifecycle = build_artifact_lifecycle()

        self.assertEqual(
            lifecycle.artifact_reference,
            "artifact:00000000-0000-0000-0000-000000004003",
        )
        self.assertNotIn("resolve", dir(lifecycle))

    def test_lifecycle_state_enum_values_are_deterministic_and_serializable(self) -> None:
        metadata = IntegrationLifecycleMetadata(values={"z": "last", "a": "first"})

        self.assertEqual(metadata.to_dict(), {"a": "first", "z": "last"})
        self.assertEqual(IntegrationLifecycleState.ACTIVE.value, "active")

    def test_boundary_descriptor_rejects_empty_identifier(self) -> None:
        boundary = build_boundary_model()
        boundary._boundary_identifier = ""

        result = boundary.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "boundary_identifier")

    def test_artifact_lifecycle_validation_reports_invalid_state(self) -> None:
        lifecycle = build_artifact_lifecycle()
        lifecycle._integration_lifecycle_state = "active"

        result = lifecycle.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "integration_lifecycle_state")

    def test_validate_helpers_return_validation_result(self) -> None:
        boundary = build_boundary_model()
        boundary._boundary_side = "membrane_traversal"

        result = boundary.validate()

        self.assertIsInstance(result, ValidationResult)
        self.assertFalse(result.is_valid)

    def test_lifecycle_transition_validation_allows_permitted_transition(self) -> None:
        result = validate_integration_lifecycle_transition(
            IntegrationLifecycleState.DRAFT,
            IntegrationLifecycleState.ACTIVE,
        )

        self.assertTrue(result.is_valid)

    def test_lifecycle_transition_validation_rejects_invalid_transition(self) -> None:
        result = validate_integration_lifecycle_transition(
            IntegrationLifecycleState.ARCHIVED,
            IntegrationLifecycleState.ACTIVE,
        )

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "invalid_lifecycle_transition")

    def test_lifecycle_to_dict_is_deterministic(self) -> None:
        lifecycle = build_artifact_lifecycle()

        first = lifecycle.to_dict()
        second = lifecycle.to_dict()

        self.assertEqual(first, second)
        self.assertEqual(first["integration_lifecycle_state"], "active")


if __name__ == "__main__":
    unittest.main()
