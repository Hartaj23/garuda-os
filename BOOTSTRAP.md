# PROJECT GARUDA

# BOOTSTRAP.md

Institutional Bootstrap Guide

Version: 2.0

Last Updated: 2026-07-07

Document Owner: Project Garuda Engineering Governance

---

# Purpose

This document is the institutional entry point for every new architecture thread, AI coding agent,
and engineering contributor initializing work in Project Garuda.

Project Garuda has crossed an important threshold: future work inherits a mature engineering system
rather than creating one. This bootstrap establishes the frozen governance baseline from which all
new foundational work begins.

For architectural synthesis, read [`PROJECT_GARUDA_MASTER.md`](PROJECT_GARUDA_MASTER.md). For the
complete engineering handbook, read [`GAR-REFERENCE-0001.md`](GAR-REFERENCE-0001.md).

Do not begin implementation until the full bootstrap sequence is complete and explicit architecture
approval is granted.

---

# Reference Principle

This bootstrap describes the repository as it exists at publication. It is descriptive rather than
normative. Where conflict exists, GAR constitutions, ADRs, approved sprint specifications, and the
committed repository always take precedence.

---

# Repository as Single Source of Truth

The Git repository is the authoritative record of Project Garuda.

- Implemented behavior lives in committed code and tests
- Constitutional authority lives in ratified GAR documents
- Architectural decisions live in approved ADRs
- Authorized work lives in approved sprint specifications
- Institutional state lives in release artifacts, closure reports, and synchronized context documents

Never infer architecture from code alone. Never treat conversation context as authority over the
repository.

---

# Frozen Governance Baseline

The following are frozen and SHALL NOT be reopened without explicit constitutional authorization:

| Area | Status |
| --- | --- |
| Phase I foundations | Complete and immutable |
| GAR-0001 through GAR-0017 | Frozen at v1.0 |
| ADR-0001 through ADR-0011 | Approved and frozen |
| GAR-SPRINT-0001 through GAR-SPRINT-0010 | Closed |
| Release `v0.10.0-alpha` | Published |
| GAR-REFERENCE-0001 | Published |

Completed sprints, release artifacts, and constitutional documents are historical records. Post-release
documentation maintenance does not reopen closed sprints.

---

# Architectural Authority versus Implementation Authority

| Role | Authority | Responsibility |
| --- | --- | --- |
| Founder | Ratification | Ratifies constitutions and releases |
| Chief Systems Architect | Architecture | Drafts constitutions, ADRs, sprint specifications; reviews missions |
| Principal Implementation Engineer | Implementation | Plans, implements, tests, and documents under approved scope only |

AI coding agents are implementation engineers, not architects.

- Constitutional drafting requires Founder authorization
- ADR drafting requires architectural authority
- Sprint specification requires approved constitutional chain
- Implementation requires approved mission plan and architecture review

---

# Canonical Sprint Exemplar

**GAR-SPRINT-0010** is the Canonical Foundation Reference for Phase II.

Future foundational sprints inherit — not recreate — Sprint 0010 institutional assets:

- Constitutional chain (GAR → ADR → Sprint)
- Mission sequence (Alpha through India)
- Certification model (Mission Golf)
- SDK documentation model (Mission Hotel)
- Institutional release model (Mission India)
- Governance baseline sequence

See [`GAR-REFERENCE-0001.md`](GAR-REFERENCE-0001.md) Section 16 for the complete canonical index.

---

# Garuda Engineering Standard

Every foundational sprint follows this lifecycle:

```
Constitution
      ↓
Architecture
      ↓
Sprint Specification
      ↓
Mission Planning
      ↓
Implementation
      ↓
Verification
      ↓
Certification
      ↓
Developer Enablement
      ↓
Institutional Release
      ↓
Published Release
      ↓
Governance Baseline
```

This sequence is established engineering standard — not experimental process.

---

# Institutional Layers

Project Garuda possesses five permanent institutional layers:

| Layer | Artifact type | Status |
| --- | --- | --- |
| Constitutional | GAR documents | Established |
| Architectural | ADRs | Established |
| Engineering | Sprint specifications and missions | Established |
| Institutional | Releases, certification, closure reports | Established |
| Reference | GAR-REFERENCE documents | Established |

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
| 6 | [`GAR-REFERENCE-0001.md`](GAR-REFERENCE-0001.md) | Constitutional engineering reference manual |
| 7 | Applicable GAR Constitutions | Architectural authority — see [`ARCHITECTURE.md`](ARCHITECTURE.md) |
| 8 | Approved Sprint Mission | Current authorized work — see [`docs/sprints/`](docs/sprints/README.md) |

Implementation shall not begin until steps 1 through 8 are completed and explicit approval is granted.

---

# Authority Order

When documents conflict, resolve in this order:

1. GAR Constitutions (GAR-0001 through GAR-0017 and successors)
2. Architecture Decision Records
3. Approved Sprint Documents
4. Committed Repository State
5. [`VERSION`](VERSION)
6. Release Documentation
7. [`GARUDA_CONTEXT.md`](GARUDA_CONTEXT.md)
8. Engineering Governance documents
9. Descriptive references (including this document and GAR-REFERENCE-0001)

---

# Variable State (Updated Per Release)

The following sections change as releases complete. All other sections remain intentionally stable.

## Current Release

| Field | Value |
| --- | --- |
| Release | `v0.10.0-alpha` |
| Tag | `v0.10.0-alpha` on commit `369a93b` |
| Governance baseline commit | `a3f2ba3` |
| Tests at baseline | 806 passed |

## Completed Constitutions

| Document | Status |
| --- | --- |
| GAR-0001 through GAR-0016 | Frozen v1.0 — Phase I |
| GAR-0017 | Frozen v1.0 — Phase II Constitutional Extension |
| GAR-0018 | Frozen v1.0 — Phase II Constitutional Extension (Integration) |
| GAR-0019 | Ratified v1.0 — External Capability Expansion (Runtime) |

## Completed ADRs

| ADR | Foundation |
| --- | --- |
| ADR-0001 through ADR-0010 | Phase I foundations |
| ADR-0011 | Interface Foundation (Phase II) |
| ADR-0012 | Integration Foundation (Phase II) |
| ADR-0013 | Runtime Foundation (External Capability Expansion) |

## Completed Foundations

| Foundation | Release | Phase |
| --- | --- | --- |
| Platform Core | `v0.2.0-alpha` | Phase I |
| Memory | `v0.3.0-alpha` | Phase I |
| Knowledge | `v0.4.0-alpha` | Phase I |
| Context | `v0.5.0-alpha` | Phase I |
| Reasoning | `v0.6.0-alpha` | Phase I |
| Decision | `v0.7.0-alpha` | Phase I |
| Action | `v0.8.0-alpha` | Phase I |
| Execution | `v0.9.0-alpha` | Phase I |
| Interface | `v0.10.0-alpha` | Phase II |
| Integration | `v0.11.0-alpha` | Phase II |
| Runtime | `v0.12.0-alpha` | External Capability Expansion |

## Canonical Sprint

| Field | Value |
| --- | --- |
| Canonical exemplar | GAR-SPRINT-0012 — Runtime Foundation |
| Reference manual | GAR-REFERENCE-0001 |

## Repository Status

| Field | Value |
| --- | --- |
| Repository State | Published |
| Working Tree | Clean (excluding local `.cursor/`) |
| Current Release | `v0.12.0-alpha` |
| Governance Baseline | Checkpoint 029 (Frozen) |

If this snapshot conflicts with committed repository state, the committed state takes precedence.

---

# Current Engineering Posture

GAR-SPRINT-0012 is **complete and closed** at `v0.12.0-alpha`.

The institution is in **Institutional HOLD**. No sprint is authorized automatically.

The repository records the current baseline (`v0.12.0-alpha`). Governance pauses between cycles.

Architecture 5 is closed. Founder Decision adopted the Institutional Strategic Lifecycle v1.0,
Certification as a permanent engineering phase, `docs/governance/GAR-ROADMAP.md`, and Institutional
HOLD terminology. See [`docs/governance/`](docs/governance/README.md).

Future sprint work requires separate constitutional review and Founder authorization.

---

# Mission Workflow

After bootstrap, every authorized mission follows this lifecycle:

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

Reusable prompts: [`PROMPTS.md`](PROMPTS.md) *(if present)*

Document templates: [`templates/`](templates/README.md)

---

# Approval Gates

- No implementation begins without explicit architecture approval
- Plans are reviewed before coding
- Every completed mission requires architecture review
- Git tags require separate explicit approval
- One mission. One commit

If approval is withheld: stop, do not modify the repository, wait for revised instructions.

---

# Absolute Prohibitions

- Never invent architecture
- Never implement future sprint missions
- Never modify GAR constitutional documents without approval
- Never reopen closed sprints or release artifacts
- Never rename canonical objects
- Never add persistence, REST, execution engines, scheduling, orchestration, AI behaviour,
  workflow engines, or frontend features outside approved scope
- Never modify unrelated packages
- Never fake tests, documentation, or completion

---

# Local Development Bootstrap

This is separate from the AI engineering bootstrap sequence above.

```bash
make bootstrap
```

See [`README.md`](README.md) for full setup, validation, and quick-start commands.

---

# Related Documents

| Document | Role |
| --- | --- |
| [`GAR-REFERENCE-0001.md`](GAR-REFERENCE-0001.md) | Constitutional engineering reference manual |
| [`GARUDA_NAVIGATION.md`](GARUDA_NAVIGATION.md) | Engineering governance entry point |
| [`GAR-CODEX-CONTEXT.md`](GAR-CODEX-CONTEXT.md) | Codex operational context |
| [`docs/README.md`](docs/README.md) | Documentation and governance index |
| [`docs/developer-onboarding.md`](docs/developer-onboarding.md) | Human contributor onboarding |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Contribution requirements |

---

# Change Policy

**Stable sections** (change only when engineering process evolves):

- Purpose, authority model, institutional layers, engineering standard, bootstrap sequence, prohibitions

**Variable sections** (update at each release baseline):

- Current Release
- Completed Foundations
- Completed ADRs
- Completed Constitutions
- Repository Status
- Canonical Sprint (when a newer sprint supersedes the exemplar)

Do not use this document to introduce architectural decisions. Architectural decisions belong in GAR
constitutions and approved sprint documents.

---

End of BOOTSTRAP.md
