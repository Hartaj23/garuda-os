import unittest
from datetime import datetime
from uuid import UUID

from packages.memory import (
    MemoryConfidence,
    MemoryMetadata,
    MemoryProvenance,
    MemorySource,
    MemoryType,
    UniversalMemory,
)
from packages.objects import CanonicalObject, LifecycleState


class UniversalMemoryFrameworkTest(unittest.TestCase):
    def test_universal_memory_inherits_platform_core_object_behavior(self) -> None:
        memory = UniversalMemory(
            memory_type=MemoryType.EPISODIC,
            content="Mission Alpha approved.",
            source=MemorySource(source_type="document"),
            metadata={"owner": "platform"},
            tags=["memory", "alpha"],
            created_by="codex",
        )

        self.assertIsInstance(memory, CanonicalObject)
        self.assertIsInstance(memory.object_id, UUID)
        self.assertEqual(memory.object_type, "UniversalMemory")
        self.assertEqual(memory.metadata.values["owner"], "platform")
        self.assertEqual(memory.tags, ("memory", "alpha"))
        self.assertEqual(memory.lifecycle_state, LifecycleState.DRAFT)
        self.assertEqual(memory.created_by, "codex")

    def test_memory_primitives_are_available(self) -> None:
        source = MemorySource(
            source_type="manual-entry",
            source_identifier="GAR-SPRINT-0003",
            source_label="Sprint 3 Mission Alpha",
            source_metadata={"channel": "codex"},
        )
        recorded_at = datetime.fromisoformat("2026-07-03T00:00:00+00:00")
        provenance = MemoryProvenance(
            source=source,
            recorded_at=recorded_at,
            recorded_by="hartaj",
            trace_metadata={"review": "approved"},
        )
        metadata = MemoryMetadata(values={"domain": "platform"})

        memory = UniversalMemory(
            memory_type=MemoryType.SEMANTIC,
            content={"statement": "Memory confidence records certainty."},
            source=source,
            provenance=provenance,
            confidence=MemoryConfidence.HIGH,
            memory_metadata=metadata,
        )

        self.assertEqual(memory.memory_type, MemoryType.SEMANTIC)
        self.assertEqual(memory.source, source)
        self.assertEqual(memory.provenance, provenance)
        self.assertEqual(memory.confidence, MemoryConfidence.HIGH)
        self.assertEqual(memory.memory_metadata.values["domain"], "platform")

    def test_valid_memory_passes_platform_validation(self) -> None:
        memory = UniversalMemory(
            memory_type=MemoryType.DECLARATIVE,
            content="Universal Memory is a platform object.",
            source=MemorySource(source_type="unit-test"),
            confidence=MemoryConfidence.MEDIUM,
        )

        result = memory.validate()

        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_memory_validation_reports_invalid_memory_type(self) -> None:
        memory = UniversalMemory(
            memory_type=MemoryType.PROCEDURAL,
            content="Validate invalid memory type.",
            source=MemorySource(source_type="unit-test"),
        )
        memory._memory_type = "procedural"

        result = memory.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "memory_type")

    def test_memory_validation_reports_missing_content(self) -> None:
        memory = UniversalMemory(
            memory_type=MemoryType.EPISODIC,
            content=None,
            source=MemorySource(source_type="unit-test"),
        )

        result = memory.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "content")

    def test_memory_validation_reports_empty_source_type(self) -> None:
        memory = UniversalMemory(
            memory_type=MemoryType.EPISODIC,
            content="Validate source type.",
            source=MemorySource(source_type=""),
        )

        result = memory.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "source.source_type")

    def test_memory_validation_reports_invalid_confidence(self) -> None:
        memory = UniversalMemory(
            memory_type=MemoryType.EPISODIC,
            content="Validate confidence.",
            source=MemorySource(source_type="unit-test"),
        )
        memory._confidence = "high"

        result = memory.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "confidence")

    def test_memory_validation_reports_invalid_provenance(self) -> None:
        memory = UniversalMemory(
            memory_type=MemoryType.EPISODIC,
            content="Validate provenance.",
            source=MemorySource(source_type="unit-test"),
        )
        memory._provenance = "manual"

        result = memory.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "provenance")

    def test_memory_validation_reports_invalid_memory_metadata(self) -> None:
        memory = UniversalMemory(
            memory_type=MemoryType.EPISODIC,
            content="Validate memory metadata.",
            source=MemorySource(source_type="unit-test"),
        )
        memory._memory_metadata = {"domain": "platform"}

        result = memory.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "memory_metadata")

    def test_memory_lifecycle_transitions_use_existing_platform_rules(self) -> None:
        memory = UniversalMemory(
            memory_type=MemoryType.PROCEDURAL,
            content="Use inherited lifecycle transitions.",
            source=MemorySource(source_type="unit-test"),
        )

        memory.transition_to(LifecycleState.ACTIVE)

        self.assertEqual(memory.lifecycle_state, LifecycleState.ACTIVE)

    def test_to_dict_returns_deterministic_memory_payload(self) -> None:
        source = MemorySource(
            source_type="document",
            source_identifier="GAR-SPRINT-0003",
            source_metadata={"b": 2, "a": 1},
        )
        memory = UniversalMemory(
            memory_type=MemoryType.SEMANTIC,
            content="Deterministic payload support.",
            source=source,
            memory_metadata=MemoryMetadata(values={"z": "last", "a": "first"}),
        )

        payload = memory.to_dict()

        self.assertEqual(payload["object_type"], "UniversalMemory")
        self.assertEqual(payload["memory_type"], "semantic")
        self.assertEqual(payload["source"]["source_metadata"], {"a": 1, "b": 2})
        self.assertEqual(payload["memory_metadata"], {"a": "first", "z": "last"})
        self.assertNotIn("storage", payload)
        self.assertNotIn("retrieval", payload)


if __name__ == "__main__":
    unittest.main()
