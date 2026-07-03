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
    MemoryOrigin,
    MemoryRetrievalCriteria,
    MemoryRetrievalRequest,
    MemoryRetrievalResponse,
    MemorySource,
    MemoryType,
    RetrievalMetadata,
    RetrievalStatus,
    UniversalMemory,
    validate_index_contract,
    validate_retrieval_criteria,
    validate_retrieval_metadata,
    validate_retrieval_request,
    validate_retrieval_response,
)
from packages.objects import LifecycleState, ObjectSerializer


class MemoryRetrievalContractTest(unittest.TestCase):
    def test_retrieval_status_values_are_contract_states(self) -> None:
        self.assertEqual(
            {status.value for status in RetrievalStatus},
            {"pending", "completed", "empty", "unsupported", "invalid"},
        )

    def test_retrieval_metadata_is_immutable_and_deterministic(self) -> None:
        request_timestamp = datetime.fromisoformat("2026-07-03T00:00:00+00:00")
        response_timestamp = datetime.fromisoformat("2026-07-03T00:01:00+00:00")
        metadata = RetrievalMetadata(
            contract_version="1.0",
            request_timestamp=request_timestamp,
            response_timestamp=response_timestamp,
            platform_compatibility="garuda-memory-v1",
        )

        self.assertEqual(
            metadata.to_dict(),
            {
                "contract_version": "1.0",
                "request_timestamp": "2026-07-03T00:00:00+00:00",
                "response_timestamp": "2026-07-03T00:01:00+00:00",
                "platform_compatibility": "garuda-memory-v1",
            },
        )
        with self.assertRaises(FrozenInstanceError):
            metadata.contract_version = "2.0"

    def test_retrieval_metadata_validation_reports_invalid_version(self) -> None:
        metadata = RetrievalMetadata(contract_version="")

        result = validate_retrieval_metadata(metadata)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "contract_version")

    def test_retrieval_criteria_are_immutable_and_deterministic(self) -> None:
        criteria = MemoryRetrievalCriteria(
            memory_types=[MemoryType.SEMANTIC],
            origins=[MemoryOrigin.HUMAN],
            acquisition_methods=[AcquisitionMethod.MANUAL_ENTRY],
            acquisition_channels=[AcquisitionChannel.DOCUMENT],
            confidence=MemoryConfidence.HIGH,
            lifecycle_states=[LifecycleState.ACTIVE],
        )

        self.assertIsInstance(criteria.memory_types, tuple)
        self.assertEqual(
            criteria.to_dict(),
            {
                "memory_types": ["semantic"],
                "origins": ["human"],
                "acquisition_methods": ["manual_entry"],
                "acquisition_channels": ["document"],
                "confidence": "high",
                "lifecycle_states": ["active"],
            },
        )
        with self.assertRaises(FrozenInstanceError):
            criteria.confidence = MemoryConfidence.LOW

    def test_retrieval_criteria_validation_reports_invalid_value(self) -> None:
        criteria = MemoryRetrievalCriteria(memory_types=[MemoryType.SEMANTIC])
        object.__setattr__(criteria, "memory_types", ("semantic",))

        result = validate_retrieval_criteria(criteria)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "memory_types[0]")

    def test_retrieval_request_is_intent_only(self) -> None:
        metadata = RetrievalMetadata(
            request_timestamp=datetime.fromisoformat("2026-07-03T00:00:00+00:00"),
        )
        request = MemoryRetrievalRequest(
            request_id="request-001",
            schema_version="1.0",
            criteria=MemoryRetrievalCriteria(memory_types=[MemoryType.EPISODIC]),
            metadata=metadata,
        )

        payload = request.to_dict()

        self.assertEqual(payload["request_id"], "request-001")
        self.assertEqual(payload["criteria"]["memory_types"], ["episodic"])
        self.assertNotIn("search", payload)
        self.assertNotIn("query", payload)
        self.assertNotIn("resolve", payload)
        self.assertTrue(validate_retrieval_request(request).is_valid)

    def test_retrieval_request_validation_reports_missing_identifier(self) -> None:
        request = MemoryRetrievalRequest(
            request_id="",
            criteria=MemoryRetrievalCriteria(),
        )

        result = validate_retrieval_request(request)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "request_id")

    def test_retrieval_response_contains_opaque_memory_identifiers_only(self) -> None:
        metadata = RetrievalMetadata(
            request_timestamp=datetime.fromisoformat("2026-07-03T00:00:00+00:00"),
            response_timestamp=datetime.fromisoformat("2026-07-03T00:02:00+00:00"),
        )
        response = MemoryRetrievalResponse(
            request_id="request-001",
            metadata=metadata,
            status=RetrievalStatus.COMPLETED,
            memory_ids=["memory-001", "memory-002"],
        )

        payload = response.to_dict()

        self.assertIsInstance(response.memory_ids, tuple)
        self.assertEqual(payload["status"], "completed")
        self.assertEqual(payload["memory_ids"], ["memory-001", "memory-002"])
        self.assertNotIn("memories", payload)
        self.assertNotIn("objects", payload)
        self.assertTrue(validate_retrieval_response(response).is_valid)

    def test_retrieval_response_rejects_non_opaque_memory_identifier(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000000005"),
            memory_type=MemoryType.SEMANTIC,
            content="Responses must not contain memory objects.",
            source=MemorySource(source_type="unit-test"),
        )
        response = MemoryRetrievalResponse(
            request_id="request-001",
            metadata=RetrievalMetadata(),
            status=RetrievalStatus.COMPLETED,
            memory_ids=("memory-001",),
        )
        object.__setattr__(response, "memory_ids", (memory,))

        result = validate_retrieval_response(response)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "memory_ids[0]")

    def test_retrieval_response_validation_reports_invalid_status(self) -> None:
        response = MemoryRetrievalResponse(
            request_id="request-001",
            metadata=RetrievalMetadata(),
        )
        object.__setattr__(response, "status", "completed")

        result = validate_retrieval_response(response)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "status")

    def test_platform_integration_with_memory_index_contract(self) -> None:
        contract = IndexContract(
            metadata=IndexMetadata(),
            fields=(
                IndexField("memory_type", IndexFieldType.ENUM),
                IndexField("confidence", IndexFieldType.ENUM),
            ),
        )
        criteria = MemoryRetrievalCriteria(
            memory_types=[MemoryType.SEMANTIC],
            confidence=MemoryConfidence.HIGH,
        )

        self.assertTrue(validate_index_contract(contract).is_valid)
        self.assertTrue(validate_retrieval_criteria(criteria).is_valid)

    def test_platform_core_serialization_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000000006"),
            memory_type=MemoryType.SEMANTIC,
            content="Platform Core serialization remains independent.",
            source=MemorySource(source_type="unit-test"),
        )

        payload = ObjectSerializer.serialize(memory)

        self.assertEqual(payload["object_type"], "UniversalMemory")
        self.assertEqual(payload["object_id"], "00000000-0000-0000-0000-000000000006")

    def test_retrieval_contract_exposes_no_retrieval_behavior(self) -> None:
        request = MemoryRetrievalRequest(
            request_id="request-001",
            criteria=MemoryRetrievalCriteria(),
        )
        response = MemoryRetrievalResponse(
            request_id="request-001",
            metadata=RetrievalMetadata(),
        )
        forbidden_names = {
            "retrieve",
            "search",
            "filter",
            "rank",
            "score",
            "query",
            "resolve",
            "populate",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(request))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(response))))


if __name__ == "__main__":
    unittest.main()
