from __future__ import annotations

from typing import Any


class ObjectFactory:
    """Placeholder factory interface for future canonical object creation."""

    def create(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Object factory creation is not implemented in Mission Bravo")
