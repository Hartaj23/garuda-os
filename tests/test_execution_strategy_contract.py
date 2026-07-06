import unittest
from dataclasses import FrozenInstanceError
from uuid import UUID

from packages.action import ActionType, UniversalAction
from packages.context import ContextType, UniversalContext
from packages.decision import DecisionType, UniversalDecision
from packages.execution import (
    ExecutionInputCollection,
    ExecutionInputReference,
    ExecutionInputType,
    ExecutionOrigin,
    ExecutionProvenance,
    ExecutionStrategy,
    ExecutionStrategyContract,
    ExecutionStrategyMetadata,
    ExecutionStrategyType,
    ExecutionType,
    UniversalExecution,
    validate_execution_strategy,
    validate_execution_strategy_contract,
    validate_execution_strategy_metadata,
)
from packages.knowledge import KnowledgeType, UniversalKnowledge
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import ObjectSerializer, ValidationResult
from packages.reasoning import ReasoningType, UniversalReasoning


class ExecutionStrategyContractTest(unittest.TestCase):
    def build_strategy(self) -> ExecutionStrategy:
        return ExecutionStrategy(
            strategy_type=ExecutionStrategyType.PROCEDURAL,
            name="operator-review",
            description="Review provided execution inputs.",
            metadata=ExecutionStrategyMetadata(values={"z": "last", "a": "first"}),
        )

    def build_contract(self) -> ExecutionStrategyContract:
        return ExecutionStrategyContract(
            strategies=(
                self.build_strategy(),
                ExecutionStrategy(
                    strategy_type=ExecutionStrategyType.POLICY_BASED,
                    name="policy-check",
                    metadata=ExecutionStrategyMetadata(values={"rule": "manual"}),
                ),
            ),
            metadata=ExecutionStrategyMetadata(values={"mission": "delta"}),
            contract_version="1.0",
        )

    def test_execution_strategy_type_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {strategy_type.value for strategy_type in ExecutionStrategyType},
            {
                "manual",
                "procedural",
                "policy_based",
                "event_driven",
                "review_based",
                "unknown",
            },
        )

    def test_execution_strategy_metadata_is_immutable_and_deterministic(self) -> None:
        metadata = ExecutionStrategyMetadata(values={"z": "last", "a": "first"})

        self.assertEqual(metadata.to_dict(), {"a": "first", "z": "last"})
        with self.assertRaises(FrozenInstanceError):
            metadata.values = ()

    def test_execution_strategy_constructs_deterministic_payload(self) -> None:
        strategy = self.build_strategy()

        self.assertEqual(
            strategy.to_dict(),
            {
                "strategy_type": "procedural",
                "name": "operator-review",
                "description": "Review provided execution inputs.",
                "metadata": {"a": "first", "z": "last"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            strategy.name = "changed"

    def test_execution_strategy_contract_constructs_deterministic_payload(self) -> None:
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
            validate_execution_strategy_metadata(ExecutionStrategyMetadata()),
            ValidationResult,
        )
        self.assertTrue(validate_execution_strategy(self.build_strategy()).is_valid)
        self.assertTrue(validate_execution_strategy_contract(self.build_contract()).is_valid)

    def test_validation_reports_invalid_strategy_shape(self) -> None:
        strategy = self.build_strategy()
        object.__setattr__(strategy, "strategy_type", "procedural")
        object.__setattr__(strategy, "name", "")
        object.__setattr__(strategy, "description", object())
        object.__setattr__(strategy, "metadata", {"bad": "mutable"})

        result = validate_execution_strategy(strategy)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "execution_strategy.strategy_type",
                "execution_strategy.name",
                "execution_strategy.description",
                "execution_strategy.metadata",
            },
        )

    def test_validation_reports_invalid_contract_shape(self) -> None:
        contract = self.build_contract()
        object.__setattr__(contract, "contract_version", "")
        object.__setattr__(contract, "strategies", ("not-a-strategy",))
        object.__setattr__(contract, "metadata", {"bad": "mutable"})

        result = validate_execution_strategy_contract(contract)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "execution_strategy_contract.contract_version",
                "execution_strategy_contract.strategies[0]",
                "execution_strategy_contract.metadata",
            },
        )

    def test_validation_reports_empty_contract(self) -> None:
        contract = ExecutionStrategyContract(strategies=())

        result = validate_execution_strategy_contract(contract)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            result.errors[0].code,
            "empty_execution_strategy_contract_strategies",
        )

    def test_platform_core_serializer_compatibility_is_preserved(self) -> None:
        execution = UniversalExecution(
            object_id=UUID("00000000-0000-0000-0000-000000009301"),
            execution_type=ExecutionType.ACTION,
        )

        payload = ObjectSerializer.serialize(execution)

        self.assertEqual(payload["object_type"], "UniversalExecution")
        self.assertEqual(payload["object_id"], "00000000-0000-0000-0000-000000009301")
        self.assertNotIn("strategy", payload)
        self.assertNotIn("strategy_contract", payload)

    def test_all_foundation_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000009302"),
            memory_type=MemoryType.SEMANTIC,
            content="Execution strategy contracts coexist with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-delta"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000009303"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000009304"),
            context_type=ContextType.ANALYTICAL,
        )
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000009305"),
            reasoning_type=ReasoningType.DEDUCTIVE,
        )
        decision = UniversalDecision(
            object_id=UUID("00000000-0000-0000-0000-000000009306"),
            decision_type=DecisionType.RECOMMENDATION,
        )
        action = UniversalAction(
            object_id=UUID("00000000-0000-0000-0000-000000009307"),
            action_type=ActionType.TASK,
        )
        execution = UniversalExecution(
            execution_type=ExecutionType.OBSERVATION,
            execution_inputs=ExecutionInputCollection(
                references=(
                    ExecutionInputReference(ExecutionInputType.MEMORY, str(memory.object_id)),
                    ExecutionInputReference(ExecutionInputType.KNOWLEDGE, str(knowledge.object_id)),
                    ExecutionInputReference(ExecutionInputType.CONTEXT, str(context.object_id)),
                    ExecutionInputReference(ExecutionInputType.REASONING, str(reasoning.object_id)),
                    ExecutionInputReference(ExecutionInputType.DECISION, str(decision.object_id)),
                    ExecutionInputReference(ExecutionInputType.ACTION, str(action.object_id)),
                ),
            ),
            execution_provenance=ExecutionProvenance(
                origin=ExecutionOrigin.ACTION,
                input_references=(
                    ExecutionInputReference(ExecutionInputType.ACTION, str(action.object_id)),
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
        self.assertTrue(execution.validate().is_valid)
        self.assertTrue(validate_execution_strategy(strategy).is_valid)
        self.assertTrue(validate_execution_strategy_contract(contract).is_valid)

    def test_execution_foundation_behavior_is_preserved(self) -> None:
        execution = UniversalExecution(execution_type=ExecutionType.ACTION)
        payload = execution.to_dict()

        self.assertTrue(execution.validate().is_valid)
        self.assertEqual(payload["execution_type"], "action")
        self.assertNotIn("execution_strategy", payload)
        self.assertNotIn("execution_strategy_contract", payload)

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
