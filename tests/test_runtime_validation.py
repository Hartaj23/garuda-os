import unittest
from datetime import datetime
from uuid import UUID

from packages.execution import ExecutionType, UniversalExecution
from packages.integration import (
    CanonicalIntegrationContract,
    IntegrationContractMetadata,
    IntegrationFoundation,
    IntegrationParticipantReference,
    IntegrationParticipantReferenceCollection,
    build_interface_subordination as build_integration_interface_subordination,
)
from packages.interface import (
    CanonicalInterfacePayload,
    CanonicalInterfaceRequest,
    InterfaceContextReferenceCollection,
    InterfaceContractMetadata,
    InterfaceCorrelation,
    InterfaceFoundation,
    InterfaceOrigin,
)
from packages.objects import CanonicalObject, ObjectSerializer, ValidationCategory, ValidationResult
from packages.runtime import (
    CanonicalRuntimeContextClassification,
    CanonicalRuntimeContract,
    RuntimeArtifactLifecycle,
    RuntimeBoundaryExclusivity,
    RuntimeBoundaryModel,
    RuntimeBoundarySide,
    RuntimeClassificationMetadata,
    RuntimeContextClassification,
    RuntimeContextClassificationHook,
    RuntimeContextClassificationHookCollection,
    RuntimeContextReference,
    RuntimeContextReferenceCollection,
    RuntimeContractMetadata,
    RuntimeFoundation,
    RuntimeLifecycleMetadata,
    RuntimeLifecycleState,
    RuntimeSubordinationRule,
    RuntimeValidationDescriptor,
    RuntimeValidationPolicy,
    RuntimeValidationRecord,
    RuntimeValidationRule,
    RuntimeValidationRuleKind,
    RuntimeValidationTarget,
    RuntimeVersionCompatibilityRule,
    build_integration_subordination,
    build_interface_subordination,
    build_runtime_validation_report,
    compose_cross_model_runtime_validation,
    compose_runtime_validation_results,
    evaluate_runtime_artifact,
    serialize_runtime_validation_outcome,
    validate_runtime_operational_runtime_exclusion,
    validation_result_to_outcome,
)


TIMESTAMP = datetime.fromisoformat("2026-07-07T00:00:00+00:00")


def build_interface_request() -> CanonicalInterfaceRequest:
    return CanonicalInterfaceRequest(
        object_id=UUID("00000000-0000-0000-0000-000000007001"),
        contract_metadata=InterfaceContractMetadata(values={"channel": "membrane"}),
        correlation=InterfaceCorrelation(correlation_id="corr-runtime-echo"),
        origin=InterfaceOrigin(origin_identifier="origin:external-system"),
        context_references=InterfaceContextReferenceCollection(),
        canonical_payload=CanonicalInterfacePayload(values={"scope": "runtime"}),
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_integration_contract(
    interface_contract: CanonicalInterfaceRequest,
    *,
    object_id: UUID = UUID("00000000-0000-0000-0000-000000007002"),
) -> CanonicalIntegrationContract:
    return CanonicalIntegrationContract(
        object_id=object_id,
        contract_metadata=IntegrationContractMetadata(values={"governance": "integration"}),
        interface_subordination=build_integration_interface_subordination(interface_contract),
        participant_references=IntegrationParticipantReferenceCollection(
            references=(
                IntegrationParticipantReference(
                    participant_identifier="participant:00000000-0000-0000-0000-000000007003",
                ),
            )
        ),
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_runtime_contract() -> CanonicalRuntimeContract:
    interface_request = build_interface_request()
    integration_contract = build_integration_contract(interface_request)

    return CanonicalRuntimeContract(
        object_id=UUID("00000000-0000-0000-0000-000000007004"),
        contract_metadata=RuntimeContractMetadata(values={"governance": "runtime"}),
        integration_subordination=build_integration_subordination(integration_contract),
        interface_subordination=build_interface_subordination(interface_request),
        context_references=RuntimeContextReferenceCollection(
            references=(
                RuntimeContextReference(
                    context_identifier="context:00000000-0000-0000-0000-000000007005",
                ),
            )
        ),
        metadata={"owner": "runtime"},
        tags=["runtime", "echo"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_boundary_model() -> RuntimeBoundaryModel:
    return RuntimeBoundaryModel(
        object_id=UUID("00000000-0000-0000-0000-000000007006"),
        boundary_identifier="runtime-stack-traversal",
        boundary_side=RuntimeBoundarySide.STACK_TRAVERSAL,
        exclusivity=RuntimeBoundaryExclusivity(
            traverses_integration_foundation=True,
            traverses_interface_foundation=True,
        ),
        boundary_metadata=RuntimeLifecycleMetadata(values={"scope": "runtime"}),
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_artifact_lifecycle() -> RuntimeArtifactLifecycle:
    boundary = build_boundary_model()
    return RuntimeArtifactLifecycle(
        object_id=UUID("00000000-0000-0000-0000-000000007007"),
        runtime_lifecycle_state=RuntimeLifecycleState.ACTIVE,
        boundary_descriptor=boundary.to_descriptor(),
        artifact_reference="artifact:00000000-0000-0000-0000-000000007008",
        lifecycle_metadata=RuntimeLifecycleMetadata(values={"phase": "echo"}),
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_classification_record() -> CanonicalRuntimeContextClassification:
    primary_reference = RuntimeContextReference(
        context_identifier="context:00000000-0000-0000-0000-000000007009",
    )
    return CanonicalRuntimeContextClassification(
        object_id=UUID("00000000-0000-0000-0000-000000007010"),
        context_reference=primary_reference,
        classification=RuntimeContextClassification.EXTERNAL_FACING,
        classification_hooks=RuntimeContextClassificationHookCollection(
            hooks=(
                RuntimeContextClassificationHook(
                    context_reference=primary_reference,
                    classification=RuntimeContextClassification.EXTERNAL_FACING,
                ),
            )
        ),
        classification_metadata=RuntimeClassificationMetadata(values={"taxonomy": "runtime"}),
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_contract_policy() -> RuntimeValidationPolicy:
    return RuntimeValidationPolicy(
        policy_identifier="canonical-runtime-contract:v1",
        policy_version="1.0",
        validation_target=RuntimeValidationTarget.CONTRACT,
        target_object_type="CanonicalRuntimeContract",
        version_rule=RuntimeVersionCompatibilityRule(
            required_schema_version="1.0",
            minimum_object_version=1,
        ),
        validation_rules=(
            RuntimeValidationRule(
                rule_identifier="artifact-structure",
                rule_kind=RuntimeValidationRuleKind.ARTIFACT_STRUCTURE,
            ),
            RuntimeValidationRule(
                rule_identifier="subordination",
                rule_kind=RuntimeValidationRuleKind.SUBORDINATION,
            ),
        ),
    )


def policy_for_object_type(
    target: RuntimeValidationTarget,
    object_type: str,
) -> RuntimeValidationPolicy:
    return RuntimeValidationPolicy(
        policy_identifier=f"{object_type.lower()}:v1",
        validation_target=target,
        target_object_type=object_type,
    )


class RuntimeValidationTest(unittest.TestCase):
    def test_package_exports_import_cleanly(self) -> None:
        import packages.runtime as runtime_pkg

        for symbol in (
            "CANONICAL_RUNTIME_ARTIFACT_TYPES",
            "RuntimeValidationPolicy",
            "RuntimeValidationRecord",
            "evaluate_runtime_artifact",
            "compose_runtime_validation_results",
            "build_runtime_validation_report",
        ):
            self.assertIn(symbol, runtime_pkg.__all__)
            self.assertTrue(hasattr(runtime_pkg, symbol))

    def test_validation_determinism_repeated_evaluation(self) -> None:
        contract = build_runtime_contract()
        policy = build_contract_policy()

        outcomes = [
            validation_result_to_outcome(evaluate_runtime_artifact(contract, policy)).to_dict()
            for _ in range(5)
        ]

        self.assertTrue(all(outcome == outcomes[0] for outcome in outcomes))

    def test_valid_runtime_contract_passes(self) -> None:
        result = evaluate_runtime_artifact(build_runtime_contract(), build_contract_policy())

        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_valid_foundation_passes(self) -> None:
        foundation = RuntimeFoundation(
            created_by="codex",
            updated_by="codex",
            created_at=TIMESTAMP,
            updated_at=TIMESTAMP,
        )
        policy = policy_for_object_type(
            RuntimeValidationTarget.FOUNDATION,
            "RuntimeFoundation",
        )

        result = evaluate_runtime_artifact(foundation, policy)

        self.assertTrue(result.is_valid)

    def test_valid_boundary_passes(self) -> None:
        result = evaluate_runtime_artifact(
            build_boundary_model(),
            policy_for_object_type(RuntimeValidationTarget.BOUNDARY, "RuntimeBoundaryModel"),
        )

        self.assertTrue(result.is_valid)

    def test_valid_lifecycle_passes(self) -> None:
        result = evaluate_runtime_artifact(
            build_artifact_lifecycle(),
            policy_for_object_type(RuntimeValidationTarget.LIFECYCLE, "RuntimeArtifactLifecycle"),
        )

        self.assertTrue(result.is_valid)

    def test_valid_classification_passes(self) -> None:
        result = evaluate_runtime_artifact(
            build_classification_record(),
            policy_for_object_type(
                RuntimeValidationTarget.CLASSIFICATION,
                "CanonicalRuntimeContextClassification",
            ),
        )

        self.assertTrue(result.is_valid)

    def test_version_mismatch_fails(self) -> None:
        contract = build_runtime_contract()
        policy = RuntimeValidationPolicy(
            policy_identifier="strict-schema",
            validation_target=RuntimeValidationTarget.CONTRACT,
            target_object_type="CanonicalRuntimeContract",
            version_rule=RuntimeVersionCompatibilityRule(required_schema_version="2.0"),
        )

        result = evaluate_runtime_artifact(contract, policy)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "artifact.schema_version")

    def test_validation_independence_rejects_integration_foundation(self) -> None:
        foundation = IntegrationFoundation()
        policy = build_contract_policy()

        result = evaluate_runtime_artifact(foundation, policy)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "invalid_validation_artifact_type")

    def test_validation_independence_rejects_interface_foundation(self) -> None:
        foundation = InterfaceFoundation()
        policy = build_contract_policy()

        result = evaluate_runtime_artifact(foundation, policy)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "invalid_validation_artifact_type")

    def test_variability_containment_accepts_runtime_foundation(self) -> None:
        foundation = RuntimeFoundation()
        policy = policy_for_object_type(
            RuntimeValidationTarget.FOUNDATION,
            "RuntimeFoundation",
        )

        result = evaluate_runtime_artifact(foundation, policy)

        self.assertTrue(result.is_valid)

    def test_operational_runtime_exclusion_rejects_universal_execution(self) -> None:
        execution = UniversalExecution(execution_type=ExecutionType.ACTION)

        result = validate_runtime_operational_runtime_exclusion(execution)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "operational_runtime_exclusion_violation")

    def test_dual_subordination_match_validation(self) -> None:
        interface_request = build_interface_request()
        integration_contract = build_integration_contract(interface_request)
        contract = build_runtime_contract()
        policy = RuntimeValidationPolicy(
            policy_identifier="subordination-match",
            validation_target=RuntimeValidationTarget.CONTRACT,
            target_object_type="CanonicalRuntimeContract",
            subordination_rule=RuntimeSubordinationRule(
                require_valid_subordination=True,
                require_integration_contract_match=True,
                require_interface_contract_match=True,
            ),
        )

        matched = evaluate_runtime_artifact(
            contract,
            policy,
            integration_contract=integration_contract,
            interface_contract=interface_request,
        )
        mismatched = evaluate_runtime_artifact(
            contract,
            policy,
            integration_contract=integration_contract,
            interface_contract=InterfaceFoundation(),
        )

        self.assertTrue(matched.is_valid)
        self.assertFalse(mismatched.is_valid)
        self.assertEqual(mismatched.errors[0].code, "interface_subordination_mismatch")

    def test_validation_record_inherits_platform_core(self) -> None:
        contract = build_runtime_contract()
        policy = build_contract_policy()
        outcome = validation_result_to_outcome(evaluate_runtime_artifact(contract, policy))
        record = RuntimeValidationRecord(
            object_id=UUID("00000000-0000-0000-0000-000000007011"),
            validation_descriptor=RuntimeValidationDescriptor(
                validation_target=RuntimeValidationTarget.CONTRACT,
                target_object_type="CanonicalRuntimeContract",
            ),
            validation_policy=policy,
            validation_outcome=outcome,
        )

        self.assertIsInstance(record, CanonicalObject)
        self.assertEqual(record.object_type, "RuntimeValidationRecord")
        self.assertTrue(record.validate().is_valid)

    def test_validation_policy_is_immutable(self) -> None:
        policy = build_contract_policy()

        with self.assertRaises(Exception):
            policy.policy_identifier = "changed"  # type: ignore[misc]

    def test_validation_issue_has_no_business_or_transport_semantics(self) -> None:
        outcome = validation_result_to_outcome(
            evaluate_runtime_artifact(build_runtime_contract(), build_contract_policy())
        )

        payload = str(outcome.to_dict())
        self.assertNotIn("retry", payload.lower())
        self.assertNotIn("http", payload.lower())
        self.assertNotIn("schedule", payload.lower())
        self.assertNotIn("invoke", payload.lower())

    def test_evaluator_has_no_side_effects(self) -> None:
        contract = build_runtime_contract()
        before = contract.to_dict()
        policy = build_contract_policy()

        evaluate_runtime_artifact(contract, policy)

        self.assertEqual(contract.to_dict(), before)

    def test_platform_core_serialization_for_validation_record(self) -> None:
        contract = build_runtime_contract()
        policy = build_contract_policy()
        outcome = validation_result_to_outcome(evaluate_runtime_artifact(contract, policy))
        record = RuntimeValidationRecord(
            validation_descriptor=RuntimeValidationDescriptor(
                validation_target=RuntimeValidationTarget.CONTRACT,
                target_object_type="CanonicalRuntimeContract",
            ),
            validation_policy=policy,
            validation_outcome=outcome,
        )

        core_payload = ObjectSerializer.serialize(record)

        self.assertEqual(core_payload["object_type"], "RuntimeValidationRecord")

    def test_policy_target_mismatch_fails_deterministically(self) -> None:
        contract = build_runtime_contract()
        policy = RuntimeValidationPolicy(
            policy_identifier="mismatch",
            validation_target=RuntimeValidationTarget.FOUNDATION,
            target_object_type="RuntimeFoundation",
        )

        result = evaluate_runtime_artifact(contract, policy)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "policy_target_mismatch")

    def test_validation_report_aggregates_results(self) -> None:
        contract = build_runtime_contract()
        policy = build_contract_policy()
        invalid_policy = RuntimeValidationPolicy(
            policy_identifier="invalid-schema",
            validation_target=RuntimeValidationTarget.CONTRACT,
            target_object_type="CanonicalRuntimeContract",
            version_rule=RuntimeVersionCompatibilityRule(required_schema_version="2.0"),
        )

        report = build_runtime_validation_report(
            evaluate_runtime_artifact(contract, policy),
            evaluate_runtime_artifact(contract, invalid_policy),
        )

        self.assertFalse(report.is_valid)
        self.assertEqual(len(report.outcomes), 2)

    def test_cross_model_validation_composition(self) -> None:
        contract = build_runtime_contract()
        policies = (
            build_contract_policy(),
            RuntimeValidationPolicy(
                policy_identifier="structure-only",
                validation_target=RuntimeValidationTarget.CONTRACT,
                target_object_type="CanonicalRuntimeContract",
            ),
        )

        result = compose_cross_model_runtime_validation(contract, *policies)

        self.assertTrue(result.is_valid)

    def test_compose_runtime_validation_results_preserves_stable_issue_order(self) -> None:
        first = ValidationResult()
        first.add_error("alpha", ValidationCategory.SCHEMA, field="artifact.alpha")
        second = ValidationResult()
        second.add_error("beta", ValidationCategory.SCHEMA, field="artifact.beta")

        forward = compose_runtime_validation_results(first, second)
        reverse = compose_runtime_validation_results(second, first)

        self.assertFalse(forward.is_valid)
        self.assertEqual(len(forward.errors), 2)
        self.assertEqual([error.field for error in forward.errors], [error.field for error in reverse.errors])
        self.assertEqual(forward.errors[0].field, "artifact.alpha")
        self.assertEqual(forward.errors[1].field, "artifact.beta")

    def test_serialize_runtime_validation_outcome_is_deterministic(self) -> None:
        outcome = validation_result_to_outcome(
            evaluate_runtime_artifact(build_runtime_contract(), build_contract_policy())
        )

        first = serialize_runtime_validation_outcome(outcome)
        second = serialize_runtime_validation_outcome(outcome)

        self.assertEqual(first, second)

    def test_no_cognitive_foundation_imports_in_validation_modules(self) -> None:
        import packages.runtime.validation.framework as framework_module
        import packages.runtime.validation.policy as policy_module

        forbidden_prefixes = (
            "packages.memory",
            "packages.knowledge",
            "packages.context",
            "packages.reasoning",
            "packages.decision",
            "packages.action",
            "packages.execution",
        )

        for module in (policy_module, framework_module):
            with open(module.__file__, encoding="utf-8") as module_file:
                source = module_file.read()
            for prefix in forbidden_prefixes:
                self.assertNotIn(prefix, source)


if __name__ == "__main__":
    unittest.main()
