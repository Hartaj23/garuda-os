from .foundation import (
    IntegrationFoundation,
    IntegrationFoundationCategory,
    IntegrationFoundationMetadata,
    validate_integration_foundation,
)
from .interface_dependency import (
    IntegrationInterfaceDependency,
    resolve_interface_foundation_type,
)

__all__ = [
    "IntegrationFoundation",
    "IntegrationFoundationCategory",
    "IntegrationFoundationMetadata",
    "IntegrationInterfaceDependency",
    "resolve_interface_foundation_type",
    "validate_integration_foundation",
]
