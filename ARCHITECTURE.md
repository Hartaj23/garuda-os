# Architecture Governance

Garuda implementation is governed by the approved GAR architecture documents, not by assumptions inside the codebase.

Code, configuration, tests and documentation must remain consistent with the architecture. If implementation work reveals ambiguity, contributors must stop and request clarification before adding or changing behavior.

## Primary Governing Documents

- GAR-INDEX
- GAR-0001 Constitution
- GAR-0011 Reference Architecture
- GAR-0012 Developer Playbook
- GAR-0013 AI Coding Agent Operating Manual

## Contributor Guide

Before implementing a change:

1. Complete the repository bootstrap sequence in `GARUDA_NAVIGATION.md`.
2. Confirm the work is authorized by the current approved sprint mission specification.
3. Read the relevant GAR documents.
4. Identify affected contracts, objects, events and architectural boundaries.
5. Plan tests and documentation before implementation.
6. Keep changes small, reviewable and traceable.
7. Avoid future-sprint functionality.

## Engineering Governance Layer v1.0

Repository engineering governance is defined at the repository root:

- `ENGINEERING_GOVERNANCE_v1.0.md` *(frozen baseline)*
- `AGENTS.md`
- `GARUDA_CONTEXT.md`
- `GARUDA_WORKFLOW.md`
- `GARUDA_GLOSSARY.md`
- `GARUDA_NAVIGATION.md`
- `PROMPTS.md` *(optional)*
- `templates/`

See [`docs/README.md`](docs/README.md) for governance layer links.

Implementation must not rename canonical objects, invent architecture, introduce undocumented frameworks or bypass the approved governance process.
