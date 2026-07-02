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

1. Confirm the work is authorized by the current approved sprint.
2. Read the relevant GAR documents.
3. Identify affected contracts, objects, events and architectural boundaries.
4. Plan tests and documentation before implementation.
5. Keep changes small, reviewable and traceable.
6. Avoid future-sprint functionality.

Implementation must not rename canonical objects, invent architecture, introduce undocumented frameworks or bypass the approved governance process.
