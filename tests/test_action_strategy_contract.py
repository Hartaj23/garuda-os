import unittest
from dataclasses import FrozenInstanceError
from uuid import UUID

from packages.action import (
    ActionInputCollection,
    ActionInputReference,
    ActionInputType,
    ActionOrigin,
    ActionProvenance,
    ActionStrategy,
    ActionStrategyContract,
    ActionStrategyMetadata,
    ActionStrategyType,
    ActionType,
    UniversalAction,
    validate_action_strategy,
    validate_action_strategy_contract,
    validate_action_strategy_metadata,
)
from packages.context import ContextType, UniversalContext
from packages.decision import DecisionType, UniversalDecision
from packages.knowledge import KnowledgeType, UniversalKnowledge
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import ObjectSerializer, ValidationResult
from packages.reasoning import ReasoningType, UniversalReasoning


class ActionStrategyContractTest(unittest.TestCase):
    def build_strategy(self) -> ActionStrategy:
        return ActionStrategy(
            strategy_type=ActionStrategyType.PROCEDURAL,
            name="operator-review",
            description="Review provided action inputs.",
            metadata=ActionStrategyMetadata(values={"z": "last", "a": "first"}),
        )

    def build_contract(self) -> ActionStrategyContract:
        return ActionStrategyContract(
            strategies=(
                self.build_strategy(),
                ActionStrategy(
                    strategy_type=ActionStrategyType.POLICY_BASED,
                    name="policy-check",
                    metadata=ActionStrategyMetadata(values={"rule": "manual"}),
                ),
            ),
            metadata=ActionStrategyMetadata(values={"mission": "delta"}),
            contract_version="1.0",
        )

    def test_action_strategy_type_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {strategy_type.value for strategy_type in ActionStrategyType},
            {
                "manual",
                "procedural",
                "policy_based",
                "event_driven",
                "review_based",
                "unknown",
            },
        )

    def test_action_strategy_metadata_is_immutable_and_deterministic(self) -> None:
        metadata = ActionStrategyMetadata(values={"z": "last", "a": "first"})

        self.assertEqual(metadata.to_dict(), {"a": "first", "z": "last"})
        with self.assertRaises(FrozenInstanceError):
            metadata.values = ()

    def test_action_strategy_constructs_deterministic_payload(self) -> None:
        strategy = self.build_strategy()

        self.assertEqual(
            strategy.to_dict(),
            {
                "strategy_type": "procedural",
                "name": "operator-review",
                "description": "Review provided action inputs.",
                "metadata": {"a": "first", "z": "last"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            strategy.name = "changed"

    def test_action_strategy_contract_constructs_deterministic_payload(self) -> None:
        contract = self.build_contract()

        self.assertEqual(
            contract.to_dict(),
            {
                "contract_version": "1.0",
                "strategies": [
                    self.build_strategy().to_dict(),
                    {
                        "strategy_type": "policy_based",
                        "name": "policy-check",
                        "description": None,
                        "metadata": {"rule": "manual"},
                    },
                ],
                "metadata": {"mission": "delta"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            contract.contract_version = "2.0"

    def test_validation_helpers_return_platform_validation_results(self) -> None:
        self.assertIsInstance(
            validate_action_strategy_metadata(ActionStrategyMetadata()),
            ValidationResult,
        )
        self.assertTrue(validate_action_strategy(self.build_strategy()).is_valid)
        self.assertTrue(validate_action_strategy_contract(self.build_contract()).is_valid)

    def test_validation_reports_invalid_strategy_shape(self) -> None:
        strategy = self.build_strategy()
        object.__setattr__(strategy, "strategy_type", "procedural")
        object.__setattr__(strategy, "name", "")
        object.__setattr__(strategy, "description", object())
        object.__setattr__(strategy, "metadata", {"bad": "mutable"})

        result = validate_action_strategy(strategy)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "action_strategy.strategy_type",
                "action_strategy.name",
                "action_strategy.description",
                "action_strategy.metadata",
            },
        )

    def test_validation_reports_invalid_contract_shape(self) -> None:
        contract = self.build_contract()
        object.__setattr__(contract, "contract_version", "")
        object.__setattr__(contract, "strategies", ("not-a-strategy",))
        object.__setattr__(contract, "metadata", {"bad": "mutable"})

        result = validate_action_strategy_contract(contract)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "action_strategy_contract.contract_version",
                "action_strategy_contract.strategies[0]",
                "action_strategy_contract.metadata",
            },
        )

    def test_validation_reports_empty_contract(self) -> None:
        contract = ActionStrategyContract(strategies=())

        result = validate_action_strategy_contract(contract)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            result.errors[0].code,
            "empty_action_strategy_contract_strategies",
        )

    def test_platform_core_serializer_compatibility_is_preserved(self) -> None:
        action = UniversalAction(
            object_id=UUID("00000000-0000-0000-0000-000000008301"),
            action_type=ActionType.TASK,
        )

        payload = ObjectSerializer.serialize(action)

        self.assertEqual(payload["object_type"], "UniversalAction")
        self.assertEqual(payload["object_id"], "00000000-0000-0000-0000-000000008301")
        self.assertNotIn("strategy", payload)
        self.assertNotIn("strategy_contract", payload)

    def test_all_foundation_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000008302"),
            memory_type=MemoryType.SEMANTIC,
            content="Action strategy contracts coexist with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-delta"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000008303"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000008304"),
            context_type=ContextType.ANALYTICAL,
        )
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000008305"),
            reasoning_type=ReasoningType.DEDUCTIVE,
        )
        decision = UniversalDecision(
            object_id=UUID("00000000-0000-0000-0000-000000008306"),
            decision_type=DecisionType.RECOMMENDATION,
        )
        action = UniversalAction(
            action_type=ActionType.OBSERVATION,
            action_inputs=ActionInputCollection(
                references=(
                    ActionInputReference(ActionInputType.MEMORY, str(memory.object_id)),
                    ActionInputReference(ActionInputType.KNOWLEDGE, str(knowledge.object_id)),
                    ActionInputReference(ActionInputType.CONTEXT, str(context.object_id)),
                    ActionInputReference(ActionInputType.REASONING, str(reasoning.object_id)),
                    ActionInputReference(ActionInputType.DECISION, str(decision.object_id)),
                ),
            ),
            action_provenance=ActionProvenance(
                origin=ActionOrigin.DECISION,
                input_references=(
                    ActionInputReference(ActionInputType.DECISION, str(decision.object_id)),
                ),
            ),
        )
        strategy = self.build_strategy()
        contract = self.build_contract()

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertTrue(reasoning.validate().is_valid)
        self.assertTrue(decision.validate().is_valid)
        self.assertTrue(action.validate().is_valid)
        self.assertTrue(validate_action_strategy(strategy).is_valid)
        self.assertTrue(validate_action_strategy_contract(contract).is_valid)

    def test_action_foundation_behavior_is_preserved(self) -> None:
        action = UniversalAction(action_type=ActionType.APPROVAL)
        payload = action.to_dict()

        self.assertTrue(action.validate().is_valid)
        self.assertEqual(payload["action_type"], "approval")
        self.assertNotIn("action_strategy", payload)
        self.assertNotIn("action_strategy_contract", payload)

    def test_no_execution_evaluation_or_future_behavior_is_exposed(self) -> None:
        strategy = self.build_strategy()
        contract = self.build_contract()
        forbidden_names = {
            "ai",
            "autonomous",
            "compute",
            "evaluate",
            "execute",
            "optimize",
            "orchestrate",
            "persist",
            "plan",
            "resolve",
            "schedule",
            "search",
            "workflow",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(strategy))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(contract))))


if __name__ == "__main__":
    unittest.main()
