import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime
from uuid import UUID

from packages.context import ContextType, UniversalContext
from packages.knowledge import KnowledgeType, UniversalKnowledge
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import (
    CanonicalObject,
    LifecycleState,
    ObjectSerializer,
    Relationship,
    RelationshipType,
    ValidationResult,
)
from packages.reasoning import (
    ReasoningConfidence,
    ReasoningMetadata,
    ReasoningState,
    ReasoningType,
    UniversalReasoning,
)


class UniversalReasoningFrameworkTest(unittest.TestCase):
    def test_universal_reasoning_constructs_as_canonical_object(self) -> None:
        reasoning = UniversalReasoning(
            reasoning_type=ReasoningType.DEDUCTIVE,
            reasoning_state=ReasoningState.EVALUATED,
            reasoning_confidence=ReasoningConfidence(level="medium", rationale="documented"),
            reasoning_metadata=ReasoningMetadata(values={"domain": "platform"}),
            metadata={"owner": "reasoning"},
            tags=["reasoning", "alpha"],
            created_by="codex",
        )

        self.assertIsInstance(reasoning, CanonicalObject)
        self.assertIsInstance(reasoning.object_id, UUID)
        self.assertEqual(reasoning.object_type, "UniversalReasoning")
        self.assertEqual(reasoning.reasoning_type, ReasoningType.DEDUCTIVE)
        self.assertEqual(reasoning.reasoning_state, ReasoningState.EVALUATED)
        self.assertEqual(reasoning.reasoning_confidence.level, "medium")
        self.assertEqual(reasoning.reasoning_metadata.to_dict(), {"domain": "platform"})
        self.assertEqual(reasoning.metadata.values["owner"], "reasoning")
        self.assertEqual(reasoning.tags, ("reasoning", "alpha"))
        self.assertEqual(reasoning.created_by, "codex")

    def test_reasoning_type_values_are_descriptive_only(self) -> None:
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

    def test_reasoning_state_values_are_governance_values(self) -> None:
        self.assertEqual(
            {state.value for state in ReasoningState},
            {"draft", "evaluated", "validated", "accepted", "superseded", "archived"},
        )

    def test_reasoning_confidence_is_immutable_value_object(self) -> None:
        confidence = ReasoningConfidence(level="high", rationale="certified")

        self.assertEqual(confidence.to_dict(), {"level": "high", "rationale": "certified"})
        with self.assertRaises(FrozenInstanceError):
            confidence.level = "low"

    def test_invalid_reasoning_confidence_level_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            ReasoningConfidence(level="certain")

    def test_reasoning_metadata_is_immutable_and_deterministic(self) -> None:
        metadata = ReasoningMetadata(values={"z": "last", "a": "first"})

        self.assertEqual(metadata.to_dict(), {"a": "first", "z": "last"})
        with self.assertRaises(FrozenInstanceError):
            metadata.values = ()

    def test_valid_reasoning_passes_platform_validation(self) -> None:
        reasoning = UniversalReasoning(
            reasoning_type=ReasoningType.CAUSAL,
            reasoning_state=ReasoningState.VALIDATED,
            reasoning_confidence=ReasoningConfidence(level="high"),
        )

        result = reasoning.validate()

        self.assertIsInstance(result, ValidationResult)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_validation_reports_invalid_reasoning_shape(self) -> None:
        reasoning = UniversalReasoning(reasoning_type=ReasoningType.CONSISTENCY)
        reasoning._reasoning_type = "consistency"
        reasoning._reasoning_state = "validated"
        reasoning._reasoning_confidence = "high"
        reasoning._reasoning_metadata = {"bad": "mutable"}

        result = reasoning.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "reasoning_type",
                "reasoning_state",
                "reasoning_confidence",
                "reasoning_metadata",
            },
        )

    def test_deterministic_payload_preserves_platform_and_reasoning_fields(self) -> None:
        timestamp = datetime.fromisoformat("2026-07-05T00:00:00+00:00")
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000006001"),
            reasoning_type=ReasoningType.COMPARATIVE,
            reasoning_state=ReasoningState.ACCEPTED,
            reasoning_confidence=ReasoningConfidence(level="high", rationale="validated"),
            reasoning_metadata=ReasoningMetadata(values={"z": "last", "a": "first"}),
            metadata={"owner": "platform"},
            tags=["alpha"],
            lifecycle_state=LifecycleState.ACTIVE,
            created_at=timestamp,
            updated_at=timestamp,
        )

        payload = reasoning.to_dict()

        self.assertEqual(payload, reasoning.to_dict())
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
        self.assertEqual(payload["object_type"], "UniversalReasoning")
        self.assertEqual(payload["metadata"], {"owner": "platform"})
        self.assertEqual(payload["reasoning_type"], "comparative")
        self.assertEqual(payload["reasoning_state"], "accepted")
        self.assertEqual(payload["reasoning_confidence"], {"level": "high", "rationale": "validated"})
        self.assertEqual(payload["reasoning_metadata"], {"a": "first", "z": "last"})

    def test_lifecycle_and_relationship_surfaces_remain_platform_core_behavior(self) -> None:
        reasoning = UniversalReasoning(reasoning_type=ReasoningType.TEMPORAL)
        relationship = Relationship(
            source_object_id=reasoning.object_id,
            target_object_id=UUID("00000000-0000-0000-0000-000000006002"),
            relationship_type=RelationshipType.REFERENCES,
        )

        reasoning.transition_to(LifecycleState.ACTIVE)

        self.assertEqual(reasoning.lifecycle_state, LifecycleState.ACTIVE)
        self.assertEqual(reasoning.relationships, {})
        self.assertEqual(relationship.to_dict()["source_object_id"], str(reasoning.object_id))
        self.assertEqual(relationship.to_dict()["relationship_type"], "references")

    def test_object_serializer_handles_inherited_platform_fields(self) -> None:
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000006003"),
            reasoning_type=ReasoningType.ABDUCTIVE,
            metadata={"owner": "platform"},
        )

        payload = ObjectSerializer.serialize(reasoning)

        self.assertEqual(payload["object_type"], "UniversalReasoning")
        self.assertEqual(payload["object_id"], "00000000-0000-0000-0000-000000006003")
        self.assertEqual(payload["metadata"], {"owner": "platform"})
        self.assertNotIn("reasoning_type", payload)

    def test_memory_knowledge_and_context_foundation_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000006004"),
            memory_type=MemoryType.SEMANTIC,
            content="Reasoning framework coexists with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-alpha"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000006005"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000006006"),
            context_type=ContextType.ANALYTICAL,
        )
        reasoning = UniversalReasoning(reasoning_type=ReasoningType.DEPENDENCY)

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertTrue(reasoning.validate().is_valid)

    def test_no_reasoning_execution_or_future_behavior_is_exposed(self) -> None:
        reasoning = UniversalReasoning(reasoning_type=ReasoningType.INDUCTIVE)
        forbidden_names = {
            "ai",
            "conclude",
            "decide",
            "execute",
            "infer",
            "plan",
            "persist",
            "reason",
            "search",
            "workflow",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(reasoning))))


if __name__ == "__main__":
    unittest.main()
