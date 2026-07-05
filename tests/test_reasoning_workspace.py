import unittest
from datetime import datetime
from uuid import UUID

from packages.context import ContextType, UniversalContext
from packages.knowledge import KnowledgeType, UniversalKnowledge
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import LifecycleState, ObjectSerializer, ValidationResult
from packages.reasoning import (
    ChainType,
    ReasoningChain,
    ReasoningState,
    ReasoningStrategy,
    ReasoningType,
    ReasoningWorkspace,
    StrategyType,
    UniversalReasoning,
    WorkspaceStatistics,
    validate_reasoning_reference,
    validate_reasoning_workspace,
    validate_workspace_statistics,
)


def build_reasoning(
    reasoning_id: str = "00000000-0000-0000-0000-000000006501",
) -> UniversalReasoning:
    timestamp = datetime.fromisoformat("2026-07-05T00:00:00+00:00")
    return UniversalReasoning(
        object_id=UUID(reasoning_id),
        reasoning_type=ReasoningType.DEDUCTIVE,
        reasoning_state=ReasoningState.DRAFT,
        created_at=timestamp,
        updated_at=timestamp,
    )


class ReasoningWorkspaceTest(unittest.TestCase):
    def test_create_workspace_with_empty_statistics(self) -> None:
        workspace = ReasoningWorkspace()

        statistics = workspace.statistics()

        self.assertIsInstance(statistics, WorkspaceStatistics)
        self.assertEqual(statistics.total_reasoning_objects, 0)
        self.assertEqual(statistics.active_reasoning_objects, 0)
        self.assertEqual(statistics.archived_reasoning_objects, 0)
        self.assertEqual(workspace.identifiers(), ())

    def test_add_reasoning_and_lookup_by_exact_identifier(self) -> None:
        workspace = ReasoningWorkspace()
        reasoning = build_reasoning()

        workspace.add(reasoning)

        self.assertIs(workspace.get(reasoning.object_id), reasoning)
        self.assertIs(workspace.get(str(reasoning.object_id)), reasoning)
        self.assertEqual(workspace.identifiers(), (reasoning.object_id,))

    def test_workspace_preserves_object_identity(self) -> None:
        workspace = ReasoningWorkspace()
        reasoning = build_reasoning()

        workspace.add(reasoning)
        retrieved = workspace.get(reasoning.object_id)

        self.assertIs(retrieved, reasoning)

    def test_reject_non_universal_reasoning_reference(self) -> None:
        result = validate_reasoning_reference(object())

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "reasoning")

        with self.assertRaises(ValueError):
            ReasoningWorkspace().add(object())

    def test_reject_duplicate_identifier(self) -> None:
        workspace = ReasoningWorkspace()
        first = build_reasoning()
        second = build_reasoning()

        workspace.add(first)

        with self.assertRaises(ValueError):
            workspace.add(second)

    def test_remove_reasoning_by_exact_identifier(self) -> None:
        workspace = ReasoningWorkspace()
        reasoning = build_reasoning()
        workspace.add(reasoning)

        removed = workspace.remove(str(reasoning.object_id))

        self.assertIs(removed, reasoning)
        self.assertIsNone(workspace.get(reasoning.object_id))
        self.assertEqual(workspace.identifiers(), ())

    def test_missing_identifier_returns_none(self) -> None:
        workspace = ReasoningWorkspace()

        self.assertIsNone(workspace.get("00000000-0000-0000-0000-000000006599"))
        self.assertIsNone(workspace.remove("00000000-0000-0000-0000-000000006599"))

    def test_enumerate_identifiers_is_deterministic(self) -> None:
        workspace = ReasoningWorkspace()
        second = build_reasoning("00000000-0000-0000-0000-000000006503")
        first = build_reasoning("00000000-0000-0000-0000-000000006502")

        workspace.add(second)
        workspace.add(first)

        self.assertEqual(workspace.identifiers(), (first.object_id, second.object_id))

    def test_clear_workspace_removes_all_references(self) -> None:
        workspace = ReasoningWorkspace()
        workspace.add(build_reasoning())

        workspace.clear()

        self.assertEqual(workspace.identifiers(), ())
        self.assertEqual(workspace.statistics().total_reasoning_objects, 0)

    def test_workspace_statistics_are_descriptive_and_deterministic(self) -> None:
        workspace = ReasoningWorkspace()
        draft = build_reasoning("00000000-0000-0000-0000-000000006504")
        active = build_reasoning("00000000-0000-0000-0000-000000006505")
        archived = build_reasoning("00000000-0000-0000-0000-000000006506")
        active.transition_to(LifecycleState.ACTIVE)
        archived.transition_to(LifecycleState.ACTIVE)
        archived.transition_to(LifecycleState.ARCHIVED)

        workspace.add(archived)
        workspace.add(draft)
        workspace.add(active)

        statistics = workspace.statistics()

        self.assertEqual(
            statistics.to_dict(),
            {
                "total_reasoning_objects": 3,
                "active_reasoning_objects": 1,
                "archived_reasoning_objects": 1,
            },
        )
        self.assertTrue(validate_workspace_statistics(statistics).is_valid)

    def test_statistics_validation_reports_invalid_shape(self) -> None:
        statistics = WorkspaceStatistics(
            total_reasoning_objects=1,
            active_reasoning_objects=1,
            archived_reasoning_objects=0,
        )
        object.__setattr__(statistics, "total_reasoning_objects", -1)
        object.__setattr__(statistics, "active_reasoning_objects", -1)
        object.__setattr__(statistics, "archived_reasoning_objects", -1)

        result = validate_workspace_statistics(statistics)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "workspace_statistics.total_reasoning_objects",
                "workspace_statistics.active_reasoning_objects",
                "workspace_statistics.archived_reasoning_objects",
            },
        )

    def test_statistics_validation_reports_invalid_totals(self) -> None:
        statistics = WorkspaceStatistics(
            total_reasoning_objects=1,
            active_reasoning_objects=1,
            archived_reasoning_objects=1,
        )

        result = validate_workspace_statistics(statistics)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "invalid_workspace_statistics_totals")

    def test_workspace_validation_uses_platform_validation_result(self) -> None:
        workspace = ReasoningWorkspace()
        workspace.add(build_reasoning())

        result = validate_reasoning_workspace(workspace)

        self.assertIsInstance(result, ValidationResult)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_workspace_validation_reports_identity_mismatch(self) -> None:
        workspace = ReasoningWorkspace()
        reasoning = build_reasoning()
        workspace._reasoning_objects[
            UUID("00000000-0000-0000-0000-000000006507")
        ] = reasoning

        result = workspace.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "reasoning_reference_identity_mismatch")

    def test_workspace_validation_reports_invalid_stored_reference(self) -> None:
        workspace = ReasoningWorkspace()
        workspace._reasoning_objects[
            UUID("00000000-0000-0000-0000-000000006508")
        ] = object()

        result = workspace.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "invalid_stored_reasoning_reference")

    def test_workspace_is_not_serializable(self) -> None:
        workspace = ReasoningWorkspace()

        self.assertFalse(hasattr(workspace, "to_dict"))

    def test_platform_core_serialization_compatibility_is_preserved(self) -> None:
        reasoning = build_reasoning()
        workspace = ReasoningWorkspace()
        workspace.add(reasoning)

        payload = ObjectSerializer.serialize(workspace.get(reasoning.object_id))

        self.assertEqual(payload["object_type"], "UniversalReasoning")
        self.assertEqual(payload["object_id"], str(reasoning.object_id))

    def test_chain_and_strategy_contract_compatibility_without_behavior(self) -> None:
        workspace = ReasoningWorkspace()
        reasoning = build_reasoning()
        workspace.add(reasoning)
        chain = ReasoningChain(chain_type=ChainType.LINEAR)
        strategy = ReasoningStrategy(
            strategy_type=StrategyType.SEQUENTIAL,
            name="ordered-review",
        )

        self.assertEqual(chain.to_dict()["chain_type"], "linear")
        self.assertEqual(strategy.to_dict()["strategy_type"], "sequential")
        self.assertIs(workspace.get(reasoning.object_id), reasoning)

    def test_memory_knowledge_and_context_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000006509"),
            memory_type=MemoryType.SEMANTIC,
            content="Reasoning workspace coexists with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-foxtrot"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000006510"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000006511"),
            context_type=ContextType.ANALYTICAL,
        )
        workspace = ReasoningWorkspace()
        workspace.add(build_reasoning())

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertTrue(workspace.validate().is_valid)

    def test_workspace_exposes_no_future_behavior(self) -> None:
        workspace = ReasoningWorkspace()
        forbidden_names = {
            "ai",
            "conclude",
            "evaluate",
            "execute",
            "infer",
            "orchestrate",
            "persist",
            "rank",
            "reason",
            "resolve",
            "retrieve",
            "search",
            "workflow",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(workspace))))


if __name__ == "__main__":
    unittest.main()
