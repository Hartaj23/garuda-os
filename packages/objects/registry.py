from __future__ import annotations

from typing import Any, TypeVar

from .core import CanonicalObject, GarudaObject

T = TypeVar("T", bound=GarudaObject)


class ObjectRegistry:
    """Minimal registry for canonical object types only."""

    def __init__(self) -> None:
        self._registry: dict[str, type[GarudaObject]] = {}

    def register(self, object_type: type[T]) -> type[T]:
        if not issubclass(object_type, CanonicalObject):
            raise TypeError("Only CanonicalObject subclasses can be registered")
        if object_type.__name__ in self._registry:
            raise ValueError(f"Object type already registered: {object_type.__name__}")
        self._registry[object_type.__name__] = object_type
        return object_type

    def lookup(self, object_name: str) -> type[GarudaObject] | None:
        return self._registry.get(object_name)

    def lookup_by_class(self, object_type: type[Any]) -> type[GarudaObject] | None:
        return self._registry.get(object_type.__name__)

    def enumerate(self) -> tuple[type[GarudaObject], ...]:
        return tuple(self._registry.values())

    def validate(self) -> None:
        for object_type in self._registry.values():
            if not issubclass(object_type, CanonicalObject):
                raise TypeError(f"Registry contains non-canonical type: {object_type.__name__}")
