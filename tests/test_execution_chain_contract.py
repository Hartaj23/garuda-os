import unittest
from dataclasses import FrozenInstanceError
from uuid import UUID

from packages.action import ActionType, UniversalAction
from packages.context import ContextType, UniversalContext
from packages.decision import DecisionType, UniversalDecision
from packages.execution import (
    ExecutionChain,
    ExecutionChainContract,
    ExecutionChainMetadata,
    ExecutionChainType,
    ExecutionInputCollection,
    ExecutionInputReference,
    ExecutionInputType,
    ExecutionOrigin,
    ExecutionProvenance,
    ExecutionStepReference,
    ExecutionStrategy,
    ExecutionStrategyType,
    ExecutionType,
    UniversalExecution,
    validate_execution_chain,
    validate_execution_chain_contract,
    validate_execution_chain_metadata,
    validate_execution_step_reference,
)
from packages.knowledge import KnowledgeType, UniversalKnowledge
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import ObjectSerializer, ValidationResult
from packages.reasoning import ReasoningType, UniversalReasoning


class ExecutionChainContractTest(unittest.TestCase):
    def build_step(self) -> ExecutionStepReference:
        return ExecutionStepReference(
            execution_identifier="execution:00000000-0000-0000-0000-000000009401",
            metadata=ExecutionChainMetadata(values={"z": "last", "a": "first"}),
        )

    def build_chain(self) -> ExecutionChain:
        return ExecutionChain(
            chain_type=ExecutionChainType.SEQUENTIAL,
            steps=(self.build_step(),),
            metadata=ExecutionChainMetadata(values={"mission": "echo"}),
        )

    def build_contract(self) -> ExecutionChainContract:
        return ExecutionChainContract(
            chains=(
                self.build_chain(),
                ExecutionChain(
                    chain_type=ExecutionChainType.REVIEW,
                    steps=(
                        ExecutionStepReference(
                            execution_identifier=(
                                "execution:00000000-0000-0000-0000-000000009402"
                            ),
                        ),
                    ),
                ),
            ),
            metadata=ExecutionChainMetadata(values={"mission": "echo"}),
            contract_version="1.0",
        )

    def test_execution_chain_type_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {chain_type.value for chain_type in ExecutionChainType},
            {"sequential", "parallel", "dependency", "review", "fallback", "unknown"},
        )

    def test_execution_chain_metadata_is_immutable_and_deterministic(self) -> None:
        metadata = ExecutionChainMetadata(values={"z": "last", "a": "first"})

        self.assertEqual(metadata.to_dict(), {"a": "first", "z": "last"})
        with self.assertRaises(FrozenInstanceError):
            metadata.values = ()

    def test_execution_step_reference_is_opaque_and_deterministic(self) -> None:
        step = self.build_step()

        self.assertEqual(
            step.to_dict(),
            {
                "execution_identifier": "execution:00000000-0000-0000-0000-000000009401",
                "metadata": {"a": "first", "z": "last"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            step.execution_identifier = "changed"

    def test_execution_chain_constructs_deterministic_payload(self) -> None:
        chain = self.build_chain()

        self.assertEqual(
            chain.to_dict(),
            {
                "chain_type": "sequential",
                "steps": [self.build_step().to_dict()],
                "metadata": {"mission": "echo"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            chain.chain_type = ExecutionChainType.DEPENDENCY

    def test_execution_chain_contract_constructs_deterministic_payload(self) -> None:
        contract = self.build_contract()

        self.assertEqual(
            contract.to_dict(),
            {
                "contract_version": "1.0",
                "chains": [
                    self.build_chain().to_dict(),
                    {
                        "chain_type": "review",
                        "steps": [
                            {
                                "execution_identifier": (
                                    "execution:00000000-0000-0000-0000-000000009402"
                                ),
                                "metadata": {},
                            }
                        ],
                        "metadata": {},
                    },
                ],
                "metadata": {"mission": "echo"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            contract.contract_version = "2.0"

    def test_validation_helpers_return_platform_validation_results(self) -> None:
        self.assertIsInstance(
            validate_execution_chain_metadata(ExecutionChainMetadata()),
            ValidationResult,
        )
        self.assertTrue(validate_execution_step_reference(self.build_step()).is_valid)
        self.assertTrue(validate_execution_chain(self.build_chain()).is_valid)
        self.assertTrue(validate_execution_chain_contract(self.build_contract()).is_valid)

    def test_validation_reports_invalid_step_shape(self) -> None:
        step = self.build_step()
        object.__setattr__(step, "execution_identifier", "")
        object.__setattr__(step, "metadata", {"bad": "mutable"})

        result = validate_execution_step_reference(step)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "execution_step_reference.execution_identifier",
                "execution_step_reference.metadata",
            },
        )

    def test_validation_reports_invalid_chain_shape(self) -> None:
        chain = self.build_chain()
        object.__setattr__(chain, "chain_type", "sequential")
        object.__setattr__(chain, "steps", ("not-a-step",))
        object.__setattr__(chain, "metadata", {"bad": "mutable"})

        result = validate_execution_chain(chain)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "execution_chain.chain_type",
                "execution_chain.steps[0]",
                "execution_chain.metadata",
            },
        )

    def test_validation_reports_invalid_contract_shape(self) -> None:
        contract = self.build_contract()
        object.__setattr__(contract, "contract_version", "")
        object.__setattr__(contract, "chains", ("not-a-chain",))
        object.__setattr__(contract, "metadata", {"bad": "mutable"})

        result = validate_execution_chain_contract(contract)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "execution_chain_contract.contract_version",
                "execution_chain_contract.chains[0]",
                "execution_chain_contract.metadata",
            },
        )

    def test_validation_reports_empty_contract(self) -> None:
        contract = ExecutionChainContract(chains=())

        result = validate_execution_chain_contract(contract)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "empty_execution_chain_contract_chains")

    def test_platform_core_serializer_compatibility_is_preserved(self) -> None:
        execution = UniversalExecution(
            object_id=UUID("00000000-0000-0000-0000-000000009403"),
            execution_type=ExecutionType.ACTION,
        )

        payload = ObjectSerializer.serialize(execution)

        self.assertEqual(payload["object_type"], "UniversalExecution")
        self.assertEqual(payload["object_id"], "00000000-0000-0000-0000-000000009403")
        self.assertNotIn("chain", payload)
        self.assertNotIn("chain_contract", payload)

    def test_all_foundation_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000009404"),
            memory_type=MemoryType.SEMANTIC,
            content="Execution chain contracts coexist with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-echo"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000009405"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000009406"),
            context_type=ContextType.ANALYTICAL,
        )
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000009407"),
            reasoning_type=ReasoningType.DEDUCTIVE,
        )
        decision = UniversalDecision(
            object_id=UUID("00000000-0000-0000-0000-000000009408"),
            decision_type=DecisionType.RECOMMENDATION,
        )
        action = UniversalAction(
            object_id=UUID("00000000-0000-0000-0000-000000009409"),
            action_type=ActionType.TASK,
        )
        execution = UniversalExecution(
            object_id=UUID("00000000-0000-0000-0000-000000009410"),
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
        strategy = ExecutionStrategy(
            strategy_type=ExecutionStrategyType.PROCEDURAL,
            name="operator-review",
        )
        chain = ExecutionChain(
            chain_type=ExecutionChainType.DEPENDENCY,
            steps=(ExecutionStepReference(execution_identifier=str(execution.object_id)),),
        )

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertTrue(reasoning.validate().is_valid)
        self.assertTrue(decision.validate().is_valid)
        self.assertTrue(action.validate().is_valid)
        self.assertTrue(execution.validate().is_valid)
        self.assertEqual(strategy.strategy_type, ExecutionStrategyType.PROCEDURAL)
        self.assertTrue(validate_execution_chain(chain).is_valid)

    def test_execution_foundation_behavior_is_preserved(self) -> None:
        execution = UniversalExecution(execution_type=ExecutionType.ACTION)
        payload = execution.to_dict()

        self.assertTrue(execution.validate().is_valid)
        self.assertEqual(payload["execution_type"], "action")
        self.assertNotIn("execution_chain", payload)
        self.assertNotIn("execution_chain_contract", payload)

    def test_chain_references_do_not_embed_universal_execution(self) -> None:
        execution = UniversalExecution(execution_type=ExecutionType.OBSERVATION)
        step = ExecutionStepReference(execution_identifier=str(execution.object_id))

        self.assertIsInstance(step.execution_identifier, str)
        self.assertNotIsInstance(step.execution_identifier, UniversalExecution)

    def test_no_execution_resolution_or_future_behavior_is_exposed(self) -> None:
        step = self.build_step()
        chain = self.build_chain()
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

        self.assertTrue(forbidden_names.isdisjoint(set(dir(step))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(chain))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(contract))))


if __name__ == "__main__":
    unittest.main()
