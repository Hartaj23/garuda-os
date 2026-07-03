import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime
from uuid import UUID

from packages.memory import (
    AcquisitionChannel,
    AcquisitionMethod,
    IndexContract,
    IndexField,
    IndexFieldType,
    IndexMetadata,
    MemoryConfidence,
    MemoryIndexDescriptor,
    MemoryOrigin,
    MemoryProvenance,
    MemorySource,
    MemoryType,
    ProvenanceMetadata,
    UniversalMemory,
    validate_index_contract,
    validate_index_field,
    validate_index_metadata,
)
from packages.objects import ObjectSerializer


def build_memory() -> UniversalMemory:
    created_at = datetime.fromisoformat("2026-07-03T00:00:00+00:00")
    source = MemorySource(source_type="document")
    provenance = MemoryProvenance(
        source=source,
        recorded_at=created_at,
        provenance_metadata=ProvenanceMetadata(
            acquisition_timestamp=created_at,
            origin=MemoryOrigin.HUMAN,
            acquisition_method=AcquisitionMethod.MANUAL_ENTRY,
            acquisition_channel=AcquisitionChannel.DOCUMENT,
        ),
    )
    return UniversalMemory(
        object_id=UUID("00000000-0000-0000-0000-000000000004"),
        memory_type=MemoryType.SEMANTIC,
        content="Index contracts describe memory attributes.",
        source=source,
        provenance=provenance,
        confidence=MemoryConfidence.HIGH,
        created_at=created_at,
        updated_at=created_at,
    )


class MemoryIndexContractTest(unittest.TestCase):
    def test_index_field_constructs_immutable_deterministic_payload(self) -> None:
        field = IndexField("memory_type", IndexFieldType.ENUM)

        self.assertEqual(
            field.to_dict(),
            {
                "field_name": "memory_type",
                "field_type": "enum",
                "indexable": True,
            },
        )
        with self.assertRaises(FrozenInstanceError):
            field.field_name = "confidence"

    def test_supported_index_field_types_are_platform_values(self) -> None:
        self.assertEqual(
            {field_type.value for field_type in IndexFieldType},
            {"string", "uuid", "datetime", "enum", "integer", "boolean"},
        )

    def test_index_field_validation_reports_invalid_definition(self) -> None:
        field = IndexField("", IndexFieldType.STRING)

        result = validate_index_field(field)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "field_name")

    def test_index_metadata_constructs_and_validates_version_compatibility(self) -> None:
        metadata = IndexMetadata(
            schema_version="1.0",
            descriptor_version=1,
            platform_compatibility="garuda-memory-v1",
        )

        result = validate_index_metadata(metadata)

        self.assertTrue(result.is_valid)
        self.assertEqual(metadata.to_dict()["platform_compatibility"], "garuda-memory-v1")

    def test_index_metadata_validation_reports_invalid_version(self) -> None:
        metadata = IndexMetadata(descriptor_version=0)

        result = validate_index_metadata(metadata)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "descriptor_version")

    def test_default_index_contract_describes_approved_fields_only(self) -> None:
        contract = IndexContract(
            metadata=IndexMetadata(),
            fields=(
                IndexField("memory_id", IndexFieldType.UUID),
                IndexField("memory_type", IndexFieldType.ENUM),
                IndexField("origin", IndexFieldType.ENUM),
                IndexField("acquisition_method", IndexFieldType.ENUM),
                IndexField("acquisition_channel", IndexFieldType.ENUM),
                IndexField("lifecycle_state", IndexFieldType.ENUM),
                IndexField("confidence", IndexFieldType.ENUM),
                IndexField("created_at", IndexFieldType.DATETIME),
            ),
        )

        self.assertEqual(
            [field.field_name for field in contract.fields],
            [
                "memory_id",
                "memory_type",
                "origin",
                "acquisition_method",
                "acquisition_channel",
                "lifecycle_state",
                "confidence",
                "created_at",
            ],
        )
        self.assertTrue(validate_index_contract(contract).is_valid)

    def test_index_contract_is_immutable_and_deterministic(self) -> None:
        contract = IndexContract(
            metadata=IndexMetadata(),
            fields=[
                IndexField("memory_id", IndexFieldType.UUID),
                IndexField("created_at", IndexFieldType.DATETIME),
            ],
        )

        self.assertIsInstance(contract.fields, tuple)
        self.assertEqual(
            contract.to_dict(),
            {
                "metadata": {
                    "schema_version": "1.0",
                    "descriptor_version": 1,
                    "platform_compatibility": "garuda-memory-v1",
                },
                "fields": [
                    {
                        "field_name": "memory_id",
                        "field_type": "uuid",
                        "indexable": True,
                    },
                    {
                        "field_name": "created_at",
                        "field_type": "datetime",
                        "indexable": True,
                    },
                ],
            },
        )
        with self.assertRaises(FrozenInstanceError):
            contract.metadata = IndexMetadata(schema_version="2.0")

    def test_index_contract_validation_reports_duplicate_fields(self) -> None:
        contract = IndexContract(
            metadata=IndexMetadata(),
            fields=(
                IndexField("memory_id", IndexFieldType.UUID),
                IndexField("memory_id", IndexFieldType.UUID),
            ),
        )

        result = validate_index_contract(contract)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "fields[1].field_name")

    def test_memory_index_descriptor_is_descriptive_only(self) -> None:
        descriptor = MemoryIndexDescriptor(
            memory_id="00000000-0000-0000-0000-000000000004",
            memory_type="semantic",
            origin="human",
            acquisition_method="manual_entry",
            acquisition_channel="document",
            lifecycle_state="draft",
            confidence="high",
            created_at="2026-07-03T00:00:00+00:00",
        )

        payload = descriptor.to_dict()

        self.assertEqual(payload["memory_type"], "semantic")
        self.assertNotIn("store", payload)
        self.assertNotIn("retrieve", payload)
        self.assertNotIn("search", payload)
        with self.assertRaises(FrozenInstanceError):
            descriptor.confidence = "low"

    def test_memory_descriptor_represents_indexable_attributes(self) -> None:
        memory = build_memory()
        provenance_metadata = memory.provenance.provenance_metadata
        descriptor = MemoryIndexDescriptor(
            memory_id=str(memory.object_id),
            memory_type=memory.memory_type.value,
            origin=provenance_metadata.origin.value,
            acquisition_method=provenance_metadata.acquisition_method.value,
            acquisition_channel=provenance_metadata.acquisition_channel.value,
            lifecycle_state=memory.lifecycle_state.value,
            confidence=memory.confidence.value,
            created_at=memory.created_at.isoformat(),
        )

        self.assertEqual(
            descriptor.to_dict(),
            {
                "memory_id": "00000000-0000-0000-0000-000000000004",
                "memory_type": "semantic",
                "origin": "human",
                "acquisition_method": "manual_entry",
                "acquisition_channel": "document",
                "lifecycle_state": "draft",
                "confidence": "high",
                "created_at": "2026-07-03T00:00:00+00:00",
            },
        )

    def test_platform_serialization_and_validation_remain_compatible(self) -> None:
        memory = build_memory()
        contract = IndexContract(metadata=IndexMetadata(), fields=())

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(validate_index_contract(contract).is_valid)
        self.assertEqual(ObjectSerializer.serialize(memory)["object_type"], "UniversalMemory")

    def test_index_contract_exposes_no_query_or_retrieval_behavior(self) -> None:
        contract = IndexContract(metadata=IndexMetadata(), fields=())
        forbidden_names = {
            "store",
            "retrieve",
            "search",
            "filter",
            "rank",
            "query",
            "resolve",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(contract))))


if __name__ == "__main__":
    unittest.main()
