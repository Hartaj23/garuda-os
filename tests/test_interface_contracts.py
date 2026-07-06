import unittest
from datetime import datetime
from uuid import UUID

from packages.interface import (
    CanonicalInterfacePayload,
    CanonicalInterfaceRequest,
    CanonicalInterfaceResponse,
    InterfaceContextReference,
    InterfaceContextReferenceCollection,
    InterfaceContractMetadata,
    InterfaceCorrelation,
    InterfaceOrigin,
    InterfaceResponseError,
    InterfaceResponseErrorCollection,
    InterfaceResponseResult,
    InterfaceResponseStatus,
    InterfaceResponseWarning,
    validate_canonical_interface_request,
    validate_canonical_interface_response,
)
from packages.objects import CanonicalObject, ObjectSerializer, ValidationResult


TIMESTAMP = datetime.fromisoformat("2026-07-06T00:00:00+00:00")


def build_request() -> CanonicalInterfaceRequest:
    return CanonicalInterfaceRequest(
        object_id=UUID("00000000-0000-0000-0000-000000002001"),
        contract_metadata=InterfaceContractMetadata(values={"channel": "membrane"}),
        correlation=InterfaceCorrelation(
            correlation_id="corr-000000000001",
            trace_metadata=InterfaceContractMetadata(values={"trace": "bravo"}),
        ),
        origin=InterfaceOrigin(
            origin_identifier="origin:external-system",
            origin_metadata=InterfaceContractMetadata(values={"scope": "boundary"}),
        ),
        context_references=InterfaceContextReferenceCollection(
            references=(
                InterfaceContextReference(
                    reference_identifier="context:00000000-0000-0000-0000-000000002002",
                    reference_metadata=InterfaceContractMetadata(values={"role": "input"}),
                ),
            )
        ),
        canonical_payload=CanonicalInterfacePayload(values={"z": "last", "a": "first"}),
        metadata={"owner": "interface"},
        tags=["interface", "bravo"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_response() -> CanonicalInterfaceResponse:
    return CanonicalInterfaceResponse(
        object_id=UUID("00000000-0000-0000-0000-000000002003"),
        status=InterfaceResponseStatus.SUCCESS,
        result=InterfaceResponseResult(values={"outcome": "accepted"}),
        warnings=(
            InterfaceResponseWarning(
                message="Non-blocking warning",
                warning_metadata=InterfaceContractMetadata(values={"level": "info"}),
            ),
        ),
        errors=InterfaceResponseErrorCollection(
            errors=(
                InterfaceResponseError(
                    message="Structured error message",
                    error_metadata=InterfaceContractMetadata(values={"detail": "example"}),
                ),
            )
        ),
        contract_metadata=InterfaceContractMetadata(values={"response": "canonical"}),
        metadata={"owner": "interface"},
        tags=["interface", "bravo"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


class InterfaceContractsTest(unittest.TestCase):
    def test_golf_scenario_1_both_contracts_inherit_platform_core(self) -> None:
        request = build_request()
        response = build_response()

        self.assertIsInstance(request, CanonicalObject)
        self.assertIsInstance(response, CanonicalObject)
        self.assertEqual(request.object_type, "CanonicalInterfaceRequest")
        self.assertEqual(response.object_type, "CanonicalInterfaceResponse")

    def test_golf_scenario_2_canonical_serialization_without_custom_adapters(self) -> None:
        request = build_request()
        response = build_response()

        request_core = ObjectSerializer.serialize(request)
        response_core = ObjectSerializer.serialize(response)
        request_payload = request.to_dict()
        response_payload = response.to_dict()

        self.assertEqual(request_core["object_type"], "CanonicalInterfaceRequest")
        self.assertEqual(response_core["object_type"], "CanonicalInterfaceResponse")
        self.assertEqual(request_payload["canonical_payload"], {"a": "first", "z": "last"})
        self.assertEqual(response_payload["status"], "success")
        self.assertEqual(
            request_payload["context_references"]["references"][0]["reference_identifier"],
            "context:00000000-0000-0000-0000-000000002002",
        )

    def test_golf_scenario_3_platform_validation_passes(self) -> None:
        request = build_request()
        response = build_response()

        self.assertTrue(request.validate().is_valid)
        self.assertTrue(response.validate().is_valid)

    def test_golf_scenario_4_identity_preserved_through_serialization_cycle(self) -> None:
        request = build_request()
        response = build_response()

        request_id = str(request.object_id)
        response_id = str(response.object_id)

        self.assertEqual(request.to_dict()["object_id"], request_id)
        self.assertEqual(response.to_dict()["object_id"], response_id)
        self.assertEqual(ObjectSerializer.serialize(request)["object_id"], request_id)
        self.assertEqual(ObjectSerializer.serialize(response)["object_id"], response_id)

    def test_golf_scenario_5_no_cognitive_foundation_imports_in_contract_package(self) -> None:
        import packages.interface.contracts.common as common_module
        import packages.interface.contracts.request as request_module
        import packages.interface.contracts.response as response_module

        forbidden_prefixes = (
            "packages.memory",
            "packages.knowledge",
            "packages.context",
            "packages.reasoning",
            "packages.decision",
            "packages.action",
            "packages.execution",
        )

        for module in (common_module, request_module, response_module):
            module_name = module.__name__
            with open(module.__file__, encoding="utf-8") as module_file:
                source = module_file.read()
            for prefix in forbidden_prefixes:
                self.assertNotIn(prefix, source, f"{module_name} must not import {prefix}")

    def test_context_references_store_opaque_identifiers_only(self) -> None:
        request = build_request()
        reference = request.context_references.references[0]

        self.assertEqual(
            reference.reference_identifier,
            "context:00000000-0000-0000-0000-000000002002",
        )
        self.assertNotIn("resolve", dir(reference))

    def test_canonical_payload_remains_technology_neutral(self) -> None:
        payload = CanonicalInterfacePayload(
            values={
                "statement": "canonical data only",
                "format_hint": "none",
            }
        )

        self.assertEqual(
            payload.to_dict(),
            {
                "format_hint": "none",
                "statement": "canonical data only",
            },
        )
        self.assertNotIn("http", str(payload.to_dict()).lower())
        self.assertNotIn("grpc", str(payload.to_dict()).lower())

    def test_request_validation_reports_invalid_correlation(self) -> None:
        request = build_request()
        request._correlation = "invalid"

        result = request.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "correlation")

    def test_response_validation_reports_invalid_status(self) -> None:
        response = build_response()
        response._status = "success"

        result = response.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "status")

    def test_response_errors_define_structure_only(self) -> None:
        error = InterfaceResponseError(message="Structured message only")

        self.assertEqual(error.to_dict()["message"], "Structured message only")
        self.assertNotIn("code", error.to_dict())
        self.assertNotIn("retry", error.to_dict())

    def test_validate_helpers_return_validation_result(self) -> None:
        request = build_request()
        request._origin = "invalid"

        request_result = validate_canonical_interface_request(request)
        response_result = validate_canonical_interface_response(build_response())

        self.assertIsInstance(request_result, ValidationResult)
        self.assertFalse(request_result.is_valid)
        self.assertTrue(response_result.is_valid)

    def test_shared_contract_models_are_immutable(self) -> None:
        metadata = InterfaceContractMetadata(values={"a": 1})
        correlation = InterfaceCorrelation(correlation_id="corr-001")

        with self.assertRaises(Exception):
            metadata.values = (("b", 2),)  # type: ignore[misc]

        with self.assertRaises(Exception):
            correlation.correlation_id = "changed"  # type: ignore[misc]

    def test_request_to_dict_is_deterministic(self) -> None:
        request = build_request()

        first = request.to_dict()
        second = request.to_dict()

        self.assertEqual(first, second)
        self.assertEqual(first["contract_metadata"], {"channel": "membrane"})
        self.assertEqual(first["origin"]["origin_identifier"], "origin:external-system")


if __name__ == "__main__":
    unittest.main()
