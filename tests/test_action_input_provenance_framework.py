import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime
from uuid import UUID

from packages.action import (
    ActionConfidence,
    ActionInputCollection,
    ActionInputReference,
    ActionInputType,
    ActionMetadata,
    ActionOrigin,
    ActionOutcome,
    ActionProvenance,
    ActionState,
    ActionType,
    UniversalAction,
    validate_action_input_collection,
    validate_action_input_reference,
    validate_action_provenance,
)
from packages.context import ContextType, UniversalContext
from packages.decision import DecisionType, UniversalDecision
from packages.knowledge import KnowledgeType, UniversalKnowledge
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import ObjectSerializer, ValidationResult
from packages.reasoning import ReasoningType, UniversalReasoning


TIMESTAMP = datetime.fromisoformat("2026-07-05T00:00:00+00:00")


class ActionInputProvenanceFrameworkTest(unittest.TestCase):
    def build_reference(self) -> ActionInputReference:
        return ActionInputReference(
            input_type=ActionInputType.DECISION,
            identifier="decision:00000000-0000-0000-0000-000000008101",
            reference_metadata={"z": "last", "a": "first"},
        )

    def build_inputs(self) -> ActionInputCollection:
        return ActionInputCollection(references=(self.build_reference(),))

    def build_provenance(self) -> ActionProvenance:
        return ActionProvenance(
            origin=ActionOrigin.DECISION,
            source_identifier="decision:00000000-0000-0000-0000-000000008101",
            created_at=TIMESTAMP,
            input_references=(self.build_reference(),),
            provenance_metadata={"z": "last", "a": "first"},
        )

    def test_action_input_type_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {input_type.value for input_type in ActionInputType},
            {"memory", "knowledge", "context", "reasoning", "decision", "external"},
        )

    def test_action_input_reference_is_immutable_and_deterministic(self) -> None:
        reference = self.build_reference()

        self.assertEqual(
            reference.to_dict(),
            {
                "input_type": "decision",
                "identifier": "decision:00000000-0000-0000-0000-000000008101",
                "reference_metadata": {"a": "first", "z": "last"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            reference.identifier = "changed"

    def test_action_input_collection_is_immutable_and_deterministic(self) -> None:
        inputs = self.build_inputs()

        self.assertEqual(inputs.to_dict(), {"references": [self.build_reference().to_dict()]})
        with self.assertRaises(FrozenInstanceError):
            inputs.references = ()

    def test_action_origin_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {origin.value for origin in ActionOrigin},
            {"human", "system", "imported", "external", "decision", "unknown"},
        )

    def test_action_provenance_is_immutable_and_deterministic(self) -> None:
        provenance = self.build_provenance()

        self.assertEqual(
            provenance.to_dict(),
            {
                "origin": "decision",
                "source_identifier": "decision:00000000-0000-0000-0000-000000008101",
                "created_at": TIMESTAMP.isoformat(),
                "input_references": [self.build_reference().to_dict()],
                "provenance_metadata": {"a": "first", "z": "last"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            provenance.source_identifier = "changed"

    def test_validation_helpers_return_platform_validation_results(self) -> None:
        self.assertIsInstance(
            validate_action_input_reference(self.build_reference()),
            ValidationResult,
        )
        self.assertTrue(validate_action_input_reference(self.build_reference()).is_valid)
        self.assertTrue(validate_action_input_collection(self.build_inputs()).is_valid)
        self.assertTrue(validate_action_provenance(self.build_provenance()).is_valid)

    def test_validation_reports_invalid_input_reference_shape(self) -> None:
        reference = self.build_reference()
        object.__setattr__(reference, "input_type", "decision")
        object.__setattr__(reference, "identifier", "")
        object.__setattr__(reference, "reference_metadata", {"bad": "mutable"})

        result = validate_action_input_reference(reference)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "action_input_reference.input_type",
                "action_input_reference.identifier",
                "action_input_reference.reference_metadata",
            },
        )

    def test_validation_reports_invalid_input_collection_shape(self) -> None:
        inputs = self.build_inputs()
        object.__setattr__(inputs, "references", ("not-a-reference",))

        result = validate_action_input_collection(inputs)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "action_inputs.references[0]")

    def test_validation_reports_invalid_provenance_shape(self) -> None:
        provenance = self.build_provenance()
        object.__setattr__(provenance, "origin", "decision")
        object.__setattr__(provenance, "source_identifier", object())
        object.__setattr__(provenance, "created_at", "not-a-datetime")
        object.__setattr__(provenance, "input_references", ("not-a-reference",))
        object.__setattr__(provenance, "provenance_metadata", {"bad": "mutable"})

        result = validate_action_provenance(provenance)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "action_provenance.origin",
                "action_provenance.source_identifier",
                "action_provenance.created_at",
                "action_provenance.input_references[0]",
                "action_provenance.provenance_metadata",
            },
        )

    def test_universal_action_integrates_inputs_and_provenance(self) -> None:
        action = UniversalAction(
            object_id=UUID("00000000-0000-0000-0000-000000008102"),
            action_type=ActionType.APPROVAL,
            action_state=ActionState.READY,
            action_outcome=ActionOutcome.UNKNOWN,
            action_confidence=ActionConfidence(level="high"),
            action_metadata=ActionMetadata(values={"mission": "bravo"}),
            action_inputs=self.build_inputs(),
            action_provenance=self.build_provenance(),
            created_at=TIMESTAMP,
            updated_at=TIMESTAMP,
        )
        payload = action.to_dict()

        self.assertTrue(action.validate().is_valid)
        self.assertEqual(payload["action_inputs"], self.build_inputs().to_dict())
        self.assertEqual(payload["action_provenance"], self.build_provenance().to_dict())
        self.assertEqual(
            list(payload.keys())[-2:],
            ["action_inputs", "action_provenance"],
        )

    def test_mission_alpha_constructor_and_payload_compatibility_is_preserved(self) -> None:
        action = UniversalAction(action_type=ActionType.TASK)
        payload = action.to_dict()

        self.assertTrue(action.validate().is_valid)
        self.assertIsNone(action.action_inputs)
        self.assertIsNone(action.action_provenance)
        self.assertNotIn("action_inputs", payload)
        self.assertNotIn("action_provenance", payload)

    def test_platform_core_serialization_compatibility_is_preserved(self) -> None:
        action = UniversalAction(
            object_id=UUID("00000000-0000-0000-0000-000000008103"),
            action_type=ActionType.REVIEW,
            action_inputs=self.build_inputs(),
            action_provenance=self.build_provenance(),
        )

        payload = ObjectSerializer.serialize(action)

        self.assertEqual(payload["object_type"], "UniversalAction")
        self.assertEqual(payload["object_id"], "00000000-0000-0000-0000-000000008103")
        self.assertNotIn("action_inputs", payload)
        self.assertNotIn("action_provenance", payload)

    def test_existing_foundation_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000008104"),
            memory_type=MemoryType.SEMANTIC,
            content="Action input references remain opaque.",
            source=MemorySource(source_type="test", source_identifier="mission-bravo"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000008105"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000008106"),
            context_type=ContextType.ANALYTICAL,
        )
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000008107"),
            reasoning_type=ReasoningType.DEDUCTIVE,
        )
        decision = UniversalDecision(
            object_id=UUID("00000000-0000-0000-0000-000000008108"),
            decision_type=DecisionType.RECOMMENDATION,
        )
        inputs = ActionInputCollection(
            references=(
                ActionInputReference(ActionInputType.MEMORY, str(memory.object_id)),
                ActionInputReference(ActionInputType.KNOWLEDGE, str(knowledge.object_id)),
                ActionInputReference(ActionInputType.CONTEXT, str(context.object_id)),
                ActionInputReference(ActionInputType.REASONING, str(reasoning.object_id)),
                ActionInputReference(ActionInputType.DECISION, str(decision.object_id)),
            )
        )
        action = UniversalAction(
            action_type=ActionType.OBSERVATION,
            action_inputs=inputs,
        )

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertTrue(reasoning.validate().is_valid)
        self.assertTrue(decision.validate().is_valid)
        self.assertTrue(action.validate().is_valid)

    def test_no_execution_resolution_or_future_behavior_is_exposed(self) -> None:
        reference = self.build_reference()
        inputs = self.build_inputs()
        provenance = self.build_provenance()
        action = UniversalAction(
            action_type=ActionType.TASK,
            action_inputs=inputs,
            action_provenance=provenance,
        )
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

        self.assertTrue(forbidden_names.isdisjoint(set(dir(reference))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(inputs))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(provenance))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(action))))


if __name__ == "__main__":
    unittest.main()
