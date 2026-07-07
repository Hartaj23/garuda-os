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
    InterfaceContextReferenceCollection,
    InterfaceContractMetadata,
    InterfaceCorrelation,
    InterfaceOrigin,
)
from packages.objects import CanonicalObject, LifecycleState, ObjectSerializer
from packages.runtime import (
    CanonicalRuntimeContextClassification,
    CanonicalRuntimeContract,
    RuntimeArtifactLifecycle,
    RuntimeBoundaryExclusivity,
    RuntimeBoundaryModel,
    RuntimeBoundarySide,
    RuntimeClassificationMetadata,
    RuntimeContextCatalogDeclaration,
    RuntimeContextClassification,
    RuntimeContextClassificationHook,
    RuntimeContextClassificationHookCollection,
    RuntimeContextDescriptor,
    RuntimeContextReference,
    RuntimeContextReferenceCollection,
    RuntimeContractMetadata,
    RuntimeFoundation,
    RuntimeLifecycleMetadata,
    RuntimeLifecycleState,
    RuntimeRegistrationContract,
    RuntimeRegistry,
    RuntimeRegistryEntry,
    RuntimeRegistryLookupCriteria,
    RuntimeRegistryMetadata,
    build_integration_subordination,
    build_interface_subordination,
    compose_runtime_registry_entry,
    validate_runtime_registry_artifact_composition,
)


TIMESTAMP = datetime.fromisoformat("2026-07-07T00:00:00+00:00")


def build_interface_request() -> CanonicalInterfaceRequest:
    return CanonicalInterfaceRequest(
        object_id=UUID("00000000-0000-0000-0000-000000008001"),
        contract_metadata=InterfaceContractMetadata(values={"channel": "membrane"}),
        correlation=InterfaceCorrelation(correlation_id="corr-runtime-foxtrot"),
        origin=InterfaceOrigin(origin_identifier="origin:external-system"),
        context_references=InterfaceContextReferenceCollection(),
        canonical_payload=CanonicalInterfacePayload(values={"scope": "runtime"}),
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_integration_contract() -> CanonicalIntegrationContract:
    interface_request = build_interface_request()
    return CanonicalIntegrationContract(
        object_id=UUID("00000000-0000-0000-0000-000000008002"),
        contract_metadata=IntegrationContractMetadata(values={"governance": "integration"}),
        interface_subordination=build_integration_interface_subordination(interface_request),
        participant_references=IntegrationParticipantReferenceCollection(
            references=(
                IntegrationParticipantReference(
                    participant_identifier="participant:00000000-0000-0000-0000-000000008003",
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
    integration_contract = build_integration_contract()

    return CanonicalRuntimeContract(
        object_id=UUID("00000000-0000-0000-0000-000000008004"),
        contract_metadata=RuntimeContractMetadata(values={"governance": "runtime"}),
        integration_subordination=build_integration_subordination(integration_contract),
        interface_subordination=build_interface_subordination(interface_request),
        context_references=RuntimeContextReferenceCollection(
            references=(
                RuntimeContextReference(
                    context_identifier="context:00000000-0000-0000-0000-000000008005",
                ),
            )
        ),
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_boundary_model() -> RuntimeBoundaryModel:
    return RuntimeBoundaryModel(
        object_id=UUID("00000000-0000-0000-0000-000000008006"),
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
        object_id=UUID("00000000-0000-0000-0000-000000008007"),
        runtime_lifecycle_state=RuntimeLifecycleState.ACTIVE,
        boundary_descriptor=boundary.to_descriptor(),
        artifact_reference="artifact:00000000-0000-0000-0000-000000008008",
        lifecycle_metadata=RuntimeLifecycleMetadata(values={"phase": "foxtrot"}),
        lifecycle_state=LifecycleState.DRAFT,
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_classification_record() -> CanonicalRuntimeContextClassification:
    primary_reference = RuntimeContextReference(
        context_identifier="context:00000000-0000-0000-0000-000000008009",
    )
    return CanonicalRuntimeContextClassification(
        object_id=UUID("00000000-0000-0000-0000-000000008010"),
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


def build_registration_contract(
    *,
    registration_identifier: str = "registration:runtime-contract:v1",
    artifact_object_type: str = "CanonicalRuntimeContract",
    context_identifier: str = "context:00000000-0000-0000-0000-000000008005",
) -> RuntimeRegistrationContract:
    descriptor = RuntimeContextDescriptor(
        context_identifier=context_identifier,
        artifact_object_type=artifact_object_type,
        catalog_declarations=(
            RuntimeContextCatalogDeclaration(
                catalog_identifier="runtime.contract",
            ),
        ),
        descriptor_metadata=RuntimeRegistryMetadata(values={"scope": "foxtrot"}),
    )
    return RuntimeRegistrationContract(
        object_id=UUID("00000000-0000-0000-0000-000000008011"),
        registration_identifier=registration_identifier,
        context_descriptor=descriptor,
        registration_metadata=RuntimeRegistryMetadata(values={"mission": "foxtrot"}),
        metadata={"owner": "runtime"},
        tags=["runtime", "foxtrot"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


def build_registry_entry() -> RuntimeRegistryEntry:
    return compose_runtime_registry_entry(build_registration_contract())


class RuntimeRegistryTest(unittest.TestCase):
    def test_package_exports_import_cleanly(self) -> None:
        import packages.runtime as runtime_pkg

        for symbol in (
            "RuntimeRegistry",
            "RuntimeRegistrationContract",
            "RuntimeContextDescriptor",
            "compose_runtime_registry_entry",
            "validate_runtime_registry_artifact_composition",
        ):
            self.assertIn(symbol, runtime_pkg.__all__)
            self.assertTrue(hasattr(runtime_pkg, symbol))

    def test_registry_determinism_repeated_lookups(self) -> None:
        registry = RuntimeRegistry()
        registry.register(build_registry_entry())
        criteria = RuntimeRegistryLookupCriteria(
            artifact_object_type="CanonicalRuntimeContract",
        )

        results = [registry.lookup(criteria).to_dict() for _ in range(5)]

        self.assertTrue(all(result == results[0] for result in results))

    def test_registry_integrity_rejects_duplicate_registration(self) -> None:
        registry = RuntimeRegistry()
        registry.register(build_registry_entry())

        with self.assertRaises(ValueError):
            registry.register(build_registry_entry())

    def test_registry_integrity_accepts_valid_registration(self) -> None:
        registry = RuntimeRegistry()
        registry.register(build_registry_entry())

        self.assertTrue(registry.validate().is_valid)
        self.assertEqual(registry.identifiers(), ("registration:runtime-contract:v1",))

    def test_registry_independence_has_no_execution_apis(self) -> None:
        registry = RuntimeRegistry()

        forbidden = ("activate", "execute", "instantiate", "resolve", "bind", "load")
        for name in forbidden:
            self.assertNotIn(name, dir(registry))

    def test_lookup_returns_descriptive_information_only(self) -> None:
        registry = RuntimeRegistry()
        registry.register(build_registry_entry())

        result = registry.lookup_exact("registration:runtime-contract:v1")

        assert result is not None
        payload = result.to_dict()
        self.assertIn("context_descriptor", payload)
        self.assertNotIn("runtime_handle", payload)
        self.assertNotIn("provider_binding", payload)

    def test_registration_contract_inherits_platform_core(self) -> None:
        contract = build_registration_contract()

        self.assertIsInstance(contract, CanonicalObject)
        self.assertEqual(contract.object_type, "RuntimeRegistrationContract")
        self.assertTrue(contract.validate().is_valid)

    def test_lookup_by_artifact_type_uses_canonical_ordering(self) -> None:
        registry = RuntimeRegistry()
        contract_entry = build_registry_entry()
        foundation_entry = compose_runtime_registry_entry(
            build_registration_contract(
                registration_identifier="registration:runtime-foundation:v1",
                artifact_object_type="RuntimeFoundation",
                context_identifier="context:00000000-0000-0000-0000-000000008012",
            )
        )
        registry.register(foundation_entry)
        registry.register(contract_entry)

        matches = registry.lookup_by_artifact_type("CanonicalRuntimeContract")

        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].registration_identifier, "registration:runtime-contract:v1")

    def test_lookup_uses_same_canonical_ordering_as_lookup_by_artifact_type(self) -> None:
        registry = RuntimeRegistry()
        first = compose_runtime_registry_entry(
            build_registration_contract(
                registration_identifier="registration:runtime-z:v1",
                artifact_object_type="RuntimeFoundation",
                context_identifier="context:00000000-0000-0000-0000-000000008013",
            )
        )
        second = compose_runtime_registry_entry(
            build_registration_contract(
                registration_identifier="registration:runtime-a:v1",
                artifact_object_type="RuntimeFoundation",
                context_identifier="context:00000000-0000-0000-0000-000000008014",
            )
        )
        registry.register(first)
        registry.register(second)

        by_type = registry.lookup_by_artifact_type("RuntimeFoundation")
        by_criteria = registry.lookup(
            RuntimeRegistryLookupCriteria(artifact_object_type="RuntimeFoundation")
        ).entries

        self.assertEqual(
            [entry.registration_identifier for entry in by_type],
            [entry.registration_identifier for entry in by_criteria],
        )
        self.assertEqual(by_type[0].registration_identifier, "registration:runtime-a:v1")

    def test_catalog_declarations_are_descriptive_only(self) -> None:
        declaration = RuntimeContextCatalogDeclaration(
            catalog_identifier="runtime.contract",
        )

        self.assertEqual(declaration.to_dict()["catalog_identifier"], "runtime.contract")
        self.assertNotIn("priority", declaration.to_dict())

    def test_platform_core_serialization_for_registration_contract(self) -> None:
        contract = build_registration_contract()

        payload = ObjectSerializer.serialize(contract)

        self.assertEqual(payload["object_type"], "RuntimeRegistrationContract")

    def test_registry_artifact_composition_matches_published_contract(self) -> None:
        contract = build_runtime_contract()
        descriptor = RuntimeContextDescriptor(
            context_identifier="context:00000000-0000-0000-0000-000000008005",
            artifact_object_type="CanonicalRuntimeContract",
        )

        result = validate_runtime_registry_artifact_composition(contract, descriptor)

        self.assertTrue(result.is_valid)

    def test_registry_artifact_composition_rejects_type_mismatch(self) -> None:
        contract = build_runtime_contract()
        descriptor = RuntimeContextDescriptor(
            context_identifier="context:00000000-0000-0000-0000-000000008005",
            artifact_object_type="RuntimeFoundation",
        )

        result = validate_runtime_registry_artifact_composition(contract, descriptor)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "registry_artifact_type_mismatch")

    def test_compose_registry_entry_is_deterministic(self) -> None:
        first = compose_runtime_registry_entry(build_registration_contract())
        second = compose_runtime_registry_entry(build_registration_contract())

        self.assertEqual(first.to_dict(), second.to_dict())

    def test_interoperability_foundation_artifact_composition(self) -> None:
        foundation = RuntimeFoundation()
        descriptor = RuntimeContextDescriptor(
            context_identifier="context:runtime-foundation",
            artifact_object_type="RuntimeFoundation",
        )

        self.assertTrue(validate_runtime_registry_artifact_composition(foundation, descriptor).is_valid)

    def test_interoperability_boundary_artifact_composition(self) -> None:
        boundary = build_boundary_model()
        descriptor = RuntimeContextDescriptor(
            context_identifier="context:runtime-boundary",
            artifact_object_type="RuntimeBoundaryModel",
        )

        self.assertTrue(validate_runtime_registry_artifact_composition(boundary, descriptor).is_valid)

    def test_interoperability_lifecycle_artifact_composition(self) -> None:
        lifecycle = build_artifact_lifecycle()
        descriptor = RuntimeContextDescriptor(
            context_identifier="context:runtime-lifecycle",
            artifact_object_type="RuntimeArtifactLifecycle",
        )

        self.assertTrue(validate_runtime_registry_artifact_composition(lifecycle, descriptor).is_valid)

    def test_interoperability_classification_artifact_composition(self) -> None:
        classification = build_classification_record()
        descriptor = RuntimeContextDescriptor(
            context_identifier="context:runtime-classification",
            artifact_object_type="CanonicalRuntimeContextClassification",
        )

        self.assertTrue(
            validate_runtime_registry_artifact_composition(classification, descriptor).is_valid
        )

    def test_no_cognitive_foundation_imports_in_registry_modules(self) -> None:
        import packages.runtime.registry.contract as contract_module
        import packages.runtime.registry.registry as registry_module

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
