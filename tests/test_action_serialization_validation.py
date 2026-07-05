import unittest
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
    validate_action,
    validate_action_input_collection,
    validate_action_input_reference,
    validate_action_provenance,
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


class ActionSerializationValidationCertificationTest(unittest.TestCase):
    def build_reference(self) -> ActionInputReference:
        return ActionInputReference(
            input_type=ActionInputType.DECISION,
            identifier="decision:00000000-0000-0000-0000-000000008201",
            reference_metadata={"z": "last", "a": "first"},
        )

    def build_inputs(self) -> ActionInputCollection:
        return ActionInputCollection(references=(self.build_reference(),))

    def build_provenance(self) -> ActionProvenance:
        return ActionProvenance(
            origin=ActionOrigin.DECISION,
            source_identifier="decision:00000000-0000-0000-0000-000000008201",
            created_at=TIMESTAMP,
            input_references=(self.build_reference(),),
            provenance_metadata={"phase": "certification", "z": "last"},
        )

    def build_action(self) -> UniversalAction:
        return UniversalAction(
            object_id=UUID("00000000-0000-0000-0000-000000008202"),
            action_type=ActionType.APPROVAL,
            action_state=ActionState.READY,
            action_outcome=ActionOutcome.UNKNOWN,
            action_confidence=ActionConfidence(level="high", rationale="certified"),
            action_metadata=ActionMetadata(values={"z": "last", "a": "first"}),
            action_inputs=self.build_inputs(),
            action_provenance=self.build_provenance(),
            metadata={"owner": "action"},
            tags=["action", "charlie"],
            lifecycle_state=LifecycleState.DRAFT,
            created_by="codex",
            updated_by="codex",
            created_at=TIMESTAMP,
            updated_at=TIMESTAMP,
        )

    def test_action_public_models_are_certified(self) -> None:
        action = self.build_action()

        self.assertIsInstance(action, CanonicalObject)
        self.assertEqual(action.object_type, "UniversalAction")
        self.assertEqual(action.action_type, ActionType.APPROVAL)
        self.assertEqual(action.action_state, ActionState.READY)
        self.assertEqual(action.action_outcome, ActionOutcome.UNKNOWN)
        self.assertIsInstance(action.action_confidence, ActionConfidence)
        self.assertIsInstance(action.action_metadata, ActionMetadata)
        self.assertIsInstance(action.action_inputs, ActionInputCollection)
        self.assertIsInstance(action.action_provenance, ActionProvenance)

    def test_enum_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {action_type.value for action_type in ActionType},
            {"task", "review", "approval", "notification", "command", "observation"},
        )
        self.assertEqual(
            {state.value for state in ActionState},
            {"draft", "proposed", "ready", "completed", "archived"},
        )
        self.assertEqual(
            {outcome.value for outcome in ActionOutcome},
            {"succeeded", "failed", "deferred", "cancelled", "unknown"},
        )
        self.assertEqual(
            {input_type.value for input_type in ActionInputType},
            {"memory", "knowledge", "context", "reasoning", "decision", "external"},
        )
        self.assertEqual(
            {origin.value for origin in ActionOrigin},
            {"human", "system", "imported", "external", "decision", "unknown"},
        )

    def test_alpha_payload_ordering_is_preserved_without_bravo_fields(self) -> None:
        action = UniversalAction(
            object_id=UUID("00000000-0000-0000-0000-000000008203"),
            action_type=ActionType.TASK,
            created_at=TIMESTAMP,
            updated_at=TIMESTAMP,
        )
        payload = action.to_dict()

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
                "action_type",
                "action_state",
                "action_outcome",
                "action_confidence",
                "action_metadata",
            ],
        )
        self.assertNotIn("action_inputs", payload)
        self.assertNotIn("action_provenance", payload)

    def test_bravo_payload_fields_append_after_alpha_fields(self) -> None:
        payload = self.build_action().to_dict()

        self.assertEqual(payload, self.build_action().to_dict())
        self.assertEqual(
            list(payload.keys())[-2:],
            ["action_inputs", "action_provenance"],
        )
        self.assertEqual(payload["action_inputs"], self.build_inputs().to_dict())
        self.assertEqual(payload["action_provenance"], self.build_provenance().to_dict())

    def test_nested_action_payloads_are_deterministic(self) -> None:
        reference = self.build_reference()
        provenance = self.build_provenance()

        self.assertEqual(
            reference.to_dict(),
            {
                "input_type": "decision",
                "identifier": "decision:00000000-0000-0000-0000-000000008201",
                "reference_metadata": {"a": "first", "z": "last"},
            },
        )
        self.assertEqual(
            provenance.to_dict(),
            {
                "origin": "decision",
                "source_identifier": "decision:00000000-0000-0000-0000-000000008201",
                "created_at": TIMESTAMP.isoformat(),
                "input_references": [reference.to_dict()],
                "provenance_metadata": {"phase": "certification", "z": "last"},
            },
        )

    def test_validation_returns_platform_validation_result(self) -> None:
        result = self.build_action().validate()

        self.assertIsInstance(result, ValidationResult)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_local_validation_helpers_return_platform_validation_result(self) -> None:
        self.assertIsInstance(validate_action(self.build_action()), ValidationResult)
        self.assertIsInstance(
            validate_action_input_reference(self.build_reference()),
            ValidationResult,
        )
        self.assertIsInstance(
            validate_action_input_collection(self.build_inputs()),
            ValidationResult,
        )
        self.assertIsInstance(
            validate_action_provenance(self.build_provenance()),
            ValidationResult,
        )

    def test_validation_failures_are_deterministic(self) -> None:
        action = self.build_action()
        action._action_type = "approval"
        action._action_state = "ready"
        action._action_outcome = "unknown"
        action._action_confidence = "high"
        action._action_metadata = {"bad": "mutable"}
        action._action_inputs = "inputs"
        action._action_provenance = "provenance"

        result = action.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "action_type",
                "action_state",
                "action_outcome",
                "action_confidence",
                "action_metadata",
                "action_inputs",
                "action_provenance",
            },
        )

    def test_reference_and_provenance_validation_failures_are_certified(self) -> None:
        reference = self.build_reference()
        object.__setattr__(reference, "input_type", "decision")
        object.__setattr__(reference, "identifier", "")
        object.__setattr__(reference, "reference_metadata", {"bad": "mutable"})
        provenance = self.build_provenance()
        object.__setattr__(provenance, "origin", "decision")
        object.__setattr__(provenance, "source_identifier", object())
        object.__setattr__(provenance, "created_at", "not-a-datetime")
        object.__setattr__(provenance, "input_references", (reference,))
        object.__setattr__(provenance, "provenance_metadata", {"bad": "mutable"})

        reference_result = validate_action_input_reference(reference)
        provenance_result = validate_action_provenance(provenance)

        self.assertFalse(reference_result.is_valid)
        self.assertFalse(provenance_result.is_valid)
        self.assertEqual(
            {error.field for error in reference_result.errors},
            {
                "action_input_reference.input_type",
                "action_input_reference.identifier",
                "action_input_reference.reference_metadata",
            },
        )
        self.assertIn("action_provenance.origin", {error.field for error in provenance_result.errors})
        self.assertIn(
            "action_provenance.source_identifier",
            {error.field for error in provenance_result.errors},
        )

    def test_object_serializer_remains_platform_core_contract(self) -> None:
        action = self.build_action()

        payload = ObjectSerializer.serialize(action)

        self.assertEqual(payload["object_type"], "UniversalAction")
        self.assertEqual(payload["metadata"], {"owner": "action"})
        self.assertEqual(payload["tags"], ["action", "charlie"])
        self.assertNotIn("action_type", payload)
        self.assertNotIn("action_inputs", payload)
        self.assertNotIn("action_provenance", payload)

    def test_object_serializer_json_is_deterministic(self) -> None:
        action = self.build_action()

        self.assertEqual(
            ObjectSerializer.serialize_json(action),
            ObjectSerializer.serialize_json(action),
        )

    def test_object_registry_accepts_universal_action(self) -> None:
        registry = ObjectRegistry()

        registry.register(UniversalAction)

        self.assertEqual(registry.lookup("UniversalAction"), UniversalAction)
        self.assertEqual(registry.lookup_by_class(UniversalAction), UniversalAction)
        self.assertEqual(registry.enumerate(), (UniversalAction,))
        registry.validate()

    def test_lifecycle_transitions_remain_platform_core_behavior(self) -> None:
        action = self.build_action()

        action.transition_to(LifecycleState.ACTIVE)
        action.transition_to(LifecycleState.ARCHIVED)

        self.assertEqual(action.lifecycle_state, LifecycleState.ARCHIVED)
        with self.assertRaises(ValueError):
            action.transition_to(LifecycleState.ACTIVE)

    def test_relationship_compatibility_uses_platform_relationship_model(self) -> None:
        action = self.build_action()
        target_id = UUID("00000000-0000-0000-0000-000000008204")
        relationship = Relationship(
            source_object_id=action.object_id,
            target_object_id=target_id,
            relationship_type=RelationshipType.REFERENCES,
            metadata={"phase": "certification"},
        )

        payload = relationship.to_dict()

        self.assertEqual(payload["source_object_id"], str(action.object_id))
        self.assertEqual(payload["target_object_id"], str(target_id))
        self.assertEqual(payload["relationship_type"], "references")
        self.assertEqual(payload["metadata"], {"phase": "certification"})
        self.assertEqual(action.relationships, {})

    def test_existing_foundations_coexist_with_action(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000008205"),
            memory_type=MemoryType.SEMANTIC,
            content="Action certification coexists with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-charlie"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000008206"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000008207"),
            context_type=ContextType.ANALYTICAL,
        )
        reasoning = UniversalReasoning(
            object_id=UUID("00000000-0000-0000-0000-000000008208"),
            reasoning_type=ReasoningType.DEDUCTIVE,
        )
        decision = UniversalDecision(
            object_id=UUID("00000000-0000-0000-0000-000000008209"),
            decision_type=DecisionType.RECOMMENDATION,
        )
        action = UniversalAction(
            action_type=ActionType.OBSERVATION,
            action_inputs=ActionInputCollection(
                references=(
                    ActionInputReference(ActionInputType.MEMORY, str(memory.object_id)),
                    ActionInputReference(ActionInputType.KNOWLEDGE, str(knowledge.object_id)),
                    ActionInputReference(ActionInputType.CONTEXT, str(context.object_id)),
                    ActionInputReference(ActionInputType.REASONING, str(reasoning.object_id)),
                    ActionInputReference(ActionInputType.DECISION, str(decision.object_id)),
                )
            ),
        )

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertTrue(reasoning.validate().is_valid)
        self.assertTrue(decision.validate().is_valid)
        self.assertTrue(action.validate().is_valid)

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
        before = (
            memory.to_dict(),
            knowledge.to_dict(),
            context.to_dict(),
            reasoning.to_dict(),
            decision.to_dict(),
        )

        self.build_action().validate()

        after = (
            memory.to_dict(),
            knowledge.to_dict(),
            context.to_dict(),
            reasoning.to_dict(),
            decision.to_dict(),
        )

        self.assertEqual(before, after)

    def test_no_future_action_capabilities_are_exposed(self) -> None:
        action = self.build_action()
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

        self.assertTrue(forbidden_names.isdisjoint(set(dir(action))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(reference))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(inputs))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(provenance))))


if __name__ == "__main__":
    unittest.main()
