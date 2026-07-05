import unittest
from dataclasses import FrozenInstanceError
from uuid import UUID

from packages.context import ContextType, UniversalContext
from packages.decision import (
    DecisionChain,
    DecisionChainContract,
    DecisionChainMetadata,
    DecisionChainType,
    DecisionInputCollection,
    DecisionInputReference,
    DecisionInputType,
    DecisionOrigin,
    DecisionProvenance,
    DecisionStepReference,
    DecisionStrategy,
    DecisionStrategyType,
    DecisionType,
    UniversalDecision,
    validate_decision_chain,
    validate_decision_chain_contract,
    validate_decision_chain_metadata,
    validate_decision_step_reference,
)
from packages.knowledge import KnowledgeType, UniversalKnowledge
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import ObjectSerializer, ValidationResult
from packages.reasoning import ReasoningType, UniversalReasoning


class DecisionChainContractTest(unittest.TestCase):
    def build_step(self) -> DecisionStepReference:
        return DecisionStepReference(
            decision_identifier="decision:00000000-0000-0000-0000-000000007401",
            metadata=DecisionChainMetadata(values={"z": "last", "a": "first"}),
        )

    def build_chain(self) -> DecisionChain:
        return DecisionChain(
            chain_type=DecisionChainType.SEQUENTIAL,
            steps=(self.build_step(),),
            metadata=DecisionChainMetadata(values={"mission": "echo"}),
        )

    def build_contract(self) -> DecisionChainContract:
        return DecisionChainContract(
            chains=(
                self.build_chain(),
                DecisionChain(
                    chain_type=DecisionChainType.REVIEW,
                    steps=(
                        DecisionStepReference(
                            decision_identifier=(
                                "decision:00000000-0000-0000-0000-000000007402"
                            ),
                        ),
                    ),
                ),
            ),
            metadata=DecisionChainMetadata(values={"mission": "echo"}),
            contract_version="1.0",
        )

    def test_decision_chain_type_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {chain_type.value for chain_type in DecisionChainType},
            {"sequential", "hierarchical", "dependency", "alternative", "review", "unknown"},
        )

    def test_decision_chain_metadata_is_immutable_and_deterministic(self) -> None:
        metadata = DecisionChainMetadata(values={"z": "last", "a": "first"})

        self.assertEqual(metadata.to_dict(), {"a": "first", "z": "last"})
        with self.assertRaises(FrozenInstanceError):
            metadata.values = ()

    def test_decision_step_reference_is_opaque_and_deterministic(self) -> None:
        step = self.build_step()

        self.assertEqual(
            step.to_dict(),
            {
                "decision_identifier": "decision:00000000-0000-0000-0000-000000007401",
                "metadata": {"a": "first", "z": "last"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            step.decision_identifier = "changed"

    def test_decision_chain_constructs_deterministic_payload(self) -> None:
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
            chain.chain_type = DecisionChainType.DEPENDENCY

    def test_decision_chain_contract_constructs_deterministic_payload(self) -> None:
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
                                "decision_identifier": (
                                    "decision:00000000-0000-0000-0000-000000007402"
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
            validate_decision_chain_metadata(DecisionChainMetadata()),
            ValidationResult,
        )
        self.assertTrue(validate_decision_step_reference(self.build_step()).is_valid)
        self.assertTrue(validate_decision_chain(self.build_chain()).is_valid)
        self.assertTrue(validate_decision_chain_contract(self.build_contract()).is_valid)

    def test_validation_reports_invalid_step_shape(self) -> None:
        step = self.build_step()
        object.__setattr__(step, "decision_identifier", "")
        object.__setattr__(step, "metadata", {"bad": "mutable"})

        result = validate_decision_step_reference(step)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "decision_step_reference.decision_identifier",
                "decision_step_reference.metadata",
            },
        )

    def test_validation_reports_invalid_chain_shape(self) -> None:
        chain = self.build_chain()
        object.__setattr__(chain, "chain_type", "sequential")
        object.__setattr__(chain, "steps", ("not-a-step",))
        object.__setattr__(chain, "metadata", {"bad": "mutable"})

        result = validate_decision_chain(chain)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "decision_chain.chain_type",
                "decision_chain.steps[0]",
                "decision_chain.metadata",
            },
        )

    def test_validation_reports_invalid_contract_shape(self) -> None:
        contract = self.build_contract()
        object.__setattr__(contract, "contract_version", "")
        object.__setattr__(contract, "chains", ("not-a-chain",))
        object.__setattr__(contract, "metadata", {"bad": "mutable"})

        result = validate_decision_chain_contract(contract)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "decision_chain_contract.contract_version",
                "decision_chain_contract.chains[0]",
                "decision_chain_contract.metadata",
            },
        )

    def test_validation_reports_empty_contract(self) -> None:
        contract = DecisionChainContract(chains=())

        result = validate_decision_chain_contract(contract)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "empty_decision_chain_contract_chains")

    def test_platform_core_serializer_compatibility_is_preserved(self) -> None:
        decision = UniversalDecision(
            object_id=UUID("00000000-0000-0000-0000-000000007403"),
            decision_type=DecisionType.RECOMMENDATION,
        )

        payload = ObjectSerializer.serialize(decision)

        self.assertEqual(payload["object_type"], "UniversalDecision")
        self.assertEqual(payload["object_id"], "00000000-0000-0000-0000-000000007403")
        self.assertNotIn("chain", payload)
        self.assertNotIn("chain_contract", payload)

    def test_all_foundation_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000007404"),
            memory_type=MemoryType.SEMANTIC,
            content="Decision chain contracts coexist with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-echo"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000007405"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000007406"),
            context_type=ContextType.ANALYTICAL,
        )
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000007407"),
            reasoning_type=ReasoningType.DEDUCTIVE,
        )
        decision = UniversalDecision(
            object_id=UUID("00000000-0000-0000-0000-000000007408"),
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
        strategy = DecisionStrategy(
            strategy_type=DecisionStrategyType.ANALYTICAL,
            name="evidence-review",
        )
        chain = DecisionChain(
            chain_type=DecisionChainType.DEPENDENCY,
            steps=(DecisionStepReference(decision_identifier=str(decision.object_id)),),
        )

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertTrue(reasoning.validate().is_valid)
        self.assertTrue(decision.validate().is_valid)
        self.assertEqual(strategy.strategy_type, DecisionStrategyType.ANALYTICAL)
        self.assertTrue(validate_decision_chain(chain).is_valid)

    def test_decision_foundation_behavior_is_preserved(self) -> None:
        decision = UniversalDecision(decision_type=DecisionType.APPROVAL)
        payload = decision.to_dict()

        self.assertTrue(decision.validate().is_valid)
        self.assertEqual(payload["decision_type"], "approval")
        self.assertNotIn("decision_chain", payload)
        self.assertNotIn("decision_chain_contract", payload)

    def test_chain_references_do_not_embed_universal_decision(self) -> None:
        decision = UniversalDecision(decision_type=DecisionType.OBSERVATION)
        step = DecisionStepReference(decision_identifier=str(decision.object_id))

        self.assertIsInstance(step.decision_identifier, str)
        self.assertNotIsInstance(step.decision_identifier, UniversalDecision)

    def test_no_execution_resolution_or_future_behavior_is_exposed(self) -> None:
        step = self.build_step()
        chain = self.build_chain()
        contract = self.build_contract()
        forbidden_names = {
            "ai",
            "autonomous",
            "compute",
            "decide",
            "evaluate",
            "execute",
            "optimize",
            "orchestrate",
            "persist",
            "plan",
            "resolve",
            "search",
            "workflow",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(step))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(chain))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(contract))))


if __name__ == "__main__":
    unittest.main()
