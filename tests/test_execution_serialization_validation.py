import unittest
from datetime import datetime
from uuid import UUID

from packages.action import ActionType, UniversalAction
from packages.context import ContextType, UniversalContext
from packages.decision import DecisionType, UniversalDecision
from packages.execution import (
    ExecutionConfidence,
    ExecutionInputCollection,
    ExecutionInputReference,
    ExecutionInputType,
    ExecutionMetadata,
    ExecutionOrigin,
    ExecutionOutcome,
    ExecutionProvenance,
    ExecutionState,
    ExecutionType,
    UniversalExecution,
    validate_execution,
    validate_execution_input_collection,
    validate_execution_input_reference,
    validate_execution_provenance,
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


class ExecutionSerializationValidationCertificationTest(unittest.TestCase):
    def build_reference(self) -> ExecutionInputReference:
        return ExecutionInputReference(
            input_type=ExecutionInputType.ACTION,
            identifier="action:00000000-0000-0000-0000-000000009201",
            reference_metadata={"z": "last", "a": "first"},
        )

    def build_inputs(self) -> ExecutionInputCollection:
        return ExecutionInputCollection(references=(self.build_reference(),))

    def build_provenance(self) -> ExecutionProvenance:
        return ExecutionProvenance(
            origin=ExecutionOrigin.ACTION,
            source_identifier="action:00000000-0000-0000-0000-000000009201",
            created_at=TIMESTAMP,
            input_references=(self.build_reference(),),
            provenance_metadata={"phase": "certification", "z": "last"},
        )

    def build_execution(self) -> UniversalExecution:
        return UniversalExecution(
            object_id=UUID("00000000-0000-0000-0000-000000009202"),
            execution_type=ExecutionType.ACTION,
            execution_state=ExecutionState.READY,
            execution_outcome=ExecutionOutcome.UNKNOWN,
            execution_confidence=ExecutionConfidence(level="high", rationale="certified"),
            execution_metadata=ExecutionMetadata(values={"z": "last", "a": "first"}),
            execution_inputs=self.build_inputs(),
            execution_provenance=self.build_provenance(),
            metadata={"owner": "execution"},
            tags=["execution", "charlie"],
            lifecycle_state=LifecycleState.DRAFT,
            created_by="codex",
            updated_by="codex",
            created_at=TIMESTAMP,
            updated_at=TIMESTAMP,
        )

    def test_execution_public_models_are_certified(self) -> None:
        execution = self.build_execution()

        self.assertIsInstance(execution, CanonicalObject)
        self.assertEqual(execution.object_type, "UniversalExecution")
        self.assertEqual(execution.execution_type, ExecutionType.ACTION)
        self.assertEqual(execution.execution_state, ExecutionState.READY)
        self.assertEqual(execution.execution_outcome, ExecutionOutcome.UNKNOWN)
        self.assertIsInstance(execution.execution_confidence, ExecutionConfidence)
        self.assertIsInstance(execution.execution_metadata, ExecutionMetadata)
        self.assertIsInstance(execution.execution_inputs, ExecutionInputCollection)
        self.assertIsInstance(execution.execution_provenance, ExecutionProvenance)

    def test_enum_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {execution_type.value for execution_type in ExecutionType},
            {"action", "workflow", "procedure", "command", "review", "observation"},
        )
        self.assertEqual(
            {state.value for state in ExecutionState},
            {"draft", "planned", "ready", "completed", "archived"},
        )
        self.assertEqual(
            {outcome.value for outcome in ExecutionOutcome},
            {"succeeded", "failed", "cancelled", "unknown"},
        )
        self.assertEqual(
            {input_type.value for input_type in ExecutionInputType},
            {"memory", "knowledge", "context", "reasoning", "decision", "action", "external"},
        )
        self.assertEqual(
            {origin.value for origin in ExecutionOrigin},
            {"human", "system", "imported", "external", "action", "unknown"},
        )

    def test_alpha_payload_ordering_is_preserved_without_bravo_fields(self) -> None:
        execution = UniversalExecution(
            object_id=UUID("00000000-0000-0000-0000-000000009203"),
            execution_type=ExecutionType.ACTION,
            created_at=TIMESTAMP,
            updated_at=TIMESTAMP,
        )
        payload = execution.to_dict()

        self.assertEqual(
            list(payload.keys()),
            [
                "schema_version",
                "object_version",
                "object_type",
                "object_id",
                "metadata",
                "tags",
                "lifecycle_state",
                "created_by",
                "updated_by",
                "created_at",
                "updated_at",
                "execution_type",
                "execution_state",
                "execution_outcome",
                "execution_confidence",
                "execution_metadata",
            ],
        )
        self.assertNotIn("execution_inputs", payload)
        self.assertNotIn("execution_provenance", payload)

    def test_bravo_payload_fields_append_after_alpha_fields(self) -> None:
        payload = self.build_execution().to_dict()

        self.assertEqual(payload, self.build_execution().to_dict())
        self.assertEqual(
            list(payload.keys())[-2:],
            ["execution_inputs", "execution_provenance"],
        )
        self.assertEqual(payload["execution_inputs"], self.build_inputs().to_dict())
        self.assertEqual(payload["execution_provenance"], self.build_provenance().to_dict())

    def test_nested_execution_payloads_are_deterministic(self) -> None:
        reference = self.build_reference()
        provenance = self.build_provenance()

        self.assertEqual(
            reference.to_dict(),
            {
                "input_type": "action",
                "identifier": "action:00000000-0000-0000-0000-000000009201",
                "reference_metadata": {"a": "first", "z": "last"},
            },
        )
        self.assertEqual(
            provenance.to_dict(),
            {
                "origin": "action",
                "source_identifier": "action:00000000-0000-0000-0000-000000009201",
                "created_at": TIMESTAMP.isoformat(),
                "input_references": [reference.to_dict()],
                "provenance_metadata": {"phase": "certification", "z": "last"},
            },
        )

    def test_validation_returns_platform_validation_result(self) -> None:
        result = self.build_execution().validate()

        self.assertIsInstance(result, ValidationResult)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_local_validation_helpers_return_platform_validation_result(self) -> None:
        self.assertIsInstance(validate_execution(self.build_execution()), ValidationResult)
        self.assertIsInstance(
            validate_execution_input_reference(self.build_reference()),
            ValidationResult,
        )
        self.assertIsInstance(
            validate_execution_input_collection(self.build_inputs()),
            ValidationResult,
        )
        self.assertIsInstance(
            validate_execution_provenance(self.build_provenance()),
            ValidationResult,
        )

    def test_validation_failures_are_deterministic(self) -> None:
        execution = self.build_execution()
        execution._execution_type = "action"
        execution._execution_state = "ready"
        execution._execution_outcome = "unknown"
        execution._execution_confidence = "high"
        execution._execution_metadata = {"bad": "mutable"}
        execution._execution_inputs = "inputs"
        execution._execution_provenance = "provenance"

        result = execution.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "execution_type",
                "execution_state",
                "execution_outcome",
                "execution_confidence",
                "execution_metadata",
                "execution_inputs",
                "execution_provenance",
            },
        )

    def test_reference_and_provenance_validation_failures_are_certified(self) -> None:
        reference = self.build_reference()
        object.__setattr__(reference, "input_type", "action")
        object.__setattr__(reference, "identifier", "")
        object.__setattr__(reference, "reference_metadata", {"bad": "mutable"})
        provenance = self.build_provenance()
        object.__setattr__(provenance, "origin", "action")
        object.__setattr__(provenance, "source_identifier", object())
        object.__setattr__(provenance, "created_at", "not-a-datetime")
        object.__setattr__(provenance, "input_references", (reference,))
        object.__setattr__(provenance, "provenance_metadata", {"bad": "mutable"})

        reference_result = validate_execution_input_reference(reference)
        provenance_result = validate_execution_provenance(provenance)

        self.assertFalse(reference_result.is_valid)
        self.assertFalse(provenance_result.is_valid)
        self.assertEqual(
            {error.field for error in reference_result.errors},
            {
                "execution_input_reference.input_type",
                "execution_input_reference.identifier",
                "execution_input_reference.reference_metadata",
            },
        )
        self.assertIn(
            "execution_provenance.origin",
            {error.field for error in provenance_result.errors},
        )
        self.assertIn(
            "execution_provenance.source_identifier",
            {error.field for error in provenance_result.errors},
        )

    def test_object_serializer_remains_platform_core_contract(self) -> None:
        execution = self.build_execution()

        payload = ObjectSerializer.serialize(execution)

        self.assertEqual(payload["object_type"], "UniversalExecution")
        self.assertEqual(payload["metadata"], {"owner": "execution"})
        self.assertEqual(payload["tags"], ["execution", "charlie"])
        self.assertNotIn("execution_type", payload)
        self.assertNotIn("execution_inputs", payload)
        self.assertNotIn("execution_provenance", payload)

    def test_object_serializer_json_is_deterministic(self) -> None:
        execution = self.build_execution()

        self.assertEqual(
            ObjectSerializer.serialize_json(execution),
            ObjectSerializer.serialize_json(execution),
        )

    def test_object_registry_accepts_universal_execution(self) -> None:
        registry = ObjectRegistry()

        registry.register(UniversalExecution)

        self.assertEqual(registry.lookup("UniversalExecution"), UniversalExecution)
        self.assertEqual(registry.lookup_by_class(UniversalExecution), UniversalExecution)
        self.assertEqual(registry.enumerate(), (UniversalExecution,))
        registry.validate()

    def test_lifecycle_transitions_remain_platform_core_behavior(self) -> None:
        execution = self.build_execution()

        execution.transition_to(LifecycleState.ACTIVE)
        execution.transition_to(LifecycleState.ARCHIVED)

        self.assertEqual(execution.lifecycle_state, LifecycleState.ARCHIVED)
        with self.assertRaises(ValueError):
            execution.transition_to(LifecycleState.ACTIVE)

    def test_relationship_compatibility_uses_platform_relationship_model(self) -> None:
        execution = self.build_execution()
        target_id = UUID("00000000-0000-0000-0000-000000009204")
        relationship = Relationship(
            source_object_id=execution.object_id,
            target_object_id=target_id,
            relationship_type=RelationshipType.REFERENCES,
            metadata={"phase": "certification"},
        )

        payload = relationship.to_dict()

        self.assertEqual(payload["source_object_id"], str(execution.object_id))
        self.assertEqual(payload["target_object_id"], str(target_id))
        self.assertEqual(payload["relationship_type"], "references")
        self.assertEqual(payload["metadata"], {"phase": "certification"})
        self.assertEqual(execution.relationships, {})

    def test_existing_foundations_coexist_with_execution(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000009205"),
            memory_type=MemoryType.SEMANTIC,
            content="Execution certification coexists with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-charlie"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000009206"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000009207"),
            context_type=ContextType.ANALYTICAL,
        )
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000009208"),
            reasoning_type=ReasoningType.DEDUCTIVE,
        )
        decision = UniversalDecision(
            object_id=UUID("00000000-0000-0000-0000-000000009209"),
            decision_type=DecisionType.RECOMMENDATION,
        )
        action = UniversalAction(
            object_id=UUID("00000000-0000-0000-0000-000000009210"),
            action_type=ActionType.TASK,
        )
        execution = UniversalExecution(
            execution_type=ExecutionType.OBSERVATION,
            execution_inputs=ExecutionInputCollection(
                references=(
                    ExecutionInputReference(ExecutionInputType.MEMORY, str(memory.object_id)),
                    ExecutionInputReference(ExecutionInputType.KNOWLEDGE, str(knowledge.object_id)),
                    ExecutionInputReference(ExecutionInputType.CONTEXT, str(context.object_id)),
                    ExecutionInputReference(ExecutionInputType.REASONING, str(reasoning.object_id)),
                    ExecutionInputReference(ExecutionInputType.DECISION, str(decision.object_id)),
                    ExecutionInputReference(ExecutionInputType.ACTION, str(action.object_id)),
                )
            ),
        )

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertTrue(reasoning.validate().is_valid)
        self.assertTrue(decision.validate().is_valid)
        self.assertTrue(action.validate().is_valid)
        self.assertTrue(execution.validate().is_valid)

    def test_foundation_coexistence_does_not_mutate_existing_objects(self) -> None:
        memory = UniversalMemory(
            memory_type=MemoryType.SEMANTIC,
            content="Cross-foundation certification.",
            source=MemorySource(source_type="test", source_identifier="mission-charlie"),
        )
        knowledge = UniversalKnowledge(knowledge_type=KnowledgeType.FACT)
        context = UniversalContext(context_type=ContextType.ANALYTICAL)
        reasoning = UniversalReasoning(reasoning_type=ReasoningType.DEDUCTIVE)
        decision = UniversalDecision(decision_type=DecisionType.RECOMMENDATION)
        action = UniversalAction(action_type=ActionType.TASK)
        before = (
            memory.to_dict(),
            knowledge.to_dict(),
            context.to_dict(),
            reasoning.to_dict(),
            decision.to_dict(),
            action.to_dict(),
        )

        self.build_execution().validate()

        after = (
            memory.to_dict(),
            knowledge.to_dict(),
            context.to_dict(),
            reasoning.to_dict(),
            decision.to_dict(),
            action.to_dict(),
        )

        self.assertEqual(before, after)

    def test_no_future_execution_capabilities_are_exposed(self) -> None:
        execution = self.build_execution()
        reference = self.build_reference()
        inputs = self.build_inputs()
        provenance = self.build_provenance()
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

        self.assertTrue(forbidden_names.isdisjoint(set(dir(execution))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(reference))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(inputs))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(provenance))))


if __name__ == "__main__":
    unittest.main()
