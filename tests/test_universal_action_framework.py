import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime
from uuid import UUID

from packages.action import (
    ActionConfidence,
    ActionMetadata,
    ActionOutcome,
    ActionState,
    ActionType,
    UniversalAction,
)
from packages.context import ContextType, UniversalContext
from packages.decision import DecisionType, UniversalDecision
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


class UniversalActionFrameworkTest(unittest.TestCase):
    def test_universal_action_constructs_as_canonical_object(self) -> None:
        action = UniversalAction(
            action_type=ActionType.TASK,
            action_state=ActionState.PROPOSED,
            action_outcome=ActionOutcome.UNKNOWN,
            action_confidence=ActionConfidence(level="medium", rationale="documented"),
            action_metadata=ActionMetadata(values={"domain": "platform"}),
            metadata={"owner": "action"},
            tags=["action", "alpha"],
            created_by="codex",
        )

        self.assertIsInstance(action, CanonicalObject)
        self.assertIsInstance(action.object_id, UUID)
        self.assertEqual(action.object_type, "UniversalAction")
        self.assertEqual(action.action_type, ActionType.TASK)
        self.assertEqual(action.action_state, ActionState.PROPOSED)
        self.assertEqual(action.action_outcome, ActionOutcome.UNKNOWN)
        self.assertEqual(action.action_confidence.level, "medium")
        self.assertEqual(action.action_metadata.to_dict(), {"domain": "platform"})
        self.assertEqual(action.metadata.values["owner"], "action")
        self.assertEqual(action.tags, ("action", "alpha"))
        self.assertEqual(action.created_by, "codex")

    def test_action_type_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {action_type.value for action_type in ActionType},
            {
                "task",
                "review",
                "approval",
                "notification",
                "command",
                "observation",
            },
        )

    def test_action_state_values_are_descriptive_lifecycle_values(self) -> None:
        self.assertEqual(
            {state.value for state in ActionState},
            {"draft", "proposed", "ready", "completed", "archived"},
        )

    def test_action_outcome_values_are_recorded_outcomes_only(self) -> None:
        self.assertEqual(
            {outcome.value for outcome in ActionOutcome},
            {"succeeded", "failed", "deferred", "cancelled", "unknown"},
        )

    def test_action_confidence_is_immutable_value_object(self) -> None:
        confidence = ActionConfidence(level="high", rationale="certified")

        self.assertEqual(confidence.to_dict(), {"level": "high", "rationale": "certified"})
        with self.assertRaises(FrozenInstanceError):
            confidence.level = "low"

    def test_invalid_action_confidence_level_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            ActionConfidence(level="certain")

    def test_action_metadata_is_immutable_and_deterministic(self) -> None:
        metadata = ActionMetadata(values={"z": "last", "a": "first"})

        self.assertEqual(metadata.to_dict(), {"a": "first", "z": "last"})
        with self.assertRaises(FrozenInstanceError):
            metadata.values = ()

    def test_valid_action_passes_platform_validation(self) -> None:
        action = UniversalAction(
            action_type=ActionType.APPROVAL,
            action_state=ActionState.READY,
            action_outcome=ActionOutcome.UNKNOWN,
            action_confidence=ActionConfidence(level="high"),
        )

        result = action.validate()

        self.assertIsInstance(result, ValidationResult)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_validation_reports_invalid_action_shape(self) -> None:
        action = UniversalAction(action_type=ActionType.OBSERVATION)
        action._action_type = "observation"
        action._action_state = "ready"
        action._action_outcome = "succeeded"
        action._action_confidence = "high"
        action._action_metadata = {"bad": "mutable"}

        result = action.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "action_type",
                "action_state",
                "action_outcome",
                "action_confidence",
                "action_metadata",
            },
        )

    def test_deterministic_payload_preserves_platform_and_action_fields(self) -> None:
        timestamp = datetime.fromisoformat("2026-07-05T00:00:00+00:00")
        action = UniversalAction(
            object_id=UUID("00000000-0000-0000-0000-000000008001"),
            action_type=ActionType.REVIEW,
            action_state=ActionState.COMPLETED,
            action_outcome=ActionOutcome.SUCCEEDED,
            action_confidence=ActionConfidence(level="high", rationale="validated"),
            action_metadata=ActionMetadata(values={"z": "last", "a": "first"}),
            metadata={"owner": "platform"},
            tags=["alpha"],
            lifecycle_state=LifecycleState.ACTIVE,
            created_at=timestamp,
            updated_at=timestamp,
        )

        payload = action.to_dict()

        self.assertEqual(payload, action.to_dict())
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
                "action_type",
                "action_state",
                "action_outcome",
                "action_confidence",
                "action_metadata",
            ],
        )
        self.assertEqual(payload["object_type"], "UniversalAction")
        self.assertEqual(payload["metadata"], {"owner": "platform"})
        self.assertEqual(payload["action_type"], "review")
        self.assertEqual(payload["action_state"], "completed")
        self.assertEqual(payload["action_outcome"], "succeeded")
        self.assertEqual(payload["action_confidence"], {"level": "high", "rationale": "validated"})
        self.assertEqual(payload["action_metadata"], {"a": "first", "z": "last"})

    def test_lifecycle_registry_and_relationship_surfaces_remain_platform_core_behavior(self) -> None:
        action = UniversalAction(action_type=ActionType.NOTIFICATION)
        registry = ObjectRegistry()
        relationship = Relationship(
            source_object_id=action.object_id,
            target_object_id=UUID("00000000-0000-0000-0000-000000008002"),
            relationship_type=RelationshipType.REFERENCES,
        )

        registry.register(UniversalAction)
        action.transition_to(LifecycleState.ACTIVE)

        self.assertEqual(registry.lookup("UniversalAction"), UniversalAction)
        self.assertEqual(action.lifecycle_state, LifecycleState.ACTIVE)
        self.assertEqual(action.relationships, {})
        self.assertEqual(relationship.to_dict()["source_object_id"], str(action.object_id))
        self.assertEqual(relationship.to_dict()["relationship_type"], "references")

    def test_object_serializer_handles_inherited_platform_fields(self) -> None:
        action = UniversalAction(
            object_id=UUID("00000000-0000-0000-0000-000000008003"),
            action_type=ActionType.COMMAND,
            metadata={"owner": "platform"},
        )

        payload = ObjectSerializer.serialize(action)

        self.assertEqual(payload["object_type"], "UniversalAction")
        self.assertEqual(payload["object_id"], "00000000-0000-0000-0000-000000008003")
        self.assertEqual(payload["metadata"], {"owner": "platform"})
        self.assertNotIn("action_type", payload)

    def test_existing_foundation_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000008004"),
            memory_type=MemoryType.SEMANTIC,
            content="Action framework coexists with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-alpha"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000008005"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000008006"),
            context_type=ContextType.ANALYTICAL,
        )
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000008007"),
            reasoning_type=ReasoningType.DEDUCTIVE,
        )
        decision = UniversalDecision(
            object_id=UUID("00000000-0000-0000-0000-000000008008"),
            decision_type=DecisionType.RECOMMENDATION,
        )
        action = UniversalAction(action_type=ActionType.OBSERVATION)

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertTrue(reasoning.validate().is_valid)
        self.assertTrue(decision.validate().is_valid)
        self.assertTrue(action.validate().is_valid)

    def test_no_action_execution_or_future_behavior_is_exposed(self) -> None:
        action = UniversalAction(action_type=ActionType.TASK)
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

        self.assertTrue(forbidden_names.isdisjoint(set(dir(action))))


if __name__ == "__main__":
    unittest.main()
