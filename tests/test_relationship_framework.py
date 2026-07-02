import unittest
from datetime import datetime
from uuid import UUID

from packages.objects import Relationship, RelationshipDirection, RelationshipStatus, RelationshipType


class RelationshipFrameworkTest(unittest.TestCase):
    def test_relationship_uses_immutable_object_ids(self) -> None:
        relation = Relationship(
            source_object_id=UUID("00000000-0000-0000-0000-000000000001"),
            target_object_id=UUID("00000000-0000-0000-0000-000000000002"),
        )
        self.assertEqual(relation.source_object_id, UUID("00000000-0000-0000-0000-000000000001"))
        self.assertEqual(relation.target_object_id, UUID("00000000-0000-0000-0000-000000000002"))

    def test_relationship_type_direction_and_status_defaults(self) -> None:
        relation = Relationship(
            source_object_id=UUID("00000000-0000-0000-0000-000000000001"),
            target_object_id=UUID("00000000-0000-0000-0000-000000000002"),
        )
        self.assertEqual(relation.relationship_type, RelationshipType.RELATED_TO)
        self.assertEqual(relation.relationship_direction, RelationshipDirection.DIRECTED)
        self.assertEqual(relation.relationship_status, RelationshipStatus.ACTIVE)

    def test_relationship_metadata_and_audit_fields_are_preserved(self) -> None:
        created = datetime.fromisoformat("2024-01-01T00:00:00+00:00")
        relation = Relationship(
            source_object_id=UUID("00000000-0000-0000-0000-000000000001"),
            target_object_id=UUID("00000000-0000-0000-0000-000000000002"),
            metadata={"label": "primary"},
            created_by="alice",
            updated_by="alice",
            created_at=created,
            updated_at=created,
        )
        payload = relation.to_dict()
        self.assertEqual(payload["metadata"], {"label": "primary"})
        self.assertEqual(payload["created_by"], "alice")
        self.assertEqual(payload["updated_by"], "alice")
        self.assertEqual(payload["created_at"], created.isoformat())

    def test_relationship_serialization_support(self) -> None:
        relation = Relationship(
            source_object_id=UUID("00000000-0000-0000-0000-000000000001"),
            target_object_id=UUID("00000000-0000-0000-0000-000000000002"),
        )
        payload = relation.to_dict()
        self.assertIn("relationship_id", payload)
        self.assertIn("source_object_id", payload)
        self.assertIn("target_object_id", payload)


if __name__ == "__main__":
    unittest.main()
