import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime
from uuid import UUID

from packages.knowledge import (
    KnowledgeConfidence,
    KnowledgeMetadata,
    KnowledgeState,
    KnowledgeType,
    UniversalKnowledge,
)
from packages.objects import CanonicalObject, LifecycleState, ObjectSerializer


class UniversalKnowledgeFrameworkTest(unittest.TestCase):
    def test_universal_knowledge_constructs_as_canonical_object(self) -> None:
        knowledge = UniversalKnowledge(
            knowledge_type=KnowledgeType.CONCEPT,
            knowledge_state=KnowledgeState.SUPPORTED,
            confidence=KnowledgeConfidence(level="medium", rationale="documented"),
            knowledge_metadata=KnowledgeMetadata(values={"domain": "platform"}),
            metadata={"owner": "knowledge"},
            tags=["knowledge", "alpha"],
            created_by="codex",
        )

        self.assertIsInstance(knowledge, CanonicalObject)
        self.assertIsInstance(knowledge.object_id, UUID)
        self.assertEqual(knowledge.object_type, "UniversalKnowledge")
        self.assertEqual(knowledge.knowledge_type, KnowledgeType.CONCEPT)
        self.assertEqual(knowledge.knowledge_state, KnowledgeState.SUPPORTED)
        self.assertEqual(knowledge.confidence.level, "medium")
        self.assertEqual(knowledge.knowledge_metadata.to_dict(), {"domain": "platform"})
        self.assertEqual(knowledge.metadata.values["owner"], "knowledge")
        self.assertEqual(knowledge.tags, ("knowledge", "alpha"))
        self.assertEqual(knowledge.created_by, "codex")

    def test_knowledge_state_values_are_governance_values(self) -> None:
        self.assertEqual(
            {state.value for state in KnowledgeState},
            {"draft", "supported", "validated", "established", "superseded", "archived"},
        )

    def test_knowledge_confidence_is_immutable_value_object(self) -> None:
        confidence = KnowledgeConfidence(level="high", rationale="certified")

        self.assertEqual(confidence.to_dict(), {"level": "high", "rationale": "certified"})
        with self.assertRaises(FrozenInstanceError):
            confidence.level = "low"

    def test_invalid_knowledge_confidence_level_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            KnowledgeConfidence(level="certain")

    def test_knowledge_metadata_is_immutable_and_deterministic(self) -> None:
        metadata = KnowledgeMetadata(values={"z": "last", "a": "first"})

        self.assertEqual(metadata.to_dict(), {"a": "first", "z": "last"})
        with self.assertRaises(FrozenInstanceError):
            metadata.values = ()

    def test_valid_knowledge_passes_platform_validation(self) -> None:
        knowledge = UniversalKnowledge(
            knowledge_type=KnowledgeType.PRINCIPLE,
            knowledge_state=KnowledgeState.VALIDATED,
            confidence=KnowledgeConfidence(level="high"),
        )

        result = knowledge.validate()

        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_validation_reports_invalid_knowledge_type(self) -> None:
        knowledge = UniversalKnowledge(knowledge_type=KnowledgeType.FACT)
        knowledge._knowledge_type = "fact"

        result = knowledge.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "knowledge_type")

    def test_validation_reports_invalid_knowledge_state(self) -> None:
        knowledge = UniversalKnowledge(knowledge_type=KnowledgeType.FACT)
        knowledge._knowledge_state = "validated"

        result = knowledge.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "knowledge_state")

    def test_validation_reports_invalid_confidence(self) -> None:
        knowledge = UniversalKnowledge(knowledge_type=KnowledgeType.FACT)
        knowledge._confidence = "high"

        result = knowledge.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "confidence")

    def test_deterministic_payload_preserves_platform_and_knowledge_fields(self) -> None:
        timestamp = datetime.fromisoformat("2026-07-04T00:00:00+00:00")
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000000101"),
            knowledge_type=KnowledgeType.RULE,
            knowledge_state=KnowledgeState.ESTABLISHED,
            confidence=KnowledgeConfidence(level="high", rationale="validated"),
            knowledge_metadata=KnowledgeMetadata(values={"z": "last", "a": "first"}),
            metadata={"owner": "platform"},
            tags=["alpha"],
            lifecycle_state=LifecycleState.ACTIVE,
            created_at=timestamp,
            updated_at=timestamp,
        )

        payload = knowledge.to_dict()

        self.assertEqual(payload, knowledge.to_dict())
        self.assertEqual(payload["object_type"], "UniversalKnowledge")
        self.assertEqual(payload["metadata"], {"owner": "platform"})
        self.assertEqual(payload["knowledge_type"], "rule")
        self.assertEqual(payload["knowledge_state"], "established")
        self.assertEqual(payload["confidence"], {"level": "high", "rationale": "validated"})
        self.assertEqual(payload["knowledge_metadata"], {"a": "first", "z": "last"})

    def test_lifecycle_and_relationship_surfaces_remain_platform_core_behavior(self) -> None:
        knowledge = UniversalKnowledge(knowledge_type=KnowledgeType.OBSERVATION)

        knowledge.transition_to(LifecycleState.ACTIVE)

        self.assertEqual(knowledge.lifecycle_state, LifecycleState.ACTIVE)
        self.assertEqual(knowledge.relationships, {})

    def test_object_serializer_handles_inherited_platform_fields(self) -> None:
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000000102"),
            knowledge_type=KnowledgeType.FACT,
            metadata={"owner": "platform"},
        )

        payload = ObjectSerializer.serialize(knowledge)

        self.assertEqual(payload["object_type"], "UniversalKnowledge")
        self.assertEqual(payload["object_id"], "00000000-0000-0000-0000-000000000102")
        self.assertEqual(payload["metadata"], {"owner": "platform"})
        self.assertNotIn("knowledge_type", payload)

    def test_no_future_knowledge_behavior_is_exposed(self) -> None:
        knowledge = UniversalKnowledge(knowledge_type=KnowledgeType.CONCEPT)
        forbidden_names = {
            "infer",
            "reason",
            "search",
            "query",
            "persist",
            "store",
            "classify",
            "evidence",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(knowledge))))


if __name__ == "__main__":
    unittest.main()
