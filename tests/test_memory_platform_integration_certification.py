import json
import unittest
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
    MemoryMetadata,
    MemoryOrigin,
    MemoryProvenance,
    MemoryReferenceStore,
    MemoryRetrievalCriteria,
    MemoryRetrievalRequest,
    MemoryRetrievalResponse,
    MemorySource,
    MemoryType,
    ProvenanceMetadata,
    ProvenanceReference,
    RetrievalMetadata,
    RetrievalStatus,
    UniversalMemory,
    validate_index_contract,
    validate_retrieval_request,
    validate_retrieval_response,
)
from packages.objects import CanonicalObject, LifecycleState, ObjectSerializer


TIMESTAMP = datetime.fromisoformat("2026-07-03T00:00:00+00:00")


def build_certified_memory(
    memory_id: str = "00000000-0000-0000-0000-000000000011",
) -> UniversalMemory:
    source = MemorySource(
        source_type="document",
        source_identifier="GAR-SPRINT-0003-GOLF",
        source_label="Mission Golf",
        source_metadata={"b": 2, "a": 1},
    )
    provenance = MemoryProvenance(
        source=source,
        recorded_at=TIMESTAMP,
        recorded_by="codex",
        trace_metadata={"z": "last", "a": "first"},
        provenance_metadata=ProvenanceMetadata(
            acquisition_timestamp=TIMESTAMP,
            origin=MemoryOrigin.HUMAN,
            acquisition_method=AcquisitionMethod.MANUAL_ENTRY,
            acquisition_channel=AcquisitionChannel.DOCUMENT,
            references=(
                ProvenanceReference(
                    reference_type="document",
                    reference_identifier="GAR-SPRINT-0003-GOLF",
                    reference_label="Mission Golf plan",
                ),
            ),
        ),
    )
    return UniversalMemory(
        object_id=UUID(memory_id),
        memory_type=MemoryType.SEMANTIC,
        content={"statement": "Memory Foundation certification."},
        source=source,
        provenance=provenance,
        confidence=MemoryConfidence.HIGH,
        memory_metadata=MemoryMetadata(values={"z": "last", "a": "first"}),
        metadata={"owner": "platform", "mission": "golf"},
        tags=["memory", "certification"],
        lifecycle_state=LifecycleState.ACTIVE,
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


class MemoryPlatformIntegrationCertificationTest(unittest.TestCase):
    def test_scenario_1_universal_memory_baseline_certification(self) -> None:
        memory = build_certified_memory()

        payload = memory.to_dict()
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))

        self.assertIsInstance(memory, CanonicalObject)
        self.assertTrue(memory.validate().is_valid)
        self.assertEqual(payload, build_certified_memory().to_dict())
        self.assertEqual(encoded, json.dumps(payload, sort_keys=True, separators=(",", ":")))
        self.assertEqual(ObjectSerializer.serialize(memory)["object_type"], "UniversalMemory")

    def test_scenario_2_source_provenance_confidence_certification(self) -> None:
        memory = build_certified_memory()
        payload = memory.to_dict()

        self.assertTrue(memory.validate().is_valid)
        self.assertEqual(payload["source"]["source_metadata"], {"a": 1, "b": 2})
        self.assertEqual(payload["confidence"], "high")
        self.assertEqual(payload["memory_metadata"], {"a": "first", "z": "last"})
        self.assertEqual(payload["provenance"]["trace_metadata"], {"a": "first", "z": "last"})
        self.assertEqual(
            payload["provenance"]["provenance_metadata"]["references"][0],
            {
                "reference_type": "document",
                "reference_identifier": "GAR-SPRINT-0003-GOLF",
                "reference_label": "Mission Golf plan",
            },
        )

    def test_scenario_3_memory_index_contract_certification(self) -> None:
        descriptor = MemoryIndexDescriptor(
            memory_id="00000000-0000-0000-0000-000000000011",
            memory_type="semantic",
            origin="human",
            acquisition_method="manual_entry",
            acquisition_channel="document",
            lifecycle_state="active",
            confidence="high",
            created_at=TIMESTAMP.isoformat(),
        )
        contract = IndexContract(
            metadata=IndexMetadata(),
            fields=(
                IndexField("memory_id", IndexFieldType.UUID),
                IndexField("memory_type", IndexFieldType.ENUM),
                IndexField("confidence", IndexFieldType.ENUM),
            ),
        )

        self.assertTrue(validate_index_contract(contract).is_valid)
        self.assertEqual(descriptor.to_dict()["memory_id"], str(UUID(int=17)))
        self.assertEqual(contract.to_dict(), contract.to_dict())
        self.assert_no_behavior(contract, {"index", "search", "query", "retrieve"})

    def test_scenario_4_memory_retrieval_contract_certification(self) -> None:
        criteria = MemoryRetrievalCriteria(
            memory_types=[MemoryType.SEMANTIC],
            origins=[MemoryOrigin.HUMAN],
            acquisition_methods=[AcquisitionMethod.MANUAL_ENTRY],
            acquisition_channels=[AcquisitionChannel.DOCUMENT],
            confidence=MemoryConfidence.HIGH,
            lifecycle_states=[LifecycleState.ACTIVE],
        )
        request = MemoryRetrievalRequest(
            request_id="request-golf-001",
            criteria=criteria,
            metadata=RetrievalMetadata(request_timestamp=TIMESTAMP),
        )
        response = MemoryRetrievalResponse(
            request_id=request.request_id,
            metadata=RetrievalMetadata(
                request_timestamp=TIMESTAMP,
                response_timestamp=TIMESTAMP,
            ),
            status=RetrievalStatus.COMPLETED,
            memory_ids=["00000000-0000-0000-0000-000000000011"],
        )

        self.assertTrue(validate_retrieval_request(request).is_valid)
        self.assertTrue(validate_retrieval_response(response).is_valid)
        self.assertEqual(response.memory_ids, ("00000000-0000-0000-0000-000000000011",))
        self.assertNotIn("memories", response.to_dict())
        self.assert_no_behavior(request, {"retrieve", "search", "filter", "rank", "score"})
        self.assert_no_behavior(response, {"resolve", "populate", "query"})

    def test_scenario_5_memory_reference_store_certification(self) -> None:
        store = MemoryReferenceStore()
        memory = build_certified_memory()

        store.add(memory)
        with self.assertRaises(ValueError):
            store.add(memory)

        self.assertEqual(store.get(memory.object_id), memory)
        self.assertEqual(store.identifiers(), (memory.object_id,))
        self.assertEqual(store.statistics().total_references, 1)
        self.assertEqual(store.remove(str(memory.object_id)), memory)
        self.assertIsNone(store.get(memory.object_id))
        store.add(memory)
        store.clear()
        self.assertEqual(store.identifiers(), ())
        self.assertEqual(store.statistics().total_references, 0)
        self.assert_no_behavior(store, {"search", "filter", "rank", "score", "query", "save"})

    def test_scenario_6_end_to_end_memory_foundation_certification(self) -> None:
        memory = build_certified_memory()
        store = MemoryReferenceStore()
        index_contract = IndexContract(
            metadata=IndexMetadata(),
            fields=(IndexField("memory_id", IndexFieldType.UUID),),
        )
        retrieval_response = MemoryRetrievalResponse(
            request_id="request-golf-002",
            metadata=RetrievalMetadata(
                request_timestamp=TIMESTAMP,
                response_timestamp=TIMESTAMP,
            ),
            status=RetrievalStatus.COMPLETED,
            memory_ids=[str(memory.object_id)],
        )

        self.assertTrue(memory.validate().is_valid)
        self.assertEqual(memory.to_dict(), build_certified_memory().to_dict())
        self.assertEqual(ObjectSerializer.serialize(memory)["object_id"], str(memory.object_id))
        self.assertEqual(memory.provenance.source.source_identifier, "GAR-SPRINT-0003-GOLF")
        self.assertTrue(validate_index_contract(index_contract).is_valid)
        self.assertTrue(validate_retrieval_response(retrieval_response).is_valid)

        store.add(memory)
        self.assertEqual(store.get(memory.object_id), memory)
        self.assertEqual(store.remove(memory.object_id), memory)
        self.assertTrue(store.validate().is_valid)
        self.assertEqual(store.statistics().total_references, 0)

    def test_explicit_memory_foundation_boundary_certification(self) -> None:
        store = MemoryReferenceStore()
        request = MemoryRetrievalRequest(
            request_id="request-golf-003",
            criteria=MemoryRetrievalCriteria(),
        )
        response = MemoryRetrievalResponse(
            request_id="request-golf-003",
            metadata=RetrievalMetadata(),
            memory_ids=["00000000-0000-0000-0000-000000000011"],
        )
        contract = IndexContract(metadata=IndexMetadata(), fields=())

        self.assert_no_behavior(contract, {"index", "search", "query", "retrieve"})
        self.assert_no_behavior(request, {"retrieve", "search", "filter", "rank", "score"})
        self.assert_no_behavior(response, {"resolve", "populate", "query"})
        self.assert_no_behavior(store, {"persist", "save", "load", "cache"})
        self.assertEqual(response.memory_ids, ("00000000-0000-0000-0000-000000000011",))

    def assert_no_behavior(self, obj: object, forbidden_names: set[str]) -> None:
        self.assertTrue(forbidden_names.isdisjoint(set(dir(obj))))


if __name__ == "__main__":
    unittest.main()
