import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime
from uuid import UUID

from packages.context import ContextType, UniversalContext
from packages.decision import (
    DecisionConfidence,
    DecisionMetadata,
    DecisionOutcome,
    DecisionState,
    DecisionType,
    UniversalDecision,
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


class UniversalDecisionFrameworkTest(unittest.TestCase):
    def test_universal_decision_constructs_as_canonical_object(self) -> None:
        decision = UniversalDecision(
            decision_type=DecisionType.RECOMMENDATION,
            decision_state=DecisionState.PROPOSED,
            decision_outcome=DecisionOutcome.UNKNOWN,
            decision_confidence=DecisionConfidence(level="medium", rationale="documented"),
            decision_metadata=DecisionMetadata(values={"domain": "platform"}),
            metadata={"owner": "decision"},
            tags=["decision", "alpha"],
            created_by="codex",
        )

        self.assertIsInstance(decision, CanonicalObject)
        self.assertIsInstance(decision.object_id, UUID)
        self.assertEqual(decision.object_type, "UniversalDecision")
        self.assertEqual(decision.decision_type, DecisionType.RECOMMENDATION)
        self.assertEqual(decision.decision_state, DecisionState.PROPOSED)
        self.assertEqual(decision.decision_outcome, DecisionOutcome.UNKNOWN)
        self.assertEqual(decision.decision_confidence.level, "medium")
        self.assertEqual(decision.decision_metadata.to_dict(), {"domain": "platform"})
        self.assertEqual(decision.metadata.values["owner"], "decision")
        self.assertEqual(decision.tags, ("decision", "alpha"))
        self.assertEqual(decision.created_by, "codex")

    def test_decision_type_values_are_descriptive_only(self) -> None:
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

    def test_decision_state_values_are_lifecycle_values(self) -> None:
        self.assertEqual(
            {state.value for state in DecisionState},
            {"draft", "proposed", "confirmed", "archived"},
        )

    def test_decision_outcome_values_are_recorded_outcomes_only(self) -> None:
        self.assertEqual(
            {outcome.value for outcome in DecisionOutcome},
            {"accepted", "rejected", "deferred", "unknown"},
        )

    def test_decision_confidence_is_immutable_value_object(self) -> None:
        confidence = DecisionConfidence(level="high", rationale="certified")

        self.assertEqual(confidence.to_dict(), {"level": "high", "rationale": "certified"})
        with self.assertRaises(FrozenInstanceError):
            confidence.level = "low"

    def test_invalid_decision_confidence_level_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            DecisionConfidence(level="certain")

    def test_decision_metadata_is_immutable_and_deterministic(self) -> None:
        metadata = DecisionMetadata(values={"z": "last", "a": "first"})

        self.assertEqual(metadata.to_dict(), {"a": "first", "z": "last"})
        with self.assertRaises(FrozenInstanceError):
            metadata.values = ()

    def test_valid_decision_passes_platform_validation(self) -> None:
        decision = UniversalDecision(
            decision_type=DecisionType.APPROVAL,
            decision_state=DecisionState.CONFIRMED,
            decision_outcome=DecisionOutcome.ACCEPTED,
            decision_confidence=DecisionConfidence(level="high"),
        )

        result = decision.validate()

        self.assertIsInstance(result, ValidationResult)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_validation_reports_invalid_decision_shape(self) -> None:
        decision = UniversalDecision(decision_type=DecisionType.OBSERVATION)
        decision._decision_type = "observation"
        decision._decision_state = "confirmed"
        decision._decision_outcome = "accepted"
        decision._decision_confidence = "high"
        decision._decision_metadata = {"bad": "mutable"}

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
            },
        )

    def test_deterministic_payload_preserves_platform_and_decision_fields(self) -> None:
        timestamp = datetime.fromisoformat("2026-07-05T00:00:00+00:00")
        decision = UniversalDecision(
            object_id=UUID("00000000-0000-0000-0000-000000007001"),
            decision_type=DecisionType.SELECTION,
            decision_state=DecisionState.CONFIRMED,
            decision_outcome=DecisionOutcome.ACCEPTED,
            decision_confidence=DecisionConfidence(level="high", rationale="validated"),
            decision_metadata=DecisionMetadata(values={"z": "last", "a": "first"}),
            metadata={"owner": "platform"},
            tags=["alpha"],
            lifecycle_state=LifecycleState.ACTIVE,
            created_at=timestamp,
            updated_at=timestamp,
        )

        payload = decision.to_dict()

        self.assertEqual(payload, decision.to_dict())
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
        self.assertEqual(payload["object_type"], "UniversalDecision")
        self.assertEqual(payload["metadata"], {"owner": "platform"})
        self.assertEqual(payload["decision_type"], "selection")
        self.assertEqual(payload["decision_state"], "confirmed")
        self.assertEqual(payload["decision_outcome"], "accepted")
        self.assertEqual(payload["decision_confidence"], {"level": "high", "rationale": "validated"})
        self.assertEqual(payload["decision_metadata"], {"a": "first", "z": "last"})

    def test_lifecycle_registry_and_relationship_surfaces_remain_platform_core_behavior(self) -> None:
        decision = UniversalDecision(decision_type=DecisionType.DEFERMENT)
        registry = ObjectRegistry()
        relationship = Relationship(
            source_object_id=decision.object_id,
            target_object_id=UUID("00000000-0000-0000-0000-000000007002"),
            relationship_type=RelationshipType.REFERENCES,
        )

        registry.register(UniversalDecision)
        decision.transition_to(LifecycleState.ACTIVE)

        self.assertEqual(registry.lookup("UniversalDecision"), UniversalDecision)
        self.assertEqual(decision.lifecycle_state, LifecycleState.ACTIVE)
        self.assertEqual(decision.relationships, {})
        self.assertEqual(relationship.to_dict()["source_object_id"], str(decision.object_id))
        self.assertEqual(relationship.to_dict()["relationship_type"], "references")

    def test_object_serializer_handles_inherited_platform_fields(self) -> None:
        decision = UniversalDecision(
            object_id=UUID("00000000-0000-0000-0000-000000007003"),
            decision_type=DecisionType.REJECTION,
            metadata={"owner": "platform"},
        )

        payload = ObjectSerializer.serialize(decision)

        self.assertEqual(payload["object_type"], "UniversalDecision")
        self.assertEqual(payload["object_id"], "00000000-0000-0000-0000-000000007003")
        self.assertEqual(payload["metadata"], {"owner": "platform"})
        self.assertNotIn("decision_type", payload)

    def test_prior_foundation_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000007004"),
            memory_type=MemoryType.SEMANTIC,
            content="Decision framework coexists with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-alpha"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000007005"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000007006"),
            context_type=ContextType.ANALYTICAL,
        )
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000007007"),
            reasoning_type=ReasoningType.DEDUCTIVE,
        )
        decision = UniversalDecision(decision_type=DecisionType.OBSERVATION)

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertTrue(reasoning.validate().is_valid)
        self.assertTrue(decision.validate().is_valid)

    def test_no_decision_execution_or_future_behavior_is_exposed(self) -> None:
        decision = UniversalDecision(decision_type=DecisionType.RECOMMENDATION)
        forbidden_names = {
            "ai",
            "autonomous",
            "compute",
            "decide",
            "execute",
            "optimize",
            "persist",
            "plan",
            "rank",
            "resolve",
            "search",
            "workflow",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(decision))))


if __name__ == "__main__":
    unittest.main()
