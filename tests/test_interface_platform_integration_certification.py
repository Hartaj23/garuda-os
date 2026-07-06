import json
import unittest
from datetime import datetime
from pathlib import Path
from uuid import UUID

from packages.action import ActionType, UniversalAction
from packages.context import ContextType, UniversalContext
from packages.decision import DecisionType, UniversalDecision
from packages.execution import ExecutionType, UniversalExecution
from packages.interface import (
    CanonicalInterfacePayload,
    CanonicalInterfaceRequest,
    CanonicalInterfaceResponse,
    CanonicalTranslationContract,
    ExternalRepresentation,
    ExternalRepresentationKind,
    InterfaceAdapterDescriptor,
    InterfaceArtifactLifecycle,
    InterfaceBoundaryExclusivity,
    InterfaceBoundaryModel,
    InterfaceBoundarySide,
    InterfaceCapabilityDeclaration,
    InterfaceContextReferenceCollection,
    InterfaceContractMetadata,
    InterfaceCorrelation,
    InterfaceFoundation,
    InterfaceLifecycleMetadata,
    InterfaceLifecycleState,
    InterfaceOrigin,
    InterfaceRegistrationContract,
    InterfaceRegistry,
    InterfaceRegistryEntry,
    InterfaceRegistryLookupCriteria,
    InterfaceRegistryMetadata,
    InterfaceResponseResult,
    InterfaceResponseStatus,
    InterfaceValidationPolicy,
    InterfaceValidationRecord,
    InterfaceValidationTarget,
    InterfaceVersionCompatibilityRule,
    TranslationDescriptor,
    TranslationDirection,
    TranslationMetadata,
    TranslationReversibilityDescriptor,
    evaluate_interface_artifact,
    normalize_to_canonical_payload,
    validate_interface_boundary_exclusivity,
)
from packages.knowledge import KnowledgeType, UniversalKnowledge
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import CanonicalObject, ObjectSerializer, ValidationResult
from packages.reasoning import ReasoningType, UniversalReasoning


TIMESTAMP = datetime.fromisoformat("2026-07-06T00:00:00+00:00")
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
INTERFACE_PACKAGE_ROOT = REPOSITORY_ROOT / "packages" / "interface"
FORBIDDEN_COGNITIVE_PREFIXES = (
    "packages.memory",
    "packages.knowledge",
    "packages.context",
    "packages.reasoning",
    "packages.decision",
    "packages.action",
    "packages.execution",
)


def build_external_representation() -> ExternalRepresentation:
    return ExternalRepresentation(
        representation_kind=ExternalRepresentationKind.STRUCTURED,
        representation_identifier="external:00000000-0000-0000-0000-000000007001",
        representation_values={"z": "last", "a": "first", "meaning": "preserve"},
        representation_metadata=TranslationMetadata(values={"source": "golf"}),
    )


def build_certified_request() -> CanonicalInterfaceRequest:
    payload = normalize_to_canonical_payload(build_external_representation())
    return CanonicalInterfaceRequest(
        object_id=UUID("00000000-0000-0000-0000-000000007002"),
        contract_metadata=InterfaceContractMetadata(values={"channel": "membrane"}),
        correlation=InterfaceCorrelation(correlation_id="corr-golf-001"),
        origin=InterfaceOrigin(origin_identifier="origin:golf"),
        context_references=InterfaceContextReferenceCollection(),
        canonical_payload=payload,
        metadata={"owner": "interface", "mission": "golf"},
        tags=["interface", "golf"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_certified_response() -> CanonicalInterfaceResponse:
    return CanonicalInterfaceResponse(
        status=InterfaceResponseStatus.SUCCESS,
        result=InterfaceResponseResult(values={"outcome": "accepted"}),
        object_id=UUID("00000000-0000-0000-0000-000000007003"),
        contract_metadata=InterfaceContractMetadata(values={"response": "canonical"}),
        metadata={"owner": "interface", "mission": "golf"},
        tags=["interface", "golf"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_certified_boundary_model() -> InterfaceBoundaryModel:
    return InterfaceBoundaryModel(
        object_id=UUID("00000000-0000-0000-0000-000000007004"),
        boundary_identifier="constitutional-membrane",
        boundary_side=InterfaceBoundarySide.MEMBRANE,
        exclusivity=InterfaceBoundaryExclusivity(single_membrane=True),
        boundary_metadata=InterfaceLifecycleMetadata(values={"scope": "phase-ii"}),
        metadata={"owner": "interface", "mission": "golf"},
        tags=["interface", "golf"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_certified_artifact_lifecycle(
    request: CanonicalInterfaceRequest,
) -> InterfaceArtifactLifecycle:
    boundary = build_certified_boundary_model()
    return InterfaceArtifactLifecycle(
        object_id=UUID("00000000-0000-0000-0000-000000007005"),
        interface_lifecycle_state=InterfaceLifecycleState.ACTIVE,
        boundary_descriptor=boundary.to_descriptor(),
        artifact_reference=f"artifact:{request.object_id}",
        lifecycle_metadata=InterfaceLifecycleMetadata(values={"phase": "golf"}),
        metadata={"owner": "interface", "mission": "golf"},
        tags=["interface", "golf"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_certified_translation_contract() -> CanonicalTranslationContract:
    source = build_external_representation()
    canonical_payload = normalize_to_canonical_payload(source)
    descriptor = TranslationDescriptor(
        translation_direction=TranslationDirection.INBOUND_TO_CANONICAL,
        source_representation_identifier=source.representation_identifier,
        target_payload_schema_identifier="canonical-payload:v1",
        reversibility=TranslationReversibilityDescriptor(
            preservation_complete=True,
            preserved_field_identifiers=("a", "meaning", "z"),
        ),
    )
    return CanonicalTranslationContract(
        object_id=UUID("00000000-0000-0000-0000-000000007006"),
        translation_descriptor=descriptor,
        source_representation=source,
        canonical_payload=canonical_payload,
        translation_metadata=TranslationMetadata(values={"mission": "golf"}),
        metadata={"owner": "interface", "mission": "golf"},
        tags=["interface", "golf"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_certified_validation_record(
    request: CanonicalInterfaceRequest,
) -> InterfaceValidationRecord:
    policy = InterfaceValidationPolicy(
        policy_identifier="canonical-request:golf",
        policy_version="1.0",
        validation_target=InterfaceValidationTarget.REQUEST,
        target_object_type="CanonicalInterfaceRequest",
        version_rule=InterfaceVersionCompatibilityRule(
            required_schema_version="1.0",
            minimum_object_version=1,
        ),
    )
    from packages.interface import InterfaceValidationDescriptor, validation_result_to_outcome

    outcome = validation_result_to_outcome(evaluate_interface_artifact(request, policy))
    descriptor = InterfaceValidationDescriptor(
        validation_target=InterfaceValidationTarget.REQUEST,
        target_object_type="CanonicalInterfaceRequest",
    )
    return InterfaceValidationRecord(
        object_id=UUID("00000000-0000-0000-0000-000000007007"),
        validation_descriptor=descriptor,
        validation_policy=policy,
        validation_outcome=outcome,
        metadata={"owner": "interface", "mission": "golf"},
        tags=["interface", "golf"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_certified_registration_contract() -> InterfaceRegistrationContract:
    descriptor = InterfaceAdapterDescriptor(
        adapter_identifier="adapter:canonical-request:golf",
        artifact_object_type="CanonicalInterfaceRequest",
        capability_declarations=(
            InterfaceCapabilityDeclaration(capability_identifier="contract.request"),
        ),
        descriptor_metadata=InterfaceRegistryMetadata(values={"scope": "golf"}),
    )
    return InterfaceRegistrationContract(
        object_id=UUID("00000000-0000-0000-0000-000000007008"),
        registration_identifier="registration:canonical-request:golf",
        adapter_descriptor=descriptor,
        registration_metadata=InterfaceRegistryMetadata(values={"mission": "golf"}),
        metadata={"owner": "interface", "mission": "golf"},
        tags=["interface", "golf"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_certified_registry_entry() -> InterfaceRegistryEntry:
    contract = build_certified_registration_contract()
    return InterfaceRegistryEntry(
        registration_identifier=contract.registration_identifier,
        registration_contract=contract,
        adapter_descriptor=contract.adapter_descriptor,
    )


def build_certified_foundation() -> InterfaceFoundation:
    return InterfaceFoundation(
        object_id=UUID("00000000-0000-0000-0000-000000007009"),
        metadata={"owner": "interface", "mission": "golf"},
        tags=["interface", "golf"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def certified_canonical_object_inventory() -> tuple[tuple[str, CanonicalObject], ...]:
    request = build_certified_request()
    return (
        ("InterfaceFoundation", build_certified_foundation()),
        ("CanonicalInterfaceRequest", request),
        ("CanonicalInterfaceResponse", build_certified_response()),
        ("InterfaceBoundaryModel", build_certified_boundary_model()),
        ("InterfaceArtifactLifecycle", build_certified_artifact_lifecycle(request)),
        ("CanonicalTranslationContract", build_certified_translation_contract()),
        ("InterfaceValidationRecord", build_certified_validation_record(request)),
        ("InterfaceRegistrationContract", build_certified_registration_contract()),
    )


def interface_production_modules() -> tuple[Path, ...]:
    return tuple(
        sorted(
            path
            for path in INTERFACE_PACKAGE_ROOT.rglob("*.py")
            if path.name != "__init__.py"
        )
    )


class InterfacePlatformIntegrationCertificationTest(unittest.TestCase):
    def test_scenario_1_platform_core_inheritance_certification(self) -> None:
        for expected_type, artifact in certified_canonical_object_inventory():
            with self.subTest(object_type=expected_type):
                self.assertIsInstance(artifact, CanonicalObject)
                self.assertEqual(artifact.object_type, expected_type)
                self.assertIsInstance(artifact.validate(), ValidationResult)
                self.assertTrue(artifact.validate().is_valid)

    def test_scenario_2_canonical_serialization_certification(self) -> None:
        for expected_type, artifact in certified_canonical_object_inventory():
            with self.subTest(object_type=expected_type):
                payload = ObjectSerializer.serialize(artifact)
                self.assertEqual(payload["object_type"], expected_type)
                self.assertEqual(payload["object_id"], str(artifact.object_id))

    def test_scenario_3_validation_interoperability_certification(self) -> None:
        request = build_certified_request()
        policy = InterfaceValidationPolicy(
            policy_identifier="canonical-request:golf",
            validation_target=InterfaceValidationTarget.REQUEST,
            target_object_type="CanonicalInterfaceRequest",
            version_rule=InterfaceVersionCompatibilityRule(required_schema_version="1.0"),
        )
        valid_result = evaluate_interface_artifact(request, policy)
        invalid_result = evaluate_interface_artifact(
            build_external_representation(),
            policy,
        )

        self.assertIsInstance(valid_result, ValidationResult)
        self.assertTrue(valid_result.is_valid)
        self.assertIsInstance(invalid_result, ValidationResult)
        self.assertFalse(invalid_result.is_valid)
        self.assertEqual(invalid_result.errors[0].code, "validation_containment_violation")

    def test_scenario_4_object_identity_preservation_certification(self) -> None:
        for expected_type, artifact in certified_canonical_object_inventory():
            with self.subTest(object_type=expected_type):
                before_id = str(artifact.object_id)
                serialized = ObjectSerializer.serialize(artifact)
                self.assertEqual(serialized["object_id"], before_id)
                self.assertEqual(artifact.to_dict()["object_id"], before_id)
                self.assertEqual(artifact.to_dict()["object_type"], expected_type)

    def test_scenario_5_cognitive_independence_certification(self) -> None:
        for module_path in interface_production_modules():
            with self.subTest(module=module_path.name):
                source = module_path.read_text(encoding="utf-8")
                for prefix in FORBIDDEN_COGNITIVE_PREFIXES:
                    self.assertNotIn(prefix, source)

        memory = UniversalMemory(
            memory_type=MemoryType.SEMANTIC,
            content="Interface certification coexists with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-golf"),
        )
        knowledge = UniversalKnowledge(knowledge_type=KnowledgeType.FACT)
        context = UniversalContext(context_type=ContextType.ANALYTICAL)
        reasoning = UniversalReasoning(reasoning_type=ReasoningType.DEDUCTIVE)
        decision = UniversalDecision(decision_type=DecisionType.RECOMMENDATION)
        action = UniversalAction(action_type=ActionType.TASK)
        execution = UniversalExecution(execution_type=ExecutionType.ACTION)
        request = build_certified_request()

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertTrue(reasoning.validate().is_valid)
        self.assertTrue(decision.validate().is_valid)
        self.assertTrue(action.validate().is_valid)
        self.assertTrue(execution.validate().is_valid)
        self.assertTrue(request.validate().is_valid)

    def test_scenario_6_constitutional_boundary_exclusivity_certification(self) -> None:
        boundary = build_certified_boundary_model()
        invalid_exclusivity = InterfaceBoundaryExclusivity(single_membrane=False)

        self.assertTrue(validate_interface_boundary_exclusivity(boundary.exclusivity).is_valid)
        self.assertFalse(validate_interface_boundary_exclusivity(invalid_exclusivity).is_valid)
        self.assertEqual(boundary.boundary_side, InterfaceBoundarySide.MEMBRANE)
        self.assertTrue((INTERFACE_PACKAGE_ROOT / "lifecycle" / "boundary.py").exists())
        self.assert_no_behavior(boundary, {"route", "dispatch", "transport", "authorize"})

    def test_scenario_7_translation_containment_certification(self) -> None:
        source = build_external_representation()
        payload = normalize_to_canonical_payload(source)
        policy = InterfaceValidationPolicy(
            policy_identifier="containment:golf",
            validation_target=InterfaceValidationTarget.REQUEST,
            target_object_type="CanonicalInterfaceRequest",
        )

        self.assertNotIn("representation_kind", payload.to_dict())
        self.assertNotIn("representation_identifier", payload.to_dict())
        self.assertEqual(payload.to_dict(), {"a": "first", "meaning": "preserve", "z": "last"})
        self.assertFalse(evaluate_interface_artifact(source, policy).is_valid)

    def test_scenario_8_translation_determinism_certification(self) -> None:
        source = build_external_representation()
        outputs = [
            json.dumps(normalize_to_canonical_payload(source).to_dict(), sort_keys=True)
            for _ in range(5)
        ]

        self.assertTrue(all(output == outputs[0] for output in outputs))

    def test_scenario_9_registry_determinism_and_integrity_certification(self) -> None:
        registry = InterfaceRegistry()
        entry = build_certified_registry_entry()
        registry.register(entry)
        criteria = InterfaceRegistryLookupCriteria(
            artifact_object_type="CanonicalInterfaceRequest",
        )

        lookup_payloads = [registry.lookup(criteria).to_dict() for _ in range(5)]

        self.assertTrue(all(payload == lookup_payloads[0] for payload in lookup_payloads))
        self.assertTrue(registry.validate().is_valid)

        with self.assertRaises(ValueError):
            registry.register(entry)

        self.assert_no_behavior(
            registry,
            {"activate", "bind", "execute", "instantiate", "load", "resolve"},
        )

        exact = registry.lookup_exact("registration:canonical-request:golf")
        assert exact is not None
        payload = exact.to_dict()
        self.assertNotIn("runtime_handle", payload)
        self.assertNotIn("provider_binding", payload)

    def test_scenario_10_end_to_end_constitutional_compliance_certification(self) -> None:
        source = build_external_representation()
        payload = normalize_to_canonical_payload(source)
        request = build_certified_request()
        policy = InterfaceValidationPolicy(
            policy_identifier="pipeline:golf",
            validation_target=InterfaceValidationTarget.REQUEST,
            target_object_type="CanonicalInterfaceRequest",
            version_rule=InterfaceVersionCompatibilityRule(required_schema_version="1.0"),
        )
        validation = evaluate_interface_artifact(request, policy)
        lifecycle = build_certified_artifact_lifecycle(request)
        registry = InterfaceRegistry()
        registry.register(build_certified_registry_entry())
        lookup = registry.lookup(
            InterfaceRegistryLookupCriteria(
                artifact_object_type="CanonicalInterfaceRequest",
            )
        )

        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000007711"),
            memory_type=MemoryType.SEMANTIC,
            content="End-to-end certification coexists with memory.",
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
        decision = UniversalDecision(
            object_id=UUID("00000000-0000-0000-0000-000000007715"),
            decision_type=DecisionType.RECOMMENDATION,
        )
        action = UniversalAction(
            object_id=UUID("00000000-0000-0000-0000-000000007716"),
            action_type=ActionType.TASK,
        )
        execution = UniversalExecution(
            object_id=UUID("00000000-0000-0000-0000-000000007717"),
            execution_type=ExecutionType.ACTION,
        )

        before = (
            memory.to_dict(),
            knowledge.to_dict(),
            context.to_dict(),
            reasoning.to_dict(),
            decision.to_dict(),
            action.to_dict(),
            execution.to_dict(),
        )

        self.assertEqual(payload.to_dict(), request.canonical_payload.to_dict())
        self.assertTrue(validation.is_valid)
        self.assertTrue(lifecycle.validate().is_valid)
        self.assertEqual(len(lookup.entries), 1)
        self.assertEqual(
            lookup.entries[0].registration_identifier,
            "registration:canonical-request:golf",
        )

        after = (
            memory.to_dict(),
            knowledge.to_dict(),
            context.to_dict(),
            reasoning.to_dict(),
            decision.to_dict(),
            action.to_dict(),
            execution.to_dict(),
        )
        self.assertEqual(before, after)

    def assert_no_behavior(self, obj: object, forbidden_names: set[str]) -> None:
        self.assertTrue(forbidden_names.isdisjoint(set(dir(obj))))


if __name__ == "__main__":
    unittest.main()
