import unittest
from datetime import datetime
from uuid import UUID

from packages.context import ContextType, UniversalContext
from packages.decision import (
    DecisionConfidence,
    DecisionInputCollection,
    DecisionInputReference,
    DecisionInputType,
    DecisionMetadata,
    DecisionOrigin,
    DecisionOutcome,
    DecisionProvenance,
    DecisionState,
    DecisionType,
    UniversalDecision,
    validate_decision,
    validate_decision_input_collection,
    validate_decision_input_reference,
    validate_decision_provenance,
)
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
from packages.reasoning import ReasoningType, UniversalReasoning


TIMESTAMP = datetime.fromisoformat("2026-07-05T00:00:00+00:00")


class DecisionSerializationValidationCertificationTest(unittest.TestCase):
    def build_reference(self) -> DecisionInputReference:
        return DecisionInputReference(
            input_type=DecisionInputType.REASONING,
            identifier="reasoning:00000000-0000-0000-0000-000000007201",
            reference_metadata={"z": "last", "a": "first"},
        )

    def build_inputs(self) -> DecisionInputCollection:
        return DecisionInputCollection(references=(self.build_reference(),))

    def build_provenance(self) -> DecisionProvenance:
        return DecisionProvenance(
            origin=DecisionOrigin.HUMAN,
            author="codex",
            created_at=TIMESTAMP,
            input_references=(self.build_reference(),),
            provenance_metadata={"phase": "certification", "z": "last"},
        )

    def build_decision(self) -> UniversalDecision:
        return UniversalDecision(
            object_id=UUID("00000000-0000-0000-0000-000000007202"),
            decision_type=DecisionType.APPROVAL,
            decision_state=DecisionState.CONFIRMED,
            decision_outcome=DecisionOutcome.ACCEPTED,
            decision_confidence=DecisionConfidence(level="high", rationale="certified"),
            decision_metadata=DecisionMetadata(values={"z": "last", "a": "first"}),
            decision_inputs=self.build_inputs(),
            decision_provenance=self.build_provenance(),
            metadata={"owner": "decision"},
            tags=["decision", "charlie"],
            lifecycle_state=LifecycleState.DRAFT,
            created_by="codex",
            updated_by="codex",
            created_at=TIMESTAMP,
            updated_at=TIMESTAMP,
        )

    def test_decision_public_models_are_certified(self) -> None:
        decision = self.build_decision()

        self.assertIsInstance(decision, CanonicalObject)
        self.assertEqual(decision.object_type, "UniversalDecision")
        self.assertEqual(decision.decision_type, DecisionType.APPROVAL)
        self.assertEqual(decision.decision_state, DecisionState.CONFIRMED)
        self.assertEqual(decision.decision_outcome, DecisionOutcome.ACCEPTED)
        self.assertIsInstance(decision.decision_confidence, DecisionConfidence)
        self.assertIsInstance(decision.decision_metadata, DecisionMetadata)
        self.assertIsInstance(decision.decision_inputs, DecisionInputCollection)
        self.assertIsInstance(decision.decision_provenance, DecisionProvenance)

    def test_enum_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {decision_type.value for decision_type in DecisionType},
            {
                "recommendation",
                "selection",
                "approval",
                "rejection",
                "deferment",
                "observation",
            },
        )
        self.assertEqual(
            {state.value for state in DecisionState},
            {"draft", "proposed", "confirmed", "archived"},
        )
        self.assertEqual(
            {outcome.value for outcome in DecisionOutcome},
            {"accepted", "rejected", "deferred", "unknown"},
        )
        self.assertEqual(
            {input_type.value for input_type in DecisionInputType},
            {"knowledge", "context", "reasoning", "memory", "external"},
        )
        self.assertEqual(
            {origin.value for origin in DecisionOrigin},
            {"human", "automated", "imported", "external", "unknown"},
        )

    def test_alpha_payload_ordering_is_preserved_without_bravo_fields(self) -> None:
        decision = UniversalDecision(
            object_id=UUID("00000000-0000-0000-0000-000000007203"),
            decision_type=DecisionType.RECOMMENDATION,
            created_at=TIMESTAMP,
            updated_at=TIMESTAMP,
        )
        payload = decision.to_dict()

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
                "decision_type",
                "decision_state",
                "decision_outcome",
                "decision_confidence",
                "decision_metadata",
            ],
        )
        self.assertNotIn("decision_inputs", payload)
        self.assertNotIn("decision_provenance", payload)

    def test_bravo_payload_fields_append_after_alpha_fields(self) -> None:
        payload = self.build_decision().to_dict()

        self.assertEqual(payload, self.build_decision().to_dict())
        self.assertEqual(
            list(payload.keys())[-2:],
            ["decision_inputs", "decision_provenance"],
        )
        self.assertEqual(payload["decision_inputs"], self.build_inputs().to_dict())
        self.assertEqual(payload["decision_provenance"], self.build_provenance().to_dict())

    def test_nested_decision_payloads_are_deterministic(self) -> None:
        reference = self.build_reference()
        provenance = self.build_provenance()

        self.assertEqual(
            reference.to_dict(),
            {
                "input_type": "reasoning",
                "identifier": "reasoning:00000000-0000-0000-0000-000000007201",
                "reference_metadata": {"a": "first", "z": "last"},
            },
        )
        self.assertEqual(
            provenance.to_dict(),
            {
                "origin": "human",
                "author": "codex",
                "created_at": TIMESTAMP.isoformat(),
                "input_references": [reference.to_dict()],
                "provenance_metadata": {"phase": "certification", "z": "last"},
            },
        )

    def test_validation_returns_platform_validation_result(self) -> None:
        result = self.build_decision().validate()

        self.assertIsInstance(result, ValidationResult)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_local_validation_helpers_return_platform_validation_result(self) -> None:
        self.assertIsInstance(validate_decision(self.build_decision()), ValidationResult)
        self.assertIsInstance(
            validate_decision_input_reference(self.build_reference()),
            ValidationResult,
        )
        self.assertIsInstance(
            validate_decision_input_collection(self.build_inputs()),
            ValidationResult,
        )
        self.assertIsInstance(
            validate_decision_provenance(self.build_provenance()),
            ValidationResult,
        )

    def test_validation_failures_are_deterministic(self) -> None:
        decision = self.build_decision()
        decision._decision_type = "approval"
        decision._decision_state = "confirmed"
        decision._decision_outcome = "accepted"
        decision._decision_confidence = "high"
        decision._decision_metadata = {"bad": "mutable"}
        decision._decision_inputs = "inputs"
        decision._decision_provenance = "provenance"

        result = decision.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "decision_type",
                "decision_state",
                "decision_outcome",
                "decision_confidence",
                "decision_metadata",
                "decision_inputs",
                "decision_provenance",
            },
        )

    def test_reference_and_provenance_validation_failures_are_certified(self) -> None:
        reference = self.build_reference()
        object.__setattr__(reference, "input_type", "reasoning")
        object.__setattr__(reference, "identifier", "")
        object.__setattr__(reference, "reference_metadata", {"bad": "mutable"})
        provenance = self.build_provenance()
        object.__setattr__(provenance, "origin", "human")
        object.__setattr__(provenance, "author", object())
        object.__setattr__(provenance, "created_at", "not-a-datetime")
        object.__setattr__(provenance, "input_references", (reference,))
        object.__setattr__(provenance, "provenance_metadata", {"bad": "mutable"})

        reference_result = validate_decision_input_reference(reference)
        provenance_result = validate_decision_provenance(provenance)

        self.assertFalse(reference_result.is_valid)
        self.assertFalse(provenance_result.is_valid)
        self.assertEqual(
            {error.field for error in reference_result.errors},
            {
                "decision_input_reference.input_type",
                "decision_input_reference.identifier",
                "decision_input_reference.reference_metadata",
            },
        )
        self.assertIn("decision_provenance.origin", {error.field for error in provenance_result.errors})
        self.assertIn("decision_provenance.author", {error.field for error in provenance_result.errors})

    def test_object_serializer_remains_platform_core_contract(self) -> None:
        decision = self.build_decision()

        payload = ObjectSerializer.serialize(decision)

        self.assertEqual(payload["object_type"], "UniversalDecision")
        self.assertEqual(payload["metadata"], {"owner": "decision"})
        self.assertEqual(payload["tags"], ["decision", "charlie"])
        self.assertNotIn("decision_type", payload)
        self.assertNotIn("decision_inputs", payload)
        self.assertNotIn("decision_provenance", payload)

    def test_object_serializer_json_is_deterministic(self) -> None:
        decision = self.build_decision()

        self.assertEqual(
            ObjectSerializer.serialize_json(decision),
            ObjectSerializer.serialize_json(decision),
        )

    def test_object_registry_accepts_universal_decision(self) -> None:
        registry = ObjectRegistry()

        registry.register(UniversalDecision)

        self.assertEqual(registry.lookup("UniversalDecision"), UniversalDecision)
        self.assertEqual(registry.lookup_by_class(UniversalDecision), UniversalDecision)
        self.assertEqual(registry.enumerate(), (UniversalDecision,))
        registry.validate()

    def test_lifecycle_transitions_remain_platform_core_behavior(self) -> None:
        decision = self.build_decision()

        decision.transition_to(LifecycleState.ACTIVE)
        decision.transition_to(LifecycleState.ARCHIVED)

        self.assertEqual(decision.lifecycle_state, LifecycleState.ARCHIVED)
        with self.assertRaises(ValueError):
            decision.transition_to(LifecycleState.ACTIVE)

    def test_relationship_compatibility_uses_platform_relationship_model(self) -> None:
        decision = self.build_decision()
        target_id = UUID("00000000-0000-0000-0000-000000007204")
        relationship = Relationship(
            source_object_id=decision.object_id,
            target_object_id=target_id,
            relationship_type=RelationshipType.REFERENCES,
            metadata={"phase": "certification"},
        )

        payload = relationship.to_dict()

        self.assertEqual(payload["source_object_id"], str(decision.object_id))
        self.assertEqual(payload["target_object_id"], str(target_id))
        self.assertEqual(payload["relationship_type"], "references")
        self.assertEqual(payload["metadata"], {"phase": "certification"})
        self.assertEqual(decision.relationships, {})

    def test_prior_foundations_coexist_with_decision(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000007205"),
            memory_type=MemoryType.SEMANTIC,
            content="Decision certification coexists with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-charlie"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000007206"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000007207"),
            context_type=ContextType.ANALYTICAL,
        )
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000007208"),
            reasoning_type=ReasoningType.DEDUCTIVE,
        )
        decision = UniversalDecision(
            decision_type=DecisionType.OBSERVATION,
            decision_inputs=DecisionInputCollection(
                references=(
                    DecisionInputReference(DecisionInputType.MEMORY, str(memory.object_id)),
                    DecisionInputReference(DecisionInputType.KNOWLEDGE, str(knowledge.object_id)),
                    DecisionInputReference(DecisionInputType.CONTEXT, str(context.object_id)),
                    DecisionInputReference(DecisionInputType.REASONING, str(reasoning.object_id)),
                )
            ),
        )

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertTrue(reasoning.validate().is_valid)
        self.assertTrue(decision.validate().is_valid)

    def test_foundation_coexistence_does_not_mutate_existing_objects(self) -> None:
        memory = UniversalMemory(
            memory_type=MemoryType.SEMANTIC,
            content="Cross-foundation certification.",
            source=MemorySource(source_type="test", source_identifier="mission-charlie"),
        )
        knowledge = UniversalKnowledge(knowledge_type=KnowledgeType.FACT)
        context = UniversalContext(context_type=ContextType.ANALYTICAL)
        reasoning = UniversalReasoning(reasoning_type=ReasoningType.DEDUCTIVE)
        before = (
            memory.to_dict(),
            knowledge.to_dict(),
            context.to_dict(),
            reasoning.to_dict(),
        )

        self.build_decision().validate()

        after = (
            memory.to_dict(),
            knowledge.to_dict(),
            context.to_dict(),
            reasoning.to_dict(),
        )

        self.assertEqual(before, after)

    def test_no_future_decision_capabilities_are_exposed(self) -> None:
        decision = self.build_decision()
        reference = self.build_reference()
        inputs = self.build_inputs()
        provenance = self.build_provenance()
        forbidden_names = {
            "ai",
            "autonomous",
            "compute",
            "evaluate",
            "execute",
            "optimize",
            "persist",
            "plan",
            "resolve",
            "search",
            "workflow",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(decision))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(reference))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(inputs))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(provenance))))


if __name__ == "__main__":
    unittest.main()
