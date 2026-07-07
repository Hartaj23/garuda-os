import unittest
from datetime import datetime
from uuid import UUID

from packages.integration import (
    CanonicalIntegrationRelationship,
    IntegrationContractMetadata,
    IntegrationParticipantClassification,
    IntegrationParticipantClassificationHook,
    IntegrationParticipantReference,
    IntegrationParticipantRelationshipDescriptor,
    IntegrationRelationshipKind,
    IntegrationRelationshipMetadata,
    evaluate_integration_relationship,
    validate_canonical_integration_relationship,
)
from packages.objects import CanonicalObject, ObjectSerializer, ValidationResult


TIMESTAMP = datetime.fromisoformat("2026-07-07T00:00:00+00:00")


def build_source_participant() -> IntegrationParticipantReference:
    return IntegrationParticipantReference(
        participant_identifier="participant:00000000-0000-0000-0000-000000005001",
        participant_metadata=IntegrationContractMetadata(values={"role": "source"}),
    )


def build_target_participant() -> IntegrationParticipantReference:
    return IntegrationParticipantReference(
        participant_identifier="participant:00000000-0000-0000-0000-000000005002",
        participant_metadata=IntegrationContractMetadata(values={"role": "target"}),
    )


def build_relationship_descriptor() -> IntegrationParticipantRelationshipDescriptor:
    return IntegrationParticipantRelationshipDescriptor(
        source_participant=build_source_participant(),
        target_participant=build_target_participant(),
        relationship_kind=IntegrationRelationshipKind.ASSOCIATED,
        relationship_metadata=IntegrationRelationshipMetadata(values={"scope": "delta"}),
    )


def build_relationship() -> CanonicalIntegrationRelationship:
    return CanonicalIntegrationRelationship(
        object_id=UUID("00000000-0000-0000-0000-000000005003"),
        relationship_descriptor=build_relationship_descriptor(),
        classification_hooks=(
            IntegrationParticipantClassificationHook(
                participant_reference=build_source_participant(),
                classification=IntegrationParticipantClassification.SOURCE,
            ),
            IntegrationParticipantClassificationHook(
                participant_reference=build_target_participant(),
                classification=IntegrationParticipantClassification.TARGET,
            ),
        ),
        relationship_metadata=IntegrationRelationshipMetadata(values={"mission": "delta"}),
        metadata={"owner": "integration"},
        tags=["integration", "delta"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


class IntegrationRelationshipsTest(unittest.TestCase):
    def test_relationship_record_inherits_platform_core(self) -> None:
        relationship = build_relationship()

        self.assertIsInstance(relationship, CanonicalObject)
        self.assertEqual(relationship.object_type, "CanonicalIntegrationRelationship")

    def test_canonical_serialization_without_custom_adapters(self) -> None:
        relationship = build_relationship()

        core_payload = ObjectSerializer.serialize(relationship)
        relationship_payload = relationship.to_dict()

        self.assertEqual(core_payload["object_type"], "CanonicalIntegrationRelationship")
        self.assertEqual(
            relationship_payload["relationship_descriptor"]["relationship_kind"],
            "associated",
        )

    def test_platform_validation_passes(self) -> None:
        self.assertTrue(build_relationship().validate().is_valid)

    def test_relationship_evaluation_is_deterministic(self) -> None:
        descriptor = build_relationship_descriptor()

        first = evaluate_integration_relationship(descriptor)
        second = evaluate_integration_relationship(descriptor)

        self.assertEqual(first.to_dict(), second.to_dict())
        self.assertFalse(first.is_directional)

    def test_directional_relationship_evaluation(self) -> None:
        descriptor = IntegrationParticipantRelationshipDescriptor(
            source_participant=build_source_participant(),
            target_participant=build_target_participant(),
            relationship_kind=IntegrationRelationshipKind.DEPENDENT,
        )

        evaluation = evaluate_integration_relationship(descriptor)

        self.assertTrue(evaluation.is_directional)
        self.assertEqual(evaluation.relationship_kind, IntegrationRelationshipKind.DEPENDENT)

    def test_classification_hooks_are_technology_neutral(self) -> None:
        relationship = build_relationship()
        hook = relationship.classification_hooks[0]

        self.assertEqual(hook.classification, IntegrationParticipantClassification.SOURCE)
        self.assertNotIn("http", hook.participant_reference.participant_identifier.lower())
        self.assertNotIn("provider", hook.classification.value)

    def test_relationship_validation_reports_invalid_kind(self) -> None:
        relationship = build_relationship()
        relationship._relationship_descriptor = IntegrationParticipantRelationshipDescriptor(
            source_participant=build_source_participant(),
            target_participant=build_target_participant(),
            relationship_kind="associated",
        )

        result = relationship.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "relationship_descriptor.relationship_kind")

    def test_validate_helper_returns_validation_result(self) -> None:
        relationship = build_relationship()
        relationship._relationship_metadata = "invalid"

        result = validate_canonical_integration_relationship(relationship)

        self.assertIsInstance(result, ValidationResult)
        self.assertFalse(result.is_valid)

    def test_relationship_to_dict_is_deterministic(self) -> None:
        relationship = build_relationship()

        first = relationship.to_dict()
        second = relationship.to_dict()

        self.assertEqual(first, second)
        self.assertEqual(len(first["classification_hooks"]), 2)

    def test_no_cognitive_foundation_imports_in_relationship_modules(self) -> None:
        import packages.integration.relationships.classification as classification_module
        import packages.integration.relationships.descriptor as descriptor_module
        import packages.integration.relationships.evaluation as evaluation_module
        import packages.integration.relationships.relationship as relationship_module

        forbidden_prefixes = (
            "packages.memory",
            "packages.knowledge",
            "packages.context",
            "packages.reasoning",
            "packages.decision",
            "packages.action",
            "packages.execution",
        )

        for module in (
            classification_module,
            descriptor_module,
            evaluation_module,
            relationship_module,
        ):
            with open(module.__file__, encoding="utf-8") as module_file:
                source = module_file.read()
            for prefix in forbidden_prefixes:
                self.assertNotIn(prefix, source)

    def test_relationship_framework_is_descriptive_only(self) -> None:
        relationship = build_relationship()

        self.assertNotIn("route", dir(relationship))
        self.assertNotIn("deliver", dir(relationship))
        self.assertNotIn("invoke", dir(relationship))


if __name__ == "__main__":
    unittest.main()
