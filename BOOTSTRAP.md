# PROJECT GARUDA

# BOOTSTRAP.md

AI Engineer Bootstrap Guide

Version: 1.0

Last Updated: 2026-07-06

Document Owner: Project Garuda Engineering Governance

---

# Purpose

This document is the single entry point for AI coding agents initializing work in Project Garuda.

For architecture threads and project synthesis, read [`PROJECT_GARUDA_MASTER.md`](PROJECT_GARUDA_MASTER.md)
first. This document consolidates the implementation bootstrap sequence.

Do not begin implementation until the full bootstrap sequence is complete and architecture approval
is granted.

---

# Before You Begin

Project Garuda uses Constitutional Engineering.

AI agents are implementation engineers, not architects. Preserve architectural integrity above
implementation speed. Never invent architecture. Never implement future sprint functionality.

The frozen engineering baseline is recorded in [`ENGINEERING_GOVERNANCE_v1.0.md`](ENGINEERING_GOVERNANCE_v1.0.md).

---

# Repository Bootstrap Sequence

Complete these steps in order before planning or coding.

| Step | Document | Purpose |
| --- | --- | --- |
| 1 | [`AGENTS.md`](AGENTS.md) | AI engineering operating manual |
| 2 | [`GARUDA_CONTEXT.md`](GARUDA_CONTEXT.md) | Current repository state |
| 3 | [`GARUDA_WORKFLOW.md`](GARUDA_WORKFLOW.md) | Engineering lifecycle |
| 4 | [`GARUDA_GLOSSARY.md`](GARUDA_GLOSSARY.md) | Canonical terminology |
| 5 | [`GARUDA_NAVIGATION.md`](GARUDA_NAVIGATION.md) | Document hierarchy and navigation |
| 6 | Applicable GAR Constitutions | Architectural authority — see [`ARCHITECTURE.md`](ARCHITECTURE.md) |
| 7 | Approved Sprint Mission | Current authorized work — see [`docs/sprints/`](docs/sprints/README.md) |

Implementation shall not begin until steps 1 through 7 are completed.

---

# Current Repository Snapshot

Read [`GARUDA_CONTEXT.md`](GARUDA_CONTEXT.md) for authoritative state. Snapshot at document creation:

| Field | Value |
| --- | --- |
| Release | `v0.9.0-alpha` |
| Sprint | GAR-SPRINT-0009 (Complete) |
| Foundations | Platform Core, Memory, Knowledge, Context, Reasoning, Decision, Action, Execution |
| Tests | 712 passing |
| Next milestone | GAR-SPRINT-0010 (planning only — not authorized for implementation) |

If this snapshot conflicts with committed repository state, the committed state takes precedence.

---

# Mission Workflow

After bootstrap, every mission follows this lifecycle:

```
Read Mission Specification
↓
Produce Implementation Plan
↓
Wait for Architecture Approval
↓
Implement Approved Scope Only
↓
Write Tests
↓
Write Documentation
↓
Run Verification
↓
Architecture Review
↓
Git Commit
↓
Completion Report
↓
Stop
```

Never begin the next mission automatically.

Reusable prompts for this workflow are in [`PROMPTS.md`](PROMPTS.md).

Document templates are in [`templates/`](templates/README.md).

---

# Approval Gates

- No implementation begins without explicit architecture approval.
- Plans are reviewed before coding.
- Every completed mission requires architecture review.
- Git tags require separate explicit approval.
- One mission. One commit.

If approval is withheld: stop, do not modify the repository, wait for revised instructions.

---

# Authority Order

When documents conflict, resolve in this order:

1. GAR Constitutions (GAR-0001 through GAR-0016)
2. Approved Sprint Documents
3. Committed Repository State
4. [`VERSION`](VERSION)
5. Release Documentation
6. [`GARUDA_CONTEXT.md`](GARUDA_CONTEXT.md)
7. Engineering Governance documents

Never infer architecture from code alone.

---

# Absolute Prohibitions

- Never invent architecture.
- Never implement future sprint missions.
- Never modify GAR constitutional documents without approval.
- Never rename canonical objects.
- Never add persistence, REST, execution engines, scheduling, orchestration, AI behaviour,
  workflow engines, or frontend features outside approved scope.
- Never modify unrelated packages.
- Never fake tests, documentation, or completion.

---

# Local Development Bootstrap

This is separate from the AI engineering bootstrap sequence above.

To set up the local development environment:

```bash
make bootstrap
```

See [`README.md`](README.md) for full setup, validation, and quick-start commands.

---

# Related Documents

| Document | Role |
| --- | --- |
| [`GARUDA_NAVIGATION.md`](GARUDA_NAVIGATION.md) | Engineering governance entry point |
| [`docs/README.md`](docs/README.md) | Documentation and governance index |
| [`docs/developer-onboarding.md`](docs/developer-onboarding.md) | Human contributor onboarding |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Contribution requirements |

---

# Change Policy

Update this document when:

- The repository bootstrap sequence changes
- Engineering governance structure changes
- A new release milestone requires snapshot updates

Do not use this document to introduce architectural decisions. Architectural decisions belong in GAR
constitutions and approved sprint documents.

---

End of BOOTSTRAP.md
