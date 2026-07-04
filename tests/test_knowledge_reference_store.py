import unittest
from datetime import datetime
from uuid import UUID

from packages.knowledge import (
    ClassificationDimension,
    KnowledgeClassificationContract,
    KnowledgeCategory,
    KnowledgeQueryContract,
    KnowledgeReferenceStore,
    KnowledgeType,
    QueryType,
    StoreStatistics,
    UniversalKnowledge,
    validate_knowledge_classification_contract,
    validate_knowledge_query_contract,
    validate_knowledge_reference,
    validate_reference_store,
    validate_store_statistics,
)
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import ObjectSerializer, ValidationResult


def build_knowledge(
    knowledge_id: str = "00000000-0000-0000-0000-000000000801",
) -> UniversalKnowledge:
    timestamp = datetime.fromisoformat("2026-07-04T00:00:00+00:00")
    return UniversalKnowledge(
        object_id=UUID(knowledge_id),
        knowledge_type=KnowledgeType.FACT,
        created_at=timestamp,
        updated_at=timestamp,
    )


class KnowledgeReferenceStoreTest(unittest.TestCase):
    def test_create_store_with_empty_statistics(self) -> None:
        store = KnowledgeReferenceStore()

        stats = store.statistics()

        self.assertIsInstance(stats, StoreStatistics)
        self.assertEqual(stats.total_knowledge_objects, 0)
        self.assertEqual(store.identifiers(), ())

    def test_add_knowledge_and_retrieve_by_exact_identifier(self) -> None:
        store = KnowledgeReferenceStore()
        knowledge = build_knowledge()

        store.add(knowledge)

        self.assertEqual(store.get(knowledge.object_id), knowledge)
        self.assertEqual(store.get(str(knowledge.object_id)), knowledge)
        self.assertEqual(store.identifiers(), (knowledge.object_id,))

    def test_reject_duplicate_identifier(self) -> None:
        store = KnowledgeReferenceStore()
        first = build_knowledge()
        second = build_knowledge()

        store.add(first)

        with self.assertRaises(ValueError):
            store.add(second)

    def test_reject_non_universal_knowledge_reference(self) -> None:
        result = validate_knowledge_reference(object())

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "knowledge")

    def test_add_rejects_non_universal_knowledge_reference(self) -> None:
        store = KnowledgeReferenceStore()

        with self.assertRaises(ValueError):
            store.add(object())

    def test_remove_reference_by_exact_identifier(self) -> None:
        store = KnowledgeReferenceStore()
        knowledge = build_knowledge()
        store.add(knowledge)

        removed = store.remove(str(knowledge.object_id))

        self.assertEqual(removed, knowledge)
        self.assertIsNone(store.get(knowledge.object_id))
        self.assertEqual(store.identifiers(), ())

    def test_missing_identifier_returns_none(self) -> None:
        store = KnowledgeReferenceStore()

        self.assertIsNone(store.get("00000000-0000-0000-0000-000000000899"))
        self.assertIsNone(store.remove("00000000-0000-0000-0000-000000000899"))

    def test_enumerate_identifiers_is_deterministic(self) -> None:
        store = KnowledgeReferenceStore()
        second = build_knowledge("00000000-0000-0000-0000-000000000803")
        first = build_knowledge("00000000-0000-0000-0000-000000000802")

        store.add(second)
        store.add(first)

        self.assertEqual(store.identifiers(), (first.object_id, second.object_id))

    def test_clear_store_removes_all_references(self) -> None:
        store = KnowledgeReferenceStore()
        store.add(build_knowledge())

        store.clear()

        self.assertEqual(store.identifiers(), ())
        self.assertEqual(store.statistics().total_knowledge_objects, 0)

    def test_store_validation_uses_platform_validation_result(self) -> None:
        store = KnowledgeReferenceStore()
        knowledge = build_knowledge()
        store.add(knowledge)

        result = validate_reference_store(store)

        self.assertIsInstance(result, ValidationResult)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_store_validation_reports_identity_mismatch(self) -> None:
        store = KnowledgeReferenceStore()
        knowledge = build_knowledge()
        store._references[UUID("00000000-0000-0000-0000-000000000804")] = knowledge

        result = store.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].code, "knowledge_reference_identity_mismatch")

    def test_store_statistics_are_informational_and_deterministic(self) -> None:
        store = KnowledgeReferenceStore()
        knowledge = build_knowledge()

        before = store.statistics()
        store.add(knowledge)
        after = store.statistics()

        self.assertTrue(validate_store_statistics(after).is_valid)
        self.assertEqual(before.total_knowledge_objects, 0)
        self.assertEqual(after.total_knowledge_objects, 1)
        self.assertEqual(after.to_dict(), after.to_dict())
        self.assertIn("created_at", after.to_dict())
        self.assertIn("last_modified_at", after.to_dict())

    def test_store_statistics_validation_reports_invalid_shape(self) -> None:
        stats = StoreStatistics(
            total_knowledge_objects=0,
            created_at=datetime.fromisoformat("2026-07-04T00:00:00+00:00"),
            last_modified_at=datetime.fromisoformat("2026-07-04T00:00:00+00:00"),
        )
        object.__setattr__(stats, "total_knowledge_objects", -1)

        result = validate_store_statistics(stats)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "statistics.total_knowledge_objects")

    def test_classification_contract_compatibility_without_classification_behavior(self) -> None:
        contract = KnowledgeClassificationContract(
            supported_categories=(KnowledgeCategory.FACTUAL,),
            supported_dimensions=(ClassificationDimension("domain"),),
        )
        store = KnowledgeReferenceStore()
        knowledge = build_knowledge()
        store.add(knowledge)

        self.assertTrue(validate_knowledge_classification_contract(contract).is_valid)
        self.assertEqual(store.identifiers(), (knowledge.object_id,))

    def test_query_contract_compatibility_without_query_execution(self) -> None:
        contract = KnowledgeQueryContract(
            supported_query_types=(QueryType.EXACT_IDENTIFIER,),
            supported_constraint_types=("identifier",),
        )
        store = KnowledgeReferenceStore()
        knowledge = build_knowledge()
        store.add(knowledge)

        self.assertTrue(validate_knowledge_query_contract(contract).is_valid)
        self.assertEqual(store.get(str(knowledge.object_id)), knowledge)

    def test_platform_core_serialization_compatibility_is_preserved(self) -> None:
        knowledge = build_knowledge()
        store = KnowledgeReferenceStore()
        store.add(knowledge)

        payload = ObjectSerializer.serialize(store.get(knowledge.object_id))

        self.assertEqual(payload["object_type"], "UniversalKnowledge")
        self.assertEqual(payload["object_id"], str(knowledge.object_id))

    def test_memory_foundation_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000000805"),
            memory_type=MemoryType.SEMANTIC,
            content="Knowledge reference store coexists with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-foxtrot"),
        )
        store = KnowledgeReferenceStore()
        store.add(build_knowledge())

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(store.validate().is_valid)

    def test_store_exposes_no_search_query_persistence_or_cache_behavior(self) -> None:
        store = KnowledgeReferenceStore()
        forbidden_names = {
            "cache",
            "database",
            "execute",
            "filter",
            "persist",
            "query",
            "rank",
            "retrieve",
            "save",
            "search",
            "semantic_lookup",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(store))))


if __name__ == "__main__":
    unittest.main()
