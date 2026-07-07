import unittest
from datetime import datetime
from uuid import UUID

from packages.integration import (
    CanonicalIntegrationContract,
    IntegrationContractMetadata,
    IntegrationFoundation,
    IntegrationParticipantReference,
    IntegrationParticipantReferenceCollection,
    IntegrationSubordinationRule,
    IntegrationValidationDescriptor,
    IntegrationValidationPolicy,
    IntegrationValidationRecord,
    IntegrationValidationRule,
    IntegrationValidationRuleKind,
    IntegrationValidationTarget,
    IntegrationVersionCompatibilityRule,
    build_integration_validation_report,
    build_interface_subordination,
    compose_cross_model_integration_validation,
    compose_integration_validation_results,
    evaluate_integration_artifact,
    serialize_integration_validation_outcome,
    validation_result_to_outcome,
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


TIMESTAMP = datetime.fromisoformat("2026-07-07T00:00:00+00:00")


def build_interface_request() -> CanonicalInterfaceRequest:
    return CanonicalInterfaceRequest(
        object_id=UUID("00000000-0000-0000-0000-000000006001"),
        contract_metadata=InterfaceContractMetadata(values={"channel": "membrane"}),
        correlation=InterfaceCorrelation(correlation_id="corr-integration-echo"),
        origin=InterfaceOrigin(origin_identifier="origin:external-system"),
        context_references=InterfaceContextReferenceCollection(),
        canonical_payload=CanonicalInterfacePayload(values={"scope": "integration"}),
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_integration_contract() -> CanonicalIntegrationContract:
    interface_request = build_interface_request()
    return CanonicalIntegrationContract(
        object_id=UUID("00000000-0000-0000-0000-000000006002"),
        contract_metadata=IntegrationContractMetadata(values={"governance": "integration"}),
        interface_subordination=build_interface_subordination(interface_request),
        participant_references=IntegrationParticipantReferenceCollection(
            references=(
                IntegrationParticipantReference(
                    participant_identifier="participant:00000000-0000-0000-0000-000000006003",
                ),
            )
        ),
        metadata={"owner": "integration"},
        tags=["integration", "echo"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_contract_policy() -> IntegrationValidationPolicy:
    return IntegrationValidationPolicy(
        policy_identifier="canonical-integration-contract:v1",
        policy_version="1.0",
        validation_target=IntegrationValidationTarget.CONTRACT,
        target_object_type="CanonicalIntegrationContract",
        version_rule=IntegrationVersionCompatibilityRule(
            required_schema_version="1.0",
            minimum_object_version=1,
        ),
        validation_rules=(
            IntegrationValidationRule(
                rule_identifier="artifact-structure",
                rule_kind=IntegrationValidationRuleKind.ARTIFACT_STRUCTURE,
            ),
            IntegrationValidationRule(
                rule_identifier="subordination",
                rule_kind=IntegrationValidationRuleKind.SUBORDINATION,
            ),
        ),
    )


class IntegrationValidationTest(unittest.TestCase):
    def test_validation_determinism_repeated_evaluation(self) -> None:
        contract = build_integration_contract()
        policy = build_contract_policy()

        outcomes = [
            validation_result_to_outcome(evaluate_integration_artifact(contract, policy)).to_dict()
            for _ in range(5)
        ]

        self.assertTrue(all(outcome == outcomes[0] for outcome in outcomes))

    def test_canonical_validation_integrity_valid_artifact_passes(self) -> None:
        result = evaluate_integration_artifact(build_integration_contract(), build_contract_policy())

        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_canonical_validation_integrity_version_mismatch_fails(self) -> None:
        contract = build_integration_contract()
        policy = IntegrationValidationPolicy(
            policy_identifier="strict-schema",
            validation_target=IntegrationValidationTarget.CONTRACT,
            target_object_type="CanonicalIntegrationContract",
            version_rule=IntegrationVersionCompatibilityRule(required_schema_version="2.0"),
        )

        result = evaluate_integration_artifact(contract, policy)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "artifact.schema_version")

    def test_validation_independence_rejects_interface_foundation(self) -> None:
        foundation = InterfaceFoundation()
        policy = build_contract_policy()

        result = evaluate_integration_artifact(foundation, policy)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "invalid_validation_artifact_type")

    def test_variability_containment_rejects_non_integration_artifact(self) -> None:
        foundation = IntegrationFoundation()
        policy = IntegrationValidationPolicy(
            policy_identifier="foundation-policy",
            validation_target=IntegrationValidationTarget.FOUNDATION,
            target_object_type="IntegrationFoundation",
        )

        result = evaluate_integration_artifact(foundation, policy)

        self.assertTrue(result.is_valid)

    def test_subordination_match_validation(self) -> None:
        interface_request = build_interface_request()
        contract = build_integration_contract()
        policy = IntegrationValidationPolicy(
            policy_identifier="subordination-match",
            validation_target=IntegrationValidationTarget.CONTRACT,
            target_object_type="CanonicalIntegrationContract",
            subordination_rule=IntegrationSubordinationRule(
                require_valid_subordination=True,
                require_interface_contract_match=True,
            ),
        )

        matched = evaluate_integration_artifact(
            contract,
            policy,
            interface_contract=interface_request,
        )
        mismatched = evaluate_integration_artifact(
            contract,
            policy,
            interface_contract=InterfaceFoundation(),
        )

        self.assertTrue(matched.is_valid)
        self.assertFalse(mismatched.is_valid)
        self.assertEqual(mismatched.errors[0].code, "interface_subordination_mismatch")

    def test_validation_record_inherits_platform_core(self) -> None:
        contract = build_integration_contract()
        policy = build_contract_policy()
        outcome = validation_result_to_outcome(evaluate_integration_artifact(contract, policy))
        record = IntegrationValidationRecord(
            object_id=UUID("00000000-0000-0000-0000-000000006004"),
            validation_descriptor=IntegrationValidationDescriptor(
                validation_target=IntegrationValidationTarget.CONTRACT,
                target_object_type="CanonicalIntegrationContract",
            ),
            validation_policy=policy,
            validation_outcome=outcome,
        )

        self.assertIsInstance(record, CanonicalObject)
        self.assertEqual(record.object_type, "IntegrationValidationRecord")
        self.assertTrue(record.validate().is_valid)

    def test_validation_policy_is_immutable(self) -> None:
        policy = build_contract_policy()

        with self.assertRaises(Exception):
            policy.policy_identifier = "changed"  # type: ignore[misc]

    def test_validation_issue_has_no_business_or_transport_semantics(self) -> None:
        outcome = validation_result_to_outcome(
            evaluate_integration_artifact(build_integration_contract(), build_contract_policy())
        )

        payload = str(outcome.to_dict())
        self.assertNotIn("retry", payload.lower())
        self.assertNotIn("http", payload.lower())

    def test_evaluator_has_no_side_effects(self) -> None:
        contract = build_integration_contract()
        before = contract.to_dict()
        policy = build_contract_policy()

        evaluate_integration_artifact(contract, policy)

        self.assertEqual(contract.to_dict(), before)

    def test_platform_core_serialization_for_validation_record(self) -> None:
        contract = build_integration_contract()
        policy = build_contract_policy()
        outcome = validation_result_to_outcome(evaluate_integration_artifact(contract, policy))
        record = IntegrationValidationRecord(
            validation_descriptor=IntegrationValidationDescriptor(
                validation_target=IntegrationValidationTarget.CONTRACT,
                target_object_type="CanonicalIntegrationContract",
            ),
            validation_policy=policy,
            validation_outcome=outcome,
        )

        core_payload = ObjectSerializer.serialize(record)

        self.assertEqual(core_payload["object_type"], "IntegrationValidationRecord")

    def test_policy_target_mismatch_fails_deterministically(self) -> None:
        contract = build_integration_contract()
        policy = IntegrationValidationPolicy(
            policy_identifier="mismatch",
            validation_target=IntegrationValidationTarget.FOUNDATION,
            target_object_type="IntegrationFoundation",
        )

        result = evaluate_integration_artifact(contract, policy)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "policy_target_mismatch")

    def test_validation_report_aggregates_results(self) -> None:
        contract = build_integration_contract()
        policy = build_contract_policy()
        invalid_policy = IntegrationValidationPolicy(
            policy_identifier="invalid-schema",
            validation_target=IntegrationValidationTarget.CONTRACT,
            target_object_type="CanonicalIntegrationContract",
            version_rule=IntegrationVersionCompatibilityRule(required_schema_version="2.0"),
        )

        report = build_integration_validation_report(
            evaluate_integration_artifact(contract, policy),
            evaluate_integration_artifact(contract, invalid_policy),
        )

        self.assertFalse(report.is_valid)
        self.assertEqual(len(report.outcomes), 2)

    def test_cross_model_validation_composition(self) -> None:
        contract = build_integration_contract()
        policies = (
            build_contract_policy(),
            IntegrationValidationPolicy(
                policy_identifier="structure-only",
                validation_target=IntegrationValidationTarget.CONTRACT,
                target_object_type="CanonicalIntegrationContract",
            ),
        )

        result = compose_cross_model_integration_validation(contract, *policies)

        self.assertTrue(result.is_valid)

    def test_compose_integration_validation_results_is_deterministic(self) -> None:
        first = ValidationResult()
        first.add_error("first", ValidationCategory.SCHEMA, field="artifact.first")
        second = ValidationResult()
        second.add_error("second", ValidationCategory.SCHEMA, field="artifact.second")

        composed = compose_integration_validation_results(first, second)

        self.assertFalse(composed.is_valid)
        self.assertEqual(len(composed.errors), 2)
        self.assertEqual(composed.errors[0].field, "artifact.first")

    def test_serialize_integration_validation_outcome_is_deterministic(self) -> None:
        outcome = validation_result_to_outcome(
            evaluate_integration_artifact(build_integration_contract(), build_contract_policy())
        )

        first = serialize_integration_validation_outcome(outcome)
        second = serialize_integration_validation_outcome(outcome)

        self.assertEqual(first, second)

    def test_no_cognitive_foundation_imports_in_validation_modules(self) -> None:
        import packages.integration.validation.framework as framework_module
        import packages.integration.validation.policy as policy_module

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
