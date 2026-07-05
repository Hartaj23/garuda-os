import json
import unittest
from datetime import datetime
from uuid import UUID

from packages.action import (
    ActionChain,
    ActionChainContract,
    ActionChainMetadata,
    ActionChainType,
    ActionConfidence,
    ActionInputCollection,
    ActionInputReference,
    ActionInputType,
    ActionMetadata,
    ActionOrigin,
    ActionOutcome,
    ActionProvenance,
    ActionState,
    ActionStepReference,
    ActionStrategy,
    ActionStrategyContract,
    ActionStrategyMetadata,
    ActionStrategyType,
    ActionType,
    ActionWorkspace,
    UniversalAction,
    WorkspaceStatistics,
    validate_action_chain,
    validate_action_chain_contract,
    validate_action_input_collection,
    validate_action_provenance,
    validate_action_strategy,
    validate_action_strategy_contract,
    validate_action_workspace,
)
from packages.context import ContextType, UniversalContext
from packages.decision import DecisionType, UniversalDecision
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


def build_certified_inputs() -> ActionInputCollection:
    return ActionInputCollection(
        references=(
            ActionInputReference(
                input_type=ActionInputType.MEMORY,
                identifier="memory:00000000-0000-0000-0000-000000008701",
                reference_metadata={"z": "last", "a": "first"},
            ),
            ActionInputReference(
                input_type=ActionInputType.KNOWLEDGE,
                identifier="knowledge:00000000-0000-0000-0000-000000008702",
            ),
            ActionInputReference(
                input_type=ActionInputType.DECISION,
                identifier="decision:00000000-0000-0000-0000-000000008703",
            ),
        )
    )


def build_certified_provenance() -> ActionProvenance:
    inputs = build_certified_inputs()
    return ActionProvenance(
        origin=ActionOrigin.DECISION,
        source_identifier="decision:00000000-0000-0000-0000-000000008703",
        created_at=TIMESTAMP,
        input_references=inputs.references,
        provenance_metadata={"z": "last", "a": "first"},
    )


def build_certified_action(
    action_id: str = "00000000-0000-0000-0000-000000008601",
) -> UniversalAction:
    return UniversalAction(
        object_id=UUID(action_id),
        action_type=ActionType.TASK,
        action_state=ActionState.READY,
        action_outcome=ActionOutcome.UNKNOWN,
        action_confidence=ActionConfidence(level="high", rationale="certified"),
        action_metadata=ActionMetadata(values={"z": "last", "a": "first"}),
        action_inputs=build_certified_inputs(),
        action_provenance=build_certified_provenance(),
        metadata={"owner": "platform", "mission": "golf"},
        tags=["action", "certification"],
        lifecycle_state=LifecycleState.DRAFT,
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


class ActionPlatformIntegrationCertificationTest(unittest.TestCase):
    def test_scenario_1_universal_action_platform_certification(self) -> None:
        action = build_certified_action()
        payload = action.to_dict()
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        registry = ObjectRegistry()
        registry.register(UniversalAction)
        relationship = Relationship(
            source_object_id=action.object_id,
            target_object_id=UUID("00000000-0000-0000-0000-000000008801"),
            relationship_type=RelationshipType.REFERENCES,
        )

        self.assertIsInstance(action, CanonicalObject)
        self.assertIsInstance(action.validate(), ValidationResult)
        self.assertTrue(action.validate().is_valid)
        self.assertEqual(payload, build_certified_action().to_dict())
        self.assertEqual(encoded, json.dumps(payload, sort_keys=True, separators=(",", ":")))
        self.assertEqual(ObjectSerializer.serialize(action)["object_type"], "UniversalAction")
        self.assertEqual(registry.lookup("UniversalAction"), UniversalAction)
        action.transition_to(LifecycleState.ACTIVE)
        self.assertEqual(action.lifecycle_state, LifecycleState.ACTIVE)
        self.assertEqual(relationship.to_dict()["source_object_id"], str(action.object_id))
        self.assertEqual(relationship.to_dict()["relationship_type"], "references")

    def test_scenario_2_action_input_and_provenance_certification(self) -> None:
        inputs = build_certified_inputs()
        provenance = build_certified_provenance()

        self.assertTrue(validate_action_input_collection(inputs).is_valid)
        self.assertTrue(validate_action_provenance(provenance).is_valid)
        self.assertEqual(
            inputs.to_dict()["references"][0],
            {
                "input_type": "memory",
                "identifier": "memory:00000000-0000-0000-0000-000000008701",
                "reference_metadata": {"a": "first", "z": "last"},
            },
        )
        self.assertEqual(
            provenance.to_dict()["provenance_metadata"],
            {"a": "first", "z": "last"},
        )
        self.assert_no_behavior(inputs, {"resolve", "retrieve", "search"})
        self.assert_no_behavior(provenance, {"evaluate", "resolve", "verify"})

    def test_scenario_3_action_strategy_contract_certification(self) -> None:
        strategy = ActionStrategy(
            strategy_type=ActionStrategyType.MANUAL,
            name="operator-review",
            description="Descriptive strategy only.",
            metadata=ActionStrategyMetadata(values={"z": "last", "a": "first"}),
        )
        contract = ActionStrategyContract(
            strategies=(strategy,),
            metadata=ActionStrategyMetadata(values={"mission": "golf"}),
            contract_version="1.0",
        )

        self.assertTrue(validate_action_strategy(strategy).is_valid)
        self.assertTrue(validate_action_strategy_contract(contract).is_valid)
        self.assertEqual(strategy.to_dict(), strategy.to_dict())
        self.assertEqual(contract.to_dict(), contract.to_dict())
        self.assertEqual(strategy.to_dict()["metadata"], {"a": "first", "z": "last"})
        self.assert_no_behavior(strategy, {"execute", "optimize", "rank"})
        self.assert_no_behavior(contract, {"engine", "execute", "orchestrate"})

    def test_scenario_4_action_chain_contract_certification(self) -> None:
        step = ActionStepReference(
            action_identifier="action:00000000-0000-0000-0000-000000008901",
            metadata=ActionChainMetadata(values={"z": "last", "a": "first"}),
        )
        chain = ActionChain(
            chain_type=ActionChainType.SEQUENTIAL,
            steps=(step,),
            metadata=ActionChainMetadata(values={"mission": "golf"}),
        )
        contract = ActionChainContract(
            chains=(chain,),
            metadata=ActionChainMetadata(values={"mission": "golf"}),
            contract_version="1.0",
        )

        self.assertTrue(validate_action_chain(chain).is_valid)
        self.assertTrue(validate_action_chain_contract(contract).is_valid)
        self.assertEqual(chain.to_dict(), chain.to_dict())
        self.assertEqual(contract.to_dict(), contract.to_dict())
        self.assertEqual(
            chain.to_dict()["steps"][0]["action_identifier"],
            "action:00000000-0000-0000-0000-000000008901",
        )
        self.assert_no_behavior(chain, {"execute", "orchestrate", "resolve", "search"})
        self.assert_no_behavior(contract, {"engine", "execute", "orchestrate"})

    def test_scenario_5_action_workspace_certification(self) -> None:
        workspace = ActionWorkspace()
        action = build_certified_action()

        self.assertIsInstance(workspace.statistics(), WorkspaceStatistics)
        workspace.add(action)
        with self.assertRaises(ValueError):
            workspace.add(action)

        self.assertIs(workspace.get(action.object_id), action)
        self.assertIs(workspace.get(str(action.object_id)), action)
        self.assertEqual(workspace.identifiers(), (action.object_id,))
        self.assertEqual(workspace.statistics().total_actions, 1)
        self.assertEqual(workspace.statistics().active_actions, 0)
        self.assertEqual(workspace.statistics().archived_actions, 0)
        self.assertIs(workspace.remove(str(action.object_id)), action)
        self.assertIsNone(workspace.get(action.object_id))
        workspace.add(action)
        workspace.clear()
        self.assertEqual(workspace.identifiers(), ())
        self.assertEqual(workspace.statistics().total_actions, 0)
        self.assertTrue(validate_action_workspace(workspace).is_valid)
        self.assertFalse(hasattr(workspace, "to_dict"))
        self.assert_no_behavior(workspace, {"execute", "persist", "rank", "schedule", "search"})

    def test_scenario_6_end_to_end_action_foundation_certification(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000008711"),
            memory_type=MemoryType.SEMANTIC,
            content="Action certification coexists with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-golf"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000008712"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000008713"),
            context_type=ContextType.ANALYTICAL,
        )
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000008714"),
            reasoning_type=ReasoningType.DEDUCTIVE,
        )
        decision = UniversalDecision(
            object_id=UUID("00000000-0000-0000-0000-000000008715"),
            decision_type=DecisionType.RECOMMENDATION,
        )
        action = build_certified_action()
        strategy = ActionStrategy(
            strategy_type=ActionStrategyType.MANUAL,
            name="operator-review",
        )
        strategy_contract = ActionStrategyContract(strategies=(strategy,))
        chain = ActionChain(
            chain_type=ActionChainType.SEQUENTIAL,
            steps=(ActionStepReference(str(action.object_id)),),
        )
        chain_contract = ActionChainContract(chains=(chain,))
        workspace = ActionWorkspace()

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertTrue(reasoning.validate().is_valid)
        self.assertTrue(decision.validate().is_valid)
        self.assertTrue(action.validate().is_valid)
        self.assertEqual(ObjectSerializer.serialize(action)["object_id"], str(action.object_id))
        self.assertTrue(validate_action_input_collection(action.action_inputs).is_valid)
        self.assertTrue(validate_action_provenance(action.action_provenance).is_valid)
        self.assertTrue(validate_action_strategy_contract(strategy_contract).is_valid)
        self.assertTrue(validate_action_chain_contract(chain_contract).is_valid)

        workspace.add(action)
        self.assertIs(workspace.get(action.object_id), action)
        self.assertIs(workspace.remove(action.object_id), action)
        self.assertTrue(workspace.validate().is_valid)
        self.assertEqual(workspace.identifiers(), ())
        self.assertEqual(workspace.statistics().total_actions, 0)

    def test_explicit_action_foundation_boundary_certification(self) -> None:
        action = build_certified_action()
        inputs = build_certified_inputs()
        provenance = build_certified_provenance()
        strategy = ActionStrategy(
            strategy_type=ActionStrategyType.MANUAL,
            name="operator-review",
        )
        strategy_contract = ActionStrategyContract(strategies=(strategy,))
        chain = ActionChain(chain_type=ActionChainType.SEQUENTIAL)
        chain_contract = ActionChainContract(chains=(chain,))
        workspace = ActionWorkspace()

        self.assert_no_behavior(action, {"execute", "optimize", "schedule", "resolve"})
        self.assert_no_behavior(inputs, {"resolve", "retrieve", "search"})
        self.assert_no_behavior(provenance, {"evaluate", "verify", "resolve"})
        self.assert_no_behavior(strategy, {"execute", "optimize", "rank"})
        self.assert_no_behavior(strategy_contract, {"engine", "execute", "orchestrate"})
        self.assert_no_behavior(chain, {"execute", "orchestrate", "resolve"})
        self.assert_no_behavior(chain_contract, {"engine", "execute", "orchestrate"})
        self.assert_no_behavior(
            workspace,
            {"execute", "persist", "rank", "schedule", "search", "workflow"},
        )

    def test_cross_foundation_certification_does_not_modify_other_foundations(self) -> None:
        memory = UniversalMemory(
            memory_type=MemoryType.SEMANTIC,
            content="Cross-foundation certification.",
            source=MemorySource(source_type="test", source_identifier="mission-golf"),
        )
        knowledge = UniversalKnowledge(knowledge_type=KnowledgeType.FACT)
        context = UniversalContext(context_type=ContextType.ANALYTICAL)
        reasoning = UniversalReasoning(reasoning_type=ReasoningType.DEDUCTIVE)
        decision = UniversalDecision(decision_type=DecisionType.RECOMMENDATION)
        action = build_certified_action()

        before = (
            memory.to_dict(),
            knowledge.to_dict(),
            context.to_dict(),
            reasoning.to_dict(),
            decision.to_dict(),
        )
        action.validate()
        ActionWorkspace().add(action)
        after = (
            memory.to_dict(),
            knowledge.to_dict(),
            context.to_dict(),
            reasoning.to_dict(),
            decision.to_dict(),
        )

        self.assertEqual(before, after)

    def assert_no_behavior(self, obj: object, forbidden_names: set[str]) -> None:
        self.assertTrue(forbidden_names.isdisjoint(set(dir(obj))))


if __name__ == "__main__":
    unittest.main()
