from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Callable, Protocol
from uuid import UUID, uuid4


class LifecycleState(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


class ValidationHook(Protocol):
    def __call__(self, obj: "GarudaObject") -> None: ...


@dataclass(slots=True)
class Metadata:
    values: dict[str, Any] = field(default_factory=dict)


class GarudaObject:
    """Minimal platform-level object foundation for Garuda."""

    object_type: str = "GarudaObject"
    schema_version: str = "1.0"
    object_version: int = 1

    def __init__(
        self,
        object_id: UUID | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | tuple[str, ...] | None = None,
        lifecycle_state: LifecycleState | None = None,
        created_by: str | None = None,
        updated_by: str | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        self._object_id = object_id or uuid4()
        self.object_type = type(self).__name__
        self._metadata = Metadata(values=metadata or {})
        self._tags = tuple(tags or ())
        self._lifecycle_state = lifecycle_state or LifecycleState.DRAFT
        self._created_at = created_at or datetime.now(tz=UTC)
        self._updated_at = updated_at or self._created_at
        self._created_by = created_by
        self._updated_by = updated_by
        self._validation_hooks: list[ValidationHook] = []
        self._behaviors: dict[str, Any] = {}
        self._relationships: dict[str, Any] = {}

    @property
    def object_id(self) -> UUID:
        return self._object_id

    @property
    def metadata(self) -> Metadata:
        return self._metadata

    @property
    def tags(self) -> tuple[str, ...]:
        return self._tags

    @property
    def lifecycle_state(self) -> LifecycleState:
        return self._lifecycle_state

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @property
    def created_by(self) -> str | None:
        return self._created_by

    @property
    def updated_by(self) -> str | None:
        return self._updated_by

    @property
    def behaviors(self) -> dict[str, Any]:
        return self._behaviors

    @property
    def relationships(self) -> dict[str, Any]:
        return self._relationships

    def register_validation_hook(self, hook: ValidationHook) -> None:
        self._validation_hooks.append(hook)

    def register_behavior(self, name: str, value: Any) -> None:
        self._behaviors[name] = value

    def validate(self) -> None:
        for hook in self._validation_hooks:
            hook(self)

    def transition_to(self, new_state: LifecycleState) -> None:
        allowed = {
            LifecycleState.DRAFT: {LifecycleState.ACTIVE},
            LifecycleState.ACTIVE: {LifecycleState.ARCHIVED},
            LifecycleState.ARCHIVED: set(),
        }
        if new_state not in allowed.get(self._lifecycle_state, set()):
            raise ValueError(f"Invalid lifecycle transition: {self._lifecycle_state} -> {new_state}")
        self._lifecycle_state = new_state
        self._updated_at = datetime.now(tz=UTC)


class CanonicalObject(GarudaObject):
    """Base class for future canonical objects."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.object_type == "CanonicalObject":
            self.__class__.object_type = self.__class__.__name__
