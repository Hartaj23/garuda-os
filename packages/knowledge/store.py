from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from packages.objects import ValidationCategory, ValidationResult

from .core import UniversalKnowledge


@dataclass(frozen=True, slots=True)
class StoreStatistics:
    total_knowledge_objects: int
    created_at: datetime
    last_modified_at: datetime

    def to_dict(self) -> dict[str, object]:
        return {
            "total_knowledge_objects": self.total_knowledge_objects,
            "created_at": self.created_at.isoformat(),
            "last_modified_at": self.last_modified_at.isoformat(),
        }


class KnowledgeReferenceStore:
    """Process-local reference container for UniversalKnowledge objects."""

    def __init__(self) -> None:
        now = datetime.now(tz=UTC)
        self._references: dict[UUID, UniversalKnowledge] = {}
        self._created_at = now
        self._last_modified_at = now

    def add(self, knowledge: UniversalKnowledge) -> None:
        result = validate_knowledge_reference(knowledge)
        if not result.is_valid:
            raise ValueError(result.errors[0].message)
        if knowledge.object_id in self._references:
            raise ValueError(f"Knowledge reference already exists: {knowledge.object_id}")
        self._references[knowledge.object_id] = knowledge
        self._touch()

    def get(self, knowledge_id: UUID | str) -> UniversalKnowledge | None:
        return self._references.get(_coerce_knowledge_id(knowledge_id))

    def remove(self, knowledge_id: UUID | str) -> UniversalKnowledge | None:
        knowledge = self._references.pop(_coerce_knowledge_id(knowledge_id), None)
        if knowledge is not None:
            self._touch()
        return knowledge

    def identifiers(self) -> tuple[UUID, ...]:
        return tuple(sorted(self._references.keys(), key=str))

    def clear(self) -> None:
        if self._references:
            self._references.clear()
            self._touch()

    def statistics(self) -> StoreStatistics:
        return StoreStatistics(
            total_knowledge_objects=len(self._references),
            created_at=self._created_at,
            last_modified_at=self._last_modified_at,
        )

    def validate(self) -> ValidationResult:
        return validate_reference_store(self)

    def _touch(self) -> None:
        self._last_modified_at = datetime.now(tz=UTC)


def validate_knowledge_reference(knowledge: object) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(knowledge, UniversalKnowledge):
        result.add_error(
            "Knowledge reference store accepts only UniversalKnowledge instances.",
            ValidationCategory.SCHEMA,
            field="knowledge",
            code="invalid_knowledge_reference",
        )
        return result

    result.merge(knowledge.validate())
    return result


def validate_store_statistics(statistics: object) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(statistics, StoreStatistics):
        result.add_error(
            "Store statistics validation requires a StoreStatistics instance.",
            ValidationCategory.SCHEMA,
            field="statistics",
            code="invalid_store_statistics",
        )
        return result

    if statistics.total_knowledge_objects < 0:
        result.add_error(
            "Store statistics total knowledge objects cannot be negative.",
            ValidationCategory.METADATA,
            field="statistics.total_knowledge_objects",
            code="invalid_store_statistics_total",
        )

    if not hasattr(statistics.created_at, "isoformat"):
        result.add_error(
            "Store statistics creation timestamp must be datetime-like.",
            ValidationCategory.METADATA,
            field="statistics.created_at",
            code="invalid_store_statistics_created_at",
        )

    if not hasattr(statistics.last_modified_at, "isoformat"):
        result.add_error(
            "Store statistics last modification timestamp must be datetime-like.",
            ValidationCategory.METADATA,
            field="statistics.last_modified_at",
            code="invalid_store_statistics_last_modified_at",
        )

    return result


def validate_reference_store(store: object) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(store, KnowledgeReferenceStore):
        result.add_error(
            "Store validation requires a KnowledgeReferenceStore instance.",
            ValidationCategory.SCHEMA,
            field="store",
            code="invalid_knowledge_reference_store",
        )
        return result

    seen_ids: set[UUID] = set()
    for knowledge_id, knowledge in store._references.items():
        if knowledge_id in seen_ids:
            result.add_error(
                "Knowledge reference identifiers must be unique.",
                ValidationCategory.IDENTITY,
                field="knowledge_id",
                code="duplicate_knowledge_reference",
            )
        seen_ids.add(knowledge_id)

        if not isinstance(knowledge, UniversalKnowledge):
            result.add_error(
                "Stored knowledge references must be UniversalKnowledge instances.",
                ValidationCategory.SCHEMA,
                field=str(knowledge_id),
                code="invalid_stored_knowledge_reference",
            )
        elif knowledge.object_id != knowledge_id:
            result.add_error(
                "Stored knowledge reference key must match object identity.",
                ValidationCategory.IDENTITY,
                field=str(knowledge_id),
                code="knowledge_reference_identity_mismatch",
            )
        else:
            result.merge(knowledge.validate())

    result.merge(validate_store_statistics(store.statistics()))
    return result


def _coerce_knowledge_id(knowledge_id: UUID | str) -> UUID:
    if isinstance(knowledge_id, UUID):
        return knowledge_id
    return UUID(knowledge_id)
