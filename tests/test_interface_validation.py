import unittest
from datetime import datetime
from uuid import UUID

from packages.interface import (
    CanonicalInterfacePayload,
    CanonicalInterfaceRequest,
    ExternalRepresentation,
    ExternalRepresentationKind,
    InterfaceContextReferenceCollection,
    InterfaceContractMetadata,
    InterfaceCorrelation,
    InterfaceOrigin,
    InterfaceValidationDescriptor,
    InterfaceValidationPolicy,
    InterfaceValidationRecord,
    InterfaceValidationTarget,
    InterfaceVersionCompatibilityRule,
    evaluate_interface_artifact,
    validation_result_to_outcome,
)
from packages.objects import CanonicalObject, ObjectSerializer, ValidationResult


TIMESTAMP = datetime.fromisoformat("2026-07-06T00:00:00+00:00")


def build_request() -> CanonicalInterfaceRequest:
    return CanonicalInterfaceRequest(
        object_id=UUID("00000000-0000-0000-0000-000000005001"),
        contract_metadata=InterfaceContractMetadata(values={"channel": "membrane"}),
        correlation=InterfaceCorrelation(correlation_id="corr-echo-001"),
        origin=InterfaceOrigin(origin_identifier="origin:echo"),
        context_references=InterfaceContextReferenceCollection(),
        canonical_payload=CanonicalInterfacePayload(values={"scope": "echo"}),
        metadata={"owner": "interface"},
        tags=["interface", "echo"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_request_policy() -> InterfaceValidationPolicy:
    return InterfaceValidationPolicy(
        policy_identifier="canonical-request:v1",
        policy_version="1.0",
        validation_target=InterfaceValidationTarget.REQUEST,
        target_object_type="CanonicalInterfaceRequest",
        version_rule=InterfaceVersionCompatibilityRule(
            required_schema_version="1.0",
            minimum_object_version=1,
        ),
    )


class InterfaceValidationTest(unittest.TestCase):
    def test_validation_determinism_repeated_evaluation(self) -> None:
        request = build_request()
        policy = build_request_policy()

        outcomes = [
            validation_result_to_outcome(evaluate_interface_artifact(request, policy)).to_dict()
            for _ in range(5)
        ]

        self.assertTrue(all(outcome == outcomes[0] for outcome in outcomes))

    def test_canonical_validation_integrity_valid_artifact_passes(self) -> None:
        result = evaluate_interface_artifact(build_request(), build_request_policy())

        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_canonical_validation_integrity_version_mismatch_fails(self) -> None:
        request = build_request()
        policy = InterfaceValidationPolicy(
            policy_identifier="strict-schema",
            validation_target=InterfaceValidationTarget.REQUEST,
            target_object_type="CanonicalInterfaceRequest",
            version_rule=InterfaceVersionCompatibilityRule(required_schema_version="2.0"),
        )

        result = evaluate_interface_artifact(request, policy)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "artifact.schema_version")

    def test_validation_independence_rejects_external_representation(self) -> None:
        external = ExternalRepresentation(
            representation_kind=ExternalRepresentationKind.OPAQUE,
            representation_identifier="external:echo",
        )
        policy = build_request_policy()

        result = evaluate_interface_artifact(external, policy)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "validation_containment_violation")

    def test_validation_record_inherits_platform_core(self) -> None:
        request = build_request()
        policy = build_request_policy()
        outcome = validation_result_to_outcome(evaluate_interface_artifact(request, policy))
        descriptor = InterfaceValidationDescriptor(
            validation_target=InterfaceValidationTarget.REQUEST,
            target_object_type="CanonicalInterfaceRequest",
        )
        record = InterfaceValidationRecord(
            object_id=UUID("00000000-0000-0000-0000-000000005002"),
            validation_descriptor=descriptor,
            validation_policy=policy,
            validation_outcome=outcome,
        )

        self.assertIsInstance(record, CanonicalObject)
        self.assertEqual(record.object_type, "InterfaceValidationRecord")
        self.assertTrue(record.validate().is_valid)

    def test_validation_policy_is_immutable(self) -> None:
        policy = build_request_policy()

        with self.assertRaises(Exception):
            policy.policy_identifier = "changed"  # type: ignore[misc]

    def test_validation_issue_has_no_business_or_transport_semantics(self) -> None:
        outcome = validation_result_to_outcome(
            evaluate_interface_artifact(build_request(), build_request_policy())
        )

        payload = str(outcome.to_dict())
        self.assertNotIn("retry", payload.lower())
        self.assertNotIn("http", payload.lower())

    def test_evaluator_has_no_side_effects(self) -> None:
        request = build_request()
        before = request.to_dict()
        policy = build_request_policy()

        evaluate_interface_artifact(request, policy)

        self.assertEqual(request.to_dict(), before)

    def test_platform_core_serialization_for_validation_record(self) -> None:
        request = build_request()
        policy = build_request_policy()
        outcome = validation_result_to_outcome(evaluate_interface_artifact(request, policy))
        record = InterfaceValidationRecord(
            validation_descriptor=InterfaceValidationDescriptor(
                validation_target=InterfaceValidationTarget.REQUEST,
                target_object_type="CanonicalInterfaceRequest",
            ),
            validation_policy=policy,
            validation_outcome=outcome,
        )

        core_payload = ObjectSerializer.serialize(record)

        self.assertEqual(core_payload["object_type"], "InterfaceValidationRecord")

    def test_policy_target_mismatch_fails_deterministically(self) -> None:
        request = build_request()
        policy = InterfaceValidationPolicy(
            policy_identifier="mismatch",
            validation_target=InterfaceValidationTarget.RESPONSE,
            target_object_type="CanonicalInterfaceResponse",
        )

        result = evaluate_interface_artifact(request, policy)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "policy_target_mismatch")

    def test_no_cognitive_foundation_imports_in_validation_modules(self) -> None:
        import packages.interface.validation.framework as framework_module
        import packages.interface.validation.policy as policy_module

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
