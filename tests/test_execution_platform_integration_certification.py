import json
import unittest
from datetime import datetime
from uuid import UUID

from packages.action import ActionType, UniversalAction
from packages.context import ContextType, UniversalContext
from packages.decision import DecisionType, UniversalDecision
from packages.execution import (
    ExecutionChain,
    ExecutionChainContract,
    ExecutionChainMetadata,
    ExecutionChainType,
    ExecutionConfidence,
    ExecutionInputCollection,
    ExecutionInputReference,
    ExecutionInputType,
    ExecutionMetadata,
    ExecutionOrigin,
    ExecutionOutcome,
    ExecutionProvenance,
    ExecutionState,
    ExecutionStepReference,
    ExecutionStrategy,
    ExecutionStrategyContract,
    ExecutionStrategyMetadata,
    ExecutionStrategyType,
    ExecutionType,
    ExecutionWorkspace,
    UniversalExecution,
    WorkspaceStatistics,
    validate_execution_chain,
    validate_execution_chain_contract,
    validate_execution_input_collection,
    validate_execution_provenance,
    validate_execution_strategy,
    validate_execution_strategy_contract,
    validate_execution_workspace,
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


TIMESTAMP = datetime.fromisoformat("2026-07-06T00:00:00+00:00")


def build_certified_inputs() -> ExecutionInputCollection:
    return ExecutionInputCollection(
        references=(
            ExecutionInputReference(
                input_type=ExecutionInputType.MEMORY,
                identifier="memory:00000000-0000-0000-0000-000000009701",
                reference_metadata={"z": "last", "a": "first"},
            ),
            ExecutionInputReference(
                input_type=ExecutionInputType.KNOWLEDGE,
                identifier="knowledge:00000000-0000-0000-0000-000000009702",
            ),
            ExecutionInputReference(
                input_type=ExecutionInputType.ACTION,
                identifier="action:00000000-0000-0000-0000-000000009703",
            ),
        )
    )


def build_certified_provenance() -> ExecutionProvenance:
    inputs = build_certified_inputs()
    return ExecutionProvenance(
        origin=ExecutionOrigin.ACTION,
        source_identifier="action:00000000-0000-0000-0000-000000009703",
        created_at=TIMESTAMP,
        input_references=inputs.references,
        provenance_metadata={"z": "last", "a": "first"},
    )


def build_certified_execution(
    execution_id: str = "00000000-0000-0000-0000-000000009601",
) -> UniversalExecution:
    return UniversalExecution(
        object_id=UUID(execution_id),
        execution_type=ExecutionType.ACTION,
        execution_state=ExecutionState.READY,
        execution_outcome=ExecutionOutcome.UNKNOWN,
        execution_confidence=ExecutionConfidence(level="high", rationale="certified"),
        execution_metadata=ExecutionMetadata(values={"z": "last", "a": "first"}),
        execution_inputs=build_certified_inputs(),
        execution_provenance=build_certified_provenance(),
        metadata={"owner": "platform", "mission": "golf"},
        tags=["execution", "certification"],
        lifecycle_state=LifecycleState.DRAFT,
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


class ExecutionPlatformIntegrationCertificationTest(unittest.TestCase):
    def test_scenario_1_universal_execution_platform_certification(self) -> None:
        execution = build_certified_execution()
        payload = execution.to_dict()
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        registry = ObjectRegistry()
        registry.register(UniversalExecution)
        relationship = Relationship(
            source_object_id=execution.object_id,
            target_object_id=UUID("00000000-0000-0000-0000-000000009801"),
            relationship_type=RelationshipType.REFERENCES,
        )

        self.assertIsInstance(execution, CanonicalObject)
        self.assertIsInstance(execution.validate(), ValidationResult)
        self.assertTrue(execution.validate().is_valid)
        self.assertEqual(payload, build_certified_execution().to_dict())
        self.assertEqual(encoded, json.dumps(payload, sort_keys=True, separators=(",", ":")))
        self.assertEqual(
            ObjectSerializer.serialize(execution)["object_type"],
            "UniversalExecution",
        )
        self.assertEqual(registry.lookup("UniversalExecution"), UniversalExecution)
        execution.transition_to(LifecycleState.ACTIVE)
        self.assertEqual(execution.lifecycle_state, LifecycleState.ACTIVE)
        self.assertEqual(relationship.to_dict()["source_object_id"], str(execution.object_id))
        self.assertEqual(relationship.to_dict()["relationship_type"], "references")

    def test_scenario_2_execution_input_and_provenance_certification(self) -> None:
        inputs = build_certified_inputs()
        provenance = build_certified_provenance()

        self.assertTrue(validate_execution_input_collection(inputs).is_valid)
        self.assertTrue(validate_execution_provenance(provenance).is_valid)
        self.assertEqual(
            inputs.to_dict()["references"][0],
            {
                "input_type": "memory",
                "identifier": "memory:00000000-0000-0000-0000-000000009701",
                "reference_metadata": {"a": "first", "z": "last"},
            },
        )
        self.assertEqual(
            provenance.to_dict()["provenance_metadata"],
            {"a": "first", "z": "last"},
        )
        self.assert_no_behavior(inputs, {"resolve", "retrieve", "search"})
        self.assert_no_behavior(provenance, {"evaluate", "resolve", "verify"})

    def test_scenario_3_execution_strategy_contract_certification(self) -> None:
        strategy = ExecutionStrategy(
            strategy_type=ExecutionStrategyType.MANUAL,
            name="operator-review",
            description="Descriptive strategy only.",
            metadata=ExecutionStrategyMetadata(values={"z": "last", "a": "first"}),
        )
        contract = ExecutionStrategyContract(
            strategies=(strategy,),
            metadata=ExecutionStrategyMetadata(values={"mission": "golf"}),
            contract_version="1.0",
        )

        self.assertTrue(validate_execution_strategy(strategy).is_valid)
        self.assertTrue(validate_execution_strategy_contract(contract).is_valid)
        self.assertEqual(strategy.to_dict(), strategy.to_dict())
        self.assertEqual(contract.to_dict(), contract.to_dict())
        self.assertEqual(strategy.to_dict()["metadata"], {"a": "first", "z": "last"})
        self.assert_no_behavior(strategy, {"execute", "optimize", "rank"})
        self.assert_no_behavior(contract, {"engine", "execute", "orchestrate"})

    def test_scenario_4_execution_chain_contract_certification(self) -> None:
        step = ExecutionStepReference(
            execution_identifier="execution:00000000-0000-0000-0000-000000009901",
            metadata=ExecutionChainMetadata(values={"z": "last", "a": "first"}),
        )
        chain = ExecutionChain(
            chain_type=ExecutionChainType.SEQUENTIAL,
            steps=(step,),
            metadata=ExecutionChainMetadata(values={"mission": "golf"}),
        )
        contract = ExecutionChainContract(
            chains=(chain,),
            metadata=ExecutionChainMetadata(values={"mission": "golf"}),
            contract_version="1.0",
        )

        self.assertTrue(validate_execution_chain(chain).is_valid)
        self.assertTrue(validate_execution_chain_contract(contract).is_valid)
        self.assertEqual(chain.to_dict(), chain.to_dict())
        self.assertEqual(contract.to_dict(), contract.to_dict())
        self.assertEqual(
            chain.to_dict()["steps"][0]["execution_identifier"],
            "execution:00000000-0000-0000-0000-000000009901",
        )
        self.assert_no_behavior(chain, {"execute", "orchestrate", "resolve", "search"})
        self.assert_no_behavior(contract, {"engine", "execute", "orchestrate"})

    def test_scenario_5_execution_workspace_certification(self) -> None:
        workspace = ExecutionWorkspace()
        execution = build_certified_execution()

        self.assertIsInstance(workspace.statistics(), WorkspaceStatistics)
        workspace.add(execution)
        with self.assertRaises(ValueError):
            workspace.add(execution)

        self.assertIs(workspace.get(execution.object_id), execution)
        self.assertIs(workspace.get(str(execution.object_id)), execution)
        self.assertEqual(workspace.identifiers(), (execution.object_id,))
        self.assertEqual(workspace.statistics().total_executions, 1)
        self.assertEqual(workspace.statistics().active_executions, 0)
        self.assertEqual(workspace.statistics().archived_executions, 0)
        self.assertIs(workspace.remove(str(execution.object_id)), execution)
        self.assertIsNone(workspace.get(execution.object_id))
        workspace.add(execution)
        workspace.clear()
        self.assertEqual(workspace.identifiers(), ())
        self.assertEqual(workspace.statistics().total_executions, 0)
        self.assertTrue(validate_execution_workspace(workspace).is_valid)
        self.assertFalse(hasattr(workspace, "to_dict"))
        self.assert_no_behavior(workspace, {"execute", "persist", "rank", "schedule", "search"})

    def test_scenario_6_end_to_end_execution_foundation_certification(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000009711"),
            memory_type=MemoryType.SEMANTIC,
            content="Execution certification coexists with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-golf"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000009712"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000009713"),
            context_type=ContextType.ANALYTICAL,
        )
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000009714"),
            reasoning_type=ReasoningType.DEDUCTIVE,
        )
        decision = UniversalDecision(
            object_id=UUID("00000000-0000-0000-0000-000000009715"),
            decision_type=DecisionType.RECOMMENDATION,
        )
        action = UniversalAction(
            object_id=UUID("00000000-0000-0000-0000-000000009716"),
            action_type=ActionType.TASK,
        )
        execution = build_certified_execution()
        strategy = ExecutionStrategy(
            strategy_type=ExecutionStrategyType.MANUAL,
            name="operator-review",
        )
        strategy_contract = ExecutionStrategyContract(strategies=(strategy,))
        chain = ExecutionChain(
            chain_type=ExecutionChainType.SEQUENTIAL,
            steps=(ExecutionStepReference(str(execution.object_id)),),
        )
        chain_contract = ExecutionChainContract(chains=(chain,))
        workspace = ExecutionWorkspace()

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertTrue(reasoning.validate().is_valid)
        self.assertTrue(decision.validate().is_valid)
        self.assertTrue(action.validate().is_valid)
        self.assertTrue(execution.validate().is_valid)
        self.assertEqual(
            ObjectSerializer.serialize(execution)["object_id"],
            str(execution.object_id),
        )
        self.assertTrue(validate_execution_input_collection(execution.execution_inputs).is_valid)
        self.assertTrue(validate_execution_provenance(execution.execution_provenance).is_valid)
        self.assertTrue(validate_execution_strategy_contract(strategy_contract).is_valid)
        self.assertTrue(validate_execution_chain_contract(chain_contract).is_valid)

        workspace.add(execution)
        self.assertIs(workspace.get(execution.object_id), execution)
        self.assertIs(workspace.remove(execution.object_id), execution)
        self.assertTrue(workspace.validate().is_valid)
        self.assertEqual(workspace.identifiers(), ())
        self.assertEqual(workspace.statistics().total_executions, 0)

    def test_explicit_execution_foundation_boundary_certification(self) -> None:
        execution = build_certified_execution()
        inputs = build_certified_inputs()
        provenance = build_certified_provenance()
        strategy = ExecutionStrategy(
            strategy_type=ExecutionStrategyType.MANUAL,
            name="operator-review",
        )
        strategy_contract = ExecutionStrategyContract(strategies=(strategy,))
        chain = ExecutionChain(chain_type=ExecutionChainType.SEQUENTIAL)
        chain_contract = ExecutionChainContract(chains=(chain,))
        workspace = ExecutionWorkspace()

        self.assert_no_behavior(execution, {"execute", "optimize", "schedule", "resolve"})
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
        action = UniversalAction(action_type=ActionType.TASK)
        execution = build_certified_execution()

        before = (
            memory.to_dict(),
            knowledge.to_dict(),
            context.to_dict(),
            reasoning.to_dict(),
            decision.to_dict(),
            action.to_dict(),
        )
        execution.validate()
        ExecutionWorkspace().add(execution)
        after = (
            memory.to_dict(),
            knowledge.to_dict(),
            context.to_dict(),
            reasoning.to_dict(),
            decision.to_dict(),
            action.to_dict(),
        )

        self.assertEqual(before, after)

    def assert_no_behavior(self, obj: object, forbidden_names: set[str]) -> None:
        self.assertTrue(forbidden_names.isdisjoint(set(dir(obj))))


if __name__ == "__main__":
    unittest.main()
