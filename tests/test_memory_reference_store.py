import unittest
from datetime import datetime
from uuid import UUID

from packages.memory import (
    IndexContract,
    IndexField,
    IndexFieldType,
    IndexMetadata,
    MemoryReferenceStore,
    MemoryRetrievalResponse,
    MemorySource,
    MemoryType,
    RetrievalMetadata,
    RetrievalStatus,
    StoreStatistics,
    UniversalMemory,
    validate_index_contract,
    validate_memory_reference,
    validate_reference_store,
    validate_retrieval_response,
)
from packages.objects import ObjectSerializer


def build_memory(memory_id: str = "00000000-0000-0000-0000-000000000007") -> UniversalMemory:
    timestamp = datetime.fromisoformat("2026-07-03T00:00:00+00:00")
    return UniversalMemory(
        object_id=UUID(memory_id),
        memory_type=MemoryType.SEMANTIC,
        content="Reference store keeps process-local memory references.",
        source=MemorySource(source_type="unit-test"),
        created_at=timestamp,
        updated_at=timestamp,
    )


class MemoryReferenceStoreTest(unittest.TestCase):
    def test_create_store_with_empty_statistics(self) -> None:
        store = MemoryReferenceStore()

        stats = store.statistics()

        self.assertIsInstance(stats, StoreStatistics)
        self.assertEqual(stats.total_references, 0)
        self.assertEqual(store.identifiers(), ())

    def test_add_memory_reference_and_retrieve_by_exact_identifier(self) -> None:
        store = MemoryReferenceStore()
        memory = build_memory()

        store.add(memory)

        self.assertEqual(store.get(memory.object_id), memory)
        self.assertEqual(store.get(str(memory.object_id)), memory)
        self.assertEqual(store.identifiers(), (memory.object_id,))

    def test_reject_duplicate_identifier(self) -> None:
        store = MemoryReferenceStore()
        first = build_memory()
        second = build_memory()

        store.add(first)

        with self.assertRaises(ValueError):
            store.add(second)

    def test_remove_reference_by_exact_identifier(self) -> None:
        store = MemoryReferenceStore()
        memory = build_memory()
        store.add(memory)

        removed = store.remove(str(memory.object_id))

        self.assertEqual(removed, memory)
        self.assertIsNone(store.get(memory.object_id))
        self.assertEqual(store.identifiers(), ())

    def test_missing_identifier_returns_none(self) -> None:
        store = MemoryReferenceStore()

        self.assertIsNone(store.get("00000000-0000-0000-0000-000000000099"))
        self.assertIsNone(store.remove("00000000-0000-0000-0000-000000000099"))

    def test_enumerate_identifiers_is_deterministic(self) -> None:
        store = MemoryReferenceStore()
        second = build_memory("00000000-0000-0000-0000-000000000009")
        first = build_memory("00000000-0000-0000-0000-000000000008")

        store.add(second)
        store.add(first)

        self.assertEqual(store.identifiers(), (first.object_id, second.object_id))

    def test_clear_store_removes_all_references(self) -> None:
        store = MemoryReferenceStore()
        store.add(build_memory())

        store.clear()

        self.assertEqual(store.identifiers(), ())
        self.assertEqual(store.statistics().total_references, 0)

    def test_reject_non_universal_memory_reference(self) -> None:
        result = validate_memory_reference(object())

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "memory")

    def test_store_validation_uses_platform_validation_result(self) -> None:
        store = MemoryReferenceStore()
        memory = build_memory()
        store.add(memory)

        result = validate_reference_store(store)

        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_store_validation_reports_identity_mismatch(self) -> None:
        store = MemoryReferenceStore()
        memory = build_memory()
        store._references[UUID("00000000-0000-0000-0000-000000000010")] = memory

        result = store.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "memory_reference_identity_mismatch")

    def test_store_statistics_are_informational_and_deterministic(self) -> None:
        store = MemoryReferenceStore()
        memory = build_memory()

        before = store.statistics()
        store.add(memory)
        after = store.statistics()

        self.assertEqual(before.total_references, 0)
        self.assertEqual(after.total_references, 1)
        self.assertIn("created_at", after.to_dict())
        self.assertIn("last_modified_at", after.to_dict())

    def test_index_contract_compatibility_without_indexing_behavior(self) -> None:
        contract = IndexContract(
            metadata=IndexMetadata(),
            fields=(IndexField("memory_id", IndexFieldType.UUID),),
        )
        store = MemoryReferenceStore()
        memory = build_memory()
        store.add(memory)

        self.assertTrue(validate_index_contract(contract).is_valid)
        self.assertEqual(store.identifiers(), (memory.object_id,))

    def test_retrieval_contract_compatibility_with_opaque_identifiers_only(self) -> None:
        store = MemoryReferenceStore()
        memory = build_memory()
        store.add(memory)
        response = MemoryRetrievalResponse(
            request_id="request-001",
            metadata=RetrievalMetadata(),
            status=RetrievalStatus.COMPLETED,
            memory_ids=[str(memory_id) for memory_id in store.identifiers()],
        )

        self.assertTrue(validate_retrieval_response(response).is_valid)
        self.assertEqual(response.memory_ids, (str(memory.object_id),))

    def test_platform_core_serialization_compatibility_is_preserved(self) -> None:
        memory = build_memory()
        store = MemoryReferenceStore()
        store.add(memory)

        payload = ObjectSerializer.serialize(store.get(memory.object_id))

        self.assertEqual(payload["object_type"], "UniversalMemory")
        self.assertEqual(payload["object_id"], str(memory.object_id))

    def test_store_exposes_no_search_query_or_persistence_behavior(self) -> None:
        store = MemoryReferenceStore()
        forbidden_names = {
            "search",
            "filter",
            "rank",
            "score",
            "query",
            "persist",
            "save",
            "load",
            "cache",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(store))))


if __name__ == "__main__":
    unittest.main()
