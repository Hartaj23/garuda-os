import unittest
from datetime import datetime
from uuid import UUID

from packages.knowledge import (
    EvidenceReference,
    EvidenceType,
    KnowledgeConfidence,
    KnowledgeEvidence,
    KnowledgeMetadata,
    KnowledgeOrigin,
    KnowledgeProvenance,
    KnowledgeState,
    KnowledgeType,
    UniversalKnowledge,
)
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import (
    CanonicalObject,
    LifecycleState,
    ObjectRegistry,
    ObjectSerializer,
    Relationship,
    RelationshipType,
    ValidationResult,
)


class KnowledgeSerializationValidationIntegrationTest(unittest.TestCase):
    def build_reference(self) -> EvidenceReference:
        return EvidenceReference(
            reference_type=EvidenceType.MEMORY_REFERENCE,
            reference_identifier="memory:00000000-0000-0000-0000-000000000501",
            reference_label="Certified memory reference",
            reference_metadata={"z": "last", "a": "first"},
        )

    def build_knowledge(self) -> UniversalKnowledge:
        timestamp = datetime.fromisoformat("2026-07-04T00:00:00+00:00")
        reference = self.build_reference()
        return UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000000502"),
            knowledge_type=KnowledgeType.PRINCIPLE,
            knowledge_state=KnowledgeState.VALIDATED,
            confidence=KnowledgeConfidence(level="high", rationale="certified"),
            knowledge_metadata=KnowledgeMetadata(values={"z": "last", "a": "first"}),
            evidence=KnowledgeEvidence(
                references=(reference,),
                evidence_metadata={"source": "mission-charlie"},
            ),
            provenance=KnowledgeProvenance(
                origin=KnowledgeOrigin.VALIDATED_MEMORY,
                creator="codex",
                created_at=timestamp,
                evidence_references=(reference,),
                provenance_metadata={"phase": "certification"},
            ),
            metadata={"owner": "knowledge"},
            tags=["knowledge", "charlie"],
            lifecycle_state=LifecycleState.DRAFT,
            created_by="codex",
            updated_by="codex",
            created_at=timestamp,
            updated_at=timestamp,
        )

    def test_universal_knowledge_is_canonical_platform_object(self) -> None:
        knowledge = self.build_knowledge()

        self.assertIsInstance(knowledge, CanonicalObject)
        self.assertEqual(knowledge.object_type, "UniversalKnowledge")
        self.assertEqual(knowledge.schema_version, "1.0")
        self.assertEqual(knowledge.object_version, 1)

    def test_to_dict_payload_is_deterministic_and_preserves_existing_keys(self) -> None:
        knowledge = self.build_knowledge()
        payload = knowledge.to_dict()

        self.assertEqual(payload, knowledge.to_dict())
        self.assertEqual(
            list(payload.keys()),
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
                "knowledge_type",
                "knowledge_state",
                "confidence",
                "knowledge_metadata",
                "evidence",
                "provenance",
            ],
        )
        self.assertEqual(payload["knowledge_type"], "principle")
        self.assertEqual(payload["knowledge_state"], "validated")
        self.assertEqual(payload["confidence"], {"level": "high", "rationale": "certified"})
        self.assertEqual(payload["knowledge_metadata"], {"a": "first", "z": "last"})

    def test_nested_knowledge_payloads_are_deterministic(self) -> None:
        knowledge = self.build_knowledge()
        payload = knowledge.to_dict()

        self.assertEqual(
            payload["evidence"],
            {
                "references": [
                    {
                        "reference_type": "memory_reference",
                        "reference_identifier": (
                            "memory:00000000-0000-0000-0000-000000000501"
                        ),
                        "reference_label": "Certified memory reference",
                        "reference_metadata": {"a": "first", "z": "last"},
                    }
                ],
                "evidence_metadata": {"source": "mission-charlie"},
            },
        )
        self.assertEqual(
            payload["provenance"],
            {
                "origin": "validated_memory",
                "creator": "codex",
                "created_at": "2026-07-04T00:00:00+00:00",
                "evidence_references": payload["evidence"]["references"],
                "provenance_metadata": {"phase": "certification"},
            },
        )

    def test_validation_returns_platform_validation_result(self) -> None:
        result = self.build_knowledge().validate()

        self.assertIsInstance(result, ValidationResult)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_validation_covers_knowledge_specific_contracts(self) -> None:
        knowledge = self.build_knowledge()
        knowledge._knowledge_type = "principle"
        knowledge._knowledge_state = "validated"
        knowledge._confidence = "high"
        knowledge._knowledge_metadata = {"a": "first"}
        knowledge._evidence = "evidence"
        knowledge._provenance = "provenance"

        result = knowledge.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "knowledge_type",
                "knowledge_state",
                "confidence",
                "knowledge_metadata",
                "evidence",
                "provenance",
            },
        )

    def test_validation_covers_evidence_reference_shape(self) -> None:
        evidence = KnowledgeEvidence()
        object.__setattr__(evidence, "references", ("not-a-reference",))
        knowledge = UniversalKnowledge(
            knowledge_type=KnowledgeType.FACT,
            evidence=evidence,
        )

        result = knowledge.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "evidence.references[0]")

    def test_validation_covers_provenance_origin_and_reference_shape(self) -> None:
        provenance = KnowledgeProvenance(origin=KnowledgeOrigin.SYSTEM_FACT)
        object.__setattr__(provenance, "origin", "system_fact")
        object.__setattr__(provenance, "evidence_references", ("not-a-reference",))
        knowledge = UniversalKnowledge(
            knowledge_type=KnowledgeType.FACT,
            provenance=provenance,
        )

        result = knowledge.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {"provenance.origin", "provenance.evidence_references[0]"},
        )

    def test_object_serializer_remains_platform_core_contract(self) -> None:
        knowledge = self.build_knowledge()

        payload = ObjectSerializer.serialize(knowledge)

        self.assertEqual(payload["object_type"], "UniversalKnowledge")
        self.assertEqual(payload["metadata"], {"owner": "knowledge"})
        self.assertEqual(payload["tags"], ["knowledge", "charlie"])
        self.assertNotIn("knowledge_type", payload)
        self.assertNotIn("evidence", payload)
        self.assertNotIn("provenance", payload)

    def test_object_serializer_json_is_deterministic(self) -> None:
        knowledge = self.build_knowledge()

        self.assertEqual(
            ObjectSerializer.serialize_json(knowledge),
            ObjectSerializer.serialize_json(knowledge),
        )

    def test_object_registry_accepts_universal_knowledge(self) -> None:
        registry = ObjectRegistry()

        registry.register(UniversalKnowledge)

        self.assertEqual(registry.lookup("UniversalKnowledge"), UniversalKnowledge)
        self.assertEqual(registry.lookup_by_class(UniversalKnowledge), UniversalKnowledge)
        self.assertEqual(registry.enumerate(), (UniversalKnowledge,))
        registry.validate()

    def test_lifecycle_transitions_remain_platform_core_behavior(self) -> None:
        knowledge = self.build_knowledge()

        knowledge.transition_to(LifecycleState.ACTIVE)
        knowledge.transition_to(LifecycleState.ARCHIVED)

        self.assertEqual(knowledge.lifecycle_state, LifecycleState.ARCHIVED)
        with self.assertRaises(ValueError):
            knowledge.transition_to(LifecycleState.ACTIVE)

    def test_relationship_compatibility_uses_platform_relationship_model(self) -> None:
        knowledge = self.build_knowledge()
        target_id = UUID("00000000-0000-0000-0000-000000000503")
        relationship = Relationship(
            source_object_id=knowledge.object_id,
            target_object_id=target_id,
            relationship_type=RelationshipType.REFERENCES,
            metadata={"context": "certification"},
        )

        payload = relationship.to_dict()

        self.assertEqual(payload["source_object_id"], str(knowledge.object_id))
        self.assertEqual(payload["target_object_id"], str(target_id))
        self.assertEqual(payload["relationship_type"], "references")
        self.assertEqual(payload["metadata"], {"context": "certification"})
        self.assertEqual(knowledge.relationships, {})

    def test_mission_alpha_constructor_compatibility_is_preserved(self) -> None:
        knowledge = UniversalKnowledge(knowledge_type=KnowledgeType.CONCEPT)
        payload = knowledge.to_dict()

        self.assertTrue(knowledge.validate().is_valid)
        self.assertEqual(payload["knowledge_type"], "concept")
        self.assertEqual(payload["knowledge_state"], "draft")
        self.assertEqual(payload["confidence"], {"level": "unknown", "rationale": None})
        self.assertEqual(payload["knowledge_metadata"], {})
        self.assertEqual(payload["evidence"], {"references": [], "evidence_metadata": {}})
        self.assertIsNone(payload["provenance"])

    def test_mission_bravo_evidence_and_provenance_contracts_are_preserved(self) -> None:
        reference = self.build_reference()
        evidence = KnowledgeEvidence(references=(reference,))
        provenance = KnowledgeProvenance(
            origin=KnowledgeOrigin.VALIDATED_MEMORY,
            evidence_references=(reference,),
        )
        knowledge = UniversalKnowledge(
            knowledge_type=KnowledgeType.FACT,
            evidence=evidence,
            provenance=provenance,
        )

        self.assertEqual(knowledge.evidence, evidence)
        self.assertEqual(knowledge.provenance, provenance)
        self.assertEqual(knowledge.to_dict()["evidence"], evidence.to_dict())
        self.assertEqual(knowledge.to_dict()["provenance"], provenance.to_dict())

    def test_memory_and_knowledge_foundations_coexist_without_direct_object_links(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000000504"),
            memory_type=MemoryType.SEMANTIC,
            content="Memory Foundation coexists with Knowledge Foundation.",
            source=MemorySource(source_type="test", source_identifier="mission-charlie"),
        )
        knowledge = UniversalKnowledge(
            knowledge_type=KnowledgeType.FACT,
            evidence=KnowledgeEvidence(
                references=(
                    EvidenceReference(
                        reference_type=EvidenceType.MEMORY_REFERENCE,
                        reference_identifier=str(memory.object_id),
                    ),
                )
            ),
        )

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertIsInstance(knowledge.evidence.references[0].reference_identifier, str)
        self.assertNotIsInstance(
            knowledge.evidence.references[0].reference_identifier,
            UniversalMemory,
        )

    def test_no_future_knowledge_capabilities_are_exposed(self) -> None:
        knowledge = self.build_knowledge()
        forbidden_names = {
            "ai",
            "classify",
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
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(knowledge))))


if __name__ == "__main__":
    unittest.main()
