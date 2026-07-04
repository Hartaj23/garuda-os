import unittest
from datetime import datetime
from uuid import UUID

from packages.context import (
    ContextConfidence,
    ContextMetadata,
    ContextScope,
    ContextScopeType,
    ContextSource,
    ContextSourceType,
    ContextState,
    ContextType,
    UniversalContext,
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


class ContextSerializationValidationCertificationTest(unittest.TestCase):
    def build_source(self) -> ContextSource:
        return ContextSource(
            source_type=ContextSourceType.KNOWLEDGE,
            source_identifier="knowledge:00000000-0000-0000-0000-000000001101",
            created_at=datetime.fromisoformat("2026-07-04T00:00:00+00:00"),
            source_metadata={"z": "last", "a": "first"},
        )

    def build_scope(self) -> ContextScope:
        return ContextScope(
            scope_type=ContextScopeType.TASK,
            boundary_identifier="task:context-certification",
            lifetime_metadata={"expires": "manual"},
            scope_metadata={"z": "last", "a": "first"},
        )

    def build_context(self) -> UniversalContext:
        timestamp = datetime.fromisoformat("2026-07-04T00:00:00+00:00")
        return UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000001102"),
            context_type=ContextType.ANALYTICAL,
            context_state=ContextState.VALIDATED,
            context_confidence=ContextConfidence(level="high", rationale="complete"),
            context_metadata=ContextMetadata(values={"z": "last", "a": "first"}),
            context_source=self.build_source(),
            context_scope=self.build_scope(),
            metadata={"owner": "context"},
            tags=["context", "charlie"],
            lifecycle_state=LifecycleState.DRAFT,
            created_by="codex",
            updated_by="codex",
            created_at=timestamp,
            updated_at=timestamp,
        )

    def test_universal_context_baseline_is_canonical_object(self) -> None:
        context = UniversalContext(context_type=ContextType.CONVERSATIONAL)

        self.assertIsInstance(context, CanonicalObject)
        self.assertEqual(context.object_type, "UniversalContext")
        self.assertTrue(context.validate().is_valid)

    def test_universal_context_with_source_validates(self) -> None:
        context = UniversalContext(
            context_type=ContextType.ANALYTICAL,
            context_source=self.build_source(),
        )

        self.assertTrue(context.validate().is_valid)
        self.assertEqual(context.to_dict()["context_source"], self.build_source().to_dict())
        self.assertIsNone(context.to_dict()["context_scope"])

    def test_universal_context_with_scope_validates(self) -> None:
        context = UniversalContext(
            context_type=ContextType.ANALYTICAL,
            context_scope=self.build_scope(),
        )

        self.assertTrue(context.validate().is_valid)
        self.assertIsNone(context.to_dict()["context_source"])
        self.assertEqual(context.to_dict()["context_scope"], self.build_scope().to_dict())

    def test_universal_context_with_source_and_scope_payload_is_deterministic(self) -> None:
        context = self.build_context()
        payload = context.to_dict()

        self.assertEqual(payload, context.to_dict())
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
                "context_type",
                "context_state",
                "context_confidence",
                "context_metadata",
                "context_source",
                "context_scope",
            ],
        )
        self.assertEqual(payload["context_source"], self.build_source().to_dict())
        self.assertEqual(payload["context_scope"], self.build_scope().to_dict())

    def test_context_source_and_scope_payloads_are_deterministic(self) -> None:
        source = self.build_source()
        scope = self.build_scope()

        self.assertEqual(source.to_dict(), source.to_dict())
        self.assertEqual(scope.to_dict(), scope.to_dict())
        self.assertEqual(source.to_dict()["source_metadata"], {"a": "first", "z": "last"})
        self.assertEqual(scope.to_dict()["scope_metadata"], {"a": "first", "z": "last"})

    def test_validation_returns_platform_validation_result(self) -> None:
        result = self.build_context().validate()

        self.assertIsInstance(result, ValidationResult)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_validation_failures_cover_context_contracts(self) -> None:
        context = self.build_context()
        context._context_type = "analytical"
        context._context_state = "validated"
        context._context_confidence = "high"
        context._context_metadata = {"scope": "bad"}
        context._context_source = "source"
        context._context_scope = "scope"

        result = context.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "context_type",
                "context_state",
                "context_confidence",
                "context_metadata",
                "context_source",
                "context_scope",
            },
        )

    def test_validation_failures_cover_source_and_scope_details(self) -> None:
        source = self.build_source()
        scope = self.build_scope()
        object.__setattr__(source, "source_type", "knowledge")
        object.__setattr__(source, "source_metadata", {"bad": "mutable"})
        object.__setattr__(scope, "scope_type", "task")
        object.__setattr__(scope, "scope_metadata", {"bad": "mutable"})
        context = UniversalContext(
            context_type=ContextType.ANALYTICAL,
            context_source=source,
            context_scope=scope,
        )

        result = context.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "context_source.source_type",
                "context_source.source_metadata",
                "context_scope.scope_type",
                "context_scope.scope_metadata",
            },
        )

    def test_object_serializer_certifies_inherited_platform_fields_only(self) -> None:
        context = self.build_context()

        payload = ObjectSerializer.serialize(context)

        self.assertEqual(payload["object_type"], "UniversalContext")
        self.assertEqual(payload["metadata"], {"owner": "context"})
        self.assertEqual(payload["tags"], ["context", "charlie"])
        self.assertNotIn("context_type", payload)
        self.assertNotIn("context_source", payload)
        self.assertNotIn("context_scope", payload)

    def test_object_registry_accepts_universal_context(self) -> None:
        registry = ObjectRegistry()

        registry.register(UniversalContext)

        self.assertEqual(registry.lookup("UniversalContext"), UniversalContext)
        self.assertEqual(registry.lookup_by_class(UniversalContext), UniversalContext)
        self.assertEqual(registry.enumerate(), (UniversalContext,))
        registry.validate()

    def test_lifecycle_transitions_remain_platform_core_behavior(self) -> None:
        context = UniversalContext(context_type=ContextType.OPERATIONAL)

        context.transition_to(LifecycleState.ACTIVE)
        context.transition_to(LifecycleState.ARCHIVED)

        self.assertEqual(context.lifecycle_state, LifecycleState.ARCHIVED)
        with self.assertRaises(ValueError):
            context.transition_to(LifecycleState.ACTIVE)

    def test_relationship_availability_uses_platform_relationship_model(self) -> None:
        context = self.build_context()
        target_id = UUID("00000000-0000-0000-0000-000000001103")
        relationship = Relationship(
            source_object_id=context.object_id,
            target_object_id=target_id,
            relationship_type=RelationshipType.REFERENCES,
        )

        payload = relationship.to_dict()

        self.assertEqual(context.relationships, {})
        self.assertEqual(payload["source_object_id"], str(context.object_id))
        self.assertEqual(payload["target_object_id"], str(target_id))
        self.assertEqual(payload["relationship_type"], "references")

    def test_memory_and_knowledge_foundations_coexist_with_context(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000001104"),
            memory_type=MemoryType.SEMANTIC,
            content="Context certification coexists with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-charlie"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000001105"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = self.build_context()

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)

    def test_no_future_context_behavior_is_exposed(self) -> None:
        context = self.build_context()
        forbidden_names = {
            "ai",
            "compose",
            "infer",
            "persist",
            "prioritize",
            "reason",
            "retrieve",
            "search",
            "select",
            "workflow",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(context))))


if __name__ == "__main__":
    unittest.main()
