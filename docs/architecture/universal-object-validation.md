# Universal Object Validation

## Scope

This document describes the Mission Foxtrot validation framework for the Universal Object
System.

## Contract

- Validation is represented by explicit result and error models.
- Validation errors are categorized by platform-level object concern.
- Validation severities allow informational, warning, error, and critical findings.
- Validation helpers inspect only universal object structure and invariants.
- `GarudaObject.validate()` runs platform validation and registered validation hooks.

## Validation model

`ValidationResult` contains zero or more `ValidationError` instances. A result is valid when
it contains no error or critical findings. Informational and warning findings do not make a
result invalid.

`ValidationError` records:

- message
- category
- severity
- optional field
- optional code
- optional context

## Categories

- identity
- metadata
- lifecycle
- behavior
- relationships
- schema
- version

## Hook behavior

Existing validation hooks remain supported. Hooks may continue to perform side effects or raise
exceptions. Hooks may also return a `ValidationResult` or `ValidationError`, which is merged into
the object validation result.

## Explicitly out of scope

- Business-rule validation
- Trading validation
- Portfolio validation
- AI validation
- Database validation
- Persistence
- REST endpoints
- Frontend validation
- Workflow engine
- Knowledge Graph
- Memory
