import unittest
from datetime import datetime
from uuid import UUID

from packages.interface import (
    CanonicalTranslationContract,
    ExternalRepresentation,
    ExternalRepresentationKind,
    TranslationDescriptor,
    TranslationDirection,
    TranslationMetadata,
    TranslationReversibilityDescriptor,
    normalize_to_canonical_payload,
)
from packages.objects import CanonicalObject, ObjectSerializer


TIMESTAMP = datetime.fromisoformat("2026-07-06T00:00:00+00:00")


def build_external_representation() -> ExternalRepresentation:
    return ExternalRepresentation(
        representation_kind=ExternalRepresentationKind.STRUCTURED,
        representation_identifier="external:00000000-0000-0000-0000-000000004001",
        representation_values={"z": "last", "a": "first", "meaning": "preserve"},
        representation_metadata=TranslationMetadata(values={"source": "delta"}),
    )


def build_translation_contract() -> CanonicalTranslationContract:
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
        object_id=UUID("00000000-0000-0000-0000-000000004002"),
        translation_descriptor=descriptor,
        source_representation=source,
        canonical_payload=canonical_payload,
        translation_metadata=TranslationMetadata(values={"mission": "delta"}),
        metadata={"owner": "interface"},
        tags=["interface", "delta"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


class InterfaceTranslationTest(unittest.TestCase):
    def test_golf_scenario_8_translation_determinism(self) -> None:
        source = build_external_representation()

        first = normalize_to_canonical_payload(source)
        second = normalize_to_canonical_payload(source)

        self.assertEqual(first.to_dict(), second.to_dict())
        self.assertEqual(first.to_dict(), {"a": "first", "meaning": "preserve", "z": "last"})

    def test_golf_scenario_8_identical_output_across_repeated_executions(self) -> None:
        source = build_external_representation()
        outputs = [normalize_to_canonical_payload(source).to_dict() for _ in range(5)]

        self.assertTrue(all(output == outputs[0] for output in outputs))

    def test_golf_scenario_8_canonical_representation_preservation(self) -> None:
        source = build_external_representation()
        payload = normalize_to_canonical_payload(source)

        self.assertEqual(payload.to_dict()["meaning"], "preserve")
        self.assertEqual(dict(source.representation_values), payload.to_dict())

    def test_golf_scenario_7_variability_containment(self) -> None:
        contract = build_translation_contract()
        payload = contract.canonical_payload.to_dict()

        self.assertIn("representation_kind", contract.source_representation.to_dict())
        self.assertNotIn("representation_kind", payload)
        self.assertNotIn("representation_identifier", payload)

    def test_golf_scenario_1_translation_contract_inherits_platform_core(self) -> None:
        contract = build_translation_contract()

        self.assertIsInstance(contract, CanonicalObject)
        self.assertEqual(contract.object_type, "CanonicalTranslationContract")

    def test_golf_scenario_2_canonical_serialization_without_custom_adapters(self) -> None:
        contract = build_translation_contract()

        core_payload = ObjectSerializer.serialize(contract)
        contract_payload = contract.to_dict()

        self.assertEqual(core_payload["object_type"], "CanonicalTranslationContract")
        self.assertEqual(contract_payload["canonical_payload"]["meaning"], "preserve")

    def test_golf_scenario_3_platform_validation_passes(self) -> None:
        self.assertTrue(build_translation_contract().validate().is_valid)

    def test_golf_scenario_5_no_cognitive_foundation_imports_in_translation_modules(self) -> None:
        import packages.interface.translation.contract as contract_module
        import packages.interface.translation.normalizer as normalizer_module
        import packages.interface.translation.representation as representation_module

        forbidden_prefixes = (
            "packages.memory",
            "packages.knowledge",
            "packages.context",
            "packages.reasoning",
            "packages.decision",
            "packages.action",
            "packages.execution",
        )

        for module in (representation_module, normalizer_module, contract_module):
            with open(module.__file__, encoding="utf-8") as module_file:
                source = module_file.read()
            for prefix in forbidden_prefixes:
                self.assertNotIn(prefix, source)

    def test_normalizer_is_pure_without_side_effects(self) -> None:
        source = build_external_representation()
        before = source.to_dict()

        normalize_to_canonical_payload(source)

        self.assertEqual(source.to_dict(), before)

    def test_reversibility_descriptor_is_architectural_only(self) -> None:
        descriptor = TranslationReversibilityDescriptor(
            preservation_complete=True,
            preserved_field_identifiers=("a", "z"),
        )

        self.assertTrue(descriptor.preservation_complete)
        self.assertNotIn("reverse", dir(descriptor))

    def test_translation_direction_supports_inbound_only(self) -> None:
        self.assertEqual(
            list(TranslationDirection),
            [TranslationDirection.INBOUND_TO_CANONICAL],
        )

    def test_translation_contract_rejects_invalid_descriptor_type(self) -> None:
        contract = build_translation_contract()
        contract._translation_descriptor = "invalid"

        result = contract.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "translation_descriptor")

    def test_external_representation_has_no_protocol_semantics(self) -> None:
        source = build_external_representation()
        payload = source.to_dict()

        self.assertEqual(payload["representation_kind"], "structured")
        self.assertNotIn("http", str(payload).lower())
        self.assertNotIn("json", str(payload).lower())


if __name__ == "__main__":
    unittest.main()
