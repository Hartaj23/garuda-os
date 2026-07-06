import unittest
from datetime import datetime
from uuid import UUID

from packages.interface import (
    InterfaceAdapterDescriptor,
    InterfaceCapabilityDeclaration,
    InterfaceRegistrationContract,
    InterfaceRegistry,
    InterfaceRegistryEntry,
    InterfaceRegistryLookupCriteria,
    InterfaceRegistryMetadata,
)
from packages.objects import CanonicalObject, ObjectSerializer


TIMESTAMP = datetime.fromisoformat("2026-07-06T00:00:00+00:00")


def build_registration_contract() -> InterfaceRegistrationContract:
    descriptor = InterfaceAdapterDescriptor(
        adapter_identifier="adapter:canonical-request",
        artifact_object_type="CanonicalInterfaceRequest",
        capability_declarations=(
            InterfaceCapabilityDeclaration(capability_identifier="contract.request"),
        ),
        descriptor_metadata=InterfaceRegistryMetadata(values={"scope": "foxtrot"}),
    )
    return InterfaceRegistrationContract(
        object_id=UUID("00000000-0000-0000-0000-000000006001"),
        registration_identifier="registration:canonical-request:v1",
        adapter_descriptor=descriptor,
        registration_metadata=InterfaceRegistryMetadata(values={"mission": "foxtrot"}),
        metadata={"owner": "interface"},
        tags=["interface", "foxtrot"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_registry_entry() -> InterfaceRegistryEntry:
    contract = build_registration_contract()
    return InterfaceRegistryEntry(
        registration_identifier=contract.registration_identifier,
        registration_contract=contract,
        adapter_descriptor=contract.adapter_descriptor,
    )


class InterfaceRegistryTest(unittest.TestCase):
    def test_registry_determinism_repeated_lookups(self) -> None:
        registry = InterfaceRegistry()
        registry.register(build_registry_entry())
        criteria = InterfaceRegistryLookupCriteria(
            artifact_object_type="CanonicalInterfaceRequest",
        )

        results = [registry.lookup(criteria).to_dict() for _ in range(5)]

        self.assertTrue(all(result == results[0] for result in results))

    def test_registry_integrity_rejects_duplicate_registration(self) -> None:
        registry = InterfaceRegistry()
        registry.register(build_registry_entry())

        with self.assertRaises(ValueError):
            registry.register(build_registry_entry())

    def test_registry_integrity_accepts_valid_registration(self) -> None:
        registry = InterfaceRegistry()
        registry.register(build_registry_entry())

        self.assertTrue(registry.validate().is_valid)
        self.assertEqual(registry.identifiers(), ("registration:canonical-request:v1",))

    def test_registry_independence_has_no_execution_apis(self) -> None:
        registry = InterfaceRegistry()

        forbidden = ("activate", "execute", "instantiate", "resolve", "bind", "load")
        for name in forbidden:
            self.assertNotIn(name, dir(registry))

    def test_lookup_returns_descriptive_information_only(self) -> None:
        registry = InterfaceRegistry()
        registry.register(build_registry_entry())

        result = registry.lookup_exact("registration:canonical-request:v1")

        assert result is not None
        payload = result.to_dict()
        self.assertIn("adapter_descriptor", payload)
        self.assertNotIn("runtime_handle", payload)
        self.assertNotIn("provider_binding", payload)

    def test_registration_contract_inherits_platform_core(self) -> None:
        contract = build_registration_contract()

        self.assertIsInstance(contract, CanonicalObject)
        self.assertEqual(contract.object_type, "InterfaceRegistrationContract")
        self.assertTrue(contract.validate().is_valid)

    def test_lookup_by_artifact_type_is_sorted(self) -> None:
        registry = InterfaceRegistry()
        first = build_registry_entry()
        second_contract = InterfaceRegistrationContract(
            registration_identifier="registration:canonical-response:v1",
            adapter_descriptor=InterfaceAdapterDescriptor(
                adapter_identifier="adapter:canonical-response",
                artifact_object_type="CanonicalInterfaceResponse",
            ),
        )
        second = InterfaceRegistryEntry(
            registration_identifier=second_contract.registration_identifier,
            registration_contract=second_contract,
            adapter_descriptor=second_contract.adapter_descriptor,
        )
        registry.register(second)
        registry.register(first)

        matches = registry.lookup_by_artifact_type("CanonicalInterfaceRequest")

        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].registration_identifier, "registration:canonical-request:v1")

    def test_capability_declarations_are_descriptive_only(self) -> None:
        capability = InterfaceCapabilityDeclaration(capability_identifier="contract.request")

        self.assertEqual(capability.to_dict()["capability_identifier"], "contract.request")
        self.assertNotIn("priority", capability.to_dict())

    def test_platform_core_serialization_for_registration_contract(self) -> None:
        contract = build_registration_contract()

        payload = ObjectSerializer.serialize(contract)

        self.assertEqual(payload["object_type"], "InterfaceRegistrationContract")

    def test_no_cognitive_foundation_imports_in_registry_modules(self) -> None:
        import packages.interface.registry.contract as contract_module
        import packages.interface.registry.registry as registry_module

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
