import unittest
from dataclasses import FrozenInstanceError
from uuid import UUID

from packages.context import ContextType, UniversalContext
from packages.knowledge import KnowledgeType, UniversalKnowledge
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import ObjectSerializer, ValidationResult
from packages.reasoning import (
    ChainMetadata,
    ChainType,
    ReasoningChain,
    ReasoningChainContract,
    ReasoningInputCollection,
    ReasoningInputReference,
    ReasoningInputType,
    ReasoningStepReference,
    ReasoningStrategy,
    ReasoningType,
    StrategyType,
    UniversalReasoning,
    validate_chain_metadata,
    validate_reasoning_chain,
    validate_reasoning_chain_contract,
    validate_reasoning_step_reference,
)


class ReasoningChainContractTest(unittest.TestCase):
    def build_step(self) -> ReasoningStepReference:
        return ReasoningStepReference(
            identifier="reasoning:00000000-0000-0000-0000-000000006401",
            sequence=1,
            metadata=ChainMetadata(values={"z": "last", "a": "first"}),
        )

    def build_chain(self) -> ReasoningChain:
        return ReasoningChain(
            chain_type=ChainType.LINEAR,
            steps=(self.build_step(),),
            metadata=ChainMetadata(values={"mission": "echo"}),
        )

    def build_contract(self) -> ReasoningChainContract:
        return ReasoningChainContract(
            supported_chain_types=(
                ChainType.LINEAR,
                ChainType.BRANCHING,
                ChainType.HIERARCHICAL,
                ChainType.DEPENDENCY,
                ChainType.COMPARATIVE,
            ),
            metadata=ChainMetadata(values={"mission": "echo"}),
            contract_version="1.0",
        )

    def test_chain_type_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {chain_type.value for chain_type in ChainType},
            {"linear", "branching", "hierarchical", "dependency", "comparative"},
        )

    def test_chain_metadata_is_immutable_and_deterministic(self) -> None:
        metadata = ChainMetadata(values={"z": "last", "a": "first"})

        self.assertEqual(metadata.to_dict(), {"a": "first", "z": "last"})
        with self.assertRaises(FrozenInstanceError):
            metadata.values = ()

    def test_reasoning_step_reference_is_opaque_and_deterministic(self) -> None:
        step = self.build_step()

        self.assertEqual(
            step.to_dict(),
            {
                "identifier": "reasoning:00000000-0000-0000-0000-000000006401",
                "sequence": 1,
                "metadata": {"a": "first", "z": "last"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            step.identifier = "changed"

    def test_reasoning_chain_constructs_deterministic_payload(self) -> None:
        chain = self.build_chain()

        self.assertEqual(
            chain.to_dict(),
            {
                "chain_type": "linear",
                "steps": [self.build_step().to_dict()],
                "metadata": {"mission": "echo"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            chain.chain_type = ChainType.BRANCHING

    def test_reasoning_chain_contract_constructs_deterministic_payload(self) -> None:
        contract = self.build_contract()

        self.assertEqual(
            contract.to_dict(),
            {
                "contract_version": "1.0",
                "supported_chain_types": [
                    "linear",
                    "branching",
                    "hierarchical",
                    "dependency",
                    "comparative",
                ],
                "metadata": {"mission": "echo"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            contract.contract_version = "2.0"

    def test_validation_helpers_return_platform_validation_results(self) -> None:
        self.assertIsInstance(validate_chain_metadata(ChainMetadata()), ValidationResult)
        self.assertTrue(validate_reasoning_step_reference(self.build_step()).is_valid)
        self.assertTrue(validate_reasoning_chain(self.build_chain()).is_valid)
        self.assertTrue(validate_reasoning_chain_contract(self.build_contract()).is_valid)

    def test_validation_reports_invalid_step_shape(self) -> None:
        step = self.build_step()
        object.__setattr__(step, "identifier", "")
        object.__setattr__(step, "sequence", -1)
        object.__setattr__(step, "metadata", {"bad": "mutable"})

        result = validate_reasoning_step_reference(step)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "reasoning_step_reference.identifier",
                "reasoning_step_reference.sequence",
                "reasoning_step_reference.metadata",
            },
        )

    def test_validation_reports_invalid_chain_shape(self) -> None:
        chain = self.build_chain()
        object.__setattr__(chain, "chain_type", "linear")
        object.__setattr__(chain, "steps", ("not-a-step",))
        object.__setattr__(chain, "metadata", {"bad": "mutable"})

        result = validate_reasoning_chain(chain)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "reasoning_chain.chain_type",
                "reasoning_chain.steps[0]",
                "reasoning_chain.metadata",
            },
        )

    def test_validation_reports_invalid_contract_shape(self) -> None:
        contract = self.build_contract()
        object.__setattr__(contract, "contract_version", "")
        object.__setattr__(contract, "supported_chain_types", ("linear",))
        object.__setattr__(contract, "metadata", {"bad": "mutable"})

        result = validate_reasoning_chain_contract(contract)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "reasoning_chain_contract.contract_version",
                "reasoning_chain_contract.supported_chain_types[0]",
                "reasoning_chain_contract.metadata",
            },
        )

    def test_platform_core_serializer_compatibility_is_preserved(self) -> None:
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000006402"),
            reasoning_type=ReasoningType.CONSISTENCY,
        )

        payload = ObjectSerializer.serialize(reasoning)

        self.assertEqual(payload["object_type"], "UniversalReasoning")
        self.assertEqual(payload["object_id"], "00000000-0000-0000-0000-000000006402")
        self.assertNotIn("chain", payload)
        self.assertNotIn("chain_contract", payload)

    def test_memory_knowledge_context_and_reasoning_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000006403"),
            memory_type=MemoryType.SEMANTIC,
            content="Chain contracts coexist with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-echo"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000006404"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000006405"),
            context_type=ContextType.ANALYTICAL,
        )
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000006406"),
            reasoning_type=ReasoningType.DEPENDENCY,
            reasoning_inputs=ReasoningInputCollection(
                references=(
                    ReasoningInputReference(ReasoningInputType.MEMORY, str(memory.object_id)),
                    ReasoningInputReference(ReasoningInputType.KNOWLEDGE, str(knowledge.object_id)),
                    ReasoningInputReference(ReasoningInputType.CONTEXT, str(context.object_id)),
                )
            ),
        )
        strategy = ReasoningStrategy(
            strategy_type=StrategyType.SEQUENTIAL,
            name="ordered-review",
        )
        chain = ReasoningChain(
            chain_type=ChainType.DEPENDENCY,
            steps=(ReasoningStepReference(identifier=str(reasoning.object_id), sequence=1),),
        )

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertTrue(reasoning.validate().is_valid)
        self.assertEqual(strategy.strategy_type, StrategyType.SEQUENTIAL)
        self.assertTrue(validate_reasoning_chain(chain).is_valid)

    def test_no_execution_inference_or_future_behavior_is_exposed(self) -> None:
        step = self.build_step()
        chain = self.build_chain()
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
            "resolve",
            "search",
            "workflow",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(step))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(chain))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(contract))))


if __name__ == "__main__":
    unittest.main()
