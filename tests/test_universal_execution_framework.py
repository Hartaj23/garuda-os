import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime
from uuid import UUID

from packages.action import ActionType, UniversalAction
from packages.context import ContextType, UniversalContext
from packages.decision import DecisionType, UniversalDecision
from packages.execution import (
    ExecutionConfidence,
    ExecutionMetadata,
    ExecutionOutcome,
    ExecutionState,
    ExecutionType,
    UniversalExecution,
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


class UniversalExecutionFrameworkTest(unittest.TestCase):
    def test_universal_execution_constructs_as_canonical_object(self) -> None:
        execution = UniversalExecution(
            execution_type=ExecutionType.ACTION,
            execution_state=ExecutionState.PLANNED,
            execution_outcome=ExecutionOutcome.UNKNOWN,
            execution_confidence=ExecutionConfidence(level="medium", rationale="documented"),
            execution_metadata=ExecutionMetadata(values={"domain": "platform"}),
            metadata={"owner": "execution"},
            tags=["execution", "alpha"],
            created_by="codex",
        )

        self.assertIsInstance(execution, CanonicalObject)
        self.assertIsInstance(execution.object_id, UUID)
        self.assertEqual(execution.object_type, "UniversalExecution")
        self.assertEqual(execution.execution_type, ExecutionType.ACTION)
        self.assertEqual(execution.execution_state, ExecutionState.PLANNED)
        self.assertEqual(execution.execution_outcome, ExecutionOutcome.UNKNOWN)
        self.assertEqual(execution.execution_confidence.level, "medium")
        self.assertEqual(execution.execution_metadata.to_dict(), {"domain": "platform"})
        self.assertEqual(execution.metadata.values["owner"], "execution")
        self.assertEqual(execution.tags, ("execution", "alpha"))
        self.assertEqual(execution.created_by, "codex")

    def test_execution_type_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {execution_type.value for execution_type in ExecutionType},
            {"action", "workflow", "procedure", "command", "review", "observation"},
        )

    def test_execution_state_values_are_descriptive_lifecycle_values(self) -> None:
        self.assertEqual(
            {state.value for state in ExecutionState},
            {"draft", "planned", "ready", "completed", "archived"},
        )

    def test_execution_outcome_values_are_recorded_outcomes_only(self) -> None:
        self.assertEqual(
            {outcome.value for outcome in ExecutionOutcome},
            {"succeeded", "failed", "cancelled", "unknown"},
        )

    def test_execution_confidence_is_immutable_value_object(self) -> None:
        confidence = ExecutionConfidence(level="high", rationale="certified")

        self.assertEqual(confidence.to_dict(), {"level": "high", "rationale": "certified"})
        with self.assertRaises(FrozenInstanceError):
            confidence.level = "low"

    def test_invalid_execution_confidence_level_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            ExecutionConfidence(level="certain")

    def test_execution_metadata_is_immutable_and_deterministic(self) -> None:
        metadata = ExecutionMetadata(values={"z": "last", "a": "first"})

        self.assertEqual(metadata.to_dict(), {"a": "first", "z": "last"})
        with self.assertRaises(FrozenInstanceError):
            metadata.values = ()

    def test_valid_execution_passes_platform_validation(self) -> None:
        execution = UniversalExecution(
            execution_type=ExecutionType.PROCEDURE,
            execution_state=ExecutionState.READY,
            execution_outcome=ExecutionOutcome.UNKNOWN,
            execution_confidence=ExecutionConfidence(level="high"),
        )

        result = execution.validate()

        self.assertIsInstance(result, ValidationResult)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_validation_reports_invalid_execution_shape(self) -> None:
        execution = UniversalExecution(execution_type=ExecutionType.OBSERVATION)
        execution._execution_type = "observation"
        execution._execution_state = "ready"
        execution._execution_outcome = "succeeded"
        execution._execution_confidence = "high"
        execution._execution_metadata = {"bad": "mutable"}

        result = execution.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "execution_type",
                "execution_state",
                "execution_outcome",
                "execution_confidence",
                "execution_metadata",
            },
        )

    def test_deterministic_payload_preserves_platform_and_execution_fields(self) -> None:
        timestamp = datetime.fromisoformat("2026-07-06T00:00:00+00:00")
        execution = UniversalExecution(
            object_id=UUID("00000000-0000-0000-0000-000000009001"),
            execution_type=ExecutionType.REVIEW,
            execution_state=ExecutionState.COMPLETED,
            execution_outcome=ExecutionOutcome.SUCCEEDED,
            execution_confidence=ExecutionConfidence(level="high", rationale="validated"),
            execution_metadata=ExecutionMetadata(values={"z": "last", "a": "first"}),
            metadata={"owner": "platform"},
            tags=["alpha"],
            lifecycle_state=LifecycleState.ACTIVE,
            created_at=timestamp,
            updated_at=timestamp,
        )

        payload = execution.to_dict()

        self.assertEqual(payload, execution.to_dict())
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
                "execution_type",
                "execution_state",
                "execution_outcome",
                "execution_confidence",
                "execution_metadata",
            ],
        )
        self.assertEqual(payload["object_type"], "UniversalExecution")
        self.assertEqual(payload["metadata"], {"owner": "platform"})
        self.assertEqual(payload["execution_type"], "review")
        self.assertEqual(payload["execution_state"], "completed")
        self.assertEqual(payload["execution_outcome"], "succeeded")
        self.assertEqual(
            payload["execution_confidence"],
            {"level": "high", "rationale": "validated"},
        )
        self.assertEqual(payload["execution_metadata"], {"a": "first", "z": "last"})

    def test_lifecycle_registry_and_relationship_surfaces_remain_platform_core_behavior(self) -> None:
        execution = UniversalExecution(execution_type=ExecutionType.COMMAND)
        registry = ObjectRegistry()
        relationship = Relationship(
            source_object_id=execution.object_id,
            target_object_id=UUID("00000000-0000-0000-0000-000000009002"),
            relationship_type=RelationshipType.REFERENCES,
        )

        registry.register(UniversalExecution)
        execution.transition_to(LifecycleState.ACTIVE)

        self.assertEqual(registry.lookup("UniversalExecution"), UniversalExecution)
        self.assertEqual(execution.lifecycle_state, LifecycleState.ACTIVE)
        self.assertEqual(execution.relationships, {})
        self.assertEqual(relationship.to_dict()["source_object_id"], str(execution.object_id))
        self.assertEqual(relationship.to_dict()["relationship_type"], "references")

    def test_object_serializer_handles_inherited_platform_fields(self) -> None:
        execution = UniversalExecution(
            object_id=UUID("00000000-0000-0000-0000-000000009003"),
            execution_type=ExecutionType.ACTION,
            metadata={"owner": "platform"},
        )

        payload = ObjectSerializer.serialize(execution)

        self.assertEqual(payload["object_type"], "UniversalExecution")
        self.assertEqual(payload["object_id"], "00000000-0000-0000-0000-000000009003")
        self.assertEqual(payload["metadata"], {"owner": "platform"})
        self.assertNotIn("execution_type", payload)

    def test_existing_foundation_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000009004"),
            memory_type=MemoryType.SEMANTIC,
            content="Execution framework coexists with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-alpha"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000009005"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000009006"),
            context_type=ContextType.ANALYTICAL,
        )
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000009007"),
            reasoning_type=ReasoningType.DEDUCTIVE,
        )
        decision = UniversalDecision(
            object_id=UUID("00000000-0000-0000-0000-000000009008"),
            decision_type=DecisionType.RECOMMENDATION,
        )
        action = UniversalAction(
            object_id=UUID("00000000-0000-0000-0000-000000009009"),
            action_type=ActionType.TASK,
        )
        execution = UniversalExecution(execution_type=ExecutionType.OBSERVATION)

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertTrue(reasoning.validate().is_valid)
        self.assertTrue(decision.validate().is_valid)
        self.assertTrue(action.validate().is_valid)
        self.assertTrue(execution.validate().is_valid)

    def test_no_execution_or_future_behavior_is_exposed(self) -> None:
        execution = UniversalExecution(execution_type=ExecutionType.ACTION)
        forbidden_names = {
            "ai",
            "autonomous",
            "compute",
            "execute",
            "optimize",
            "orchestrate",
            "persist",
            "plan",
            "rank",
            "resolve",
            "schedule",
            "search",
            "workflow",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(execution))))


if __name__ == "__main__":
    unittest.main()
