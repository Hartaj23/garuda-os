import unittest
from datetime import datetime
from uuid import UUID

from packages.interface import (
    InterfaceArtifactLifecycle,
    InterfaceBoundaryDescriptor,
    InterfaceBoundaryExclusivity,
    InterfaceBoundaryModel,
    InterfaceBoundarySide,
    InterfaceLifecycleMetadata,
    InterfaceLifecycleState,
    validate_interface_boundary_exclusivity,
)
from packages.objects import CanonicalObject, LifecycleState, ObjectSerializer, ValidationResult


TIMESTAMP = datetime.fromisoformat("2026-07-06T00:00:00+00:00")


def build_boundary_model() -> InterfaceBoundaryModel:
    return InterfaceBoundaryModel(
        object_id=UUID("00000000-0000-0000-0000-000000003001"),
        boundary_identifier="constitutional-membrane",
        boundary_side=InterfaceBoundarySide.MEMBRANE,
        exclusivity=InterfaceBoundaryExclusivity(single_membrane=True),
        boundary_metadata=InterfaceLifecycleMetadata(values={"scope": "phase-ii"}),
        metadata={"owner": "interface"},
        tags=["interface", "charlie"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_artifact_lifecycle() -> InterfaceArtifactLifecycle:
    boundary = build_boundary_model()
    return InterfaceArtifactLifecycle(
        object_id=UUID("00000000-0000-0000-0000-000000003002"),
        interface_lifecycle_state=InterfaceLifecycleState.ACTIVE,
        boundary_descriptor=boundary.to_descriptor(),
        artifact_reference="artifact:00000000-0000-0000-0000-000000003003",
        lifecycle_metadata=InterfaceLifecycleMetadata(values={"phase": "charlie"}),
        lifecycle_state=LifecycleState.DRAFT,
        metadata={"owner": "interface"},
        tags=["interface", "charlie"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


class InterfaceLifecycleTest(unittest.TestCase):
    def test_golf_scenario_1_lifecycle_artifacts_inherit_platform_core(self) -> None:
        boundary = build_boundary_model()
        lifecycle = build_artifact_lifecycle()

        self.assertIsInstance(boundary, CanonicalObject)
        self.assertIsInstance(lifecycle, CanonicalObject)
        self.assertEqual(boundary.object_type, "InterfaceBoundaryModel")
        self.assertEqual(lifecycle.object_type, "InterfaceArtifactLifecycle")

    def test_golf_scenario_2_canonical_serialization_without_custom_adapters(self) -> None:
        boundary = build_boundary_model()
        lifecycle = build_artifact_lifecycle()

        boundary_core = ObjectSerializer.serialize(boundary)
        lifecycle_core = ObjectSerializer.serialize(lifecycle)

        self.assertEqual(boundary_core["object_type"], "InterfaceBoundaryModel")
        self.assertEqual(lifecycle_core["object_type"], "InterfaceArtifactLifecycle")
        self.assertEqual(
            boundary.to_dict()["boundary_identifier"],
            "constitutional-membrane",
        )
        self.assertEqual(
            lifecycle.to_dict()["interface_lifecycle_state"],
            "active",
        )

    def test_golf_scenario_3_platform_validation_passes(self) -> None:
        self.assertTrue(build_boundary_model().validate().is_valid)
        self.assertTrue(build_artifact_lifecycle().validate().is_valid)

    def test_golf_scenario_4_identity_preserved_through_serialization_cycle(self) -> None:
        boundary = build_boundary_model()
        lifecycle = build_artifact_lifecycle()

        self.assertEqual(
            boundary.to_dict()["object_id"],
            str(boundary.object_id),
        )
        self.assertEqual(
            ObjectSerializer.serialize(lifecycle)["object_id"],
            str(lifecycle.object_id),
        )

    def test_golf_scenario_5_no_cognitive_foundation_imports_in_lifecycle_modules(self) -> None:
        import packages.interface.lifecycle.artifact as artifact_module
        import packages.interface.lifecycle.boundary as boundary_module
        import packages.interface.lifecycle.states as states_module

        forbidden_prefixes = (
            "packages.memory",
            "packages.knowledge",
            "packages.context",
            "packages.reasoning",
            "packages.decision",
            "packages.action",
            "packages.execution",
        )

        for module in (states_module, boundary_module, artifact_module):
            with open(module.__file__, encoding="utf-8") as module_file:
                source = module_file.read()
            for prefix in forbidden_prefixes:
                self.assertNotIn(prefix, source)

    def test_golf_scenario_6_boundary_exclusivity_requires_single_membrane(self) -> None:
        boundary = build_boundary_model()
        boundary._exclusivity = InterfaceBoundaryExclusivity(single_membrane=False)

        result = boundary.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "exclusivity.single_membrane")

    def test_golf_scenario_6_boundary_exclusivity_certification(self) -> None:
        exclusivity = InterfaceBoundaryExclusivity(single_membrane=True)

        result = validate_interface_boundary_exclusivity(exclusivity)

        self.assertTrue(result.is_valid)
        self.assertTrue(exclusivity.single_membrane)

    def test_lifecycle_states_are_descriptive_metadata_only(self) -> None:
        lifecycle = build_artifact_lifecycle()

        self.assertEqual(lifecycle.interface_lifecycle_state, InterfaceLifecycleState.ACTIVE)
        self.assertEqual(lifecycle.lifecycle_state, LifecycleState.DRAFT)
        self.assertNotIn("transition", dir(lifecycle.interface_lifecycle_state))

    def test_boundary_model_is_declarative_only(self) -> None:
        boundary = build_boundary_model()

        self.assertEqual(boundary.boundary_side, InterfaceBoundarySide.MEMBRANE)
        self.assertNotIn("route", dir(boundary))
        self.assertNotIn("dispatch", dir(boundary))

    def test_artifact_reference_remains_opaque(self) -> None:
        lifecycle = build_artifact_lifecycle()

        self.assertEqual(
            lifecycle.artifact_reference,
            "artifact:00000000-0000-0000-0000-000000003003",
        )
        self.assertNotIn("resolve", dir(lifecycle))

    def test_lifecycle_state_enum_values_are_deterministic_and_serializable(self) -> None:
        metadata = InterfaceLifecycleMetadata(values={"z": "last", "a": "first"})

        self.assertEqual(metadata.to_dict(), {"a": "first", "z": "last"})
        self.assertEqual(InterfaceLifecycleState.ACTIVE.value, "active")

    def test_boundary_descriptor_rejects_empty_identifier(self) -> None:
        boundary = build_boundary_model()
        boundary._boundary_identifier = ""

        result = boundary.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "boundary_identifier")

    def test_artifact_lifecycle_validation_reports_invalid_state(self) -> None:
        lifecycle = build_artifact_lifecycle()
        lifecycle._interface_lifecycle_state = "active"

        result = lifecycle.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "interface_lifecycle_state")

    def test_validate_helpers_return_validation_result(self) -> None:
        boundary = build_boundary_model()
        boundary._boundary_side = "membrane"

        result = boundary.validate()

        self.assertIsInstance(result, ValidationResult)
        self.assertFalse(result.is_valid)


if __name__ == "__main__":
    unittest.main()
