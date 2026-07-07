from __future__ import annotations

from dataclasses import dataclass

from packages.interface import InterfaceFoundation


@dataclass(frozen=True, slots=True)
class IntegrationInterfaceDependency:
    """Lawful Interface Foundation dependency wiring for Mission Alpha."""

    interface_foundation_type: type[InterfaceFoundation] = InterfaceFoundation
    interface_object_type: str = "InterfaceFoundation"

    def is_compatible(self, foundation: InterfaceFoundation) -> bool:
        return isinstance(foundation, self.interface_foundation_type)


def resolve_interface_foundation_type() -> type[InterfaceFoundation]:
    return InterfaceFoundation
