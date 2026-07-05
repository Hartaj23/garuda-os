import unittest
from dataclasses import FrozenInstanceError
from uuid import UUID

from packages.context import ContextType, UniversalContext
from packages.knowledge import KnowledgeType, UniversalKnowledge
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import ObjectSerializer, ValidationResult
from packages.reasoning import (
    ReasoningInputCollection,
    ReasoningInputReference,
    ReasoningInputType,
    ReasoningOrigin,
    ReasoningProvenance,
    ReasoningStrategy,
    ReasoningStrategyContract,
    ReasoningType,
    StrategyMetadata,
    StrategyType,
    UniversalReasoning,
    validate_reasoning_strategy,
    validate_reasoning_strategy_contract,
    validate_strategy_metadata,
)


class ReasoningStrategyContractTest(unittest.TestCase):
    def build_strategy(self) -> ReasoningStrategy:
        return ReasoningStrategy(
            strategy_type=StrategyType.SEQUENTIAL,
            name="ordered-review",
            description="Review inputs in declared order.",
            metadata=StrategyMetadata(values={"z": "last", "a": "first"}),
        )

    def build_contract(self) -> ReasoningStrategyContract:
        return ReasoningStrategyContract(
            supported_strategy_types=(
                StrategyType.SEQUENTIAL,
                StrategyType.PARALLEL,
                StrategyType.COMPARATIVE,
                StrategyType.ELIMINATION,
                StrategyType.DEPENDENCY,
                StrategyType.VALIDATION,
            ),
            metadata=StrategyMetadata(values={"mission": "delta"}),
            contract_version="1.0",
        )

    def test_strategy_type_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {strategy_type.value for strategy_type in StrategyType},
            {
                "sequential",
                "parallel",
                "comparative",
                "elimination",
                "dependency",
                "validation",
            },
        )

    def test_strategy_metadata_is_immutable_and_deterministic(self) -> None:
        metadata = StrategyMetadata(values={"z": "last", "a": "first"})

        self.assertEqual(metadata.to_dict(), {"a": "first", "z": "last"})
        with self.assertRaises(FrozenInstanceError):
            metadata.values = ()

    def test_reasoning_strategy_constructs_deterministic_payload(self) -> None:
        strategy = self.build_strategy()

        self.assertEqual(
            strategy.to_dict(),
            {
                "strategy_type": "sequential",
                "name": "ordered-review",
                "description": "Review inputs in declared order.",
                "metadata": {"a": "first", "z": "last"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            strategy.name = "changed"

    def test_reasoning_strategy_contract_constructs_deterministic_payload(self) -> None:
        contract = self.build_contract()

        self.assertEqual(
            contract.to_dict(),
            {
                "contract_version": "1.0",
                "supported_strategy_types": [
                    "sequential",
                    "parallel",
                    "comparative",
                    "elimination",
                    "dependency",
                    "validation",
                ],
                "metadata": {"mission": "delta"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            contract.contract_version = "2.0"

    def test_validation_helpers_return_platform_validation_results(self) -> None:
        self.assertIsInstance(validate_strategy_metadata(StrategyMetadata()), ValidationResult)
        self.assertTrue(validate_reasoning_strategy(self.build_strategy()).is_valid)
        self.assertTrue(validate_reasoning_strategy_contract(self.build_contract()).is_valid)

    def test_validation_reports_invalid_strategy_shape(self) -> None:
        strategy = self.build_strategy()
        object.__setattr__(strategy, "strategy_type", "sequential")
        object.__setattr__(strategy, "name", "")
        object.__setattr__(strategy, "description", object())
        object.__setattr__(strategy, "metadata", {"bad": "mutable"})

        result = validate_reasoning_strategy(strategy)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "reasoning_strategy.strategy_type",
                "reasoning_strategy.name",
                "reasoning_strategy.description",
                "reasoning_strategy.metadata",
            },
        )

    def test_validation_reports_invalid_contract_shape(self) -> None:
        contract = self.build_contract()
        object.__setattr__(contract, "contract_version", "")
        object.__setattr__(contract, "supported_strategy_types", ("sequential",))
        object.__setattr__(contract, "metadata", {"bad": "mutable"})

        result = validate_reasoning_strategy_contract(contract)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "reasoning_strategy_contract.contract_version",
                "reasoning_strategy_contract.supported_strategy_types[0]",
                "reasoning_strategy_contract.metadata",
            },
        )

    def test_platform_core_serializer_compatibility_is_preserved(self) -> None:
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000006301"),
            reasoning_type=ReasoningType.CONSISTENCY,
        )

        payload = ObjectSerializer.serialize(reasoning)

        self.assertEqual(payload["object_type"], "UniversalReasoning")
        self.assertEqual(payload["object_id"], "00000000-0000-0000-0000-000000006301")
        self.assertNotIn("strategy", payload)
        self.assertNotIn("strategy_contract", payload)

    def test_memory_knowledge_context_and_reasoning_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000006302"),
            memory_type=MemoryType.SEMANTIC,
            content="Strategy contracts coexist with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-delta"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000006303"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000006304"),
            context_type=ContextType.ANALYTICAL,
        )
        reasoning = UniversalReasoning(
            reasoning_type=ReasoningType.DEPENDENCY,
            reasoning_inputs=ReasoningInputCollection(
                references=(
                    ReasoningInputReference(ReasoningInputType.MEMORY, str(memory.object_id)),
                    ReasoningInputReference(ReasoningInputType.KNOWLEDGE, str(knowledge.object_id)),
                    ReasoningInputReference(ReasoningInputType.CONTEXT, str(context.object_id)),
                ),
            ),
            reasoning_provenance=ReasoningProvenance(
                origin=ReasoningOrigin.DERIVED,
                input_references=(
                    ReasoningInputReference(ReasoningInputType.CONTEXT, str(context.object_id)),
                ),
            ),
        )
        strategy = self.build_strategy()
        contract = self.build_contract()

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertTrue(reasoning.validate().is_valid)
        self.assertTrue(validate_reasoning_strategy(strategy).is_valid)
        self.assertTrue(validate_reasoning_strategy_contract(contract).is_valid)

    def test_no_execution_inference_or_future_behavior_is_exposed(self) -> None:
        strategy = self.build_strategy()
        contract = self.build_contract()
        forbidden_names = {
            "ai",
            "conclude",
            "decide",
            "evaluate",
            "execute",
            "infer",
            "persist",
            "plan",
            "reason",
            "search",
            "workflow",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(strategy))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(contract))))


if __name__ == "__main__":
    unittest.main()
