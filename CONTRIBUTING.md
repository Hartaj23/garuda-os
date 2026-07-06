# Contributing to Garuda

Garuda implementation follows constitutional architecture, approved sprint missions, and Engineering Governance v1.0.

## Required Workflow

1. Complete the repository bootstrap sequence in `GARUDA_NAVIGATION.md`.
2. Read the relevant GAR architecture documents.
3. Confirm the approved mission specification authorizes the work.
4. Identify affected contracts, objects, events and boundaries.
5. Write or update tests.
6. Implement the smallest approved change.
7. Update documentation.
8. Run validation.
9. Request architecture review before merge.

## Engineering Governance v1.0

Before contributing, complete the repository bootstrap sequence in `GARUDA_NAVIGATION.md`:

1. `AGENTS.md`
2. `GARUDA_CONTEXT.md`
3. `GARUDA_WORKFLOW.md`
4. `GARUDA_GLOSSARY.md`
5. `GARUDA_NAVIGATION.md`
6. Applicable GAR Constitutions
7. Approved Sprint Mission

Optional resources:

- `PROMPTS.md`
- `templates/`
- [`docs/README.md`](docs/README.md)

## Rules

- Do not invent architecture.
- Do not rename canonical objects.
- Do not add future-sprint capabilities.
- Do not place business logic in applications.
- Do not commit secrets.
- Do not skip tests or documentation.

## Task Completion Report

Every completed task must report:

- Files created
- Files modified
- Tests written
- Tests executed
- Documentation updated
- GAR-SPRINT-0001 deliverables satisfied
- Recommended next task

