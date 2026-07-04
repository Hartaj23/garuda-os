import unittest
from dataclasses import FrozenInstanceError
from datetime import UTC, datetime
from uuid import UUID

from packages.knowledge import (
    EvidenceReference,
    EvidenceType,
    KnowledgeConfidence,
    KnowledgeEvidence,
    KnowledgeOrigin,
    KnowledgeProvenance,
    KnowledgeState,
    KnowledgeType,
    UniversalKnowledge,
)
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import ObjectSerializer


class KnowledgeProvenanceFrameworkTest(unittest.TestCase):
    def test_evidence_reference_is_opaque_and_deterministic(self) -> None:
        reference = EvidenceReference(
            reference_type=EvidenceType.MEMORY_REFERENCE,
            reference_identifier="memory:0001",
            reference_label="Certified memory",
            reference_metadata={"z": "last", "a": "first"},
        )

        self.assertEqual(reference.reference_identifier, "memory:0001")
        self.assertEqual(
            reference.to_dict(),
            {
                "reference_type": "memory_reference",
                "reference_identifier": "memory:0001",
                "reference_label": "Certified memory",
                "reference_metadata": {"a": "first", "z": "last"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            reference.reference_identifier = "memory:0002"

    def test_evidence_types_are_descriptive_reference_categories(self) -> None:
        self.assertEqual(
            {evidence_type.value for evidence_type in EvidenceType},
            {
                "memory_reference",
                "document_reference",
                "external_reference",
                "observation_reference",
                "certified_evidence",
            },
        )

    def test_knowledge_evidence_records_support_without_evaluating_it(self) -> None:
        reference = EvidenceReference(
            reference_type=EvidenceType.DOCUMENT_REFERENCE,
            reference_identifier="doc:gar-0019",
        )
        evidence = KnowledgeEvidence(
            references=[reference],
            evidence_metadata={"recorded_by": "mission-bravo"},
        )

        self.assertEqual(evidence.references, (reference,))
        self.assertEqual(
            evidence.to_dict(),
            {
                "references": [reference.to_dict()],
                "evidence_metadata": {"recorded_by": "mission-bravo"},
            },
        )
        forbidden_names = {
            "compare",
            "evaluate",
            "infer",
            "rank",
            "resolve",
            "score",
            "truth",
        }
        self.assertTrue(forbidden_names.isdisjoint(set(dir(evidence))))

    def test_knowledge_origin_is_separate_from_evidence_and_provenance(self) -> None:
        self.assertEqual(
            {origin.value for origin in KnowledgeOrigin},
            {
                "validated_memory",
                "verified_observation",
                "external_reference",
                "human_curation",
                "system_fact",
            },
        )

    def test_knowledge_provenance_records_history_without_computation(self) -> None:
        timestamp = datetime.fromisoformat("2026-07-04T00:00:00+00:00")
        reference = EvidenceReference(
            reference_type=EvidenceType.EXTERNAL_REFERENCE,
            reference_identifier="external:standard",
        )
        provenance = KnowledgeProvenance(
            origin=KnowledgeOrigin.EXTERNAL_REFERENCE,
            creator="codex",
            created_at=timestamp,
            evidence_references=[reference],
            provenance_metadata={"z": "last", "a": "first"},
        )

        self.assertEqual(
            provenance.to_dict(),
            {
                "origin": "external_reference",
                "creator": "codex",
                "created_at": "2026-07-04T00:00:00+00:00",
                "evidence_references": [reference.to_dict()],
                "provenance_metadata": {"a": "first", "z": "last"},
            },
        )
        forbidden_names = {
            "compute",
            "interpret",
            "lineage",
            "resolve",
            "verify",
        }
        self.assertTrue(forbidden_names.isdisjoint(set(dir(provenance))))
        with self.assertRaises(FrozenInstanceError):
            provenance.origin = KnowledgeOrigin.SYSTEM_FACT

    def test_universal_knowledge_integrates_evidence_and_provenance(self) -> None:
        timestamp = datetime.fromisoformat("2026-07-04T00:00:00+00:00")
        reference = EvidenceReference(
            reference_type=EvidenceType.MEMORY_REFERENCE,
            reference_identifier="memory:00000000-0000-0000-0000-000000000401",
            reference_metadata={"scope": "opaque"},
        )
        evidence = KnowledgeEvidence(references=(reference,))
        provenance = KnowledgeProvenance(
            origin=KnowledgeOrigin.VALIDATED_MEMORY,
            creator="codex",
            created_at=timestamp,
            evidence_references=(reference,),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000000402"),
            knowledge_type=KnowledgeType.FACT,
            knowledge_state=KnowledgeState.SUPPORTED,
            confidence=KnowledgeConfidence(level="medium"),
            evidence=evidence,
            provenance=provenance,
            created_at=timestamp,
            updated_at=timestamp,
        )

        payload = knowledge.to_dict()

        self.assertTrue(knowledge.validate().is_valid)
        self.assertEqual(payload, knowledge.to_dict())
        self.assertEqual(payload["evidence"], evidence.to_dict())
        self.assertEqual(payload["provenance"], provenance.to_dict())
        self.assertEqual(
            list(payload.keys())[-2:],
            ["evidence", "provenance"],
        )

    def test_mission_alpha_construction_and_payload_keys_remain_compatible(self) -> None:
        knowledge = UniversalKnowledge(knowledge_type=KnowledgeType.CONCEPT)
        payload = knowledge.to_dict()

        self.assertTrue(knowledge.validate().is_valid)
        self.assertEqual(payload["knowledge_type"], "concept")
        self.assertEqual(payload["knowledge_state"], "draft")
        self.assertEqual(payload["confidence"], {"level": "unknown", "rationale": None})
        self.assertEqual(payload["knowledge_metadata"], {})
        self.assertEqual(payload["evidence"], {"references": [], "evidence_metadata": {}})
        self.assertIsNone(payload["provenance"])

    def test_validation_reports_invalid_evidence_reference(self) -> None:
        evidence = KnowledgeEvidence()
        object.__setattr__(evidence, "references", ("memory:bad",))
        knowledge = UniversalKnowledge(
            knowledge_type=KnowledgeType.FACT,
            evidence=evidence,
        )

        result = knowledge.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "evidence.references[0]")

    def test_validation_reports_invalid_provenance_reference(self) -> None:
        provenance = KnowledgeProvenance(origin=KnowledgeOrigin.HUMAN_CURATION)
        object.__setattr__(provenance, "evidence_references", ("doc:bad",))
        knowledge = UniversalKnowledge(
            knowledge_type=KnowledgeType.FACT,
            provenance=provenance,
        )

        result = knowledge.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "provenance.evidence_references[0]")

    def test_object_serializer_remains_platform_core_only(self) -> None:
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000000403"),
            knowledge_type=KnowledgeType.FACT,
            evidence=KnowledgeEvidence(
                references=(
                    EvidenceReference(
                        reference_type=EvidenceType.CERTIFIED_EVIDENCE,
                        reference_identifier="cert:evidence",
                    ),
                )
            ),
        )

        payload = ObjectSerializer.serialize(knowledge)

        self.assertEqual(payload["object_type"], "UniversalKnowledge")
        self.assertNotIn("evidence", payload)
        self.assertNotIn("provenance", payload)

    def test_evidence_references_memory_by_identifier_only(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000000404"),
            memory_type=MemoryType.SEMANTIC,
            content="Knowledge may cite memory IDs opaquely.",
            source=MemorySource(source_type="test", source_identifier="mission-bravo"),
        )
        reference = EvidenceReference(
            reference_type=EvidenceType.MEMORY_REFERENCE,
            reference_identifier=str(memory.object_id),
        )

        self.assertEqual(reference.reference_identifier, str(memory.object_id))
        self.assertNotIsInstance(reference.reference_identifier, UniversalMemory)
        self.assertTrue(memory.validate().is_valid)

    def test_no_query_search_ranking_or_persistence_behavior_is_exposed(self) -> None:
        knowledge = UniversalKnowledge(
            knowledge_type=KnowledgeType.PRINCIPLE,
            evidence=KnowledgeEvidence(),
            provenance=KnowledgeProvenance(
                origin=KnowledgeOrigin.SYSTEM_FACT,
                created_at=datetime.now(tz=UTC),
            ),
        )
        forbidden_names = {
            "ai",
            "classify",
            "compare_evidence",
            "evaluate_evidence",
            "graph",
            "infer",
            "persist",
            "query",
            "rank_evidence",
            "reason",
            "resolve_evidence",
            "search",
            "score_evidence",
            "store",
            "truth",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(knowledge))))


if __name__ == "__main__":
    unittest.main()
