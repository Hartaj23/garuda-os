import unittest
from datetime import datetime
from uuid import UUID

from packages.integration import (
    CanonicalIntegrationContract,
    IntegrationContractMetadata,
    IntegrationContractSubordination,
    IntegrationParticipantReference,
    IntegrationParticipantReferenceCollection,
    build_interface_subordination,
    validate_canonical_integration_contract,
)
from packages.interface import (
    CanonicalInterfacePayload,
    CanonicalInterfaceRequest,
    CanonicalInterfaceResponse,
    InterfaceContextReferenceCollection,
    InterfaceContractMetadata,
    InterfaceCorrelation,
    InterfaceOrigin,
    InterfaceResponseResult,
    InterfaceResponseStatus,
)
from packages.objects import CanonicalObject, ObjectSerializer, ValidationResult


TIMESTAMP = datetime.fromisoformat("2026-07-07T00:00:00+00:00")


def build_interface_request() -> CanonicalInterfaceRequest:
    return CanonicalInterfaceRequest(
        object_id=UUID("00000000-0000-0000-0000-000000003001"),
        contract_metadata=InterfaceContractMetadata(values={"channel": "membrane"}),
        correlation=InterfaceCorrelation(correlation_id="corr-integration-bravo"),
        origin=InterfaceOrigin(origin_identifier="origin:external-system"),
        context_references=InterfaceContextReferenceCollection(),
        canonical_payload=CanonicalInterfacePayload(values={"scope": "integration"}),
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_interface_response() -> CanonicalInterfaceResponse:
    return CanonicalInterfaceResponse(
        object_id=UUID("00000000-0000-0000-0000-000000003002"),
        status=InterfaceResponseStatus.SUCCESS,
        result=InterfaceResponseResult(values={"outcome": "accepted"}),
        contract_metadata=InterfaceContractMetadata(values={"response": "canonical"}),
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_integration_contract(
    interface_contract: CanonicalInterfaceRequest | CanonicalInterfaceResponse,
) -> CanonicalIntegrationContract:
    return CanonicalIntegrationContract(
        object_id=UUID("00000000-0000-0000-0000-000000003003"),
        contract_metadata=IntegrationContractMetadata(values={"governance": "integration"}),
        interface_subordination=build_interface_subordination(
            interface_contract,
            subordination_metadata=IntegrationContractMetadata(values={"link": "interface"}),
        ),
        participant_references=IntegrationParticipantReferenceCollection(
            references=(
                IntegrationParticipantReference(
                    participant_identifier="participant:00000000-0000-0000-0000-000000003004",
                    participant_metadata=IntegrationContractMetadata(values={"role": "source"}),
                ),
            )
        ),
        metadata={"owner": "integration"},
        tags=["integration", "bravo"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


class IntegrationContractsTest(unittest.TestCase):
    def test_integration_contract_inherits_platform_core(self) -> None:
        contract = build_integration_contract(build_interface_request())

        self.assertIsInstance(contract, CanonicalObject)
        self.assertEqual(contract.object_type, "CanonicalIntegrationContract")

    def test_subordination_links_to_interface_request(self) -> None:
        interface_request = build_interface_request()
        contract = build_integration_contract(interface_request)

        self.assertTrue(contract.interface_subordination.is_subordinate_to(interface_request))
        self.assertEqual(
            contract.interface_subordination.interface_contract_object_type,
            "CanonicalInterfaceRequest",
        )
        self.assertEqual(
            contract.interface_subordination.interface_contract_object_id,
            "00000000-0000-0000-0000-000000003001",
        )

    def test_subordination_links_to_interface_response(self) -> None:
        interface_response = build_interface_response()
        contract = build_integration_contract(interface_response)

        self.assertTrue(contract.interface_subordination.is_subordinate_to(interface_response))
        self.assertEqual(
            contract.interface_subordination.interface_contract_object_type,
            "CanonicalInterfaceResponse",
        )

    def test_subordination_rejects_non_matching_interface_contract(self) -> None:
        interface_request = build_interface_request()
        contract = build_integration_contract(interface_request)

        self.assertFalse(
            contract.interface_subordination.is_subordinate_to(build_interface_response())
        )

    def test_participant_references_are_technology_neutral(self) -> None:
        contract = build_integration_contract(build_interface_request())
        reference = contract.participant_references.references[0]

        self.assertEqual(
            reference.participant_identifier,
            "participant:00000000-0000-0000-0000-000000003004",
        )
        self.assertNotIn("http", reference.participant_identifier.lower())
        self.assertNotIn("credential", str(reference.to_dict()).lower())

    def test_valid_contract_passes_platform_validation(self) -> None:
        contract = build_integration_contract(build_interface_request())

        self.assertTrue(contract.validate().is_valid)

    def test_contract_validation_reports_invalid_subordination_type(self) -> None:
        contract = build_integration_contract(build_interface_request())
        contract._interface_subordination = IntegrationContractSubordination(
            interface_contract_object_id="00000000-0000-0000-0000-000000003001",
            interface_contract_object_type="InvalidInterfaceContract",
        )

        result = contract.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "interface_subordination.interface_contract_object_type")

    def test_contract_validation_reports_invalid_participant_reference(self) -> None:
        contract = build_integration_contract(build_interface_request())
        contract._participant_references = IntegrationParticipantReferenceCollection(
            references=(
                IntegrationParticipantReference(participant_identifier=""),
            )
        )

        result = contract.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(
            result.errors[0].field,
            "participant_references.references[0].participant_identifier",
        )

    def test_validate_helper_returns_validation_result(self) -> None:
        contract = build_integration_contract(build_interface_request())
        contract._contract_metadata = "invalid"

        result = validate_canonical_integration_contract(contract)

        self.assertIsInstance(result, ValidationResult)
        self.assertFalse(result.is_valid)

    def test_contract_to_dict_is_deterministic(self) -> None:
        contract = build_integration_contract(build_interface_request())

        first = contract.to_dict()
        second = contract.to_dict()

        self.assertEqual(first, second)
        self.assertEqual(first["contract_metadata"], {"governance": "integration"})
        self.assertEqual(
            first["interface_subordination"]["interface_contract_object_type"],
            "CanonicalInterfaceRequest",
        )

    def test_platform_core_serialization_without_custom_adapters(self) -> None:
        contract = build_integration_contract(build_interface_request())

        core_payload = ObjectSerializer.serialize(contract)
        contract_payload = contract.to_dict()

        self.assertEqual(core_payload["object_type"], "CanonicalIntegrationContract")
        self.assertEqual(
            contract_payload["participant_references"]["references"][0]["participant_identifier"],
            "participant:00000000-0000-0000-0000-000000003004",
        )

    def test_no_cognitive_foundation_imports_in_contract_package(self) -> None:
        import packages.integration.contracts.common as common_module
        import packages.integration.contracts.contract as contract_module
        import packages.integration.contracts.subordination as subordination_module

        forbidden_prefixes = (
            "packages.memory",
            "packages.knowledge",
            "packages.context",
            "packages.reasoning",
            "packages.decision",
            "packages.action",
            "packages.execution",
        )

        for module in (common_module, contract_module, subordination_module):
            module_name = module.__name__
            with open(module.__file__, encoding="utf-8") as module_file:
                source = module_file.read()
            for prefix in forbidden_prefixes:
                self.assertNotIn(prefix, source, f"{module_name} must not import {prefix}")

    def test_interface_foundation_contracts_remain_unmodified(self) -> None:
        interface_request = build_interface_request()

        self.assertEqual(interface_request.object_type, "CanonicalInterfaceRequest")
        self.assertTrue(interface_request.validate().is_valid)


if __name__ == "__main__":
    unittest.main()
