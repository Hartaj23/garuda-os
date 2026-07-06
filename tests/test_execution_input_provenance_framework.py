import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime
from uuid import UUID

from packages.action import ActionType, UniversalAction
from packages.context import ContextType, UniversalContext
from packages.decision import DecisionType, UniversalDecision
from packages.execution import (
    ExecutionConfidence,
    ExecutionInputCollection,
    ExecutionInputReference,
    ExecutionInputType,
    ExecutionMetadata,
    ExecutionOrigin,
    ExecutionOutcome,
    ExecutionProvenance,
    ExecutionState,
    ExecutionType,
    UniversalExecution,
    validate_execution_input_collection,
    validate_execution_input_reference,
    validate_execution_provenance,
)
from packages.knowledge import KnowledgeType, UniversalKnowledge
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import ObjectSerializer, ValidationResult
from packages.reasoning import ReasoningType, UniversalReasoning


TIMESTAMP = datetime.fromisoformat("2026-07-06T00:00:00+00:00")


class ExecutionInputProvenanceFrameworkTest(unittest.TestCase):
    def build_reference(self) -> ExecutionInputReference:
        return ExecutionInputReference(
            input_type=ExecutionInputType.ACTION,
            identifier="action:00000000-0000-0000-0000-000000009101",
            reference_metadata={"z": "last", "a": "first"},
        )

    def build_inputs(self) -> ExecutionInputCollection:
        return ExecutionInputCollection(references=(self.build_reference(),))

    def build_provenance(self) -> ExecutionProvenance:
        return ExecutionProvenance(
            origin=ExecutionOrigin.ACTION,
            source_identifier="action:00000000-0000-0000-0000-000000009101",
            created_at=TIMESTAMP,
            input_references=(self.build_reference(),),
            provenance_metadata={"z": "last", "a": "first"},
        )

    def test_execution_input_type_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {input_type.value for input_type in ExecutionInputType},
            {"memory", "knowledge", "context", "reasoning", "decision", "action", "external"},
        )

    def test_execution_input_reference_is_immutable_and_deterministic(self) -> None:
        reference = self.build_reference()

        self.assertEqual(
            reference.to_dict(),
            {
                "input_type": "action",
                "identifier": "action:00000000-0000-0000-0000-000000009101",
                "reference_metadata": {"a": "first", "z": "last"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            reference.identifier = "changed"

    def test_execution_input_collection_is_immutable_and_deterministic(self) -> None:
        inputs = self.build_inputs()

        self.assertEqual(inputs.to_dict(), {"references": [self.build_reference().to_dict()]})
        with self.assertRaises(FrozenInstanceError):
            inputs.references = ()

    def test_execution_origin_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {origin.value for origin in ExecutionOrigin},
            {"human", "system", "imported", "external", "action", "unknown"},
        )

    def test_execution_provenance_is_immutable_and_deterministic(self) -> None:
        provenance = self.build_provenance()

        self.assertEqual(
            provenance.to_dict(),
            {
                "origin": "action",
                "source_identifier": "action:00000000-0000-0000-0000-000000009101",
                "created_at": TIMESTAMP.isoformat(),
                "input_references": [self.build_reference().to_dict()],
                "provenance_metadata": {"a": "first", "z": "last"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            provenance.source_identifier = "changed"

    def test_validation_helpers_return_platform_validation_results(self) -> None:
        self.assertIsInstance(
            validate_execution_input_reference(self.build_reference()),
            ValidationResult,
        )
        self.assertTrue(validate_execution_input_reference(self.build_reference()).is_valid)
        self.assertTrue(validate_execution_input_collection(self.build_inputs()).is_valid)
        self.assertTrue(validate_execution_provenance(self.build_provenance()).is_valid)

    def test_validation_reports_invalid_input_reference_shape(self) -> None:
        reference = self.build_reference()
        object.__setattr__(reference, "input_type", "action")
        object.__setattr__(reference, "identifier", "")
        object.__setattr__(reference, "reference_metadata", {"bad": "mutable"})

        result = validate_execution_input_reference(reference)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "execution_input_reference.input_type",
                "execution_input_reference.identifier",
                "execution_input_reference.reference_metadata",
            },
        )

    def test_validation_reports_invalid_input_collection_shape(self) -> None:
        inputs = self.build_inputs()
        object.__setattr__(inputs, "references", ("not-a-reference",))

        result = validate_execution_input_collection(inputs)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "execution_inputs.references[0]")

    def test_validation_reports_invalid_provenance_shape(self) -> None:
        provenance = self.build_provenance()
        object.__setattr__(provenance, "origin", "action")
        object.__setattr__(provenance, "source_identifier", object())
        object.__setattr__(provenance, "created_at", "not-a-datetime")
        object.__setattr__(provenance, "input_references", ("not-a-reference",))
        object.__setattr__(provenance, "provenance_metadata", {"bad": "mutable"})

        result = validate_execution_provenance(provenance)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "execution_provenance.origin",
                "execution_provenance.source_identifier",
                "execution_provenance.created_at",
                "execution_provenance.input_references[0]",
                "execution_provenance.provenance_metadata",
            },
        )

    def test_universal_execution_integrates_inputs_and_provenance(self) -> None:
        execution = UniversalExecution(
            object_id=UUID("00000000-0000-0000-0000-000000009102"),
            execution_type=ExecutionType.ACTION,
            execution_state=ExecutionState.READY,
            execution_outcome=ExecutionOutcome.UNKNOWN,
            execution_confidence=ExecutionConfidence(level="high"),
            execution_metadata=ExecutionMetadata(values={"mission": "bravo"}),
            execution_inputs=self.build_inputs(),
            execution_provenance=self.build_provenance(),
            created_at=TIMESTAMP,
            updated_at=TIMESTAMP,
        )
        payload = execution.to_dict()

        self.assertTrue(execution.validate().is_valid)
        self.assertEqual(payload["execution_inputs"], self.build_inputs().to_dict())
        self.assertEqual(payload["execution_provenance"], self.build_provenance().to_dict())
        self.assertEqual(
            list(payload.keys())[-2:],
            ["execution_inputs", "execution_provenance"],
        )

    def test_mission_alpha_constructor_and_payload_compatibility_is_preserved(self) -> None:
        execution = UniversalExecution(execution_type=ExecutionType.ACTION)
        payload = execution.to_dict()

        self.assertTrue(execution.validate().is_valid)
        self.assertIsNone(execution.execution_inputs)
        self.assertIsNone(execution.execution_provenance)
        self.assertNotIn("execution_inputs", payload)
        self.assertNotIn("execution_provenance", payload)

    def test_platform_core_serialization_compatibility_is_preserved(self) -> None:
        execution = UniversalExecution(
            object_id=UUID("00000000-0000-0000-0000-000000009103"),
            execution_type=ExecutionType.REVIEW,
            execution_inputs=self.build_inputs(),
            execution_provenance=self.build_provenance(),
        )

        payload = ObjectSerializer.serialize(execution)

        self.assertEqual(payload["object_type"], "UniversalExecution")
        self.assertEqual(payload["object_id"], "00000000-0000-0000-0000-000000009103")
        self.assertNotIn("execution_inputs", payload)
        self.assertNotIn("execution_provenance", payload)

    def test_existing_foundation_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000009104"),
            memory_type=MemoryType.SEMANTIC,
            content="Execution input references remain opaque.",
            source=MemorySource(source_type="test", source_identifier="mission-bravo"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000009105"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000009106"),
            context_type=ContextType.ANALYTICAL,
        )
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000009107"),
            reasoning_type=ReasoningType.DEDUCTIVE,
        )
        decision = UniversalDecision(
            object_id=UUID("00000000-0000-0000-0000-000000009108"),
            decision_type=DecisionType.RECOMMENDATION,
        )
        action = UniversalAction(
            object_id=UUID("00000000-0000-0000-0000-000000009109"),
            action_type=ActionType.TASK,
        )
        inputs = ExecutionInputCollection(
            references=(
                ExecutionInputReference(ExecutionInputType.MEMORY, str(memory.object_id)),
                ExecutionInputReference(ExecutionInputType.KNOWLEDGE, str(knowledge.object_id)),
                ExecutionInputReference(ExecutionInputType.CONTEXT, str(context.object_id)),
                ExecutionInputReference(ExecutionInputType.REASONING, str(reasoning.object_id)),
                ExecutionInputReference(ExecutionInputType.DECISION, str(decision.object_id)),
                ExecutionInputReference(ExecutionInputType.ACTION, str(action.object_id)),
            )
        )
        execution = UniversalExecution(
            execution_type=ExecutionType.OBSERVATION,
            execution_inputs=inputs,
        )

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertTrue(reasoning.validate().is_valid)
        self.assertTrue(decision.validate().is_valid)
        self.assertTrue(action.validate().is_valid)
        self.assertTrue(execution.validate().is_valid)

    def test_no_resolution_execution_or_future_behavior_is_exposed(self) -> None:
        reference = self.build_reference()
        inputs = self.build_inputs()
        provenance = self.build_provenance()
        execution = UniversalExecution(
            execution_type=ExecutionType.ACTION,
            execution_inputs=inputs,
            execution_provenance=provenance,
        )
        forbidden_names = {
            "ai",
            "autonomous",
            "compute",
            "evaluate",
            "execute",
            "optimize",
            "orchestrate",
            "persist",
            "plan",
            "resolve",
            "schedule",
            "search",
            "workflow",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(reference))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(inputs))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(provenance))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(execution))))


if __name__ == "__main__":
    unittest.main()
