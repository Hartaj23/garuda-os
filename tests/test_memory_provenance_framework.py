import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime

from packages.memory import (
    AcquisitionChannel,
    AcquisitionMethod,
    MemoryOrigin,
    MemoryProvenance,
    MemorySource,
    MemoryType,
    ProvenanceMetadata,
    ProvenanceReference,
    UniversalMemory,
)
from packages.memory.core import validate_provenance_metadata
from packages.objects import CanonicalObject


class MemoryProvenanceFrameworkTest(unittest.TestCase):
    def test_memory_origin_values_and_default(self) -> None:
        self.assertEqual(
            {origin.value for origin in MemoryOrigin},
            {
                "human",
                "ai",
                "system",
                "imported",
                "external_service",
                "sensor",
                "unknown",
            },
        )
        self.assertEqual(ProvenanceMetadata().origin, MemoryOrigin.UNKNOWN)

    def test_acquisition_method_values_and_serialization(self) -> None:
        metadata = ProvenanceMetadata(
            acquisition_method=AcquisitionMethod.FILE_IMPORT,
        )

        self.assertEqual(
            {method.value for method in AcquisitionMethod},
            {
                "conversation",
                "observation",
                "import",
                "api",
                "manual_entry",
                "system_event",
                "file_import",
            },
        )
        self.assertEqual(metadata.to_dict()["acquisition_method"], "file_import")

    def test_acquisition_channel_values_and_deterministic_representation(self) -> None:
        metadata = ProvenanceMetadata(
            acquisition_channel=AcquisitionChannel.DOCUMENT,
        )

        self.assertEqual(
            {channel.value for channel in AcquisitionChannel},
            {
                "chat",
                "voice",
                "document",
                "api",
                "email",
                "sensor",
                "internal_platform",
            },
        )
        self.assertEqual(metadata.to_dict()["acquisition_channel"], "document")

    def test_provenance_reference_is_opaque_identifier_model(self) -> None:
        reference = ProvenanceReference(
            reference_type="document",
            reference_identifier="GAR-SPRINT-0003-BRAVO",
            reference_label="Mission Bravo plan",
        )

        self.assertEqual(
            reference.to_dict(),
            {
                "reference_type": "document",
                "reference_identifier": "GAR-SPRINT-0003-BRAVO",
                "reference_label": "Mission Bravo plan",
            },
        )
        self.assertNotIn("url", reference.to_dict())
        self.assertNotIn("lookup", reference.to_dict())
        self.assertNotIn("storage", reference.to_dict())

    def test_provenance_metadata_is_immutable_and_stores_references_as_tuple(self) -> None:
        metadata = ProvenanceMetadata(
            acquisition_timestamp=datetime.fromisoformat("2026-07-03T00:00:00+00:00"),
            origin=MemoryOrigin.HUMAN,
            acquisition_method=AcquisitionMethod.CONVERSATION,
            acquisition_channel=AcquisitionChannel.CHAT,
            references=[
                ProvenanceReference(
                    reference_type="conversation",
                    reference_identifier="conv-001",
                )
            ],
        )

        self.assertIsInstance(metadata.references, tuple)
        with self.assertRaises(FrozenInstanceError):
            metadata.origin = MemoryOrigin.AI

    def test_provenance_metadata_validates_required_fields(self) -> None:
        metadata = ProvenanceMetadata(
            origin=MemoryOrigin.SYSTEM,
            acquisition_method=AcquisitionMethod.SYSTEM_EVENT,
            acquisition_channel=AcquisitionChannel.INTERNAL_PLATFORM,
        )

        result = validate_provenance_metadata(metadata)

        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_invalid_provenance_reference_is_reported_by_validation(self) -> None:
        metadata = ProvenanceMetadata(
            references=[
                ProvenanceReference(
                    reference_type="document",
                    reference_identifier="",
                )
            ],
        )

        result = validate_provenance_metadata(metadata)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            result.errors[0].field,
            "provenance.provenance_metadata.references[0].reference_identifier",
        )

    def test_universal_memory_accepts_strengthened_provenance(self) -> None:
        source = MemorySource(
            source_type="document",
            source_identifier="GAR-SPRINT-0003-BRAVO",
        )
        provenance_metadata = ProvenanceMetadata(
            acquisition_timestamp=datetime.fromisoformat("2026-07-03T00:00:00+00:00"),
            origin=MemoryOrigin.HUMAN,
            acquisition_method=AcquisitionMethod.MANUAL_ENTRY,
            acquisition_channel=AcquisitionChannel.DOCUMENT,
            references=[
                ProvenanceReference(
                    reference_type="document",
                    reference_identifier="GAR-SPRINT-0003-BRAVO",
                )
            ],
        )
        provenance = MemoryProvenance(
            source=source,
            recorded_at=datetime.fromisoformat("2026-07-03T00:00:00+00:00"),
            recorded_by="hartaj",
            provenance_metadata=provenance_metadata,
        )

        memory = UniversalMemory(
            memory_type=MemoryType.SEMANTIC,
            content="Mission Bravo strengthens provenance.",
            source=source,
            provenance=provenance,
        )

        self.assertIsInstance(memory, CanonicalObject)
        self.assertEqual(memory.provenance.provenance_metadata, provenance_metadata)
        self.assertTrue(memory.validate().is_valid)

    def test_universal_memory_alpha_construction_still_defaults_provenance(self) -> None:
        source = MemorySource(source_type="unit-test")

        memory = UniversalMemory(
            memory_type=MemoryType.EPISODIC,
            content="Mission Alpha constructor remains valid.",
            source=source,
        )

        payload = memory.to_dict()

        self.assertTrue(memory.validate().is_valid)
        self.assertEqual(payload["source"]["source_type"], "unit-test")
        self.assertEqual(payload["provenance"]["source"]["source_type"], "unit-test")
        self.assertEqual(
            payload["provenance"]["provenance_metadata"]["origin"],
            "unknown",
        )
        self.assertEqual(
            payload["provenance"]["provenance_metadata"]["acquisition_method"],
            "manual_entry",
        )

    def test_deterministic_payload_includes_provenance_metadata(self) -> None:
        source = MemorySource(
            source_type="document",
            source_metadata={"b": 2, "a": 1},
        )
        provenance = MemoryProvenance(
            source=source,
            recorded_at=datetime.fromisoformat("2026-07-03T00:00:00+00:00"),
            trace_metadata={"z": "last", "a": "first"},
            provenance_metadata=ProvenanceMetadata(
                acquisition_timestamp=datetime.fromisoformat("2026-07-03T00:00:00+00:00"),
                origin=MemoryOrigin.IMPORTED,
                acquisition_method=AcquisitionMethod.IMPORT,
                acquisition_channel=AcquisitionChannel.DOCUMENT,
                references=(
                    ProvenanceReference(
                        reference_type="document",
                        reference_identifier="doc-001",
                    ),
                ),
            ),
        )
        memory = UniversalMemory(
            memory_type=MemoryType.DECLARATIVE,
            content="Deterministic provenance payload.",
            source=source,
            provenance=provenance,
        )

        payload = memory.to_dict()

        self.assertEqual(payload["source"]["source_metadata"], {"a": 1, "b": 2})
        self.assertEqual(payload["provenance"]["trace_metadata"], {"a": "first", "z": "last"})
        self.assertEqual(
            payload["provenance"]["provenance_metadata"],
            {
                "acquisition_timestamp": "2026-07-03T00:00:00+00:00",
                "origin": "imported",
                "acquisition_method": "import",
                "acquisition_channel": "document",
                "references": [
                    {
                        "reference_type": "document",
                        "reference_identifier": "doc-001",
                        "reference_label": None,
                    }
                ],
            },
        )


if __name__ == "__main__":
    unittest.main()
