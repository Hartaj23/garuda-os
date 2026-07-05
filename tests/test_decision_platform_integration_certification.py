import json
import unittest
from datetime import datetime
from uuid import UUID

from packages.context import ContextType, UniversalContext
from packages.decision import (
    DecisionChain,
    DecisionChainContract,
    DecisionChainMetadata,
    DecisionChainType,
    DecisionConfidence,
    DecisionInputCollection,
    DecisionInputReference,
    DecisionInputType,
    DecisionMetadata,
    DecisionOrigin,
    DecisionOutcome,
    DecisionProvenance,
    DecisionState,
    DecisionStepReference,
    DecisionStrategy,
    DecisionStrategyContract,
    DecisionStrategyMetadata,
    DecisionStrategyType,
    DecisionType,
    DecisionWorkspace,
    UniversalDecision,
    WorkspaceStatistics,
    validate_decision_chain,
    validate_decision_chain_contract,
    validate_decision_input_collection,
    validate_decision_provenance,
    validate_decision_strategy,
    validate_decision_strategy_contract,
    validate_decision_workspace,
)
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
from packages.reasoning import ReasoningType, UniversalReasoning


TIMESTAMP = datetime.fromisoformat("2026-07-05T00:00:00+00:00")


def build_certified_inputs() -> DecisionInputCollection:
    return DecisionInputCollection(
        references=(
            DecisionInputReference(
                input_type=DecisionInputType.KNOWLEDGE,
                identifier="knowledge:00000000-0000-0000-0000-000000007701",
                reference_metadata={"z": "last", "a": "first"},
            ),
            DecisionInputReference(
                input_type=DecisionInputType.CONTEXT,
                identifier="context:00000000-0000-0000-0000-000000007702",
            ),
            DecisionInputReference(
                input_type=DecisionInputType.REASONING,
                identifier="reasoning:00000000-0000-0000-0000-000000007703",
            ),
        )
    )


def build_certified_provenance() -> DecisionProvenance:
    inputs = build_certified_inputs()
    return DecisionProvenance(
        origin=DecisionOrigin.HUMAN,
        author="codex",
        created_at=TIMESTAMP,
        input_references=inputs.references,
        provenance_metadata={"z": "last", "a": "first"},
    )


def build_certified_decision(
    decision_id: str = "00000000-0000-0000-0000-000000007601",
) -> UniversalDecision:
    return UniversalDecision(
        object_id=UUID(decision_id),
        decision_type=DecisionType.RECOMMENDATION,
        decision_state=DecisionState.CONFIRMED,
        decision_outcome=DecisionOutcome.ACCEPTED,
        decision_confidence=DecisionConfidence(level="high", rationale="certified"),
        decision_metadata=DecisionMetadata(values={"z": "last", "a": "first"}),
        decision_inputs=build_certified_inputs(),
        decision_provenance=build_certified_provenance(),
        metadata={"owner": "platform", "mission": "golf"},
        tags=["decision", "certification"],
        lifecycle_state=LifecycleState.DRAFT,
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


class DecisionPlatformIntegrationCertificationTest(unittest.TestCase):
    def test_scenario_1_universal_decision_platform_certification(self) -> None:
        decision = build_certified_decision()
        payload = decision.to_dict()
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        registry = ObjectRegistry()
        registry.register(UniversalDecision)
        relationship = Relationship(
            source_object_id=decision.object_id,
            target_object_id=UUID("00000000-0000-0000-0000-000000007801"),
            relationship_type=RelationshipType.REFERENCES,
        )

        self.assertIsInstance(decision, CanonicalObject)
        self.assertIsInstance(decision.validate(), ValidationResult)
        self.assertTrue(decision.validate().is_valid)
        self.assertEqual(payload, build_certified_decision().to_dict())
        self.assertEqual(encoded, json.dumps(payload, sort_keys=True, separators=(",", ":")))
        self.assertEqual(ObjectSerializer.serialize(decision)["object_type"], "UniversalDecision")
        self.assertEqual(registry.lookup("UniversalDecision"), UniversalDecision)
        decision.transition_to(LifecycleState.ACTIVE)
        self.assertEqual(decision.lifecycle_state, LifecycleState.ACTIVE)
        self.assertEqual(relationship.to_dict()["source_object_id"], str(decision.object_id))
        self.assertEqual(relationship.to_dict()["relationship_type"], "references")

    def test_scenario_2_decision_input_and_provenance_certification(self) -> None:
        inputs = build_certified_inputs()
        provenance = build_certified_provenance()

        self.assertTrue(validate_decision_input_collection(inputs).is_valid)
        self.assertTrue(validate_decision_provenance(provenance).is_valid)
        self.assertEqual(
            inputs.to_dict()["references"][0],
            {
                "input_type": "knowledge",
                "identifier": "knowledge:00000000-0000-0000-0000-000000007701",
                "reference_metadata": {"a": "first", "z": "last"},
            },
        )
        self.assertEqual(
            provenance.to_dict()["provenance_metadata"],
            {"a": "first", "z": "last"},
        )
        self.assert_no_behavior(inputs, {"resolve", "retrieve", "search"})
        self.assert_no_behavior(provenance, {"evaluate", "resolve", "verify"})

    def test_scenario_3_decision_strategy_contract_certification(self) -> None:
        strategy = DecisionStrategy(
            strategy_type=DecisionStrategyType.ANALYTICAL,
            name="evidence-review",
            description="Descriptive strategy only.",
            metadata=DecisionStrategyMetadata(values={"z": "last", "a": "first"}),
        )
        contract = DecisionStrategyContract(
            strategies=(strategy,),
            metadata=DecisionStrategyMetadata(values={"mission": "golf"}),
            contract_version="1.0",
        )

        self.assertTrue(validate_decision_strategy(strategy).is_valid)
        self.assertTrue(validate_decision_strategy_contract(contract).is_valid)
        self.assertEqual(strategy.to_dict(), strategy.to_dict())
        self.assertEqual(contract.to_dict(), contract.to_dict())
        self.assertEqual(strategy.to_dict()["metadata"], {"a": "first", "z": "last"})
        self.assert_no_behavior(strategy, {"execute", "optimize", "rank"})
        self.assert_no_behavior(contract, {"engine", "execute", "orchestrate"})

    def test_scenario_4_decision_chain_contract_certification(self) -> None:
        step = DecisionStepReference(
            decision_identifier="decision:00000000-0000-0000-0000-000000007901",
            metadata=DecisionChainMetadata(values={"z": "last", "a": "first"}),
        )
        chain = DecisionChain(
            chain_type=DecisionChainType.SEQUENTIAL,
            steps=(step,),
            metadata=DecisionChainMetadata(values={"mission": "golf"}),
        )
        contract = DecisionChainContract(
            chains=(chain,),
            metadata=DecisionChainMetadata(values={"mission": "golf"}),
            contract_version="1.0",
        )

        self.assertTrue(validate_decision_chain(chain).is_valid)
        self.assertTrue(validate_decision_chain_contract(contract).is_valid)
        self.assertEqual(chain.to_dict(), chain.to_dict())
        self.assertEqual(contract.to_dict(), contract.to_dict())
        self.assertEqual(
            chain.to_dict()["steps"][0]["decision_identifier"],
            "decision:00000000-0000-0000-0000-000000007901",
        )
        self.assert_no_behavior(chain, {"execute", "orchestrate", "resolve", "search"})
        self.assert_no_behavior(contract, {"engine", "execute", "orchestrate"})

    def test_scenario_5_decision_workspace_certification(self) -> None:
        workspace = DecisionWorkspace()
        decision = build_certified_decision()

        self.assertIsInstance(workspace.statistics(), WorkspaceStatistics)
        workspace.add(decision)
        with self.assertRaises(ValueError):
            workspace.add(decision)

        self.assertIs(workspace.get(decision.object_id), decision)
        self.assertIs(workspace.get(str(decision.object_id)), decision)
        self.assertEqual(workspace.identifiers(), (decision.object_id,))
        self.assertEqual(workspace.statistics().total_decisions, 1)
        self.assertEqual(workspace.statistics().active_decisions, 0)
        self.assertEqual(workspace.statistics().archived_decisions, 0)
        self.assertIs(workspace.remove(str(decision.object_id)), decision)
        self.assertIsNone(workspace.get(decision.object_id))
        workspace.add(decision)
        workspace.clear()
        self.assertEqual(workspace.identifiers(), ())
        self.assertEqual(workspace.statistics().total_decisions, 0)
        self.assertTrue(validate_decision_workspace(workspace).is_valid)
        self.assertFalse(hasattr(workspace, "to_dict"))
        self.assert_no_behavior(workspace, {"execute", "persist", "rank", "search"})

    def test_scenario_6_end_to_end_decision_foundation_certification(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000007711"),
            memory_type=MemoryType.SEMANTIC,
            content="Decision certification coexists with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-golf"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000007712"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000007713"),
            context_type=ContextType.ANALYTICAL,
        )
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000007714"),
            reasoning_type=ReasoningType.DEDUCTIVE,
        )
        decision = build_certified_decision()
        strategy = DecisionStrategy(
            strategy_type=DecisionStrategyType.ANALYTICAL,
            name="evidence-review",
        )
        strategy_contract = DecisionStrategyContract(strategies=(strategy,))
        chain = DecisionChain(
            chain_type=DecisionChainType.SEQUENTIAL,
            steps=(DecisionStepReference(str(decision.object_id)),),
        )
        chain_contract = DecisionChainContract(chains=(chain,))
        workspace = DecisionWorkspace()

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertTrue(reasoning.validate().is_valid)
        self.assertTrue(decision.validate().is_valid)
        self.assertEqual(ObjectSerializer.serialize(decision)["object_id"], str(decision.object_id))
        self.assertTrue(validate_decision_input_collection(decision.decision_inputs).is_valid)
        self.assertTrue(validate_decision_provenance(decision.decision_provenance).is_valid)
        self.assertTrue(validate_decision_strategy_contract(strategy_contract).is_valid)
        self.assertTrue(validate_decision_chain_contract(chain_contract).is_valid)

        workspace.add(decision)
        self.assertIs(workspace.get(decision.object_id), decision)
        self.assertIs(workspace.remove(decision.object_id), decision)
        self.assertTrue(workspace.validate().is_valid)
        self.assertEqual(workspace.identifiers(), ())
        self.assertEqual(workspace.statistics().total_decisions, 0)

    def test_explicit_decision_foundation_boundary_certification(self) -> None:
        decision = build_certified_decision()
        inputs = build_certified_inputs()
        provenance = build_certified_provenance()
        strategy = DecisionStrategy(
            strategy_type=DecisionStrategyType.ANALYTICAL,
            name="evidence-review",
        )
        strategy_contract = DecisionStrategyContract(strategies=(strategy,))
        chain = DecisionChain(chain_type=DecisionChainType.SEQUENTIAL)
        chain_contract = DecisionChainContract(chains=(chain,))
        workspace = DecisionWorkspace()

        self.assert_no_behavior(decision, {"execute", "optimize", "plan", "resolve"})
        self.assert_no_behavior(inputs, {"resolve", "retrieve", "search"})
        self.assert_no_behavior(provenance, {"evaluate", "verify", "resolve"})
        self.assert_no_behavior(strategy, {"execute", "optimize", "rank"})
        self.assert_no_behavior(strategy_contract, {"engine", "execute", "orchestrate"})
        self.assert_no_behavior(chain, {"execute", "orchestrate", "resolve"})
        self.assert_no_behavior(chain_contract, {"engine", "execute", "orchestrate"})
        self.assert_no_behavior(workspace, {"execute", "persist", "rank", "search", "workflow"})

    def test_cross_foundation_certification_does_not_modify_other_foundations(self) -> None:
        memory = UniversalMemory(
            memory_type=MemoryType.SEMANTIC,
            content="Cross-foundation certification.",
            source=MemorySource(source_type="test", source_identifier="mission-golf"),
        )
        knowledge = UniversalKnowledge(knowledge_type=KnowledgeType.FACT)
        context = UniversalContext(context_type=ContextType.ANALYTICAL)
        reasoning = UniversalReasoning(reasoning_type=ReasoningType.DEDUCTIVE)
        decision = build_certified_decision()

        before = (
            memory.to_dict(),
            knowledge.to_dict(),
            context.to_dict(),
            reasoning.to_dict(),
        )
        decision.validate()
        DecisionWorkspace().add(decision)
        after = (
            memory.to_dict(),
            knowledge.to_dict(),
            context.to_dict(),
            reasoning.to_dict(),
        )

        self.assertEqual(before, after)

    def assert_no_behavior(self, obj: object, forbidden_names: set[str]) -> None:
        self.assertTrue(forbidden_names.isdisjoint(set(dir(obj))))


if __name__ == "__main__":
    unittest.main()
