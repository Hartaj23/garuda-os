import unittest
from datetime import datetime
from uuid import UUID

from packages.context import (
    CompositionType,
    ContextComposition,
    ContextScope,
    ContextScopeType,
    ContextSelectionRequest,
    ContextSource,
    ContextSourceType,
    ContextType,
    ContextWorkspace,
    SelectionCriterion,
    SelectionType,
    UniversalContext,
    WorkspaceStatistics,
    validate_context_reference,
    validate_context_workspace,
    validate_workspace_statistics,
)
from packages.knowledge import KnowledgeType, UniversalKnowledge
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import ObjectSerializer, ValidationResult


def build_context(
    context_id: str = "00000000-0000-0000-0000-000000004001",
) -> UniversalContext:
    timestamp = datetime.fromisoformat("2026-07-04T00:00:00+00:00")
    return UniversalContext(
        object_id=UUID(context_id),
        context_type=ContextType.ANALYTICAL,
        context_source=ContextSource(
            source_type=ContextSourceType.KNOWLEDGE,
            source_identifier="knowledge:00000000-0000-0000-0000-000000004101",
        ),
        context_scope=ContextScope(
            scope_type=ContextScopeType.TASK,
            boundary_identifier="task:mission-foxtrot",
        ),
        created_at=timestamp,
        updated_at=timestamp,
    )


class ContextWorkspaceTest(unittest.TestCase):
    def test_create_workspace_with_empty_statistics(self) -> None:
        workspace = ContextWorkspace()

        stats = workspace.statistics()

        self.assertIsInstance(stats, WorkspaceStatistics)
        self.assertEqual(stats.total_contexts, 0)
        self.assertEqual(workspace.identifiers(), ())

    def test_add_context_and_lookup_by_exact_identifier(self) -> None:
        workspace = ContextWorkspace()
        context = build_context()

        workspace.add(context)

        self.assertIs(workspace.get(context.object_id), context)
        self.assertIs(workspace.get(str(context.object_id)), context)
        self.assertEqual(workspace.identifiers(), (context.object_id,))

    def test_reject_non_universal_context_reference(self) -> None:
        result = validate_context_reference(object())

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "context")

        with self.assertRaises(ValueError):
            ContextWorkspace().add(object())

    def test_reject_duplicate_identifier(self) -> None:
        workspace = ContextWorkspace()
        first = build_context()
        second = build_context()

        workspace.add(first)

        with self.assertRaises(ValueError):
            workspace.add(second)

    def test_remove_context_by_exact_identifier(self) -> None:
        workspace = ContextWorkspace()
        context = build_context()
        workspace.add(context)

        removed = workspace.remove(str(context.object_id))

        self.assertIs(removed, context)
        self.assertIsNone(workspace.get(context.object_id))
        self.assertEqual(workspace.identifiers(), ())

    def test_missing_identifier_returns_none(self) -> None:
        workspace = ContextWorkspace()

        self.assertIsNone(workspace.get("00000000-0000-0000-0000-000000004099"))
        self.assertIsNone(workspace.remove("00000000-0000-0000-0000-000000004099"))

    def test_enumerate_identifiers_is_deterministic(self) -> None:
        workspace = ContextWorkspace()
        second = build_context("00000000-0000-0000-0000-000000004003")
        first = build_context("00000000-0000-0000-0000-000000004002")

        workspace.add(second)
        workspace.add(first)

        self.assertEqual(workspace.identifiers(), (first.object_id, second.object_id))

    def test_clear_workspace_removes_all_references(self) -> None:
        workspace = ContextWorkspace()
        workspace.add(build_context())

        workspace.clear()

        self.assertEqual(workspace.identifiers(), ())
        self.assertEqual(workspace.statistics().total_contexts, 0)

    def test_workspace_statistics_are_informational_and_deterministic(self) -> None:
        workspace = ContextWorkspace()
        context = build_context()

        before = workspace.statistics()
        workspace.add(context)
        after = workspace.statistics()

        self.assertEqual(before.total_contexts, 0)
        self.assertEqual(after.total_contexts, 1)
        self.assertIn("created_at", after.to_dict())
        self.assertIn("last_modified_at", after.to_dict())
        self.assertTrue(validate_workspace_statistics(after).is_valid)

    def test_statistics_validation_reports_invalid_shape(self) -> None:
        statistics = WorkspaceStatistics(
            total_contexts=1,
            created_at=datetime.fromisoformat("2026-07-04T00:00:00+00:00"),
            last_modified_at=datetime.fromisoformat("2026-07-04T00:00:00+00:00"),
        )
        object.__setattr__(statistics, "total_contexts", -1)
        object.__setattr__(statistics, "created_at", "not-a-datetime")
        object.__setattr__(statistics, "last_modified_at", "not-a-datetime")

        result = validate_workspace_statistics(statistics)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "workspace_statistics.total_contexts",
                "workspace_statistics.created_at",
                "workspace_statistics.last_modified_at",
            },
        )

    def test_workspace_validation_uses_platform_validation_result(self) -> None:
        workspace = ContextWorkspace()
        context = build_context()
        workspace.add(context)

        result = validate_context_workspace(workspace)

        self.assertIsInstance(result, ValidationResult)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_workspace_validation_reports_identity_mismatch(self) -> None:
        workspace = ContextWorkspace()
        context = build_context()
        workspace._contexts[UUID("00000000-0000-0000-0000-000000004004")] = context

        result = workspace.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "context_reference_identity_mismatch")

    def test_workspace_is_not_serializable(self) -> None:
        workspace = ContextWorkspace()

        self.assertFalse(hasattr(workspace, "to_dict"))

    def test_platform_core_serialization_compatibility_is_preserved(self) -> None:
        context = build_context()
        workspace = ContextWorkspace()
        workspace.add(context)

        payload = ObjectSerializer.serialize(workspace.get(context.object_id))

        self.assertEqual(payload["object_type"], "UniversalContext")
        self.assertEqual(payload["object_id"], str(context.object_id))

    def test_composition_and_selection_contract_compatibility_without_behavior(self) -> None:
        workspace = ContextWorkspace()
        context = build_context()
        workspace.add(context)
        composition = ContextComposition(
            composition_type=CompositionType.GROUPED,
            context_identifiers=(str(context.object_id),),
        )
        selection = ContextSelectionRequest(
            selection_type=SelectionType.EXACT_IDENTIFIER,
            criteria=(
                SelectionCriterion(
                    criterion_name="context_identifier",
                    operator="equals",
                    criterion_value=str(context.object_id),
                ),
            ),
        )

        self.assertEqual(composition.context_identifiers, (str(context.object_id),))
        self.assertEqual(selection.criteria[0].criterion_value, str(context.object_id))
        self.assertIs(workspace.get(context.object_id), context)

    def test_memory_and_knowledge_foundation_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000004005"),
            memory_type=MemoryType.SEMANTIC,
            content="Context workspace coexists with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-foxtrot"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000004006"),
            knowledge_type=KnowledgeType.FACT,
        )
        workspace = ContextWorkspace()
        workspace.add(build_context())

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(workspace.validate().is_valid)

    def test_workspace_exposes_no_future_behavior(self) -> None:
        workspace = ContextWorkspace()
        forbidden_names = {
            "ai",
            "compose",
            "execute",
            "filter",
            "infer",
            "persist",
            "prioritize",
            "rank",
            "reason",
            "resolve",
            "retrieve",
            "search",
            "select",
            "semantic_lookup",
            "semantic_search",
            "workflow",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(workspace))))


if __name__ == "__main__":
    unittest.main()
