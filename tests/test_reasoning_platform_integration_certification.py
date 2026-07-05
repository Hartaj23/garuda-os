import json
import unittest
from datetime import datetime
from uuid import UUID

from packages.context import ContextType, UniversalContext
from packages.knowledge import KnowledgeType, UniversalKnowledge
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import (
    CanonicalObject,
    LifecycleState,
    ObjectRegistry,
    ObjectSerializer,
    Relationship,
    RelationshipType,
    ValidationResult,
)
from packages.reasoning import (
    ChainMetadata,
    ChainType,
    ReasoningChain,
    ReasoningChainContract,
    ReasoningConfidence,
    ReasoningInputCollection,
    ReasoningInputReference,
    ReasoningInputType,
    ReasoningMetadata,
    ReasoningOrigin,
    ReasoningProvenance,
    ReasoningState,
    ReasoningStepReference,
    ReasoningStrategy,
    ReasoningStrategyContract,
    ReasoningType,
    ReasoningWorkspace,
    StrategyMetadata,
    StrategyType,
    UniversalReasoning,
    WorkspaceStatistics,
    validate_reasoning_chain,
    validate_reasoning_chain_contract,
    validate_reasoning_input_collection,
    validate_reasoning_provenance,
    validate_reasoning_strategy,
    validate_reasoning_strategy_contract,
    validate_reasoning_workspace,
)


TIMESTAMP = datetime.fromisoformat("2026-07-05T00:00:00+00:00")


def build_certified_inputs() -> ReasoningInputCollection:
    return ReasoningInputCollection(
        references=(
            ReasoningInputReference(
                input_type=ReasoningInputType.MEMORY,
                identifier="memory:00000000-0000-0000-0000-000000006701",
                reference_metadata={"z": "last", "a": "first"},
            ),
            ReasoningInputReference(
                input_type=ReasoningInputType.KNOWLEDGE,
                identifier="knowledge:00000000-0000-0000-0000-000000006702",
            ),
            ReasoningInputReference(
                input_type=ReasoningInputType.CONTEXT,
                identifier="context:00000000-0000-0000-0000-000000006703",
            ),
        )
    )


def build_certified_provenance() -> ReasoningProvenance:
    inputs = build_certified_inputs()
    return ReasoningProvenance(
        origin=ReasoningOrigin.HUMAN_DEFINED,
        creator="codex",
        created_at=TIMESTAMP,
        input_references=inputs.references,
        provenance_metadata={"z": "last", "a": "first"},
    )


def build_certified_reasoning(
    reasoning_id: str = "00000000-0000-0000-0000-000000006601",
) -> UniversalReasoning:
    return UniversalReasoning(
        object_id=UUID(reasoning_id),
        reasoning_type=ReasoningType.DEDUCTIVE,
        reasoning_state=ReasoningState.VALIDATED,
        reasoning_confidence=ReasoningConfidence(level="high", rationale="certified"),
        reasoning_metadata=ReasoningMetadata(values={"z": "last", "a": "first"}),
        reasoning_inputs=build_certified_inputs(),
        reasoning_provenance=build_certified_provenance(),
        metadata={"owner": "platform", "mission": "golf"},
        tags=["reasoning", "certification"],
        lifecycle_state=LifecycleState.DRAFT,
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


class ReasoningPlatformIntegrationCertificationTest(unittest.TestCase):
    def test_scenario_1_universal_reasoning_platform_certification(self) -> None:
        reasoning = build_certified_reasoning()
        payload = reasoning.to_dict()
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        registry = ObjectRegistry()
        registry.register(UniversalReasoning)
        relationship = Relationship(
            source_object_id=reasoning.object_id,
            target_object_id=UUID("00000000-0000-0000-0000-000000006801"),
            relationship_type=RelationshipType.REFERENCES,
        )

        self.assertIsInstance(reasoning, CanonicalObject)
        self.assertIsInstance(reasoning.validate(), ValidationResult)
        self.assertTrue(reasoning.validate().is_valid)
        self.assertEqual(payload, build_certified_reasoning().to_dict())
        self.assertEqual(encoded, json.dumps(payload, sort_keys=True, separators=(",", ":")))
        self.assertEqual(ObjectSerializer.serialize(reasoning)["object_type"], "UniversalReasoning")
        self.assertEqual(registry.lookup("UniversalReasoning"), UniversalReasoning)
        reasoning.transition_to(LifecycleState.ACTIVE)
        self.assertEqual(reasoning.lifecycle_state, LifecycleState.ACTIVE)
        self.assertEqual(relationship.to_dict()["source_object_id"], str(reasoning.object_id))
        self.assertEqual(relationship.to_dict()["relationship_type"], "references")

    def test_scenario_2_reasoning_input_and_provenance_certification(self) -> None:
        inputs = build_certified_inputs()
        provenance = build_certified_provenance()

        self.assertTrue(validate_reasoning_input_collection(inputs).is_valid)
        self.assertTrue(validate_reasoning_provenance(provenance).is_valid)
        self.assertEqual(
            inputs.to_dict()["references"][0],
            {
                "input_type": "memory",
                "identifier": "memory:00000000-0000-0000-0000-000000006701",
                "reference_metadata": {"a": "first", "z": "last"},
            },
        )
        self.assertEqual(
            provenance.to_dict()["provenance_metadata"],
            {"a": "first", "z": "last"},
        )
        self.assert_no_behavior(inputs, {"resolve", "retrieve", "search"})
        self.assert_no_behavior(provenance, {"evaluate", "resolve", "verify"})

    def test_scenario_3_reasoning_strategy_contract_certification(self) -> None:
        strategy = ReasoningStrategy(
            strategy_type=StrategyType.SEQUENTIAL,
            name="ordered-review",
            description="Descriptive strategy only.",
            metadata=StrategyMetadata(values={"z": "last", "a": "first"}),
        )
        contract = ReasoningStrategyContract(
            supported_strategy_types=(
                StrategyType.SEQUENTIAL,
                StrategyType.COMPARATIVE,
                StrategyType.VALIDATION,
            ),
            metadata=StrategyMetadata(values={"mission": "golf"}),
            contract_version="1.0",
        )

        self.assertTrue(validate_reasoning_strategy(strategy).is_valid)
        self.assertTrue(validate_reasoning_strategy_contract(contract).is_valid)
        self.assertEqual(strategy.to_dict(), strategy.to_dict())
        self.assertEqual(contract.to_dict(), contract.to_dict())
        self.assertEqual(strategy.to_dict()["metadata"], {"a": "first", "z": "last"})
        self.assert_no_behavior(strategy, {"execute", "infer", "rank", "reason"})
        self.assert_no_behavior(contract, {"engine", "execute", "orchestrate"})

    def test_scenario_4_reasoning_chain_contract_certification(self) -> None:
        step = ReasoningStepReference(
            identifier="reasoning-step:00000000-0000-0000-0000-000000006901",
            sequence=0,
            metadata=ChainMetadata(values={"z": "last", "a": "first"}),
        )
        chain = ReasoningChain(
            chain_type=ChainType.LINEAR,
            steps=(step,),
            metadata=ChainMetadata(values={"mission": "golf"}),
        )
        contract = ReasoningChainContract(
            supported_chain_types=(
                ChainType.LINEAR,
                ChainType.BRANCHING,
                ChainType.DEPENDENCY,
            ),
            metadata=ChainMetadata(values={"mission": "golf"}),
            contract_version="1.0",
        )

        self.assertTrue(validate_reasoning_chain(chain).is_valid)
        self.assertTrue(validate_reasoning_chain_contract(contract).is_valid)
        self.assertEqual(chain.to_dict(), chain.to_dict())
        self.assertEqual(contract.to_dict(), contract.to_dict())
        self.assertEqual(
            chain.to_dict()["steps"][0]["identifier"],
            "reasoning-step:00000000-0000-0000-0000-000000006901",
        )
        self.assert_no_behavior(chain, {"execute", "infer", "resolve", "search"})
        self.assert_no_behavior(contract, {"engine", "execute", "orchestrate"})

    def test_scenario_5_reasoning_workspace_certification(self) -> None:
        workspace = ReasoningWorkspace()
        reasoning = build_certified_reasoning()

        self.assertIsInstance(workspace.statistics(), WorkspaceStatistics)
        workspace.add(reasoning)
        with self.assertRaises(ValueError):
            workspace.add(reasoning)

        self.assertIs(workspace.get(reasoning.object_id), reasoning)
        self.assertIs(workspace.get(str(reasoning.object_id)), reasoning)
        self.assertEqual(workspace.identifiers(), (reasoning.object_id,))
        self.assertEqual(workspace.statistics().total_reasoning_objects, 1)
        self.assertEqual(workspace.statistics().active_reasoning_objects, 0)
        self.assertEqual(workspace.statistics().archived_reasoning_objects, 0)
        self.assertIs(workspace.remove(str(reasoning.object_id)), reasoning)
        self.assertIsNone(workspace.get(reasoning.object_id))
        workspace.add(reasoning)
        workspace.clear()
        self.assertEqual(workspace.identifiers(), ())
        self.assertEqual(workspace.statistics().total_reasoning_objects, 0)
        self.assertTrue(validate_reasoning_workspace(workspace).is_valid)
        self.assertFalse(hasattr(workspace, "to_dict"))
        self.assert_no_behavior(workspace, {"execute", "infer", "persist", "search"})

    def test_scenario_6_end_to_end_reasoning_foundation_certification(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000006711"),
            memory_type=MemoryType.SEMANTIC,
            content="Reasoning certification coexists with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-golf"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000006712"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000006713"),
            context_type=ContextType.ANALYTICAL,
        )
        reasoning = build_certified_reasoning()
        strategy_contract = ReasoningStrategyContract(
            supported_strategy_types=(StrategyType.SEQUENTIAL,),
        )
        chain_contract = ReasoningChainContract(
            supported_chain_types=(ChainType.LINEAR,),
        )
        workspace = ReasoningWorkspace()

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertTrue(reasoning.validate().is_valid)
        self.assertEqual(ObjectSerializer.serialize(reasoning)["object_id"], str(reasoning.object_id))
        self.assertTrue(validate_reasoning_input_collection(reasoning.reasoning_inputs).is_valid)
        self.assertTrue(validate_reasoning_provenance(reasoning.reasoning_provenance).is_valid)
        self.assertTrue(validate_reasoning_strategy_contract(strategy_contract).is_valid)
        self.assertTrue(validate_reasoning_chain_contract(chain_contract).is_valid)

        workspace.add(reasoning)
        self.assertIs(workspace.get(reasoning.object_id), reasoning)
        self.assertIs(workspace.remove(reasoning.object_id), reasoning)
        self.assertTrue(workspace.validate().is_valid)
        self.assertEqual(workspace.identifiers(), ())
        self.assertEqual(workspace.statistics().total_reasoning_objects, 0)

    def test_explicit_reasoning_foundation_boundary_certification(self) -> None:
        reasoning = build_certified_reasoning()
        inputs = build_certified_inputs()
        provenance = build_certified_provenance()
        strategy = ReasoningStrategy(
            strategy_type=StrategyType.SEQUENTIAL,
            name="ordered-review",
        )
        strategy_contract = ReasoningStrategyContract(
            supported_strategy_types=(StrategyType.SEQUENTIAL,),
        )
        chain = ReasoningChain(chain_type=ChainType.LINEAR)
        chain_contract = ReasoningChainContract(supported_chain_types=(ChainType.LINEAR,))
        workspace = ReasoningWorkspace()

        self.assert_no_behavior(reasoning, {"execute", "infer", "conclude", "decide", "plan"})
        self.assert_no_behavior(inputs, {"resolve", "retrieve", "search"})
        self.assert_no_behavior(provenance, {"evaluate", "verify", "resolve"})
        self.assert_no_behavior(strategy, {"execute", "infer", "rank"})
        self.assert_no_behavior(strategy_contract, {"engine", "execute", "orchestrate"})
        self.assert_no_behavior(chain, {"execute", "infer", "resolve"})
        self.assert_no_behavior(chain_contract, {"engine", "execute", "orchestrate"})
        self.assert_no_behavior(workspace, {"execute", "infer", "persist", "search", "workflow"})

    def test_cross_foundation_certification_does_not_modify_other_foundations(self) -> None:
        memory = UniversalMemory(
            memory_type=MemoryType.SEMANTIC,
            content="Cross-foundation certification.",
            source=MemorySource(source_type="test", source_identifier="mission-golf"),
        )
        knowledge = UniversalKnowledge(knowledge_type=KnowledgeType.FACT)
        context = UniversalContext(context_type=ContextType.ANALYTICAL)
        reasoning = build_certified_reasoning()

        before = (
            memory.to_dict(),
            knowledge.to_dict(),
            context.to_dict(),
        )
        reasoning.validate()
        ReasoningWorkspace().add(reasoning)
        after = (
            memory.to_dict(),
            knowledge.to_dict(),
            context.to_dict(),
        )

        self.assertEqual(before, after)

    def assert_no_behavior(self, obj: object, forbidden_names: set[str]) -> None:
        self.assertTrue(forbidden_names.isdisjoint(set(dir(obj))))


if __name__ == "__main__":
    unittest.main()
