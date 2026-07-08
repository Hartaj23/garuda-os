# PROJECT GARUDA

# GARUDA_CONTEXT.md

Project State & Engineering Context

Version: 1.0

Last Updated: 2026-07-06

---

# Purpose

This document contains the current operational state of Project Garuda.

Unlike `AGENTS.md`, which defines engineering behavior, this document tracks the evolving state of the repository.

It is updated as the project evolves and serves as the primary context source for AI engineers and human contributors.

---

# Context Authority

The current engineering state shall be determined in the following order of precedence:

1. Committed repository state
2. `VERSION`
3. Approved sprint completion reports
4. Release documentation
5. Repository validation results
6. This document

If any discrepancy exists, the committed repository state takes precedence.

This document shall be updated to reflect the repository rather than the repository being changed to match this document.

---

# Project Overview

Project Garuda is a constitutional operating system for intelligent autonomous systems.

Development follows constitutional engineering.

Engineering Governance v1.0 is complete. The frozen baseline is recorded in `ENGINEERING_GOVERNANCE_v1.0.md`.

Architecture is governed by approved GAR constitutions.

Implementation follows approved sprint missions.

---

# Current Repository Status

| Field | Value |
|---|---|
| Repository Status | Clean (tracked files) |
| Current Branch | `master` |
| Current Version | `v0.12.0-alpha` |
| Current Sprint | GAR-SPRINT-0012 (Complete) |
| Current Mission | None — Institutional HOLD |

---

# Foundation Status

## Platform Core

| Field | Value |
|---|---|
| Status | Complete |
| Release | `v0.2.0-alpha` |

---

## Memory Foundation

| Field | Value |
|---|---|
| Status | Complete |
| Release | `v0.3.0-alpha` |

---

## Knowledge Foundation

| Field | Value |
|---|---|
| Status | Complete |
| Release | `v0.4.0-alpha` |

---

## Context Foundation

| Field | Value |
|---|---|
| Status | Complete |
| Release | `v0.5.0-alpha` |

---

## Reasoning Foundation

| Field | Value |
|---|---|
| Status | Complete |
| Release | `v0.6.0-alpha` |

---

## Decision Foundation

| Field | Value |
|---|---|
| Status | Complete |
| Release | `v0.7.0-alpha` |

---

## Action Foundation

| Field | Value |
|---|---|
| Status | Complete |
| Release | `v0.8.0-alpha` |

---

## Execution Foundation

| Field | Value |
|---|---|
| Status | Complete |
| Release | `v0.9.0-alpha` |

---

## Interface Foundation

| Field | Value |
|---|---|
| Status | Complete |
| Release | `v0.10.0-alpha` |
| Phase | Phase II |
| Constitutional authority | GAR-0017 v1.0 |

---

## Integration Foundation

| Field | Value |
|---|---|
| Status | Complete |
| Release | `v0.11.0-alpha` |
| Phase | Phase II |
| Constitutional authority | GAR-0018 v1.0 |

---

## Runtime Foundation

| Field | Value |
|---|---|
| Status | Complete |
| Release | `v0.12.0-alpha` |
| Phase | External Capability Expansion |
| Constitutional authority | GAR-0019 v1.0 |

---

# Repository Health

| Check | Result |
|---|---|
| Runtime Foundation Suite (Alpha–Hotel) | PASS |
| Runtime Foundation Certification (GAR-CERT-S12-001) | PASS |
| Runtime Foundation SDK verification | PASS |
| Integration Foundation Suite (Alpha–Hotel) | PASS |
| Integration Foundation Certification (GAR-CERT-S11-001) | PASS |
| Integration Foundation SDK verification | PASS |
| Interface Foundation Suite (Alpha–Hotel) | PASS |
| Complete Test Suite | 1042 passed |
| Repository Foundation Validation | PASS |
| Engineering Toolchain Validation | PASS |

## Known Environment Limitations

- Docker CLI unavailable in current environment; compose validation skipped
- Backend FastAPI tests require project virtualenv (`.venv`)

---

# Architectural Principles

Current development preserves:

- Platform neutrality
- Deterministic serialization
- Immutable value models where appropriate
- Service independence
- Constitutional engineering
- Cross-foundation compatibility

---

# Active Development Pattern

Every foundation follows:

- Alpha
- Bravo
- Charlie
- Delta
- Echo
- Foxtrot
- Golf
- Hotel
- India

Each mission requires:

- Implementation plan
- Architecture approval
- Production implementation
- Tests
- Documentation
- Verification
- Architecture review
- Git commit

---

# AI Engineering Workflow

Every AI engineer shall:

1. Read `AGENTS.md`
2. Read `GARUDA_CONTEXT.md`
3. Read `GARUDA_WORKFLOW.md`
4. Read `GARUDA_GLOSSARY.md`
5. Read `GARUDA_NAVIGATION.md`
6. Read applicable GAR Constitutions
7. Read the approved sprint mission
8. Produce an implementation plan
9. Wait for architecture approval
10. Implement only approved scope
11. Run verification
12. Produce completion report
13. Stop

Implementation shall not begin until steps 1 through 7 are completed.

---

# Known Repository Limitations

The following systems remain intentionally unimplemented:

- Workflow engine
- Execution engine
- Scheduling
- Orchestration
- Search
- Persistence
- REST APIs
- Frontend
- AI runtime behavior
- Autonomous behavior

These will be introduced only through future approved constitutions and sprint plans.

---

# Institutional Assets

| Asset | Description |
|---|---|
| Garuda OS | Software platform — foundations through `v0.12.0-alpha` |
| Garuda Constitutional Engineering | Institutional method for platform evolution — formalized at Architecture 5 |

See [`docs/governance/GAR-ROADMAP.md`](docs/governance/GAR-ROADMAP.md) for institutional direction (descriptive only).

---

# Next Planned Work

| Field | Value |
|---|---|
| Current Sprint | GAR-SPRINT-0012 (Complete) |
| Current Status | **Institutional HOLD** — no sprint authorized |
| Architecture 5 | Closed — Founder Decision adopted (2026-07-08) |
| Next Milestone | Next constitutional cycle requires separate Founder authorization (GAR-0020 not authorized) |

---

# Change Policy

This document is a living engineering artifact.

Update when:

- Sprint changes
- Mission changes
- Version changes
- Repository health changes
- Foundation status changes
- Major engineering milestones occur

Do not use this document to introduce architectural decisions.

Architectural decisions belong in GAR constitutions.

---

# Maintenance Responsibility

This document shall be updated:

- At sprint completion
- At release preparation
- After major repository validation changes
- When foundation status changes

The document shall never be used to infer future work.

Only completed repository state shall be recorded.

---

End of GARUDA_CONTEXT.md
