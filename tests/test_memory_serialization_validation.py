import json
import unittest
from datetime import datetime
from uuid import UUID

from packages.memory import (
    AcquisitionChannel,
    AcquisitionMethod,
    MemoryConfidence,
    MemoryMetadata,
    MemoryOrigin,
    MemoryProvenance,
    MemorySource,
    MemoryType,
    ProvenanceMetadata,
    ProvenanceReference,
    UniversalMemory,
)
from packages.objects import (
    CanonicalObject,
    LifecycleState,
    ObjectRegistry,
    ObjectSerializer,
    Relationship,
    ValidationCategory,
    ValidationError,
)


def build_memory() -> UniversalMemory:
    created_at = datetime.fromisoformat("2026-07-03T00:00:00+00:00")
    source = MemorySource(
        source_type="document",
        source_identifier="GAR-SPRINT-0003-CHARLIE",
        source_label="Mission Charlie",
        source_metadata={"b": 2, "a": 1},
    )
    provenance = MemoryProvenance(
        source=source,
        recorded_at=created_at,
        recorded_by="codex",
        trace_metadata={"z": "last", "a": "first"},
        provenance_metadata=ProvenanceMetadata(
            acquisition_timestamp=created_at,
            origin=MemoryOrigin.HUMAN,
            acquisition_method=AcquisitionMethod.MANUAL_ENTRY,
            acquisition_channel=AcquisitionChannel.DOCUMENT,
            references=(
                ProvenanceReference(
                    reference_type="document",
                    reference_identifier="GAR-SPRINT-0003-CHARLIE",
                    reference_label="Mission Charlie plan",
                ),
            ),
        ),
    )
    return UniversalMemory(
        object_id=UUID("00000000-0000-0000-0000-000000000003"),
        memory_type=MemoryType.SEMANTIC,
        content={"statement": "Memory payloads are deterministic."},
        source=source,
        provenance=provenance,
        confidence=MemoryConfidence.HIGH,
        memory_metadata=MemoryMetadata(values={"z": "last", "a": "first"}),
        metadata={"owner": "platform", "mission": "charlie"},
        tags=["memory", "serialization"],
        lifecycle_state=LifecycleState.ACTIVE,
        created_by="codex",
        updated_by="codex",
        created_at=created_at,
        updated_at=created_at,
    )


class MemorySerializationValidationTest(unittest.TestCase):
    def test_universal_memory_payload_is_deterministic_and_stable(self) -> None:
        first = build_memory().to_dict()
        second = build_memory().to_dict()

        self.assertEqual(first, second)
        self.assertEqual(
            list(first.keys()),
            [
                "schema_version",
                "object_version",
                "object_type",
                "object_id",
                "metadata",
                "tags",
                "lifecycle_state",
                "created_by",
                "updated_by",
                "created_at",
                "updated_at",
                "memory_type",
                "content",
                "source",
                "provenance",
                "confidence",
                "memory_metadata",
            ],
        )

    def test_payload_preserves_metadata_provenance_confidence_and_audit_fields(self) -> None:
        payload = build_memory().to_dict()

        self.assertEqual(payload["metadata"], {"mission": "charlie", "owner": "platform"})
        self.assertEqual(payload["tags"], ["memory", "serialization"])
        self.assertEqual(payload["lifecycle_state"], "active")
        self.assertEqual(payload["created_by"], "codex")
        self.assertEqual(payload["updated_by"], "codex")
        self.assertEqual(payload["confidence"], "high")
        self.assertEqual(payload["memory_metadata"], {"a": "first", "z": "last"})
        self.assertEqual(payload["source"]["source_metadata"], {"a": 1, "b": 2})
        self.assertEqual(payload["provenance"]["trace_metadata"], {"a": "first", "z": "last"})
        self.assertEqual(
            payload["provenance"]["provenance_metadata"]["references"],
            [
                {
                    "reference_type": "document",
                    "reference_identifier": "GAR-SPRINT-0003-CHARLIE",
                    "reference_label": "Mission Charlie plan",
                }
            ],
        )

    def test_memory_payload_supports_stable_json_encoding(self) -> None:
        first_json = json.dumps(build_memory().to_dict(), sort_keys=True, separators=(",", ":"))
        second_json = json.dumps(build_memory().to_dict(), sort_keys=True, separators=(",", ":"))

        self.assertEqual(first_json, second_json)

    def test_platform_core_serializer_handles_inherited_object_contract(self) -> None:
        memory = build_memory()
        payload = ObjectSerializer.serialize(memory)

        self.assertEqual(payload["object_type"], "UniversalMemory")
        self.assertEqual(payload["object_id"], "00000000-0000-0000-0000-000000000003")
        self.assertEqual(payload["metadata"], {"mission": "charlie", "owner": "platform"})
        self.assertEqual(payload["tags"], ["memory", "serialization"])
        self.assertEqual(payload["lifecycle_state"], "active")
        self.assertNotIn("memory_type", payload)
        self.assertNotIn("provenance", payload)

    def test_platform_core_deserializer_reconstructs_core_fields_only(self) -> None:
        payload = ObjectSerializer.serialize(build_memory())
        restored = ObjectSerializer.deserialize(payload)

        self.assertEqual(restored.object_id, UUID("00000000-0000-0000-0000-000000000003"))
        self.assertEqual(restored.object_type, "UniversalMemory")
        self.assertEqual(restored.metadata.values, {"mission": "charlie", "owner": "platform"})
        self.assertEqual(restored.tags, ("memory", "serialization"))
        self.assertEqual(restored.lifecycle_state, LifecycleState.ACTIVE)
        self.assertFalse(hasattr(restored, "memory_type"))

    def test_platform_core_validation_and_memory_validation_both_execute(self) -> None:
        memory = build_memory()
        memory.schema_version = ""
        memory._confidence = "high"

        result = memory.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {"schema_version", "confidence"},
        )
        self.assertIn(ValidationCategory.SCHEMA, {error.category for error in result.errors})
        self.assertIn(ValidationCategory.METADATA, {error.category for error in result.errors})

    def test_validation_result_merges_existing_hooks_with_memory_validation(self) -> None:
        memory = build_memory()

        def hook(obj: UniversalMemory) -> ValidationError:
            return ValidationError(
                message=f"{obj.object_type} custom validation failed.",
                category=ValidationCategory.BEHAVIOR,
                field="custom",
            )

        memory.register_validation_hook(hook)
        result = memory.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "custom")

    def test_successful_memory_validation_uses_existing_validation_contract(self) -> None:
        result = build_memory().validate()

        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_registry_accepts_universal_memory_as_canonical_object(self) -> None:
        registry = ObjectRegistry()
        registry.register(UniversalMemory)

        self.assertEqual(registry.lookup("UniversalMemory"), UniversalMemory)
        self.assertEqual(registry.lookup_by_class(UniversalMemory), UniversalMemory)
        registry.validate()

    def test_lifecycle_and_relationship_interoperability_are_preserved(self) -> None:
        memory = UniversalMemory(
            memory_type=MemoryType.EPISODIC,
            content="Lifecycle and relationships remain Platform Core concepts.",
            source=MemorySource(source_type="unit-test"),
        )
        target = build_memory()

        memory.transition_to(LifecycleState.ACTIVE)
        relationship = Relationship(
            source_object_id=memory.object_id,
            target_object_id=target.object_id,
            metadata={"purpose": "serialization-validation"},
        )

        self.assertIsInstance(memory, CanonicalObject)
        self.assertEqual(memory.lifecycle_state, LifecycleState.ACTIVE)
        self.assertEqual(relationship.source_object_id, memory.object_id)
        self.assertEqual(relationship.target_object_id, target.object_id)
        self.assertEqual(
            relationship.to_dict()["metadata"],
            {"purpose": "serialization-validation"},
        )


if __name__ == "__main__":
    unittest.main()
