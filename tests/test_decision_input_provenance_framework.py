import unittest
from dataclasses import FrozenInstanceError
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
    validate_decision_input_collection,
    validate_decision_input_reference,
    validate_decision_provenance,
)
from packages.knowledge import KnowledgeType, UniversalKnowledge
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import ObjectSerializer, ValidationResult
from packages.reasoning import ReasoningType, UniversalReasoning


TIMESTAMP = datetime.fromisoformat("2026-07-05T00:00:00+00:00")


class DecisionInputProvenanceFrameworkTest(unittest.TestCase):
    def build_reference(self) -> DecisionInputReference:
        return DecisionInputReference(
            input_type=DecisionInputType.KNOWLEDGE,
            identifier="knowledge:00000000-0000-0000-0000-000000007101",
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
            provenance_metadata={"z": "last", "a": "first"},
        )

    def test_decision_input_type_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {input_type.value for input_type in DecisionInputType},
            {"knowledge", "context", "reasoning", "memory", "external"},
        )

    def test_decision_input_reference_is_immutable_and_deterministic(self) -> None:
        reference = self.build_reference()

        self.assertEqual(
            reference.to_dict(),
            {
                "input_type": "knowledge",
                "identifier": "knowledge:00000000-0000-0000-0000-000000007101",
                "reference_metadata": {"a": "first", "z": "last"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            reference.identifier = "changed"

    def test_decision_input_collection_is_immutable_and_deterministic(self) -> None:
        inputs = self.build_inputs()

        self.assertEqual(inputs.to_dict(), {"references": [self.build_reference().to_dict()]})
        with self.assertRaises(FrozenInstanceError):
            inputs.references = ()

    def test_decision_origin_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {origin.value for origin in DecisionOrigin},
            {"human", "automated", "imported", "external", "unknown"},
        )

    def test_decision_provenance_is_immutable_and_deterministic(self) -> None:
        provenance = self.build_provenance()

        self.assertEqual(
            provenance.to_dict(),
            {
                "origin": "human",
                "author": "codex",
                "created_at": TIMESTAMP.isoformat(),
                "input_references": [self.build_reference().to_dict()],
                "provenance_metadata": {"a": "first", "z": "last"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            provenance.author = "changed"

    def test_validation_helpers_return_platform_validation_results(self) -> None:
        self.assertIsInstance(
            validate_decision_input_reference(self.build_reference()),
            ValidationResult,
        )
        self.assertTrue(validate_decision_input_reference(self.build_reference()).is_valid)
        self.assertTrue(validate_decision_input_collection(self.build_inputs()).is_valid)
        self.assertTrue(validate_decision_provenance(self.build_provenance()).is_valid)

    def test_validation_reports_invalid_input_reference_shape(self) -> None:
        reference = self.build_reference()
        object.__setattr__(reference, "input_type", "knowledge")
        object.__setattr__(reference, "identifier", "")
        object.__setattr__(reference, "reference_metadata", {"bad": "mutable"})

        result = validate_decision_input_reference(reference)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "decision_input_reference.input_type",
                "decision_input_reference.identifier",
                "decision_input_reference.reference_metadata",
            },
        )

    def test_validation_reports_invalid_input_collection_shape(self) -> None:
        inputs = self.build_inputs()
        object.__setattr__(inputs, "references", ("not-a-reference",))

        result = validate_decision_input_collection(inputs)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "decision_inputs.references[0]")

    def test_validation_reports_invalid_provenance_shape(self) -> None:
        provenance = self.build_provenance()
        object.__setattr__(provenance, "origin", "human")
        object.__setattr__(provenance, "author", object())
        object.__setattr__(provenance, "created_at", "not-a-datetime")
        object.__setattr__(provenance, "input_references", ("not-a-reference",))
        object.__setattr__(provenance, "provenance_metadata", {"bad": "mutable"})

        result = validate_decision_provenance(provenance)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "decision_provenance.origin",
                "decision_provenance.author",
                "decision_provenance.created_at",
                "decision_provenance.input_references[0]",
                "decision_provenance.provenance_metadata",
            },
        )

    def test_universal_decision_integrates_inputs_and_provenance(self) -> None:
        decision = UniversalDecision(
            object_id=UUID("00000000-0000-0000-0000-000000007102"),
            decision_type=DecisionType.APPROVAL,
            decision_state=DecisionState.CONFIRMED,
            decision_outcome=DecisionOutcome.ACCEPTED,
            decision_confidence=DecisionConfidence(level="high"),
            decision_metadata=DecisionMetadata(values={"mission": "bravo"}),
            decision_inputs=self.build_inputs(),
            decision_provenance=self.build_provenance(),
            created_at=TIMESTAMP,
            updated_at=TIMESTAMP,
        )
        payload = decision.to_dict()

        self.assertTrue(decision.validate().is_valid)
        self.assertEqual(payload["decision_inputs"], self.build_inputs().to_dict())
        self.assertEqual(payload["decision_provenance"], self.build_provenance().to_dict())
        self.assertEqual(
            list(payload.keys())[-2:],
            ["decision_inputs", "decision_provenance"],
        )

    def test_mission_alpha_constructor_and_payload_compatibility_is_preserved(self) -> None:
        decision = UniversalDecision(decision_type=DecisionType.RECOMMENDATION)
        payload = decision.to_dict()

        self.assertTrue(decision.validate().is_valid)
        self.assertIsNone(decision.decision_inputs)
        self.assertIsNone(decision.decision_provenance)
        self.assertNotIn("decision_inputs", payload)
        self.assertNotIn("decision_provenance", payload)

    def test_platform_core_serialization_compatibility_is_preserved(self) -> None:
        decision = UniversalDecision(
            object_id=UUID("00000000-0000-0000-0000-000000007103"),
            decision_type=DecisionType.SELECTION,
            decision_inputs=self.build_inputs(),
            decision_provenance=self.build_provenance(),
        )

        payload = ObjectSerializer.serialize(decision)

        self.assertEqual(payload["object_type"], "UniversalDecision")
        self.assertEqual(payload["object_id"], "00000000-0000-0000-0000-000000007103")
        self.assertNotIn("decision_inputs", payload)
        self.assertNotIn("decision_provenance", payload)

    def test_prior_foundation_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000007104"),
            memory_type=MemoryType.SEMANTIC,
            content="Decision input references remain opaque.",
            source=MemorySource(source_type="test", source_identifier="mission-bravo"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000007105"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000007106"),
            context_type=ContextType.ANALYTICAL,
        )
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000007107"),
            reasoning_type=ReasoningType.DEDUCTIVE,
        )
        inputs = DecisionInputCollection(
            references=(
                DecisionInputReference(DecisionInputType.MEMORY, str(memory.object_id)),
                DecisionInputReference(DecisionInputType.KNOWLEDGE, str(knowledge.object_id)),
                DecisionInputReference(DecisionInputType.CONTEXT, str(context.object_id)),
                DecisionInputReference(DecisionInputType.REASONING, str(reasoning.object_id)),
            )
        )
        decision = UniversalDecision(
            decision_type=DecisionType.OBSERVATION,
            decision_inputs=inputs,
        )

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertTrue(reasoning.validate().is_valid)
        self.assertTrue(decision.validate().is_valid)

    def test_no_execution_resolution_or_future_behavior_is_exposed(self) -> None:
        reference = self.build_reference()
        inputs = self.build_inputs()
        provenance = self.build_provenance()
        decision = UniversalDecision(
            decision_type=DecisionType.RECOMMENDATION,
            decision_inputs=inputs,
            decision_provenance=provenance,
        )
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

        self.assertTrue(forbidden_names.isdisjoint(set(dir(reference))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(inputs))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(provenance))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(decision))))


if __name__ == "__main__":
    unittest.main()
