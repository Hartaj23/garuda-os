import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime
from uuid import UUID

from packages.context import (
    ContextConfidence,
    ContextMetadata,
    ContextState,
    ContextType,
    UniversalContext,
)
from packages.knowledge import KnowledgeType, UniversalKnowledge
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import CanonicalObject, LifecycleState, ObjectSerializer


class UniversalContextFrameworkTest(unittest.TestCase):
    def test_universal_context_constructs_as_canonical_object(self) -> None:
        context = UniversalContext(
            context_type=ContextType.CONVERSATIONAL,
            context_state=ContextState.ASSEMBLED,
            context_confidence=ContextConfidence(level="medium", rationale="bounded"),
            context_metadata=ContextMetadata(values={"scope": "conversation"}),
            metadata={"owner": "context"},
            tags=["context", "alpha"],
            created_by="codex",
        )

        self.assertIsInstance(context, CanonicalObject)
        self.assertIsInstance(context.object_id, UUID)
        self.assertEqual(context.object_type, "UniversalContext")
        self.assertEqual(context.context_type, ContextType.CONVERSATIONAL)
        self.assertEqual(context.context_state, ContextState.ASSEMBLED)
        self.assertEqual(context.context_confidence.level, "medium")
        self.assertEqual(context.context_metadata.to_dict(), {"scope": "conversation"})
        self.assertEqual(context.metadata.values["owner"], "context")
        self.assertEqual(context.tags, ("context", "alpha"))
        self.assertEqual(context.created_by, "codex")

    def test_context_type_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {context_type.value for context_type in ContextType},
            {"conversational", "operational", "analytical", "environmental", "temporal"},
        )

    def test_context_state_values_are_governance_values(self) -> None:
        self.assertEqual(
            {state.value for state in ContextState},
            {"draft", "assembled", "validated", "active", "archived"},
        )

    def test_context_confidence_is_immutable_value_object(self) -> None:
        confidence = ContextConfidence(level="high", rationale="complete")

        self.assertEqual(confidence.to_dict(), {"level": "high", "rationale": "complete"})
        with self.assertRaises(FrozenInstanceError):
            confidence.level = "low"

    def test_invalid_context_confidence_level_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            ContextConfidence(level="certain")

    def test_context_metadata_is_immutable_and_deterministic(self) -> None:
        metadata = ContextMetadata(values={"z": "last", "a": "first"})

        self.assertEqual(metadata.to_dict(), {"a": "first", "z": "last"})
        with self.assertRaises(FrozenInstanceError):
            metadata.values = ()

    def test_valid_context_passes_platform_validation(self) -> None:
        context = UniversalContext(
            context_type=ContextType.ANALYTICAL,
            context_state=ContextState.VALIDATED,
            context_confidence=ContextConfidence(level="high"),
        )

        result = context.validate()

        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_validation_reports_invalid_context_type(self) -> None:
        context = UniversalContext(context_type=ContextType.OPERATIONAL)
        context._context_type = "operational"

        result = context.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "context_type")

    def test_validation_reports_invalid_context_state(self) -> None:
        context = UniversalContext(context_type=ContextType.OPERATIONAL)
        context._context_state = "active"

        result = context.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "context_state")

    def test_validation_reports_invalid_confidence_and_metadata(self) -> None:
        context = UniversalContext(context_type=ContextType.OPERATIONAL)
        context._context_confidence = "high"
        context._context_metadata = {"scope": "bad"}

        result = context.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {"context_confidence", "context_metadata"},
        )

    def test_deterministic_payload_preserves_platform_and_context_fields(self) -> None:
        timestamp = datetime.fromisoformat("2026-07-04T00:00:00+00:00")
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000000901"),
            context_type=ContextType.TEMPORAL,
            context_state=ContextState.ACTIVE,
            context_confidence=ContextConfidence(level="high", rationale="bounded"),
            context_metadata=ContextMetadata(values={"z": "last", "a": "first"}),
            metadata={"owner": "platform"},
            tags=["alpha"],
            lifecycle_state=LifecycleState.ACTIVE,
            created_at=timestamp,
            updated_at=timestamp,
        )

        payload = context.to_dict()

        self.assertEqual(payload, context.to_dict())
        mission_alpha_keys = [
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
            "context_type",
            "context_state",
            "context_confidence",
            "context_metadata",
        ]
        self.assertEqual(list(payload.keys())[: len(mission_alpha_keys)], mission_alpha_keys)
        self.assertEqual(list(payload.keys())[-2:], ["context_source", "context_scope"])
        self.assertEqual(payload["object_type"], "UniversalContext")
        self.assertEqual(payload["metadata"], {"owner": "platform"})
        self.assertEqual(payload["context_type"], "temporal")
        self.assertEqual(payload["context_state"], "active")
        self.assertEqual(payload["context_confidence"], {"level": "high", "rationale": "bounded"})
        self.assertEqual(payload["context_metadata"], {"a": "first", "z": "last"})
        self.assertIsNone(payload["context_source"])
        self.assertIsNone(payload["context_scope"])

    def test_lifecycle_and_relationship_surfaces_remain_platform_core_behavior(self) -> None:
        context = UniversalContext(context_type=ContextType.ENVIRONMENTAL)

        context.transition_to(LifecycleState.ACTIVE)

        self.assertEqual(context.lifecycle_state, LifecycleState.ACTIVE)
        self.assertEqual(context.relationships, {})

    def test_object_serializer_handles_inherited_platform_fields(self) -> None:
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000000902"),
            context_type=ContextType.OPERATIONAL,
            metadata={"owner": "platform"},
        )

        payload = ObjectSerializer.serialize(context)

        self.assertEqual(payload["object_type"], "UniversalContext")
        self.assertEqual(payload["object_id"], "00000000-0000-0000-0000-000000000902")
        self.assertEqual(payload["metadata"], {"owner": "platform"})
        self.assertNotIn("context_type", payload)

    def test_memory_and_knowledge_foundation_interoperability_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000000903"),
            memory_type=MemoryType.SEMANTIC,
            content="Context Foundation coexists with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-alpha"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000000904"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(context_type=ContextType.ANALYTICAL)

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)

    def test_no_future_context_behavior_is_exposed(self) -> None:
        context = UniversalContext(context_type=ContextType.CONVERSATIONAL)
        forbidden_names = {
            "ai",
            "compose",
            "infer",
            "persist",
            "prioritize",
            "reason",
            "search",
            "select",
            "workflow",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(context))))


if __name__ == "__main__":
    unittest.main()
