import unittest
from dataclasses import FrozenInstanceError
from uuid import UUID

from packages.context import ContextType, UniversalContext
from packages.decision import (
    DecisionInputCollection,
    DecisionInputReference,
    DecisionInputType,
    DecisionOrigin,
    DecisionProvenance,
    DecisionStrategy,
    DecisionStrategyContract,
    DecisionStrategyMetadata,
    DecisionStrategyType,
    DecisionType,
    UniversalDecision,
    validate_decision_strategy,
    validate_decision_strategy_contract,
    validate_decision_strategy_metadata,
)
from packages.knowledge import KnowledgeType, UniversalKnowledge
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import ObjectSerializer, ValidationResult
from packages.reasoning import ReasoningType, UniversalReasoning


class DecisionStrategyContractTest(unittest.TestCase):
    def build_strategy(self) -> DecisionStrategy:
        return DecisionStrategy(
            strategy_type=DecisionStrategyType.ANALYTICAL,
            name="evidence-review",
            description="Review provided decision inputs.",
            metadata=DecisionStrategyMetadata(values={"z": "last", "a": "first"}),
        )

    def build_contract(self) -> DecisionStrategyContract:
        return DecisionStrategyContract(
            strategies=(
                self.build_strategy(),
                DecisionStrategy(
                    strategy_type=DecisionStrategyType.RULE_BASED,
                    name="policy-check",
                    metadata=DecisionStrategyMetadata(values={"rule": "manual"}),
                ),
            ),
            metadata=DecisionStrategyMetadata(values={"mission": "delta"}),
            contract_version="1.0",
        )

    def test_decision_strategy_type_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {strategy_type.value for strategy_type in DecisionStrategyType},
            {"analytical", "heuristic", "rule_based", "consensus", "expert", "unknown"},
        )

    def test_decision_strategy_metadata_is_immutable_and_deterministic(self) -> None:
        metadata = DecisionStrategyMetadata(values={"z": "last", "a": "first"})

        self.assertEqual(metadata.to_dict(), {"a": "first", "z": "last"})
        with self.assertRaises(FrozenInstanceError):
            metadata.values = ()

    def test_decision_strategy_constructs_deterministic_payload(self) -> None:
        strategy = self.build_strategy()

        self.assertEqual(
            strategy.to_dict(),
            {
                "strategy_type": "analytical",
                "name": "evidence-review",
                "description": "Review provided decision inputs.",
                "metadata": {"a": "first", "z": "last"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            strategy.name = "changed"

    def test_decision_strategy_contract_constructs_deterministic_payload(self) -> None:
        contract = self.build_contract()

        self.assertEqual(
            contract.to_dict(),
            {
                "contract_version": "1.0",
                "strategies": [
                    self.build_strategy().to_dict(),
                    {
                        "strategy_type": "rule_based",
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
            validate_decision_strategy_metadata(DecisionStrategyMetadata()),
            ValidationResult,
        )
        self.assertTrue(validate_decision_strategy(self.build_strategy()).is_valid)
        self.assertTrue(validate_decision_strategy_contract(self.build_contract()).is_valid)

    def test_validation_reports_invalid_strategy_shape(self) -> None:
        strategy = self.build_strategy()
        object.__setattr__(strategy, "strategy_type", "analytical")
        object.__setattr__(strategy, "name", "")
        object.__setattr__(strategy, "description", object())
        object.__setattr__(strategy, "metadata", {"bad": "mutable"})

        result = validate_decision_strategy(strategy)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "decision_strategy.strategy_type",
                "decision_strategy.name",
                "decision_strategy.description",
                "decision_strategy.metadata",
            },
        )

    def test_validation_reports_invalid_contract_shape(self) -> None:
        contract = self.build_contract()
        object.__setattr__(contract, "contract_version", "")
        object.__setattr__(contract, "strategies", ("not-a-strategy",))
        object.__setattr__(contract, "metadata", {"bad": "mutable"})

        result = validate_decision_strategy_contract(contract)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "decision_strategy_contract.contract_version",
                "decision_strategy_contract.strategies[0]",
                "decision_strategy_contract.metadata",
            },
        )

    def test_validation_reports_empty_contract(self) -> None:
        contract = DecisionStrategyContract(strategies=())

        result = validate_decision_strategy_contract(contract)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            result.errors[0].code,
            "empty_decision_strategy_contract_strategies",
        )

    def test_platform_core_serializer_compatibility_is_preserved(self) -> None:
        decision = UniversalDecision(
            object_id=UUID("00000000-0000-0000-0000-000000007301"),
            decision_type=DecisionType.RECOMMENDATION,
        )

        payload = ObjectSerializer.serialize(decision)

        self.assertEqual(payload["object_type"], "UniversalDecision")
        self.assertEqual(payload["object_id"], "00000000-0000-0000-0000-000000007301")
        self.assertNotIn("strategy", payload)
        self.assertNotIn("strategy_contract", payload)

    def test_all_foundation_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000007302"),
            memory_type=MemoryType.SEMANTIC,
            content="Decision strategy contracts coexist with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-delta"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000007303"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000007304"),
            context_type=ContextType.ANALYTICAL,
        )
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000007305"),
            reasoning_type=ReasoningType.DEDUCTIVE,
        )
        decision = UniversalDecision(
            decision_type=DecisionType.SELECTION,
            decision_inputs=DecisionInputCollection(
                references=(
                    DecisionInputReference(DecisionInputType.MEMORY, str(memory.object_id)),
                    DecisionInputReference(DecisionInputType.KNOWLEDGE, str(knowledge.object_id)),
                    DecisionInputReference(DecisionInputType.CONTEXT, str(context.object_id)),
                    DecisionInputReference(DecisionInputType.REASONING, str(reasoning.object_id)),
                ),
            ),
            decision_provenance=DecisionProvenance(
                origin=DecisionOrigin.HUMAN,
                input_references=(
                    DecisionInputReference(DecisionInputType.REASONING, str(reasoning.object_id)),
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
        self.assertTrue(validate_decision_strategy(strategy).is_valid)
        self.assertTrue(validate_decision_strategy_contract(contract).is_valid)

    def test_decision_foundation_behavior_is_preserved(self) -> None:
        decision = UniversalDecision(decision_type=DecisionType.APPROVAL)
        payload = decision.to_dict()

        self.assertTrue(decision.validate().is_valid)
        self.assertEqual(payload["decision_type"], "approval")
        self.assertNotIn("decision_strategy", payload)
        self.assertNotIn("decision_strategy_contract", payload)

    def test_no_execution_evaluation_or_future_behavior_is_exposed(self) -> None:
        strategy = self.build_strategy()
        contract = self.build_contract()
        forbidden_names = {
            "ai",
            "autonomous",
            "compute",
            "decide",
            "evaluate",
            "execute",
            "optimize",
            "persist",
            "plan",
            "resolve",
            "search",
            "workflow",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(strategy))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(contract))))


if __name__ == "__main__":
    unittest.main()
