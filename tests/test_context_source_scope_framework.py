import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime
from uuid import UUID

from packages.context import (
    ContextScope,
    ContextScopeType,
    ContextSource,
    ContextSourceType,
    ContextType,
    UniversalContext,
    validate_context_scope,
    validate_context_source,
)
from packages.knowledge import KnowledgeType, UniversalKnowledge
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import ObjectSerializer


class ContextSourceScopeFrameworkTest(unittest.TestCase):
    def build_source(self) -> ContextSource:
        return ContextSource(
            source_type=ContextSourceType.KNOWLEDGE,
            source_identifier="knowledge:00000000-0000-0000-0000-000000001001",
            created_at=datetime.fromisoformat("2026-07-04T00:00:00+00:00"),
            source_metadata={"z": "last", "a": "first"},
        )

    def build_scope(self) -> ContextScope:
        return ContextScope(
            scope_type=ContextScopeType.TASK,
            boundary_identifier="task:mission-bravo",
            lifetime_metadata={"expires": "manual"},
            scope_metadata={"z": "last", "a": "first"},
        )

    def test_context_source_type_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {source_type.value for source_type in ContextSourceType},
            {"memory", "knowledge", "user_input", "system_state", "external_reference"},
        )

    def test_context_source_constructs_immutable_deterministic_payload(self) -> None:
        source = self.build_source()

        self.assertEqual(
            source.to_dict(),
            {
                "source_type": "knowledge",
                "source_identifier": "knowledge:00000000-0000-0000-0000-000000001001",
                "created_at": "2026-07-04T00:00:00+00:00",
                "source_metadata": {"a": "first", "z": "last"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            source.source_identifier = "knowledge:changed"

    def test_context_scope_type_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {scope_type.value for scope_type in ContextScopeType},
            {"local", "session", "task", "workflow", "global"},
        )

    def test_context_scope_constructs_immutable_deterministic_payload(self) -> None:
        scope = self.build_scope()

        self.assertEqual(
            scope.to_dict(),
            {
                "scope_type": "task",
                "boundary_identifier": "task:mission-bravo",
                "lifetime_metadata": {"expires": "manual"},
                "scope_metadata": {"a": "first", "z": "last"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            scope.boundary_identifier = "task:changed"

    def test_universal_context_integrates_optional_source_and_scope(self) -> None:
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000001002"),
            context_type=ContextType.ANALYTICAL,
            context_source=self.build_source(),
            context_scope=self.build_scope(),
        )

        payload = context.to_dict()

        self.assertTrue(context.validate().is_valid)
        self.assertEqual(payload["context_source"], self.build_source().to_dict())
        self.assertEqual(payload["context_scope"], self.build_scope().to_dict())
        self.assertEqual(
            list(payload.keys())[-2:],
            ["context_source", "context_scope"],
        )

    def test_mission_alpha_constructor_compatibility_is_preserved(self) -> None:
        context = UniversalContext(context_type=ContextType.CONVERSATIONAL)
        payload = context.to_dict()

        self.assertTrue(context.validate().is_valid)
        self.assertEqual(payload["context_type"], "conversational")
        self.assertEqual(payload["context_state"], "draft")
        self.assertEqual(payload["context_confidence"], {"level": "unknown", "rationale": None})
        self.assertEqual(payload["context_metadata"], {})
        self.assertIsNone(payload["context_source"])
        self.assertIsNone(payload["context_scope"])

    def test_context_source_validation_reports_invalid_shape(self) -> None:
        source = self.build_source()
        object.__setattr__(source, "source_type", "knowledge")
        object.__setattr__(source, "source_identifier", "")
        object.__setattr__(source, "source_metadata", {"bad": "mutable"})

        result = validate_context_source(source)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "context_source.source_type",
                "context_source.source_identifier",
                "context_source.source_metadata",
            },
        )

    def test_context_scope_validation_reports_invalid_shape(self) -> None:
        scope = self.build_scope()
        object.__setattr__(scope, "scope_type", "task")
        object.__setattr__(scope, "boundary_identifier", "")
        object.__setattr__(scope, "lifetime_metadata", {"bad": "mutable"})
        object.__setattr__(scope, "scope_metadata", {"bad": "mutable"})

        result = validate_context_scope(scope)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "context_scope.scope_type",
                "context_scope.boundary_identifier",
                "context_scope.lifetime_metadata",
                "context_scope.scope_metadata",
            },
        )

    def test_universal_context_validation_reports_invalid_source_and_scope(self) -> None:
        context = UniversalContext(context_type=ContextType.OPERATIONAL)
        context._context_source = "source"
        context._context_scope = "scope"

        result = context.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {"context_source", "context_scope"},
        )

    def test_platform_core_serialization_compatibility_is_preserved(self) -> None:
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000001003"),
            context_type=ContextType.OPERATIONAL,
            context_source=self.build_source(),
            context_scope=self.build_scope(),
        )

        payload = ObjectSerializer.serialize(context)

        self.assertEqual(payload["object_type"], "UniversalContext")
        self.assertEqual(payload["object_id"], "00000000-0000-0000-0000-000000001003")
        self.assertNotIn("context_source", payload)
        self.assertNotIn("context_scope", payload)

    def test_memory_and_knowledge_foundation_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000001004"),
            memory_type=MemoryType.SEMANTIC,
            content="Context source may use opaque memory identifiers.",
            source=MemorySource(source_type="test", source_identifier="mission-bravo"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000001005"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            context_type=ContextType.ANALYTICAL,
            context_source=ContextSource(
                source_type=ContextSourceType.MEMORY,
                source_identifier=str(memory.object_id),
            ),
            context_scope=ContextScope(
                scope_type=ContextScopeType.LOCAL,
                boundary_identifier=str(knowledge.object_id),
            ),
        )

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)

    def test_no_resolution_boundary_or_future_behavior_is_exposed(self) -> None:
        source = self.build_source()
        scope = self.build_scope()
        context = UniversalContext(
            context_type=ContextType.ANALYTICAL,
            context_source=source,
            context_scope=scope,
        )
        forbidden_names = {
            "ai",
            "compose",
            "enforce",
            "infer",
            "persist",
            "prioritize",
            "reason",
            "resolve",
            "retrieve",
            "search",
            "select",
            "workflow",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(source))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(scope))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(context))))


if __name__ == "__main__":
    unittest.main()
