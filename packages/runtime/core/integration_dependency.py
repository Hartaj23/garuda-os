from __future__ import annotations

from dataclasses import dataclass

from packages.integration import IntegrationFoundation


@dataclass(frozen=True, slots=True)
class RuntimeIntegrationDependency:
    """Lawful Integration Foundation dependency wiring for Mission Alpha."""

    integration_foundation_type: type[IntegrationFoundation] = IntegrationFoundation
    integration_object_type: str = "IntegrationFoundation"

    def is_compatible(self, foundation: IntegrationFoundation) -> bool:
        return isinstance(foundation, self.integration_foundation_type)


def resolve_integration_foundation_type() -> type[IntegrationFoundation]:
    return IntegrationFoundation
