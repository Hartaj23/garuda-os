from __future__ import annotations

from packages.objects import ValidationCategory, ValidationResult

from .lookup import (
    IntegrationRegistryEntry,
    IntegrationRegistryLookupCriteria,
    IntegrationRegistryLookupResult,
    validate_integration_registry_entry,
)


class IntegrationRegistry:
    """Process-local deterministic catalog of Integration Foundation registrations.

    Registry operations describe registered Integration Foundation artifacts only. They have
    no side effects beyond deterministic catalog maintenance and do not instantiate,
    activate, execute, or resolve registered artifacts.

    Registry lookups return descriptive registration information only. Lookup results do
    not expose implementation instances, runtime handles, provider bindings, or
    transport-specific artifacts.
    """

    def __init__(self) -> None:
        self._entries: dict[str, IntegrationRegistryEntry] = {}

    def register(self, entry: IntegrationRegistryEntry) -> None:
        validation = validate_integration_registry_entry(entry)
        if not validation.is_valid:
            raise ValueError(validation.errors[0].message)
        if entry.registration_identifier in self._entries:
            raise ValueError(
                f"Registry entry already exists: {entry.registration_identifier}"
            )
        self._entries[entry.registration_identifier] = entry

    def lookup_exact(self, registration_identifier: str) -> IntegrationRegistryEntry | None:
        return self._entries.get(registration_identifier)

    def lookup_by_artifact_type(
        self,
        artifact_object_type: str,
    ) -> tuple[IntegrationRegistryEntry, ...]:
        matches = [
            entry
            for entry in self._entries.values()
            if entry.participant_descriptor.artifact_object_type == artifact_object_type
        ]
        return tuple(sorted(matches, key=lambda item: item.registration_identifier))

    def lookup(self, criteria: IntegrationRegistryLookupCriteria) -> IntegrationRegistryLookupResult:
        entries = list(self._entries.values())

        if criteria.registration_identifier is not None:
            exact = self.lookup_exact(criteria.registration_identifier)
            entries = [exact] if exact is not None else []

        if criteria.artifact_object_type is not None:
            entries = [
                entry
                for entry in entries
                if entry.participant_descriptor.artifact_object_type == criteria.artifact_object_type
            ]

        if criteria.participant_identifier is not None:
            entries = [
                entry
                for entry in entries
                if entry.participant_descriptor.participant_identifier == criteria.participant_identifier
            ]

        sorted_entries = tuple(sorted(entries, key=lambda item: item.registration_identifier))
        return IntegrationRegistryLookupResult(entries=sorted_entries)

    def identifiers(self) -> tuple[str, ...]:
        return tuple(sorted(self._entries.keys()))

    def validate(self) -> ValidationResult:
        result = ValidationResult()
        seen: set[str] = set()

        for registration_identifier, entry in self._entries.items():
            if registration_identifier in seen:
                result.add_error(
                    "Registry registration identifiers must be unique.",
                    ValidationCategory.IDENTITY,
                    field="registration_identifier",
                    code="duplicate_registration_identifier",
                )
            seen.add(registration_identifier)
            result.merge(validate_integration_registry_entry(entry))

        return result
