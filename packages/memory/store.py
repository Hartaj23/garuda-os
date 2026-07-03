from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from packages.objects import ValidationCategory, ValidationResult

from .core import UniversalMemory


@dataclass(frozen=True, slots=True)
class StoreStatistics:
    total_references: int
    created_at: datetime
    last_modified_at: datetime

    def to_dict(self) -> dict[str, object]:
        return {
            "total_references": self.total_references,
            "created_at": self.created_at.isoformat(),
            "last_modified_at": self.last_modified_at.isoformat(),
        }


class MemoryReferenceStore:
    """Process-local reference container for UniversalMemory objects."""

    def __init__(self) -> None:
        now = datetime.now(tz=UTC)
        self._references: dict[UUID, UniversalMemory] = {}
        self._created_at = now
        self._last_modified_at = now

    def add(self, memory: UniversalMemory) -> None:
        result = validate_memory_reference(memory)
        if not result.is_valid:
            raise ValueError(result.errors[0].message)
        if memory.object_id in self._references:
            raise ValueError(f"Memory reference already exists: {memory.object_id}")
        self._references[memory.object_id] = memory
        self._touch()

    def get(self, memory_id: UUID | str) -> UniversalMemory | None:
        return self._references.get(_coerce_memory_id(memory_id))

    def remove(self, memory_id: UUID | str) -> UniversalMemory | None:
        memory = self._references.pop(_coerce_memory_id(memory_id), None)
        if memory is not None:
            self._touch()
        return memory

    def identifiers(self) -> tuple[UUID, ...]:
        return tuple(sorted(self._references.keys(), key=str))

    def clear(self) -> None:
        if self._references:
            self._references.clear()
            self._touch()

    def statistics(self) -> StoreStatistics:
        return StoreStatistics(
            total_references=len(self._references),
            created_at=self._created_at,
            last_modified_at=self._last_modified_at,
        )

    def validate(self) -> ValidationResult:
        return validate_reference_store(self)

    def _touch(self) -> None:
        self._last_modified_at = datetime.now(tz=UTC)


def validate_memory_reference(memory: object) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(memory, UniversalMemory):
        result.add_error(
            "Memory reference store accepts only UniversalMemory instances.",
            ValidationCategory.SCHEMA,
            field="memory",
            code="invalid_memory_reference",
        )
        return result

    result.merge(memory.validate())
    return result


def validate_reference_store(store: MemoryReferenceStore) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(store, MemoryReferenceStore):
        result.add_error(
            "Store validation requires a MemoryReferenceStore instance.",
            ValidationCategory.SCHEMA,
            field="store",
            code="invalid_memory_reference_store",
        )
        return result

    seen_ids: set[UUID] = set()
    for memory_id, memory in store._references.items():
        if memory_id in seen_ids:
            result.add_error(
                "Memory reference identifiers must be unique.",
                ValidationCategory.IDENTITY,
                field="memory_id",
                code="duplicate_memory_reference",
            )
        seen_ids.add(memory_id)

        if not isinstance(memory, UniversalMemory):
            result.add_error(
                "Stored memory references must be UniversalMemory instances.",
                ValidationCategory.SCHEMA,
                field=str(memory_id),
                code="invalid_stored_memory_reference",
            )
        elif memory.object_id != memory_id:
            result.add_error(
                "Stored memory reference key must match object identity.",
                ValidationCategory.IDENTITY,
                field=str(memory_id),
                code="memory_reference_identity_mismatch",
            )
        else:
            result.merge(memory.validate())

    return result


def _coerce_memory_id(memory_id: UUID | str) -> UUID:
    if isinstance(memory_id, UUID):
        return memory_id
    return UUID(memory_id)
