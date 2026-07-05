import unittest
from datetime import datetime
from uuid import UUID

from packages.context import ContextType, UniversalContext
from packages.knowledge import KnowledgeType, UniversalKnowledge
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import (
    CanonicalObject,
    LifecycleState,
    ObjectRegistry,
    ObjectSerializer,
    Relationship,
    RelationshipType,
    ValidationResult,
)
from packages.reasoning import (
    ReasoningConfidence,
    ReasoningInputCollection,
    ReasoningInputReference,
    ReasoningInputType,
    ReasoningMetadata,
    ReasoningOrigin,
    ReasoningProvenance,
    ReasoningState,
    ReasoningType,
    UniversalReasoning,
    validate_reasoning,
    validate_reasoning_input_collection,
    validate_reasoning_input_reference,
    validate_reasoning_provenance,
)


TIMESTAMP = datetime.fromisoformat("2026-07-05T00:00:00+00:00")


class ReasoningSerializationValidationCertificationTest(unittest.TestCase):
    def build_reference(self) -> ReasoningInputReference:
        return ReasoningInputReference(
            input_type=ReasoningInputType.CONTEXT,
            identifier="context:00000000-0000-0000-0000-000000006201",
            reference_metadata={"z": "last", "a": "first"},
        )

    def build_inputs(self) -> ReasoningInputCollection:
        return ReasoningInputCollection(references=(self.build_reference(),))

    def build_provenance(self) -> ReasoningProvenance:
        return ReasoningProvenance(
            origin=ReasoningOrigin.VALIDATED,
            creator="codex",
            created_at=TIMESTAMP,
            input_references=(self.build_reference(),),
            provenance_metadata={"phase": "certification", "z": "last"},
        )

    def build_reasoning(self) -> UniversalReasoning:
        return UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000006202"),
            reasoning_type=ReasoningType.CONSISTENCY,
            reasoning_state=ReasoningState.VALIDATED,
            reasoning_confidence=ReasoningConfidence(level="high", rationale="certified"),
            reasoning_metadata=ReasoningMetadata(values={"z": "last", "a": "first"}),
            reasoning_inputs=self.build_inputs(),
            reasoning_provenance=self.build_provenance(),
            metadata={"owner": "reasoning"},
            tags=["reasoning", "charlie"],
            lifecycle_state=LifecycleState.DRAFT,
            created_by="codex",
            updated_by="codex",
            created_at=TIMESTAMP,
            updated_at=TIMESTAMP,
        )

    def test_reasoning_public_models_are_certified(self) -> None:
        reasoning = self.build_reasoning()

        self.assertIsInstance(reasoning, CanonicalObject)
        self.assertEqual(reasoning.object_type, "UniversalReasoning")
        self.assertEqual(reasoning.reasoning_type, ReasoningType.CONSISTENCY)
        self.assertEqual(reasoning.reasoning_state, ReasoningState.VALIDATED)
        self.assertIsInstance(reasoning.reasoning_confidence, ReasoningConfidence)
        self.assertIsInstance(reasoning.reasoning_metadata, ReasoningMetadata)
        self.assertIsInstance(reasoning.reasoning_inputs, ReasoningInputCollection)
        self.assertIsInstance(reasoning.reasoning_provenance, ReasoningProvenance)

    def test_enum_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {reasoning_type.value for reasoning_type in ReasoningType},
            {
                "deductive",
                "inductive",
                "abductive",
                "comparative",
                "causal",
                "temporal",
                "dependency",
                "consistency",
            },
        )
        self.assertEqual(
            {state.value for state in ReasoningState},
            {"draft", "evaluated", "validated", "accepted", "superseded", "archived"},
        )
        self.assertEqual(
            {input_type.value for input_type in ReasoningInputType},
            {"memory", "knowledge", "context", "reasoning"},
        )
        self.assertEqual(
            {origin.value for origin in ReasoningOrigin},
            {"human_defined", "system_generated", "imported", "validated", "derived"},
        )

    def test_alpha_payload_ordering_is_preserved_without_bravo_fields(self) -> None:
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000006203"),
            reasoning_type=ReasoningType.DEDUCTIVE,
            created_at=TIMESTAMP,
            updated_at=TIMESTAMP,
        )
        payload = reasoning.to_dict()

        self.assertEqual(
            list(payload.keys()),
            [
                "schema_version",
                "object_version",
                "object_type",
                "object_id",
                "metadata",
                "tags",
                "lifecycle_state",
                "created_by",
                "updated_by",
                "created_at",
                "updated_at",
                "reasoning_type",
                "reasoning_state",
                "reasoning_confidence",
                "reasoning_metadata",
            ],
        )
        self.assertNotIn("reasoning_inputs", payload)
        self.assertNotIn("reasoning_provenance", payload)

    def test_bravo_payload_fields_append_after_alpha_fields(self) -> None:
        payload = self.build_reasoning().to_dict()

        self.assertEqual(payload, self.build_reasoning().to_dict())
        self.assertEqual(
            list(payload.keys())[-2:],
            ["reasoning_inputs", "reasoning_provenance"],
        )
        self.assertEqual(payload["reasoning_inputs"], self.build_inputs().to_dict())
        self.assertEqual(payload["reasoning_provenance"], self.build_provenance().to_dict())

    def test_nested_reasoning_payloads_are_deterministic(self) -> None:
        reference = self.build_reference()
        provenance = self.build_provenance()

        self.assertEqual(
            reference.to_dict(),
            {
                "input_type": "context",
                "identifier": "context:00000000-0000-0000-0000-000000006201",
                "reference_metadata": {"a": "first", "z": "last"},
            },
        )
        self.assertEqual(
            provenance.to_dict(),
            {
                "origin": "validated",
                "creator": "codex",
                "created_at": TIMESTAMP.isoformat(),
                "input_references": [reference.to_dict()],
                "provenance_metadata": {"phase": "certification", "z": "last"},
            },
        )

    def test_validation_returns_platform_validation_result(self) -> None:
        result = self.build_reasoning().validate()

        self.assertIsInstance(result, ValidationResult)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_local_validation_helpers_return_platform_validation_result(self) -> None:
        self.assertIsInstance(validate_reasoning(self.build_reasoning()), ValidationResult)
        self.assertIsInstance(
            validate_reasoning_input_reference(self.build_reference()),
            ValidationResult,
        )
        self.assertIsInstance(
            validate_reasoning_input_collection(self.build_inputs()),
            ValidationResult,
        )
        self.assertIsInstance(
            validate_reasoning_provenance(self.build_provenance()),
            ValidationResult,
        )

    def test_validation_failures_are_deterministic(self) -> None:
        reasoning = self.build_reasoning()
        reasoning._reasoning_type = "consistency"
        reasoning._reasoning_state = "validated"
        reasoning._reasoning_confidence = "high"
        reasoning._reasoning_metadata = {"bad": "mutable"}
        reasoning._reasoning_inputs = "inputs"
        reasoning._reasoning_provenance = "provenance"

        result = reasoning.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "reasoning_type",
                "reasoning_state",
                "reasoning_confidence",
                "reasoning_metadata",
                "reasoning_inputs",
                "reasoning_provenance",
            },
        )

    def test_reference_and_provenance_validation_failures_are_certified(self) -> None:
        reference = self.build_reference()
        object.__setattr__(reference, "input_type", "context")
        object.__setattr__(reference, "identifier", "")
        object.__setattr__(reference, "reference_metadata", {"bad": "mutable"})
        provenance = self.build_provenance()
        object.__setattr__(provenance, "origin", "validated")
        object.__setattr__(provenance, "created_at", "not-a-datetime")
        object.__setattr__(provenance, "input_references", (reference,))
        object.__setattr__(provenance, "provenance_metadata", {"bad": "mutable"})

        reference_result = validate_reasoning_input_reference(reference)
        provenance_result = validate_reasoning_provenance(provenance)

        self.assertFalse(reference_result.is_valid)
        self.assertFalse(provenance_result.is_valid)
        self.assertEqual(
            {error.field for error in reference_result.errors},
            {
                "reasoning_input_reference.input_type",
                "reasoning_input_reference.identifier",
                "reasoning_input_reference.reference_metadata",
            },
        )
        self.assertIn("reasoning_provenance.origin", {error.field for error in provenance_result.errors})

    def test_object_serializer_remains_platform_core_contract(self) -> None:
        reasoning = self.build_reasoning()

        payload = ObjectSerializer.serialize(reasoning)

        self.assertEqual(payload["object_type"], "UniversalReasoning")
        self.assertEqual(payload["metadata"], {"owner": "reasoning"})
        self.assertEqual(payload["tags"], ["reasoning", "charlie"])
        self.assertNotIn("reasoning_type", payload)
        self.assertNotIn("reasoning_inputs", payload)
        self.assertNotIn("reasoning_provenance", payload)

    def test_object_serializer_json_is_deterministic(self) -> None:
        reasoning = self.build_reasoning()

        self.assertEqual(
            ObjectSerializer.serialize_json(reasoning),
            ObjectSerializer.serialize_json(reasoning),
        )

    def test_object_registry_accepts_universal_reasoning(self) -> None:
        registry = ObjectRegistry()

        registry.register(UniversalReasoning)

        self.assertEqual(registry.lookup("UniversalReasoning"), UniversalReasoning)
        self.assertEqual(registry.lookup_by_class(UniversalReasoning), UniversalReasoning)
        self.assertEqual(registry.enumerate(), (UniversalReasoning,))
        registry.validate()

    def test_lifecycle_transitions_remain_platform_core_behavior(self) -> None:
        reasoning = self.build_reasoning()

        reasoning.transition_to(LifecycleState.ACTIVE)
        reasoning.transition_to(LifecycleState.ARCHIVED)

        self.assertEqual(reasoning.lifecycle_state, LifecycleState.ARCHIVED)
        with self.assertRaises(ValueError):
            reasoning.transition_to(LifecycleState.ACTIVE)

    def test_relationship_compatibility_uses_platform_relationship_model(self) -> None:
        reasoning = self.build_reasoning()
        target_id = UUID("00000000-0000-0000-0000-000000006204")
        relationship = Relationship(
            source_object_id=reasoning.object_id,
            target_object_id=target_id,
            relationship_type=RelationshipType.REFERENCES,
            metadata={"phase": "certification"},
        )

        payload = relationship.to_dict()

        self.assertEqual(payload["source_object_id"], str(reasoning.object_id))
        self.assertEqual(payload["target_object_id"], str(target_id))
        self.assertEqual(payload["relationship_type"], "references")
        self.assertEqual(payload["metadata"], {"phase": "certification"})
        self.assertEqual(reasoning.relationships, {})

    def test_memory_knowledge_and_context_foundations_coexist_with_reasoning(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000006205"),
            memory_type=MemoryType.SEMANTIC,
            content="Reasoning certification coexists with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-charlie"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000006206"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000006207"),
            context_type=ContextType.ANALYTICAL,
        )
        reasoning = self.build_reasoning()

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertTrue(reasoning.validate().is_valid)

    def test_explicit_absence_of_future_reasoning_behavior_is_certified(self) -> None:
        reasoning = self.build_reasoning()
        reference = self.build_reference()
        inputs = self.build_inputs()
        provenance = self.build_provenance()
        forbidden_names = {
            "ai",
            "conclude",
            "decide",
            "evaluate",
            "execute",
            "infer",
            "persist",
            "plan",
            "reason",
            "resolve",
            "search",
            "workflow",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(reasoning))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(reference))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(inputs))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(provenance))))


if __name__ == "__main__":
    unittest.main()
