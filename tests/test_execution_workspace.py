import unittest
from datetime import datetime
from uuid import UUID

from packages.action import ActionType, UniversalAction
from packages.context import ContextType, UniversalContext
from packages.decision import DecisionType, UniversalDecision
from packages.execution import (
    ExecutionChain,
    ExecutionChainType,
    ExecutionState,
    ExecutionStepReference,
    ExecutionStrategy,
    ExecutionStrategyType,
    ExecutionType,
    ExecutionWorkspace,
    UniversalExecution,
    WorkspaceStatistics,
    validate_execution_reference,
    validate_execution_workspace,
    validate_workspace_statistics,
)
from packages.knowledge import KnowledgeType, UniversalKnowledge
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import LifecycleState, ObjectSerializer, ValidationResult
from packages.reasoning import ReasoningType, UniversalReasoning


def build_execution(
    execution_id: str = "00000000-0000-0000-0000-000000009501",
) -> UniversalExecution:
    timestamp = datetime.fromisoformat("2026-07-06T00:00:00+00:00")
    return UniversalExecution(
        object_id=UUID(execution_id),
        execution_type=ExecutionType.ACTION,
        execution_state=ExecutionState.DRAFT,
        created_at=timestamp,
        updated_at=timestamp,
    )


class ExecutionWorkspaceTest(unittest.TestCase):
    def test_create_workspace_with_empty_statistics(self) -> None:
        workspace = ExecutionWorkspace()

        statistics = workspace.statistics()

        self.assertIsInstance(statistics, WorkspaceStatistics)
        self.assertEqual(statistics.total_executions, 0)
        self.assertEqual(statistics.active_executions, 0)
        self.assertEqual(statistics.archived_executions, 0)
        self.assertEqual(workspace.identifiers(), ())

    def test_add_execution_and_lookup_by_exact_identifier(self) -> None:
        workspace = ExecutionWorkspace()
        execution = build_execution()

        workspace.add(execution)

        self.assertIs(workspace.get(execution.object_id), execution)
        self.assertIs(workspace.get(str(execution.object_id)), execution)
        self.assertEqual(workspace.identifiers(), (execution.object_id,))

    def test_workspace_preserves_object_identity(self) -> None:
        workspace = ExecutionWorkspace()
        execution = build_execution()

        workspace.add(execution)
        retrieved = workspace.get(execution.object_id)

        self.assertIs(retrieved, execution)

    def test_reject_non_universal_execution_reference(self) -> None:
        result = validate_execution_reference(object())

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "execution")

        with self.assertRaises(ValueError):
            ExecutionWorkspace().add(object())

    def test_reject_duplicate_identifier(self) -> None:
        workspace = ExecutionWorkspace()
        first = build_execution()
        second = build_execution()

        workspace.add(first)

        with self.assertRaises(ValueError):
            workspace.add(second)

    def test_remove_execution_by_exact_identifier(self) -> None:
        workspace = ExecutionWorkspace()
        execution = build_execution()
        workspace.add(execution)

        removed = workspace.remove(str(execution.object_id))

        self.assertIs(removed, execution)
        self.assertIsNone(workspace.get(execution.object_id))
        self.assertEqual(workspace.identifiers(), ())

    def test_missing_identifier_returns_none(self) -> None:
        workspace = ExecutionWorkspace()

        self.assertIsNone(workspace.get("00000000-0000-0000-0000-000000009599"))
        self.assertIsNone(workspace.remove("00000000-0000-0000-0000-000000009599"))

    def test_invalid_identifier_is_rejected(self) -> None:
        workspace = ExecutionWorkspace()

        with self.assertRaises(ValueError):
            workspace.get("not-a-uuid")

        with self.assertRaises(ValueError):
            workspace.remove("not-a-uuid")

    def test_enumerate_identifiers_is_deterministic(self) -> None:
        workspace = ExecutionWorkspace()
        second = build_execution("00000000-0000-0000-0000-000000009503")
        first = build_execution("00000000-0000-0000-0000-000000009502")

        workspace.add(second)
        workspace.add(first)

        self.assertEqual(workspace.identifiers(), (first.object_id, second.object_id))

    def test_clear_workspace_removes_all_references(self) -> None:
        workspace = ExecutionWorkspace()
        workspace.add(build_execution())

        workspace.clear()

        self.assertEqual(workspace.identifiers(), ())
        self.assertEqual(workspace.statistics().total_executions, 0)

    def test_workspace_statistics_are_descriptive_and_deterministic(self) -> None:
        workspace = ExecutionWorkspace()
        draft = build_execution("00000000-0000-0000-0000-000000009504")
        active = build_execution("00000000-0000-0000-0000-000000009505")
        archived = build_execution("00000000-0000-0000-0000-000000009506")
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
                "total_executions": 3,
                "active_executions": 1,
                "archived_executions": 1,
            },
        )
        self.assertTrue(validate_workspace_statistics(statistics).is_valid)

    def test_statistics_validation_reports_invalid_shape(self) -> None:
        statistics = WorkspaceStatistics(
            total_executions=1,
            active_executions=1,
            archived_executions=0,
        )
        object.__setattr__(statistics, "total_executions", -1)
        object.__setattr__(statistics, "active_executions", -1)
        object.__setattr__(statistics, "archived_executions", -1)

        result = validate_workspace_statistics(statistics)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "workspace_statistics.total_executions",
                "workspace_statistics.active_executions",
                "workspace_statistics.archived_executions",
            },
        )

    def test_statistics_validation_reports_invalid_totals(self) -> None:
        statistics = WorkspaceStatistics(
            total_executions=1,
            active_executions=1,
            archived_executions=1,
        )

        result = validate_workspace_statistics(statistics)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "invalid_workspace_statistics_totals")

    def test_workspace_validation_uses_platform_validation_result(self) -> None:
        workspace = ExecutionWorkspace()
        workspace.add(build_execution())

        result = validate_execution_workspace(workspace)

        self.assertIsInstance(result, ValidationResult)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_workspace_validation_reports_identity_mismatch(self) -> None:
        workspace = ExecutionWorkspace()
        execution = build_execution()
        workspace._executions[UUID("00000000-0000-0000-0000-000000009507")] = execution

        result = workspace.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "execution_reference_identity_mismatch")

    def test_workspace_validation_reports_invalid_stored_reference(self) -> None:
        workspace = ExecutionWorkspace()
        workspace._executions[UUID("00000000-0000-0000-0000-000000009508")] = object()

        result = workspace.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "invalid_stored_execution_reference")

    def test_workspace_is_not_serializable(self) -> None:
        workspace = ExecutionWorkspace()

        self.assertFalse(hasattr(workspace, "to_dict"))

    def test_platform_core_serialization_compatibility_is_preserved(self) -> None:
        execution = build_execution()
        workspace = ExecutionWorkspace()
        workspace.add(execution)

        payload = ObjectSerializer.serialize(workspace.get(execution.object_id))

        self.assertEqual(payload["object_type"], "UniversalExecution")
        self.assertEqual(payload["object_id"], str(execution.object_id))

    def test_chain_and_strategy_contract_compatibility_without_behavior(self) -> None:
        workspace = ExecutionWorkspace()
        execution = build_execution()
        workspace.add(execution)
        chain = ExecutionChain(
            chain_type=ExecutionChainType.SEQUENTIAL,
            steps=(ExecutionStepReference(str(execution.object_id)),),
        )
        strategy = ExecutionStrategy(
            strategy_type=ExecutionStrategyType.MANUAL,
            name="operator-review",
        )

        self.assertEqual(chain.to_dict()["chain_type"], "sequential")
        self.assertEqual(strategy.to_dict()["strategy_type"], "manual")
        self.assertIs(workspace.get(execution.object_id), execution)

    def test_existing_foundation_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000009509"),
            memory_type=MemoryType.SEMANTIC,
            content="Execution workspace coexists with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-foxtrot"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000009510"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000009511"),
            context_type=ContextType.ANALYTICAL,
        )
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000009512"),
            reasoning_type=ReasoningType.DEDUCTIVE,
        )
        decision = UniversalDecision(
            object_id=UUID("00000000-0000-0000-0000-000000009513"),
            decision_type=DecisionType.RECOMMENDATION,
        )
        action = UniversalAction(
            object_id=UUID("00000000-0000-0000-0000-000000009514"),
            action_type=ActionType.TASK,
        )
        workspace = ExecutionWorkspace()
        workspace.add(build_execution())

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertTrue(reasoning.validate().is_valid)
        self.assertTrue(decision.validate().is_valid)
        self.assertTrue(action.validate().is_valid)
        self.assertTrue(workspace.validate().is_valid)

    def test_workspace_exposes_no_future_behavior(self) -> None:
        workspace = ExecutionWorkspace()
        forbidden_names = {
            "ai",
            "autonomous",
            "compute",
            "evaluate",
            "execute",
            "orchestrate",
            "optimize",
            "persist",
            "plan",
            "rank",
            "resolve",
            "retrieve",
            "schedule",
            "search",
            "workflow",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(workspace))))


if __name__ == "__main__":
    unittest.main()
