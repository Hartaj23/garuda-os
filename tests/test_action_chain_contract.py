import unittest
from dataclasses import FrozenInstanceError
from uuid import UUID

from packages.action import (
    ActionChain,
    ActionChainContract,
    ActionChainMetadata,
    ActionChainType,
    ActionInputCollection,
    ActionInputReference,
    ActionInputType,
    ActionOrigin,
    ActionProvenance,
    ActionStepReference,
    ActionStrategy,
    ActionStrategyType,
    ActionType,
    UniversalAction,
    validate_action_chain,
    validate_action_chain_contract,
    validate_action_chain_metadata,
    validate_action_step_reference,
)
from packages.context import ContextType, UniversalContext
from packages.decision import DecisionType, UniversalDecision
from packages.knowledge import KnowledgeType, UniversalKnowledge
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import ObjectSerializer, ValidationResult
from packages.reasoning import ReasoningType, UniversalReasoning


class ActionChainContractTest(unittest.TestCase):
    def build_step(self) -> ActionStepReference:
        return ActionStepReference(
            action_identifier="action:00000000-0000-0000-0000-000000008401",
            metadata=ActionChainMetadata(values={"z": "last", "a": "first"}),
        )

    def build_chain(self) -> ActionChain:
        return ActionChain(
            chain_type=ActionChainType.SEQUENTIAL,
            steps=(self.build_step(),),
            metadata=ActionChainMetadata(values={"mission": "echo"}),
        )

    def build_contract(self) -> ActionChainContract:
        return ActionChainContract(
            chains=(
                self.build_chain(),
                ActionChain(
                    chain_type=ActionChainType.REVIEW,
                    steps=(
                        ActionStepReference(
                            action_identifier=(
                                "action:00000000-0000-0000-0000-000000008402"
                            ),
                        ),
                    ),
                ),
            ),
            metadata=ActionChainMetadata(values={"mission": "echo"}),
            contract_version="1.0",
        )

    def test_action_chain_type_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {chain_type.value for chain_type in ActionChainType},
            {"sequential", "parallel", "dependency", "review", "fallback", "unknown"},
        )

    def test_action_chain_metadata_is_immutable_and_deterministic(self) -> None:
        metadata = ActionChainMetadata(values={"z": "last", "a": "first"})

        self.assertEqual(metadata.to_dict(), {"a": "first", "z": "last"})
        with self.assertRaises(FrozenInstanceError):
            metadata.values = ()

    def test_action_step_reference_is_opaque_and_deterministic(self) -> None:
        step = self.build_step()

        self.assertEqual(
            step.to_dict(),
            {
                "action_identifier": "action:00000000-0000-0000-0000-000000008401",
                "metadata": {"a": "first", "z": "last"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            step.action_identifier = "changed"

    def test_action_chain_constructs_deterministic_payload(self) -> None:
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
            chain.chain_type = ActionChainType.DEPENDENCY

    def test_action_chain_contract_constructs_deterministic_payload(self) -> None:
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
                                "action_identifier": (
                                    "action:00000000-0000-0000-0000-000000008402"
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
            validate_action_chain_metadata(ActionChainMetadata()),
            ValidationResult,
        )
        self.assertTrue(validate_action_step_reference(self.build_step()).is_valid)
        self.assertTrue(validate_action_chain(self.build_chain()).is_valid)
        self.assertTrue(validate_action_chain_contract(self.build_contract()).is_valid)

    def test_validation_reports_invalid_step_shape(self) -> None:
        step = self.build_step()
        object.__setattr__(step, "action_identifier", "")
        object.__setattr__(step, "metadata", {"bad": "mutable"})

        result = validate_action_step_reference(step)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "action_step_reference.action_identifier",
                "action_step_reference.metadata",
            },
        )

    def test_validation_reports_invalid_chain_shape(self) -> None:
        chain = self.build_chain()
        object.__setattr__(chain, "chain_type", "sequential")
        object.__setattr__(chain, "steps", ("not-a-step",))
        object.__setattr__(chain, "metadata", {"bad": "mutable"})

        result = validate_action_chain(chain)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "action_chain.chain_type",
                "action_chain.steps[0]",
                "action_chain.metadata",
            },
        )

    def test_validation_reports_invalid_contract_shape(self) -> None:
        contract = self.build_contract()
        object.__setattr__(contract, "contract_version", "")
        object.__setattr__(contract, "chains", ("not-a-chain",))
        object.__setattr__(contract, "metadata", {"bad": "mutable"})

        result = validate_action_chain_contract(contract)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "action_chain_contract.contract_version",
                "action_chain_contract.chains[0]",
                "action_chain_contract.metadata",
            },
        )

    def test_validation_reports_empty_contract(self) -> None:
        contract = ActionChainContract(chains=())

        result = validate_action_chain_contract(contract)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "empty_action_chain_contract_chains")

    def test_platform_core_serializer_compatibility_is_preserved(self) -> None:
        action = UniversalAction(
            object_id=UUID("00000000-0000-0000-0000-000000008403"),
            action_type=ActionType.TASK,
        )

        payload = ObjectSerializer.serialize(action)

        self.assertEqual(payload["object_type"], "UniversalAction")
        self.assertEqual(payload["object_id"], "00000000-0000-0000-0000-000000008403")
        self.assertNotIn("chain", payload)
        self.assertNotIn("chain_contract", payload)

    def test_all_foundation_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000008404"),
            memory_type=MemoryType.SEMANTIC,
            content="Action chain contracts coexist with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-echo"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000008405"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000008406"),
            context_type=ContextType.ANALYTICAL,
        )
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000008407"),
            reasoning_type=ReasoningType.DEDUCTIVE,
        )
        decision = UniversalDecision(
            object_id=UUID("00000000-0000-0000-0000-000000008408"),
            decision_type=DecisionType.RECOMMENDATION,
        )
        action = UniversalAction(
            object_id=UUID("00000000-0000-0000-0000-000000008409"),
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
        strategy = ActionStrategy(
            strategy_type=ActionStrategyType.PROCEDURAL,
            name="operator-review",
        )
        chain = ActionChain(
            chain_type=ActionChainType.DEPENDENCY,
            steps=(ActionStepReference(action_identifier=str(action.object_id)),),
        )

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertTrue(reasoning.validate().is_valid)
        self.assertTrue(decision.validate().is_valid)
        self.assertTrue(action.validate().is_valid)
        self.assertEqual(strategy.strategy_type, ActionStrategyType.PROCEDURAL)
        self.assertTrue(validate_action_chain(chain).is_valid)

    def test_action_foundation_behavior_is_preserved(self) -> None:
        action = UniversalAction(action_type=ActionType.APPROVAL)
        payload = action.to_dict()

        self.assertTrue(action.validate().is_valid)
        self.assertEqual(payload["action_type"], "approval")
        self.assertNotIn("action_chain", payload)
        self.assertNotIn("action_chain_contract", payload)

    def test_chain_references_do_not_embed_universal_action(self) -> None:
        action = UniversalAction(action_type=ActionType.OBSERVATION)
        step = ActionStepReference(action_identifier=str(action.object_id))

        self.assertIsInstance(step.action_identifier, str)
        self.assertNotIsInstance(step.action_identifier, UniversalAction)

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
