import unittest
from datetime import datetime
from uuid import UUID

from packages.action import (
    ActionChain,
    ActionChainType,
    ActionState,
    ActionStepReference,
    ActionStrategy,
    ActionStrategyType,
    ActionType,
    ActionWorkspace,
    UniversalAction,
    WorkspaceStatistics,
    validate_action_reference,
    validate_action_workspace,
    validate_workspace_statistics,
)
from packages.context import ContextType, UniversalContext
from packages.decision import DecisionType, UniversalDecision
from packages.knowledge import KnowledgeType, UniversalKnowledge
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import LifecycleState, ObjectSerializer, ValidationResult
from packages.reasoning import ReasoningType, UniversalReasoning


def build_action(
    action_id: str = "00000000-0000-0000-0000-000000008501",
) -> UniversalAction:
    timestamp = datetime.fromisoformat("2026-07-05T00:00:00+00:00")
    return UniversalAction(
        object_id=UUID(action_id),
        action_type=ActionType.TASK,
        action_state=ActionState.DRAFT,
        created_at=timestamp,
        updated_at=timestamp,
    )


class ActionWorkspaceTest(unittest.TestCase):
    def test_create_workspace_with_empty_statistics(self) -> None:
        workspace = ActionWorkspace()

        statistics = workspace.statistics()

        self.assertIsInstance(statistics, WorkspaceStatistics)
        self.assertEqual(statistics.total_actions, 0)
        self.assertEqual(statistics.active_actions, 0)
        self.assertEqual(statistics.archived_actions, 0)
        self.assertEqual(workspace.identifiers(), ())

    def test_add_action_and_lookup_by_exact_identifier(self) -> None:
        workspace = ActionWorkspace()
        action = build_action()

        workspace.add(action)

        self.assertIs(workspace.get(action.object_id), action)
        self.assertIs(workspace.get(str(action.object_id)), action)
        self.assertEqual(workspace.identifiers(), (action.object_id,))

    def test_workspace_preserves_object_identity(self) -> None:
        workspace = ActionWorkspace()
        action = build_action()

        workspace.add(action)
        retrieved = workspace.get(action.object_id)

        self.assertIs(retrieved, action)

    def test_reject_non_universal_action_reference(self) -> None:
        result = validate_action_reference(object())

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "action")

        with self.assertRaises(ValueError):
            ActionWorkspace().add(object())

    def test_reject_duplicate_identifier(self) -> None:
        workspace = ActionWorkspace()
        first = build_action()
        second = build_action()

        workspace.add(first)

        with self.assertRaises(ValueError):
            workspace.add(second)

    def test_remove_action_by_exact_identifier(self) -> None:
        workspace = ActionWorkspace()
        action = build_action()
        workspace.add(action)

        removed = workspace.remove(str(action.object_id))

        self.assertIs(removed, action)
        self.assertIsNone(workspace.get(action.object_id))
        self.assertEqual(workspace.identifiers(), ())

    def test_missing_identifier_returns_none(self) -> None:
        workspace = ActionWorkspace()

        self.assertIsNone(workspace.get("00000000-0000-0000-0000-000000008599"))
        self.assertIsNone(workspace.remove("00000000-0000-0000-0000-000000008599"))

    def test_invalid_identifier_is_rejected(self) -> None:
        workspace = ActionWorkspace()

        with self.assertRaises(ValueError):
            workspace.get("not-a-uuid")

        with self.assertRaises(ValueError):
            workspace.remove("not-a-uuid")

    def test_enumerate_identifiers_is_deterministic(self) -> None:
        workspace = ActionWorkspace()
        second = build_action("00000000-0000-0000-0000-000000008503")
        first = build_action("00000000-0000-0000-0000-000000008502")

        workspace.add(second)
        workspace.add(first)

        self.assertEqual(workspace.identifiers(), (first.object_id, second.object_id))

    def test_clear_workspace_removes_all_references(self) -> None:
        workspace = ActionWorkspace()
        workspace.add(build_action())

        workspace.clear()

        self.assertEqual(workspace.identifiers(), ())
        self.assertEqual(workspace.statistics().total_actions, 0)

    def test_workspace_statistics_are_descriptive_and_deterministic(self) -> None:
        workspace = ActionWorkspace()
        draft = build_action("00000000-0000-0000-0000-000000008504")
        active = build_action("00000000-0000-0000-0000-000000008505")
        archived = build_action("00000000-0000-0000-0000-000000008506")
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
                "total_actions": 3,
                "active_actions": 1,
                "archived_actions": 1,
            },
        )
        self.assertTrue(validate_workspace_statistics(statistics).is_valid)

    def test_statistics_validation_reports_invalid_shape(self) -> None:
        statistics = WorkspaceStatistics(
            total_actions=1,
            active_actions=1,
            archived_actions=0,
        )
        object.__setattr__(statistics, "total_actions", -1)
        object.__setattr__(statistics, "active_actions", -1)
        object.__setattr__(statistics, "archived_actions", -1)

        result = validate_workspace_statistics(statistics)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "workspace_statistics.total_actions",
                "workspace_statistics.active_actions",
                "workspace_statistics.archived_actions",
            },
        )

    def test_statistics_validation_reports_invalid_totals(self) -> None:
        statistics = WorkspaceStatistics(
            total_actions=1,
            active_actions=1,
            archived_actions=1,
        )

        result = validate_workspace_statistics(statistics)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "invalid_workspace_statistics_totals")

    def test_workspace_validation_uses_platform_validation_result(self) -> None:
        workspace = ActionWorkspace()
        workspace.add(build_action())

        result = validate_action_workspace(workspace)

        self.assertIsInstance(result, ValidationResult)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_workspace_validation_reports_identity_mismatch(self) -> None:
        workspace = ActionWorkspace()
        action = build_action()
        workspace._actions[UUID("00000000-0000-0000-0000-000000008507")] = action

        result = workspace.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "action_reference_identity_mismatch")

    def test_workspace_validation_reports_invalid_stored_reference(self) -> None:
        workspace = ActionWorkspace()
        workspace._actions[UUID("00000000-0000-0000-0000-000000008508")] = object()

        result = workspace.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "invalid_stored_action_reference")

    def test_workspace_is_not_serializable(self) -> None:
        workspace = ActionWorkspace()

        self.assertFalse(hasattr(workspace, "to_dict"))

    def test_platform_core_serialization_compatibility_is_preserved(self) -> None:
        action = build_action()
        workspace = ActionWorkspace()
        workspace.add(action)

        payload = ObjectSerializer.serialize(workspace.get(action.object_id))

        self.assertEqual(payload["object_type"], "UniversalAction")
        self.assertEqual(payload["object_id"], str(action.object_id))

    def test_chain_and_strategy_contract_compatibility_without_behavior(self) -> None:
        workspace = ActionWorkspace()
        action = build_action()
        workspace.add(action)
        chain = ActionChain(
            chain_type=ActionChainType.SEQUENTIAL,
            steps=(ActionStepReference(str(action.object_id)),),
        )
        strategy = ActionStrategy(
            strategy_type=ActionStrategyType.MANUAL,
            name="operator-review",
        )

        self.assertEqual(chain.to_dict()["chain_type"], "sequential")
        self.assertEqual(strategy.to_dict()["strategy_type"], "manual")
        self.assertIs(workspace.get(action.object_id), action)

    def test_existing_foundation_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000008509"),
            memory_type=MemoryType.SEMANTIC,
            content="Action workspace coexists with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-foxtrot"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000008510"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000008511"),
            context_type=ContextType.ANALYTICAL,
        )
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000008512"),
            reasoning_type=ReasoningType.DEDUCTIVE,
        )
        decision = UniversalDecision(
            object_id=UUID("00000000-0000-0000-0000-000000008513"),
            decision_type=DecisionType.RECOMMENDATION,
        )
        workspace = ActionWorkspace()
        workspace.add(build_action())

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertTrue(reasoning.validate().is_valid)
        self.assertTrue(decision.validate().is_valid)
        self.assertTrue(workspace.validate().is_valid)

    def test_workspace_exposes_no_future_behavior(self) -> None:
        workspace = ActionWorkspace()
        forbidden_names = {
            "ai",
            "autonomous",
            "execute",
            "orchestrate",
            "optimize",
            "persist",
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
