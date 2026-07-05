import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime
from uuid import UUID

from packages.context import ContextType, UniversalContext
from packages.knowledge import KnowledgeType, UniversalKnowledge
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import ObjectSerializer, ValidationResult
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
    validate_reasoning_input_collection,
    validate_reasoning_input_reference,
    validate_reasoning_provenance,
)


TIMESTAMP = datetime.fromisoformat("2026-07-05T00:00:00+00:00")


class ReasoningInputProvenanceFrameworkTest(unittest.TestCase):
    def build_reference(self) -> ReasoningInputReference:
        return ReasoningInputReference(
            input_type=ReasoningInputType.KNOWLEDGE,
            identifier="knowledge:00000000-0000-0000-0000-000000006101",
            reference_metadata={"z": "last", "a": "first"},
        )

    def build_inputs(self) -> ReasoningInputCollection:
        return ReasoningInputCollection(references=(self.build_reference(),))

    def build_provenance(self) -> ReasoningProvenance:
        return ReasoningProvenance(
            origin=ReasoningOrigin.HUMAN_DEFINED,
            creator="codex",
            created_at=TIMESTAMP,
            input_references=(self.build_reference(),),
            provenance_metadata={"z": "last", "a": "first"},
        )

    def test_reasoning_input_type_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {input_type.value for input_type in ReasoningInputType},
            {"memory", "knowledge", "context", "reasoning"},
        )

    def test_reasoning_input_reference_is_immutable_and_deterministic(self) -> None:
        reference = self.build_reference()

        self.assertEqual(
            reference.to_dict(),
            {
                "input_type": "knowledge",
                "identifier": "knowledge:00000000-0000-0000-0000-000000006101",
                "reference_metadata": {"a": "first", "z": "last"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            reference.identifier = "changed"

    def test_reasoning_input_collection_is_immutable_and_deterministic(self) -> None:
        inputs = self.build_inputs()

        self.assertEqual(inputs.to_dict(), {"references": [self.build_reference().to_dict()]})
        with self.assertRaises(FrozenInstanceError):
            inputs.references = ()

    def test_reasoning_origin_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {origin.value for origin in ReasoningOrigin},
            {"human_defined", "system_generated", "imported", "validated", "derived"},
        )

    def test_reasoning_provenance_is_immutable_and_deterministic(self) -> None:
        provenance = self.build_provenance()

        self.assertEqual(
            provenance.to_dict(),
            {
                "origin": "human_defined",
                "creator": "codex",
                "created_at": TIMESTAMP.isoformat(),
                "input_references": [self.build_reference().to_dict()],
                "provenance_metadata": {"a": "first", "z": "last"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            provenance.creator = "changed"

    def test_validation_helpers_return_platform_validation_results(self) -> None:
        self.assertIsInstance(
            validate_reasoning_input_reference(self.build_reference()),
            ValidationResult,
        )
        self.assertTrue(validate_reasoning_input_reference(self.build_reference()).is_valid)
        self.assertTrue(validate_reasoning_input_collection(self.build_inputs()).is_valid)
        self.assertTrue(validate_reasoning_provenance(self.build_provenance()).is_valid)

    def test_validation_reports_invalid_input_reference_shape(self) -> None:
        reference = self.build_reference()
        object.__setattr__(reference, "input_type", "knowledge")
        object.__setattr__(reference, "identifier", "")
        object.__setattr__(reference, "reference_metadata", {"bad": "mutable"})

        result = validate_reasoning_input_reference(reference)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "reasoning_input_reference.input_type",
                "reasoning_input_reference.identifier",
                "reasoning_input_reference.reference_metadata",
            },
        )

    def test_validation_reports_invalid_input_collection_shape(self) -> None:
        inputs = self.build_inputs()
        object.__setattr__(inputs, "references", ("not-a-reference",))

        result = validate_reasoning_input_collection(inputs)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "reasoning_inputs.references[0]")

    def test_validation_reports_invalid_provenance_shape(self) -> None:
        provenance = self.build_provenance()
        object.__setattr__(provenance, "origin", "human_defined")
        object.__setattr__(provenance, "created_at", "not-a-datetime")
        object.__setattr__(provenance, "input_references", ("not-a-reference",))
        object.__setattr__(provenance, "provenance_metadata", {"bad": "mutable"})

        result = validate_reasoning_provenance(provenance)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "reasoning_provenance.origin",
                "reasoning_provenance.created_at",
                "reasoning_provenance.input_references[0]",
                "reasoning_provenance.provenance_metadata",
            },
        )

    def test_universal_reasoning_integrates_inputs_and_provenance(self) -> None:
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000006102"),
            reasoning_type=ReasoningType.DEDUCTIVE,
            reasoning_state=ReasoningState.VALIDATED,
            reasoning_confidence=ReasoningConfidence(level="high"),
            reasoning_metadata=ReasoningMetadata(values={"mission": "bravo"}),
            reasoning_inputs=self.build_inputs(),
            reasoning_provenance=self.build_provenance(),
            created_at=TIMESTAMP,
            updated_at=TIMESTAMP,
        )
        payload = reasoning.to_dict()

        self.assertTrue(reasoning.validate().is_valid)
        self.assertEqual(payload["reasoning_inputs"], self.build_inputs().to_dict())
        self.assertEqual(payload["reasoning_provenance"], self.build_provenance().to_dict())
        self.assertEqual(
            list(payload.keys())[-2:],
            ["reasoning_inputs", "reasoning_provenance"],
        )

    def test_mission_alpha_constructor_and_payload_compatibility_is_preserved(self) -> None:
        reasoning = UniversalReasoning(reasoning_type=ReasoningType.CAUSAL)
        payload = reasoning.to_dict()

        self.assertTrue(reasoning.validate().is_valid)
        self.assertIsNone(reasoning.reasoning_inputs)
        self.assertIsNone(reasoning.reasoning_provenance)
        self.assertNotIn("reasoning_inputs", payload)
        self.assertNotIn("reasoning_provenance", payload)

    def test_platform_core_serialization_compatibility_is_preserved(self) -> None:
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000006103"),
            reasoning_type=ReasoningType.ABDUCTIVE,
            reasoning_inputs=self.build_inputs(),
            reasoning_provenance=self.build_provenance(),
        )

        payload = ObjectSerializer.serialize(reasoning)

        self.assertEqual(payload["object_type"], "UniversalReasoning")
        self.assertEqual(payload["object_id"], "00000000-0000-0000-0000-000000006103")
        self.assertNotIn("reasoning_inputs", payload)
        self.assertNotIn("reasoning_provenance", payload)

    def test_memory_knowledge_and_context_foundation_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000006104"),
            memory_type=MemoryType.SEMANTIC,
            content="Reasoning input references remain opaque.",
            source=MemorySource(source_type="test", source_identifier="mission-bravo"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000006105"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000006106"),
            context_type=ContextType.ANALYTICAL,
        )
        inputs = ReasoningInputCollection(
            references=(
                ReasoningInputReference(ReasoningInputType.MEMORY, str(memory.object_id)),
                ReasoningInputReference(ReasoningInputType.KNOWLEDGE, str(knowledge.object_id)),
                ReasoningInputReference(ReasoningInputType.CONTEXT, str(context.object_id)),
            )
        )
        reasoning = UniversalReasoning(
            reasoning_type=ReasoningType.DEPENDENCY,
            reasoning_inputs=inputs,
        )

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertTrue(reasoning.validate().is_valid)

    def test_no_execution_resolution_or_future_behavior_is_exposed(self) -> None:
        reference = self.build_reference()
        inputs = self.build_inputs()
        provenance = self.build_provenance()
        reasoning = UniversalReasoning(
            reasoning_type=ReasoningType.INDUCTIVE,
            reasoning_inputs=inputs,
            reasoning_provenance=provenance,
        )
        forbidden_names = {
            "ai",
            "conclude",
            "evaluate",
            "execute",
            "infer",
            "persist",
            "reason",
            "resolve",
            "search",
            "workflow",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(reference))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(inputs))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(provenance))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(reasoning))))


if __name__ == "__main__":
    unittest.main()
