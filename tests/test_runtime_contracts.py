import unittest
from datetime import datetime
from uuid import UUID

from packages.integration import (
    CanonicalIntegrationContract,
    IntegrationContractMetadata,
    IntegrationParticipantReference,
    IntegrationParticipantReferenceCollection,
    build_interface_subordination as build_integration_interface_subordination,
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
from packages.runtime import (
    CanonicalRuntimeContract,
    RuntimeContextReference,
    RuntimeContextReferenceCollection,
    RuntimeContractMetadata,
    RuntimeIntegrationContractSubordination,
    RuntimeInterfaceContractSubordination,
    build_integration_subordination,
    build_interface_subordination,
    validate_canonical_runtime_contract,
)


TIMESTAMP = datetime.fromisoformat("2026-07-07T00:00:00+00:00")


def build_interface_request() -> CanonicalInterfaceRequest:
    return CanonicalInterfaceRequest(
        object_id=UUID("00000000-0000-0000-0000-000000004001"),
        contract_metadata=InterfaceContractMetadata(values={"channel": "membrane"}),
        correlation=InterfaceCorrelation(correlation_id="corr-runtime-bravo"),
        origin=InterfaceOrigin(origin_identifier="origin:external-system"),
        context_references=InterfaceContextReferenceCollection(),
        canonical_payload=CanonicalInterfacePayload(values={"scope": "runtime"}),
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_interface_response() -> CanonicalInterfaceResponse:
    return CanonicalInterfaceResponse(
        object_id=UUID("00000000-0000-0000-0000-000000004002"),
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
    *,
    object_id: UUID = UUID("00000000-0000-0000-0000-000000004003"),
) -> CanonicalIntegrationContract:
    return CanonicalIntegrationContract(
        object_id=object_id,
        contract_metadata=IntegrationContractMetadata(values={"governance": "integration"}),
        interface_subordination=build_integration_interface_subordination(
            interface_contract,
            subordination_metadata=IntegrationContractMetadata(values={"link": "interface"}),
        ),
        participant_references=IntegrationParticipantReferenceCollection(
            references=(
                IntegrationParticipantReference(
                    participant_identifier="participant:00000000-0000-0000-0000-000000004004",
                    participant_metadata=IntegrationContractMetadata(values={"role": "source"}),
                ),
            )
        ),
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_runtime_contract(
    interface_contract: CanonicalInterfaceRequest | CanonicalInterfaceResponse,
) -> CanonicalRuntimeContract:
    integration_contract = build_integration_contract(interface_contract)

    return CanonicalRuntimeContract(
        object_id=UUID("00000000-0000-0000-0000-000000004005"),
        contract_metadata=RuntimeContractMetadata(values={"governance": "runtime"}),
        integration_subordination=build_integration_subordination(
            integration_contract,
            subordination_metadata=RuntimeContractMetadata(values={"link": "integration"}),
        ),
        interface_subordination=build_interface_subordination(
            interface_contract,
            subordination_metadata=RuntimeContractMetadata(values={"link": "interface"}),
        ),
        context_references=RuntimeContextReferenceCollection(
            references=(
                RuntimeContextReference(
                    context_identifier="context:00000000-0000-0000-0000-000000004006",
                    context_metadata=RuntimeContractMetadata(values={"scope": "descriptive"}),
                ),
            )
        ),
        metadata={"owner": "runtime"},
        tags=["runtime", "bravo"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


class RuntimeContractsTest(unittest.TestCase):
    def test_package_exports_import_cleanly(self) -> None:
        import packages.runtime as runtime_pkg

        for symbol in (
            "CanonicalRuntimeContract",
            "RuntimeContractMetadata",
            "RuntimeIntegrationContractSubordination",
            "RuntimeInterfaceContractSubordination",
            "RuntimeContextReference",
            "RuntimeContextReferenceCollection",
            "build_integration_subordination",
            "build_interface_subordination",
            "validate_canonical_runtime_contract",
        ):
            self.assertIn(symbol, runtime_pkg.__all__)
            self.assertTrue(hasattr(runtime_pkg, symbol))

    def test_runtime_contract_inherits_platform_core(self) -> None:
        contract = build_runtime_contract(build_interface_request())

        self.assertIsInstance(contract, CanonicalObject)
        self.assertEqual(contract.object_type, "CanonicalRuntimeContract")

    def test_subordination_links_to_integration_contract(self) -> None:
        interface_request = build_interface_request()
        integration_contract = build_integration_contract(interface_request)
        contract = build_runtime_contract(interface_request)

        self.assertTrue(contract.integration_subordination.is_subordinate_to(integration_contract))
        self.assertEqual(
            contract.integration_subordination.integration_contract_object_type,
            "CanonicalIntegrationContract",
        )
        self.assertEqual(
            contract.integration_subordination.integration_contract_object_id,
            "00000000-0000-0000-0000-000000004003",
        )

    def test_subordination_links_to_interface_request(self) -> None:
        interface_request = build_interface_request()
        contract = build_runtime_contract(interface_request)

        self.assertTrue(contract.interface_subordination.is_subordinate_to(interface_request))
        self.assertEqual(
            contract.interface_subordination.interface_contract_object_type,
            "CanonicalInterfaceRequest",
        )
        self.assertEqual(
            contract.interface_subordination.interface_contract_object_id,
            "00000000-0000-0000-0000-000000004001",
        )

    def test_subordination_links_to_interface_response(self) -> None:
        interface_response = build_interface_response()
        contract = build_runtime_contract(interface_response)

        self.assertTrue(contract.interface_subordination.is_subordinate_to(interface_response))
        self.assertEqual(
            contract.interface_subordination.interface_contract_object_type,
            "CanonicalInterfaceResponse",
        )

    def test_stack_subordination_preserves_lawful_traversal(self) -> None:
        interface_request = build_interface_request()
        integration_contract = build_integration_contract(interface_request)
        contract = build_runtime_contract(interface_request)

        self.assertTrue(contract.integration_subordination.is_subordinate_to(integration_contract))
        self.assertTrue(contract.interface_subordination.is_subordinate_to(interface_request))
        self.assertTrue(
            integration_contract.interface_subordination.is_subordinate_to(interface_request)
        )

    def test_subordination_rejects_non_matching_integration_contract(self) -> None:
        interface_request = build_interface_request()
        contract = build_runtime_contract(interface_request)

        self.assertFalse(
            contract.integration_subordination.is_subordinate_to(
                build_integration_contract(
                    build_interface_response(),
                    object_id=UUID("00000000-0000-0000-0000-000000004099"),
                )
            )
        )

    def test_subordination_rejects_non_matching_interface_contract(self) -> None:
        interface_request = build_interface_request()
        contract = build_runtime_contract(interface_request)

        self.assertFalse(
            contract.interface_subordination.is_subordinate_to(build_interface_response())
        )

    def test_context_references_are_technology_neutral(self) -> None:
        contract = build_runtime_contract(build_interface_request())
        reference = contract.context_references.references[0]

        self.assertEqual(
            reference.context_identifier,
            "context:00000000-0000-0000-0000-000000004006",
        )
        self.assertNotIn("http", reference.context_identifier.lower())
        self.assertNotIn("credential", str(reference.to_dict()).lower())
        self.assertNotIn("engine", str(reference.to_dict()).lower())

    def test_valid_contract_passes_platform_validation(self) -> None:
        contract = build_runtime_contract(build_interface_request())

        self.assertTrue(contract.validate().is_valid)

    def test_contract_validation_reports_invalid_integration_subordination_type(self) -> None:
        contract = build_runtime_contract(build_interface_request())
        contract._integration_subordination = RuntimeIntegrationContractSubordination(
            integration_contract_object_id="00000000-0000-0000-0000-000000004003",
            integration_contract_object_type="InvalidIntegrationContract",
        )

        result = contract.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(
            result.errors[0].field,
            "integration_subordination.integration_contract_object_type",
        )

    def test_contract_validation_reports_invalid_interface_subordination_type(self) -> None:
        contract = build_runtime_contract(build_interface_request())
        contract._interface_subordination = RuntimeInterfaceContractSubordination(
            interface_contract_object_id="00000000-0000-0000-0000-000000004001",
            interface_contract_object_type="InvalidInterfaceContract",
        )

        result = contract.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(
            result.errors[0].field,
            "interface_subordination.interface_contract_object_type",
        )

    def test_contract_validation_reports_invalid_context_reference(self) -> None:
        contract = build_runtime_contract(build_interface_request())
        contract._context_references = RuntimeContextReferenceCollection(
            references=(
                RuntimeContextReference(context_identifier=""),
            )
        )

        result = contract.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(
            result.errors[0].field,
            "context_references.references[0].context_identifier",
        )

    def test_validate_helper_returns_validation_result(self) -> None:
        contract = build_runtime_contract(build_interface_request())
        contract._contract_metadata = "invalid"

        result = validate_canonical_runtime_contract(contract)

        self.assertIsInstance(result, ValidationResult)
        self.assertFalse(result.is_valid)

    def test_contract_to_dict_is_deterministic(self) -> None:
        contract = build_runtime_contract(build_interface_request())

        first = contract.to_dict()
        second = contract.to_dict()

        self.assertEqual(first, second)
        self.assertEqual(first["contract_metadata"], {"governance": "runtime"})
        self.assertEqual(
            first["integration_subordination"]["integration_contract_object_type"],
            "CanonicalIntegrationContract",
        )
        self.assertEqual(
            first["interface_subordination"]["interface_contract_object_type"],
            "CanonicalInterfaceRequest",
        )

    def test_platform_core_serialization_without_custom_adapters(self) -> None:
        contract = build_runtime_contract(build_interface_request())

        core_payload = ObjectSerializer.serialize(contract)
        contract_payload = contract.to_dict()

        self.assertEqual(core_payload["object_type"], "CanonicalRuntimeContract")
        self.assertEqual(
            contract_payload["context_references"]["references"][0]["context_identifier"],
            "context:00000000-0000-0000-0000-000000004006",
        )

    def test_no_cognitive_foundation_imports_in_contract_package(self) -> None:
        import packages.runtime.contracts.common as common_module
        import packages.runtime.contracts.contract as contract_module
        import packages.runtime.contracts.subordination as subordination_module

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

    def test_predecessor_contracts_remain_unmodified(self) -> None:
        interface_request = build_interface_request()
        integration_contract = build_integration_contract(interface_request)
        _runtime_contract = build_runtime_contract(interface_request)

        self.assertEqual(interface_request.object_type, "CanonicalInterfaceRequest")
        self.assertTrue(interface_request.validate().is_valid)
        self.assertEqual(integration_contract.object_type, "CanonicalIntegrationContract")
        self.assertTrue(integration_contract.validate().is_valid)


if __name__ == "__main__":
    unittest.main()
