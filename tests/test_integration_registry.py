import unittest
from datetime import datetime
from uuid import UUID

from packages.integration import (
    CanonicalIntegrationContract,
    IntegrationContractMetadata,
    IntegrationParticipantCatalogDeclaration,
    IntegrationParticipantDescriptor,
    IntegrationParticipantReference,
    IntegrationParticipantReferenceCollection,
    IntegrationRegistrationContract,
    IntegrationRegistry,
    IntegrationRegistryEntry,
    IntegrationRegistryLookupCriteria,
    IntegrationRegistryMetadata,
    build_interface_subordination,
    compose_integration_registry_entry,
    validate_integration_registry_artifact_composition,
)
from packages.interface import (
    CanonicalInterfacePayload,
    CanonicalInterfaceRequest,
    InterfaceContextReferenceCollection,
    InterfaceContractMetadata,
    InterfaceCorrelation,
    InterfaceOrigin,
)
from packages.objects import CanonicalObject, ObjectSerializer


TIMESTAMP = datetime.fromisoformat("2026-07-07T00:00:00+00:00")


def build_interface_request() -> CanonicalInterfaceRequest:
    return CanonicalInterfaceRequest(
        object_id=UUID("00000000-0000-0000-0000-000000007001"),
        contract_metadata=InterfaceContractMetadata(values={"channel": "membrane"}),
        correlation=InterfaceCorrelation(correlation_id="corr-integration-foxtrot"),
        origin=InterfaceOrigin(origin_identifier="origin:external-system"),
        context_references=InterfaceContextReferenceCollection(),
        canonical_payload=CanonicalInterfacePayload(values={"scope": "integration"}),
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_integration_contract() -> CanonicalIntegrationContract:
    return CanonicalIntegrationContract(
        object_id=UUID("00000000-0000-0000-0000-000000007002"),
        contract_metadata=IntegrationContractMetadata(values={"governance": "integration"}),
        interface_subordination=build_interface_subordination(build_interface_request()),
        participant_references=IntegrationParticipantReferenceCollection(
            references=(
                IntegrationParticipantReference(
                    participant_identifier="participant:00000000-0000-0000-0000-000000007003",
                ),
            )
        ),
        metadata={"owner": "integration"},
        tags=["integration", "foxtrot"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_registration_contract() -> IntegrationRegistrationContract:
    descriptor = IntegrationParticipantDescriptor(
        participant_identifier="participant:00000000-0000-0000-0000-000000007003",
        artifact_object_type="CanonicalIntegrationContract",
        catalog_declarations=(
            IntegrationParticipantCatalogDeclaration(
                catalog_identifier="integration.contract",
            ),
        ),
        descriptor_metadata=IntegrationRegistryMetadata(values={"scope": "foxtrot"}),
    )
    return IntegrationRegistrationContract(
        object_id=UUID("00000000-0000-0000-0000-000000007004"),
        registration_identifier="registration:integration-contract:v1",
        participant_descriptor=descriptor,
        registration_metadata=IntegrationRegistryMetadata(values={"mission": "foxtrot"}),
        metadata={"owner": "integration"},
        tags=["integration", "foxtrot"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_registry_entry() -> IntegrationRegistryEntry:
    return compose_integration_registry_entry(build_registration_contract())


class IntegrationRegistryTest(unittest.TestCase):
    def test_registry_determinism_repeated_lookups(self) -> None:
        registry = IntegrationRegistry()
        registry.register(build_registry_entry())
        criteria = IntegrationRegistryLookupCriteria(
            artifact_object_type="CanonicalIntegrationContract",
        )

        results = [registry.lookup(criteria).to_dict() for _ in range(5)]

        self.assertTrue(all(result == results[0] for result in results))

    def test_registry_integrity_rejects_duplicate_registration(self) -> None:
        registry = IntegrationRegistry()
        registry.register(build_registry_entry())

        with self.assertRaises(ValueError):
            registry.register(build_registry_entry())

    def test_registry_integrity_accepts_valid_registration(self) -> None:
        registry = IntegrationRegistry()
        registry.register(build_registry_entry())

        self.assertTrue(registry.validate().is_valid)
        self.assertEqual(registry.identifiers(), ("registration:integration-contract:v1",))

    def test_registry_independence_has_no_execution_apis(self) -> None:
        registry = IntegrationRegistry()

        forbidden = ("activate", "execute", "instantiate", "resolve", "bind", "load")
        for name in forbidden:
            self.assertNotIn(name, dir(registry))

    def test_lookup_returns_descriptive_information_only(self) -> None:
        registry = IntegrationRegistry()
        registry.register(build_registry_entry())

        result = registry.lookup_exact("registration:integration-contract:v1")

        assert result is not None
        payload = result.to_dict()
        self.assertIn("participant_descriptor", payload)
        self.assertNotIn("runtime_handle", payload)
        self.assertNotIn("provider_binding", payload)

    def test_registration_contract_inherits_platform_core(self) -> None:
        contract = build_registration_contract()

        self.assertIsInstance(contract, CanonicalObject)
        self.assertEqual(contract.object_type, "IntegrationRegistrationContract")
        self.assertTrue(contract.validate().is_valid)

    def test_lookup_by_artifact_type_is_sorted(self) -> None:
        registry = IntegrationRegistry()
        first = build_registry_entry()
        second_contract = IntegrationRegistrationContract(
            registration_identifier="registration:integration-foundation:v1",
            participant_descriptor=IntegrationParticipantDescriptor(
                participant_identifier="participant:00000000-0000-0000-0000-000000007005",
                artifact_object_type="IntegrationFoundation",
            ),
        )
        second = compose_integration_registry_entry(second_contract)
        registry.register(second)
        registry.register(first)

        matches = registry.lookup_by_artifact_type("CanonicalIntegrationContract")

        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].registration_identifier, "registration:integration-contract:v1")

    def test_catalog_declarations_are_descriptive_only(self) -> None:
        declaration = IntegrationParticipantCatalogDeclaration(
            catalog_identifier="integration.contract",
        )

        self.assertEqual(declaration.to_dict()["catalog_identifier"], "integration.contract")
        self.assertNotIn("priority", declaration.to_dict())

    def test_platform_core_serialization_for_registration_contract(self) -> None:
        contract = build_registration_contract()

        payload = ObjectSerializer.serialize(contract)

        self.assertEqual(payload["object_type"], "IntegrationRegistrationContract")

    def test_registry_artifact_composition_matches_published_artifact(self) -> None:
        contract = build_integration_contract()
        descriptor = IntegrationParticipantDescriptor(
            participant_identifier="participant:00000000-0000-0000-0000-000000007003",
            artifact_object_type="CanonicalIntegrationContract",
        )

        result = validate_integration_registry_artifact_composition(contract, descriptor)

        self.assertTrue(result.is_valid)

    def test_registry_artifact_composition_rejects_type_mismatch(self) -> None:
        contract = build_integration_contract()
        descriptor = IntegrationParticipantDescriptor(
            participant_identifier="participant:00000000-0000-0000-0000-000000007003",
            artifact_object_type="IntegrationFoundation",
        )

        result = validate_integration_registry_artifact_composition(contract, descriptor)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "registry_artifact_type_mismatch")

    def test_compose_registry_entry_is_deterministic(self) -> None:
        first = compose_integration_registry_entry(build_registration_contract())
        second = compose_integration_registry_entry(build_registration_contract())

        self.assertEqual(first.to_dict(), second.to_dict())

    def test_no_cognitive_foundation_imports_in_registry_modules(self) -> None:
        import packages.integration.registry.contract as contract_module
        import packages.integration.registry.registry as registry_module

        forbidden_prefixes = (
            "packages.memory",
            "packages.knowledge",
            "packages.context",
            "packages.reasoning",
            "packages.decision",
            "packages.action",
            "packages.execution",
        )

        for module in (contract_module, registry_module):
            with open(module.__file__, encoding="utf-8") as module_file:
                source = module_file.read()
            for prefix in forbidden_prefixes:
                self.assertNotIn(prefix, source)


if __name__ == "__main__":
    unittest.main()
