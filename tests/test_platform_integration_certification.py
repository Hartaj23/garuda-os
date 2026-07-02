import json
import unittest
from datetime import datetime
from uuid import UUID

from packages.objects import (
    CanonicalObject,
    LifecycleEvent,
    LifecycleEventType,
    ObjectRegistry,
    ObjectSerializer,
    Relationship,
    RelationshipDirection,
    RelationshipStatus,
    RelationshipType,
    ValidationCategory,
    ValidationError,
    ValidationResult,
    ValidationSeverity,
)


class CertificationAlphaObject(CanonicalObject):
    pass


class CertificationBetaObject(CanonicalObject):
    pass


def relationship_from_payload(payload: dict[str, object]) -> Relationship:
    return Relationship(
        source_object_id=UUID(str(payload["source_object_id"])),
        target_object_id=UUID(str(payload["target_object_id"])),
        relationship_type=RelationshipType(str(payload["relationship_type"])),
        relationship_direction=RelationshipDirection(str(payload["relationship_direction"])),
        relationship_status=RelationshipStatus(str(payload["relationship_status"])),
        metadata=dict(payload["metadata"]),
        created_by=payload["created_by"],
        updated_by=payload["updated_by"],
        created_at=datetime.fromisoformat(str(payload["created_at"])),
        updated_at=datetime.fromisoformat(str(payload["updated_at"])),
        relationship_id=UUID(str(payload["relationship_id"])),
    )


def lifecycle_event_from_payload(payload: dict[str, object]) -> LifecycleEvent:
    return LifecycleEvent(
        related_object_id=UUID(str(payload["related_object_id"])),
        event_type=LifecycleEventType(str(payload["event_type"])),
        event_timestamp=datetime.fromisoformat(str(payload["event_timestamp"])),
        event_actor=payload["event_actor"],
        event_metadata=dict(payload["event_metadata"]),
        event_version=int(payload["event_version"]),
        event_id=UUID(str(payload["event_id"])),
    )


def deterministic_validation_payload(result: ValidationResult) -> str:
    payload = [
        {
            "category": error.category.value,
            "code": error.code,
            "field": error.field,
            "message": error.message,
            "severity": error.severity.value,
        }
        for error in sorted(
            result.errors,
            key=lambda item: (
                item.category.value,
                item.severity.value,
                item.field or "",
                item.code or "",
                item.message,
            ),
        )
    ]
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


class PlatformIntegrationCertificationTest(unittest.TestCase):
    def test_scenario_1_object_validate_register_serialize_deserialize_validate(self) -> None:
        obj = CertificationAlphaObject(metadata={"owner": "platform"}, tags=["certified"])
        initial_result = obj.validate()

        registry = ObjectRegistry()
        registry.register(CertificationAlphaObject)
        payload = ObjectSerializer.serialize(obj)
        restored = ObjectSerializer.deserialize(payload)
        final_result = restored.validate()

        self.assertTrue(initial_result.is_valid)
        self.assertEqual(registry.lookup("CertificationAlphaObject"), CertificationAlphaObject)
        self.assertTrue(final_result.is_valid)
        self.assertEqual(restored.object_id, obj.object_id)
        self.assertEqual(restored.object_type, "CertificationAlphaObject")
        self.assertEqual(restored.metadata.values, {"owner": "platform"})
        self.assertEqual(restored.tags, ("certified",))

    def test_scenario_2_relationship_serialization_integrity(self) -> None:
        source = CertificationAlphaObject()
        target = CertificationBetaObject()
        relationship = Relationship(
            source_object_id=source.object_id,
            target_object_id=target.object_id,
            relationship_type=RelationshipType.DEPENDS_ON,
            metadata={"purpose": "certification"},
        )

        payload = relationship.to_dict()
        restored = relationship_from_payload(payload)

        self.assertTrue(source.validate().is_valid)
        self.assertTrue(target.validate().is_valid)
        self.assertEqual(restored.to_dict(), payload)
        self.assertEqual(restored.source_object_id, source.object_id)
        self.assertEqual(restored.target_object_id, target.object_id)
        self.assertEqual(restored.metadata, {"purpose": "certification"})

    def test_scenario_3_lifecycle_event_deterministic_payload(self) -> None:
        obj = CertificationAlphaObject()
        event = LifecycleEvent(
            related_object_id=obj.object_id,
            event_type=LifecycleEventType.OBJECT_CREATED,
            event_metadata={"zeta": 1, "alpha": 2},
            event_actor="certification",
        )

        payload = event.to_dict()
        restored = lifecycle_event_from_payload(payload)

        self.assertEqual(restored.to_dict(), payload)
        self.assertEqual(payload["related_object_id"], str(obj.object_id))
        self.assertEqual(payload["event_metadata"], {"alpha": 2, "zeta": 1})

    def test_scenario_4_registry_enumeration_and_duplicate_protection(self) -> None:
        registry = ObjectRegistry()
        registry.register(CertificationAlphaObject)
        registry.register(CertificationBetaObject)

        self.assertEqual(
            registry.enumerate(),
            (CertificationAlphaObject, CertificationBetaObject),
        )
        with self.assertRaises(ValueError):
            registry.register(CertificationAlphaObject)

    def test_scenario_5_validation_aggregation_categories_severity_determinism(self) -> None:
        result = ValidationResult()
        result.merge(
            ValidationError(
                message="Schema version is missing.",
                category=ValidationCategory.SCHEMA,
                severity=ValidationSeverity.ERROR,
                field="schema_version",
                code="missing_schema_version",
            )
        )
        result.merge(
            ValidationError(
                message="Metadata is sparse.",
                category=ValidationCategory.METADATA,
                severity=ValidationSeverity.WARNING,
                field="metadata",
                code="sparse_metadata",
            )
        )

        deterministic_payload = deterministic_validation_payload(result)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.category for error in result.errors},
            {ValidationCategory.SCHEMA, ValidationCategory.METADATA},
        )
        self.assertEqual(
            {error.severity for error in result.errors},
            {ValidationSeverity.ERROR, ValidationSeverity.WARNING},
        )
        self.assertEqual(deterministic_payload, deterministic_validation_payload(result))

    def test_scenario_6_complete_platform_core_integration(self) -> None:
        obj = CertificationAlphaObject(metadata={"scope": "platform-core"})
        registry = ObjectRegistry()
        registry.register(CertificationAlphaObject)
        registered_before = registry.enumerate()

        related = CertificationBetaObject()
        relationship = Relationship(
            source_object_id=obj.object_id,
            target_object_id=related.object_id,
            relationship_type=RelationshipType.RELATED_TO,
            metadata={"scenario": "complete-platform-core"},
        )
        event = LifecycleEvent(
            related_object_id=obj.object_id,
            event_type=LifecycleEventType.OBJECT_CREATED,
            event_metadata={"scenario": "complete-platform-core"},
            event_actor="certification",
        )

        validation_before = obj.validate()
        serialized_object = ObjectSerializer.serialize(obj)
        restored_object = ObjectSerializer.deserialize(serialized_object)

        self.assertTrue(validation_before.is_valid)
        self.assertTrue(restored_object.validate().is_valid)
        self.assertEqual(restored_object.object_id, obj.object_id)
        self.assertEqual(registry.enumerate(), registered_before)
        self.assertEqual(relationship.to_dict()["source_object_id"], str(obj.object_id))
        self.assertEqual(relationship.to_dict()["target_object_id"], str(related.object_id))
        self.assertEqual(event.to_dict()["related_object_id"], str(obj.object_id))
        self.assertEqual(event.to_dict()["event_type"], LifecycleEventType.OBJECT_CREATED.value)


if __name__ == "__main__":
    unittest.main()
