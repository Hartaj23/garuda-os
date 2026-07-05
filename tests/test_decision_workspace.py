import unittest
from datetime import datetime
from uuid import UUID

from packages.context import ContextType, UniversalContext
from packages.decision import (
    DecisionChain,
    DecisionChainType,
    DecisionState,
    DecisionStepReference,
    DecisionStrategy,
    DecisionStrategyType,
    DecisionType,
    DecisionWorkspace,
    UniversalDecision,
    WorkspaceStatistics,
    validate_decision_reference,
    validate_decision_workspace,
    validate_workspace_statistics,
)
from packages.knowledge import KnowledgeType, UniversalKnowledge
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import LifecycleState, ObjectSerializer, ValidationResult
from packages.reasoning import ReasoningType, UniversalReasoning


def build_decision(
    decision_id: str = "00000000-0000-0000-0000-000000007501",
) -> UniversalDecision:
    timestamp = datetime.fromisoformat("2026-07-05T00:00:00+00:00")
    return UniversalDecision(
        object_id=UUID(decision_id),
        decision_type=DecisionType.RECOMMENDATION,
        decision_state=DecisionState.DRAFT,
        created_at=timestamp,
        updated_at=timestamp,
    )


class DecisionWorkspaceTest(unittest.TestCase):
    def test_create_workspace_with_empty_statistics(self) -> None:
        workspace = DecisionWorkspace()

        statistics = workspace.statistics()

        self.assertIsInstance(statistics, WorkspaceStatistics)
        self.assertEqual(statistics.total_decisions, 0)
        self.assertEqual(statistics.active_decisions, 0)
        self.assertEqual(statistics.archived_decisions, 0)
        self.assertEqual(workspace.identifiers(), ())

    def test_add_decision_and_lookup_by_exact_identifier(self) -> None:
        workspace = DecisionWorkspace()
        decision = build_decision()

        workspace.add(decision)

        self.assertIs(workspace.get(decision.object_id), decision)
        self.assertIs(workspace.get(str(decision.object_id)), decision)
        self.assertEqual(workspace.identifiers(), (decision.object_id,))

    def test_workspace_preserves_object_identity(self) -> None:
        workspace = DecisionWorkspace()
        decision = build_decision()

        workspace.add(decision)
        retrieved = workspace.get(decision.object_id)

        self.assertIs(retrieved, decision)

    def test_reject_non_universal_decision_reference(self) -> None:
        result = validate_decision_reference(object())

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "decision")

        with self.assertRaises(ValueError):
            DecisionWorkspace().add(object())

    def test_reject_duplicate_identifier(self) -> None:
        workspace = DecisionWorkspace()
        first = build_decision()
        second = build_decision()

        workspace.add(first)

        with self.assertRaises(ValueError):
            workspace.add(second)

    def test_remove_decision_by_exact_identifier(self) -> None:
        workspace = DecisionWorkspace()
        decision = build_decision()
        workspace.add(decision)

        removed = workspace.remove(str(decision.object_id))

        self.assertIs(removed, decision)
        self.assertIsNone(workspace.get(decision.object_id))
        self.assertEqual(workspace.identifiers(), ())

    def test_missing_identifier_returns_none(self) -> None:
        workspace = DecisionWorkspace()

        self.assertIsNone(workspace.get("00000000-0000-0000-0000-000000007599"))
        self.assertIsNone(workspace.remove("00000000-0000-0000-0000-000000007599"))

    def test_invalid_identifier_is_rejected(self) -> None:
        workspace = DecisionWorkspace()

        with self.assertRaises(ValueError):
            workspace.get("not-a-uuid")

        with self.assertRaises(ValueError):
            workspace.remove("not-a-uuid")

    def test_enumerate_identifiers_is_deterministic(self) -> None:
        workspace = DecisionWorkspace()
        second = build_decision("00000000-0000-0000-0000-000000007503")
        first = build_decision("00000000-0000-0000-0000-000000007502")

        workspace.add(second)
        workspace.add(first)

        self.assertEqual(workspace.identifiers(), (first.object_id, second.object_id))

    def test_clear_workspace_removes_all_references(self) -> None:
        workspace = DecisionWorkspace()
        workspace.add(build_decision())

        workspace.clear()

        self.assertEqual(workspace.identifiers(), ())
        self.assertEqual(workspace.statistics().total_decisions, 0)

    def test_workspace_statistics_are_descriptive_and_deterministic(self) -> None:
        workspace = DecisionWorkspace()
        draft = build_decision("00000000-0000-0000-0000-000000007504")
        active = build_decision("00000000-0000-0000-0000-000000007505")
        archived = build_decision("00000000-0000-0000-0000-000000007506")
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
                "total_decisions": 3,
                "active_decisions": 1,
                "archived_decisions": 1,
            },
        )
        self.assertTrue(validate_workspace_statistics(statistics).is_valid)

    def test_statistics_validation_reports_invalid_shape(self) -> None:
        statistics = WorkspaceStatistics(
            total_decisions=1,
            active_decisions=1,
            archived_decisions=0,
        )
        object.__setattr__(statistics, "total_decisions", -1)
        object.__setattr__(statistics, "active_decisions", -1)
        object.__setattr__(statistics, "archived_decisions", -1)

        result = validate_workspace_statistics(statistics)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "workspace_statistics.total_decisions",
                "workspace_statistics.active_decisions",
                "workspace_statistics.archived_decisions",
            },
        )

    def test_statistics_validation_reports_invalid_totals(self) -> None:
        statistics = WorkspaceStatistics(
            total_decisions=1,
            active_decisions=1,
            archived_decisions=1,
        )

        result = validate_workspace_statistics(statistics)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "invalid_workspace_statistics_totals")

    def test_workspace_validation_uses_platform_validation_result(self) -> None:
        workspace = DecisionWorkspace()
        workspace.add(build_decision())

        result = validate_decision_workspace(workspace)

        self.assertIsInstance(result, ValidationResult)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_workspace_validation_reports_identity_mismatch(self) -> None:
        workspace = DecisionWorkspace()
        decision = build_decision()
        workspace._decisions[UUID("00000000-0000-0000-0000-000000007507")] = decision

        result = workspace.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "decision_reference_identity_mismatch")

    def test_workspace_validation_reports_invalid_stored_reference(self) -> None:
        workspace = DecisionWorkspace()
        workspace._decisions[UUID("00000000-0000-0000-0000-000000007508")] = object()

        result = workspace.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "invalid_stored_decision_reference")

    def test_workspace_is_not_serializable(self) -> None:
        workspace = DecisionWorkspace()

        self.assertFalse(hasattr(workspace, "to_dict"))

    def test_platform_core_serialization_compatibility_is_preserved(self) -> None:
        decision = build_decision()
        workspace = DecisionWorkspace()
        workspace.add(decision)

        payload = ObjectSerializer.serialize(workspace.get(decision.object_id))

        self.assertEqual(payload["object_type"], "UniversalDecision")
        self.assertEqual(payload["object_id"], str(decision.object_id))

    def test_chain_and_strategy_contract_compatibility_without_behavior(self) -> None:
        workspace = DecisionWorkspace()
        decision = build_decision()
        workspace.add(decision)
        chain = DecisionChain(
            chain_type=DecisionChainType.SEQUENTIAL,
            steps=(DecisionStepReference(str(decision.object_id)),),
        )
        strategy = DecisionStrategy(
            strategy_type=DecisionStrategyType.ANALYTICAL,
            name="evidence-review",
        )

        self.assertEqual(chain.to_dict()["chain_type"], "sequential")
        self.assertEqual(strategy.to_dict()["strategy_type"], "analytical")
        self.assertIs(workspace.get(decision.object_id), decision)

    def test_existing_foundation_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000007509"),
            memory_type=MemoryType.SEMANTIC,
            content="Decision workspace coexists with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-foxtrot"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000007510"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000007511"),
            context_type=ContextType.ANALYTICAL,
        )
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000007512"),
            reasoning_type=ReasoningType.DEDUCTIVE,
        )
        workspace = DecisionWorkspace()
        workspace.add(build_decision())

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertTrue(reasoning.validate().is_valid)
        self.assertTrue(workspace.validate().is_valid)

    def test_workspace_exposes_no_future_behavior(self) -> None:
        workspace = DecisionWorkspace()
        forbidden_names = {
            "ai",
            "autonomous",
            "execute",
            "orchestrate",
            "optimize",
            "persist",
            "plan",
            "rank",
            "resolve",
            "retrieve",
            "search",
            "workflow",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(workspace))))


if __name__ == "__main__":
    unittest.main()
