# PROJECT GARUDA

# PROJECT_GARUDA_MASTER.md

Project Garuda Master Architectural Reference

Version: 1.0

Last Updated: 2026-07-06

Document Owner: Project Garuda Engineering Governance

Status: Living architectural reference — not a constitutional document

---

# Document Authority

`PROJECT_GARUDA_MASTER.md` is the primary architectural onboarding and continuity reference for
Project Garuda.

It synthesizes the current architecture, repository, sprint history, and engineering approach.

It does not replace:

- GAR Constitutions (architectural authority)
- Approved Sprint Specifications (implementation authority)
- Committed Repository State (implementation truth)
- [`GARUDA_CONTEXT.md`](GARUDA_CONTEXT.md) (live operational state)

When conflicts exist, precedence shall be:

1. GAR Constitutions
2. Approved Sprint Specifications
3. Committed Repository State
4. [`VERSION`](VERSION) / Release Documentation
5. [`GARUDA_CONTEXT.md`](GARUDA_CONTEXT.md)
6. `PROJECT_GARUDA_MASTER.md`
7. Engineering Handbook

Part IV contains executive summaries only — never substitutes for full GAR text.

---

# Table of Contents

- [Part I — Executive Overview](#part-i--executive-overview)
- [Part II — Current Project Status](#part-ii--current-project-status)
- [Part III — Repository Architecture](#part-iii--repository-architecture)
- [Part IV — Constitutional Architecture](#part-iv--constitutional-architecture)
- [Part V — Foundation Map](#part-v--foundation-map)
- [Part VI — Sprint History](#part-vi--sprint-history)
- [Part VII — Engineering Governance](#part-vii--engineering-governance)
- [Part VIII — System Roadmap](#part-viii--system-roadmap)
- [Part IX — Architectural Dependency Graph](#part-ix--architectural-dependency-graph)
- [Part X — Current Priorities](#part-x--current-priorities)
- [Part XI — Lessons Learned](#part-xi--lessons-learned)
- [Part XII — Bootstrap for New Threads](#part-xii--bootstrap-for-new-threads)

---

# Part I — Executive Overview

## Vision

Project Garuda is a **constitutional operating system for intelligent autonomous systems** — an
Operating System for Human Intelligence.

Garuda is not an application, a trading system, or a single AI product. It is a platform for
building deterministic, reviewable, service-independent cognitive infrastructure through
constitutional engineering.

## Mission

Build Project Garuda correctly — preserving architectural integrity above implementation speed.

The objective is not to generate code. The objective is to construct a durable platform where every
foundation is deterministic, every sprint is constitutional, and every implementation is
reviewable.

## Philosophy — Constitutional Engineering

Project Garuda follows **Constitutional Engineering**:

- Architecture always precedes implementation
- Correctness always precedes speed
- Determinism always precedes convenience
- Every implementation must be reviewable
- Every change must preserve prior foundations
- AI agents are implementation engineers — not architects

Architecture may evolve only through approved constitutional documents and approved sprint missions.

## Why Garuda Exists

Human intelligence operating at scale requires more than models and applications. It requires:

- Stable object identity and lifecycle
- Deterministic serialization and validation
- Descriptive contracts that do not smuggle in runtime behavior
- Cross-foundation compatibility
- Governance that survives team and tool changes

Garuda provides the platform layer for these capabilities without binding to vendors, services, or
deployment targets.

## Long-Term Vision (5–10 Years)

Garuda aims to become a complete cognitive operating system — from universal objects through memory,
knowledge, context, reasoning, decision, action, and execution — extending toward orchestration,
persistence, and autonomous operation **only through approved constitutional evolution**.

No long-term capability in this document authorizes implementation. Future phases require GAR
constitutions and approved sprint plans.

## Design Principles

| Principle | Meaning |
| --- | --- |
| Determinism | Identical inputs produce identical outputs |
| Immutability | Value models do not mutate after construction where designed |
| Platform neutrality | Independent of vendors, services, and deployment targets |
| Service independence | No application-specific or infrastructure-specific behavior in foundations |
| Architecture first | Design before code; stop on ambiguity |
| Certification | Cross-foundation interoperability verified before release |
| One mission, one commit | Reviewable, traceable delivery units |
| Preserve foundations | Every new layer builds on all prior layers |

## Roles

| Role | Holder | Responsibility |
| --- | --- | --- |
| Founder & Vision Holder | Hartaj Sahdra | Vision and project direction |
| Chief Systems Architect | ChatGPT | Architecture, sprint design, constitutional review |
| Principal Implementation Engineer | AI Coding Agent (Cursor) | Approved-scope implementation only |
| Source of Truth | Git repository | Committed state, tests, documentation |

---

# Part II — Current Project Status

## Current Release

| Field | Value |
| --- | --- |
| Version | `v0.10.0-alpha` |
| Git tag | `v0.10.0-alpha` — *not created — pending explicit approval* |
| Sprint | GAR-SPRINT-0010 (Complete) |
| Theme | Interface Foundation (Phase II) |
| Architecture baseline | GAR-0017 |

## Current Sprint

| Field | Value |
| --- | --- |
| Active sprint | None — GAR-SPRINT-0010 complete |
| Status | Awaiting approval to tag `v0.10.0-alpha` |
| Authorization | No implementation authorized |

## Completed Foundations

| # | Foundation | Package | Release | Status |
| --- | --- | --- | --- | --- |
| — | Platform Core | `packages/objects` | `v0.2.0-alpha` | Complete |
| 1 | Memory | `packages/memory` | `v0.3.0-alpha` | Complete |
| 2 | Knowledge | `packages/knowledge` | `v0.4.0-alpha` | Complete |
| 3 | Context | `packages/context` | `v0.5.0-alpha` | Complete |
| 4 | Reasoning | `packages/reasoning` | `v0.6.0-alpha` | Complete |
| 5 | Decision | `packages/decision` | `v0.7.0-alpha` | Complete |
| 6 | Action | `packages/action` | `v0.8.0-alpha` | Complete |
| 7 | Execution | `packages/execution` | `v0.9.0-alpha` | Complete |
| 8 | Interface (Phase II) | `packages/interface` | `v0.10.0-alpha` | Complete |

## Engineering Governance

| Field | Value |
| --- | --- |
| Version | Engineering Governance v1.0 |
| Status | Complete — frozen baseline in [`ENGINEERING_GOVERNANCE_v1.0.md`](ENGINEERING_GOVERNANCE_v1.0.md) |
| Introduced | GAR-SPRINT-0009 |

Governance documents: `AGENTS.md`, `GARUDA_CONTEXT.md`, `GARUDA_WORKFLOW.md`, `GARUDA_GLOSSARY.md`,
`GARUDA_NAVIGATION.md`, `BOOTSTRAP.md`, `PROMPTS.md`, `templates/`.

## Repository Health

| Metric | Value |
| --- | --- |
| Foundations completed | 9 (including Platform Core and Interface) |
| Complete test suite | 806 passing |
| Interface Foundation suite | PASS |
| Repository foundation validation | PASS |
| Engineering toolchain validation | PASS |
| Repository status | Clean (tracked files) |

## Release History

| Version | Sprint | Foundation / Theme | Git Tag |
| --- | --- | --- | --- |
| `v0.1.0-alpha` | GAR-SPRINT-0001 | Repository & engineering platform | Tagged |
| `v0.2.0-alpha` | GAR-SPRINT-0002 | Platform Core (Universal Object System) | Tagged |
| `v0.3.0-alpha` | GAR-SPRINT-0003 | Memory Foundation | Tagged |
| `v0.4.0-alpha` | GAR-SPRINT-0004 | Knowledge Foundation | Tagged |
| `v0.5.0-alpha` | GAR-SPRINT-0005 | Context Foundation | Tagged |
| `v0.6.0-alpha` | GAR-SPRINT-0006 | Reasoning Foundation | Tagged |
| `v0.7.0-alpha` | GAR-SPRINT-0007 | Decision Foundation | Release prepared — tag not in repository |
| `v0.8.0-alpha` | GAR-SPRINT-0008 | Action Foundation | Release prepared — tag not in repository |
| `v0.9.0-alpha` | GAR-SPRINT-0009 | Execution Foundation | Tagged |
| `v0.10.0-alpha` | GAR-SPRINT-0010 | Interface Foundation (Phase II) | Release prepared — tag pending approval |

Release notes: [`docs/releases/`](docs/releases/README.md). Changelog: [`CHANGELOG.md`](CHANGELOG.md).

## Intentionally Unimplemented

The following remain outside the current release until explicitly approved:

Workflow engine, execution engine (runtime), scheduling, orchestration, search, persistence, REST
APIs, frontend runtime behavior, AI runtime behavior, autonomous behavior, trading systems,
portfolio systems, broker integrations, knowledge graph engines, query engines, retrieval engines.

---

# Part III — Repository Architecture

## Repository Map

```
Garuda/
├── PROJECT_GARUDA_MASTER.md    ← This document
├── BOOTSTRAP.md                ← AI engineer quick-start
├── AGENTS.md                   ← AI operating manual
├── GARUDA_*.md                 ← Governance handbook
├── ENGINEERING_GOVERNANCE_v1.0.md
├── VERSION / CHANGELOG.md / README.md
├── packages/                   ← Production foundations
├── tests/                      ← Repository test suite
├── docs/                       ← Architecture, engineering, SDK, sprints, releases
├── scripts/                    ← Validation and tooling
├── apps/                       ← Application shells (not foundation logic)
├── services/                   ← Service boundaries (future)
└── infrastructure/             ← Infrastructure boundaries (future)
```

## packages/

Service-independent foundation packages. Each package preserves Platform Core and all prior
foundations.

| Package | Responsibility |
| --- | --- |
| `packages/objects` | Platform Core — universal objects, registry, serialization, relationships, lifecycle, validation |
| `packages/memory` | Memory objects, provenance, index/retrieval contracts, reference store |
| `packages/knowledge` | Knowledge objects, evidence/provenance, classification/query contracts, reference store |
| `packages/context` | Context objects, source/scope, composition/selection contracts, workspace |
| `packages/reasoning` | Reasoning objects, input/provenance, strategy/chain contracts, workspace |
| `packages/decision` | Decision objects, input/provenance, strategy/chain contracts, workspace |
| `packages/action` | Action objects, input/provenance, strategy/chain contracts, workspace |
| `packages/execution` | Execution objects, input/provenance, strategy/chain contracts, workspace |

## docs/

| Directory | Purpose |
| --- | --- |
| `docs/architecture/` | Architecture documentation per foundation module |
| `docs/engineering/` | Engineering implementation notes |
| `docs/sdk/` | Public SDK documentation per foundation |
| `docs/sprints/` | Sprint certification and closure reports |
| `docs/releases/` | Release notes |

Index: [`docs/README.md`](docs/README.md). Architecture index: [`docs/architecture/README.md`](docs/architecture/README.md).

## tests/

Mission-scoped and foundation-scoped unit tests under `tests/`. Naming convention:
`test_<foundation>_<module>.py`, certification suites per sprint Golf mission.

Validation entry point: [`scripts/run_checks.py`](scripts/run_checks.py).

## scripts/

Repository validation, toolchain validation, Docker compose validation (optional). See
[`scripts/README.md`](scripts/README.md).

## Engineering Layer

```
GAR Constitutions
        ↓
PROJECT_GARUDA_MASTER.md  (this document — synthesis)
        ↓
Engineering Handbook (AGENTS, GARUDA_*, BOOTSTRAP)
        ↓
Repository (packages, tests, docs)
```

## AI Workflow

Every mission:

```
Mission Specification → Implementation Plan → Architecture Approval
→ Implementation → Testing → Documentation → Verification
→ Architecture Review → Commit → Completion Report → Stop
```

Implementation agents: [`BOOTSTRAP.md`](BOOTSTRAP.md). Architecture threads: Part XII of this
document.

## Testing Philosophy

- Every mission writes tests
- Deterministic behavior verified through unit tests and certification suites
- Complete non-backend suite run before mission completion
- Repository foundation and toolchain validation mandatory
- Failures reported honestly — never suppressed

## Documentation Hierarchy

| Level | Documents |
| --- | --- |
| Constitutional | GAR-0001 through GAR-0024 (external to repository text) |
| Master reference | `PROJECT_GARUDA_MASTER.md` |
| Operational state | `GARUDA_CONTEXT.md` |
| Implementation behavior | `docs/architecture/`, `docs/engineering/`, `docs/sdk/` |
| Sprint audit trail | `docs/sprints/*-closure-report.md` |
| Release audit trail | `docs/releases/v0.*.md` |

---

# Part IV — Constitutional Architecture

Executive architectural summaries. Full GAR constitution text is not stored in this repository.
Refer to external GAR documents for authoritative constitutional language.

**Frozen at v1.0 in repository:** GAR-0001 through GAR-0016 (`GAR-CODEX-CONTEXT.md`). Future
changes require Architecture Change Proposals under GAR-0016.

## GAR Document Index

| Document | Purpose (Summary) | Scope (Summary) | Status |
| --- | --- | --- | --- |
| GAR-INDEX | Constitutional index and navigation | All GAR documents | Approved |
| GAR-0001 | Project constitution — vision, principles, boundaries | Entire project | Frozen v1.0 |
| GAR-0002 | Platform and system boundaries | Core platform scope | Referenced |
| GAR-0003 | Application architecture | Application layer boundaries | Referenced |
| GAR-0003A | Application architecture extension | Application variants | Referenced |
| GAR-0004 | Package and module architecture | `packages/` structure | Referenced |
| GAR-0005 | Agent architecture | Agent layer boundaries | Referenced |
| GAR-0006–GAR-0010 | Platform and service architecture layers | Services, packages | Referenced |
| GAR-0011 | Reference architecture | System-wide reference model | Referenced — primary architecture doc |
| GAR-0012 | Developer playbook | Contributor engineering rules | Referenced |
| GAR-0013 | AI coding agent operating manual | AI agent behavior (superseded in repo by AGENTS.md) | Referenced |
| GAR-0014–GAR-0015 | Extended architecture governance | Architecture evolution | Referenced |
| GAR-0016 | Architecture change proposals | Constitutional evolution process | Frozen v1.0 — in VERSION |
| GAR-0017–GAR-0024 | Extended constitutional scope | Future constitutional layers | Referenced in navigation — not detailed in repository |

## Key Constitutional Decisions (Repository-Traceable)

| Decision | Effect |
| --- | --- |
| Constitutional engineering | Architecture precedes all implementation |
| Universal Object System | All foundations inherit Platform Core |
| Descriptive contracts | Strategy, chain, index, query contracts do not execute |
| Workspaces | Process-local, non-persistent, exact identifier operations |
| Certification missions | Golf missions verify cross-foundation interoperability |
| Mission India | Release preparation is documentation-only |
| GAR-0016 | No constitutional change without approved change proposal |

## Dependencies Between Constitutional Layers

```
GAR-0001 (Constitution)
    ↓
GAR-0011 (Reference Architecture)
    ↓
GAR-0004 (Packages) + GAR-0010 (Services)
    ↓
Approved Sprint Documents
    ↓
Repository Implementation
```

---

# Part V — Foundation Map

Each foundation follows the sprint mission pattern: Alpha → Bravo → Charlie → Delta → Echo →
Foxtrot → Golf → Hotel → India.

Common pattern per foundation:

- **Alpha** — Universal framework (core object + primitives)
- **Bravo** — Input and provenance
- **Charlie** — Serialization and validation certification
- **Delta** — Strategy contract (descriptive)
- **Echo** — Chain contract (descriptive)
- **Foxtrot** — Workspace (process-local)
- **Golf** — Platform integration certification
- **Hotel** — SDK documentation
- **India** — Sprint closure and release preparation

---

## Platform Core (`packages/objects`)

| Field | Value |
| --- | --- |
| Sprint | GAR-SPRINT-0002 |
| Release | `v0.2.0-alpha` |
| Purpose | Universal object identity, registry, serialization, relationships, lifecycle, validation |

**Objects:** `CanonicalObject`, `UniversalObject`, `ObjectRegistry`, `ObjectSerializer`,
`ValidationResult`, lifecycle and relationship models.

**Capabilities:** Deterministic object identity; registry; serialization framework; relationship
model; lifecycle events; validation framework.

**Architecture:** [`docs/architecture/`](docs/architecture/README.md) — Core Object Framework through
Universal Object Validation.

**Tests:** Platform Core mission and certification suites.

**SDK:** [`docs/sdk/platform-core/`](docs/sdk/platform-core/README.md)

**Known limitations:** Foundation-specific payload fields may not appear in `ObjectSerializer.serialize()` output under current Platform Core contract.

**Future extensions:** Only through approved constitutional and sprint changes.

---

## Memory Foundation (`packages/memory`)

| Field | Value |
| --- | --- |
| Sprint | GAR-SPRINT-0003 |
| Release | `v0.3.0-alpha` |
| Purpose | Descriptive memory objects with provenance, index and retrieval contracts |

**Objects:** `UniversalMemory`, memory source/provenance, index contract, retrieval contract,
in-memory reference store.

**Contracts:** Memory Index Contract, Memory Retrieval Contract — descriptive, non-executing.

**SDK:** [`docs/sdk/memory-foundation/`](docs/sdk/memory-foundation/README.md)

**Closure:** [`docs/sprints/GAR-SPRINT-0003-closure-report.md`](docs/sprints/GAR-SPRINT-0003-closure-report.md)

---

## Knowledge Foundation (`packages/knowledge`)

| Field | Value |
| --- | --- |
| Sprint | GAR-SPRINT-0004 |
| Release | `v0.4.0-alpha` |
| Purpose | Descriptive knowledge objects with evidence, classification and query contracts |

**Objects:** `UniversalKnowledge`, origin/evidence/provenance, classification contract, query
contract, reference store.

**Contracts:** Knowledge Classification Contract, Knowledge Query Contract — descriptive only.

**SDK:** [`docs/sdk/knowledge-foundation/`](docs/sdk/knowledge-foundation/README.md)

**Closure:** [`docs/sprints/GAR-SPRINT-0004-closure-report.md`](docs/sprints/GAR-SPRINT-0004-closure-report.md)

---

## Context Foundation (`packages/context`)

| Field | Value |
| --- | --- |
| Sprint | GAR-SPRINT-0005 |
| Release | `v0.5.0-alpha` |
| Purpose | Descriptive context objects with source/scope, composition and selection |

**Objects:** `UniversalContext`, source/scope framework, composition contract, selection contract,
context workspace.

**SDK:** [`docs/sdk/context-foundation/`](docs/sdk/context-foundation/README.md)

**Closure:** [`docs/sprints/GAR-SPRINT-0005-closure-report.md`](docs/sprints/GAR-SPRINT-0005-closure-report.md)

---

## Reasoning Foundation (`packages/reasoning`)

| Field | Value |
| --- | --- |
| Sprint | GAR-SPRINT-0006 |
| Release | `v0.6.0-alpha` |
| Purpose | Descriptive reasoning objects with strategy and chain contracts |

**Objects:** `UniversalReasoning`, input/provenance, strategy contract, chain contract, workspace.

**SDK:** [`docs/sdk/reasoning-foundation/`](docs/sdk/reasoning-foundation/README.md)

**Closure:** [`docs/sprints/GAR-SPRINT-0006-closure-report.md`](docs/sprints/GAR-SPRINT-0006-closure-report.md)

---

## Decision Foundation (`packages/decision`)

| Field | Value |
| --- | --- |
| Sprint | GAR-SPRINT-0007 |
| Release | `v0.7.0-alpha` |
| Purpose | Descriptive decision objects with strategy and chain contracts |

**Objects:** `UniversalDecision`, input/provenance, strategy contract, chain contract, workspace.

**SDK:** [`docs/sdk/decision-foundation/`](docs/sdk/decision-foundation/README.md)

**Closure:** [`docs/sprints/GAR-SPRINT-0007-closure-report.md`](docs/sprints/GAR-SPRINT-0007-closure-report.md)

---

## Action Foundation (`packages/action`)

| Field | Value |
| --- | --- |
| Sprint | GAR-SPRINT-0008 |
| Release | `v0.8.0-alpha` |
| Purpose | Descriptive action objects with strategy and chain contracts |

**Objects:** `UniversalAction`, input/provenance, strategy contract, chain contract, workspace.

**SDK:** [`docs/sdk/action-foundation/`](docs/sdk/action-foundation/README.md)

**Closure:** [`docs/sprints/GAR-SPRINT-0008-closure-report.md`](docs/sprints/GAR-SPRINT-0008-closure-report.md)

---

## Execution Foundation (`packages/execution`)

| Field | Value |
| --- | --- |
| Sprint | GAR-SPRINT-0009 |
| Release | `v0.9.0-alpha` |
| Purpose | Descriptive execution objects with strategy and chain contracts |

**Objects:** `UniversalExecution`, `ExecutionInputCollection`, `ExecutionProvenance`,
`ExecutionStrategy`, `ExecutionStrategyContract`, `ExecutionChain`, `ExecutionChainContract`,
`ExecutionWorkspace`.

**Contracts:** Strategy and chain contracts are descriptive — no execution behavior.

**SDK:** [`docs/sdk/execution-foundation/`](docs/sdk/execution-foundation/README.md)

**Certification:** [`docs/sprints/GAR-SPRINT-0009-execution-certification.md`](docs/sprints/GAR-SPRINT-0009-execution-certification.md)

**Closure:** [`docs/sprints/GAR-SPRINT-0009-closure-report.md`](docs/sprints/GAR-SPRINT-0009-closure-report.md)

**Known limitations:** Process-local workspace; opaque input references; no execution engines;
`ObjectSerializer` Platform Core field limitation applies.

---

# Part VI — Sprint History

## GAR-SPRINT-0001 — Repository & Engineering Platform

| Field | Value |
| --- | --- |
| Objective | Engineering platform and repository foundation |
| Release | `v0.1.0-alpha` |
| Status | Complete (repository layout, toolchain, validation) |

**Deliverables:** Repository structure, testing foundation, documentation foundation, engineering
toolchain. See [`docs/sprints/GAR-SPRINT-0001-status.md`](docs/sprints/GAR-SPRINT-0001-status.md).

**Explicitly not implemented:** Backend/frontend application logic, Docker runtime, CI/CD, AI,
trading.

---

## GAR-SPRINT-0002 — Platform Core

| Field | Value |
| --- | --- |
| Objective | Universal Object System under `packages/objects` |
| Release | `v0.2.0-alpha` |
| Missions | Alpha through India (9 missions) |

**Deliverables:** Core object framework, registry, serialization, relationships, lifecycle, validation,
certification, SDK. See [`docs/sprints/GAR-SPRINT-0002-closure-report.md`](docs/sprints/GAR-SPRINT-0002-closure-report.md).

---

## GAR-SPRINT-0003 — Memory Foundation

| Field | Value |
| --- | --- |
| Release | `v0.3.0-alpha` |
| Package | `packages/memory` |

Closure: [`docs/sprints/GAR-SPRINT-0003-closure-report.md`](docs/sprints/GAR-SPRINT-0003-closure-report.md)

---

## GAR-SPRINT-0004 — Knowledge Foundation

| Field | Value |
| --- | --- |
| Release | `v0.4.0-alpha` |
| Package | `packages/knowledge` |

Closure: [`docs/sprints/GAR-SPRINT-0004-closure-report.md`](docs/sprints/GAR-SPRINT-0004-closure-report.md)

---

## GAR-SPRINT-0005 — Context Foundation

| Field | Value |
| --- | --- |
| Release | `v0.5.0-alpha` |
| Package | `packages/context` |

Closure: [`docs/sprints/GAR-SPRINT-0005-closure-report.md`](docs/sprints/GAR-SPRINT-0005-closure-report.md)

---

## GAR-SPRINT-0006 — Reasoning Foundation

| Field | Value |
| --- | --- |
| Release | `v0.6.0-alpha` |
| Package | `packages/reasoning` |

Closure: [`docs/sprints/GAR-SPRINT-0006-closure-report.md`](docs/sprints/GAR-SPRINT-0006-closure-report.md)

---

## GAR-SPRINT-0007 — Decision Foundation

| Field | Value |
| --- | --- |
| Release | `v0.7.0-alpha` |
| Package | `packages/decision` |

Closure: [`docs/sprints/GAR-SPRINT-0007-closure-report.md`](docs/sprints/GAR-SPRINT-0007-closure-report.md)

---

## GAR-SPRINT-0008 — Action Foundation

| Field | Value |
| --- | --- |
| Release | `v0.8.0-alpha` |
| Package | `packages/action` |

Closure: [`docs/sprints/GAR-SPRINT-0008-closure-report.md`](docs/sprints/GAR-SPRINT-0008-closure-report.md)

---

## GAR-SPRINT-0009 — Execution Foundation

| Field | Value |
| --- | --- |
| Release | `v0.9.0-alpha` |
| Package | `packages/execution` |
| Engineering Governance | v1.0 introduced |

**Missions:** Alpha (Universal Execution) → India (Release Preparation).

**Deliverables:** Full execution foundation, certification, SDK, release notes, governance layer.

Closure: [`docs/sprints/GAR-SPRINT-0009-closure-report.md`](docs/sprints/GAR-SPRINT-0009-closure-report.md)

**Lessons:** Mission India is documentation-only; Engineering Governance formalized AI agent workflow;
certification suite validates full foundation stack coexistence.

---

# Part VII — Engineering Governance

Engineering Governance v1.0 defines **how** Project Garuda is built. It does not define **what**
Garuda is — that belongs to GAR Constitutions.

## How the Documents Fit Together

| Document | Role | Changes |
| --- | --- | --- |
| [`AGENTS.md`](AGENTS.md) | AI engineering operating manual — behavior rules | Rare |
| [`GARUDA_CONTEXT.md`](GARUDA_CONTEXT.md) | Live repository state — current sprint, health, foundations | Every sprint |
| [`GARUDA_WORKFLOW.md`](GARUDA_WORKFLOW.md) | Engineering lifecycle from plan to commit | Rare |
| [`GARUDA_GLOSSARY.md`](GARUDA_GLOSSARY.md) | Canonical terminology | Occasional |
| [`GARUDA_NAVIGATION.md`](GARUDA_NAVIGATION.md) | Document hierarchy and entry points | Rare |
| [`BOOTSTRAP.md`](BOOTSTRAP.md) | AI engineer quick-start bootstrap sequence | Occasional |
| [`PROMPTS.md`](PROMPTS.md) | Reusable AI prompt templates | Occasional |
| [`templates/`](templates/README.md) | Mission, review, closure, release templates | Occasional |
| [`ENGINEERING_GOVERNANCE_v1.0.md`](ENGINEERING_GOVERNANCE_v1.0.md) | Frozen baseline record | Frozen |

## Separation of Concerns

```
PROJECT_GARUDA_MASTER.md  → Why, history, roadmap synthesis (this document)
GARUDA_CONTEXT.md         → What is true right now
AGENTS.md                 → How AI engineers must behave
GARUDA_WORKFLOW.md        → How work flows through the lifecycle
GARUDA_GLOSSARY.md        → What words mean
BOOTSTRAP.md              → Fast AI engineer initialization
```

Do not duplicate content across these documents. Link instead.

---

# Part VIII — System Roadmap

**Important:** Future phases described here are architectural placeholders only. No phase beyond
Phase 1 authorizes implementation without approved GAR documents and sprint missions.

## Phase 1 — Cognitive Foundations (Complete)

```
Platform Core → Memory → Knowledge → Context → Reasoning → Decision → Action → Execution
```

| Milestone | Sprint | Release | Status |
| --- | --- | --- | --- |
| Repository platform | GAR-SPRINT-0001 | `v0.1.0-alpha` | Complete |
| Platform Core | GAR-SPRINT-0002 | `v0.2.0-alpha` | Complete |
| Memory | GAR-SPRINT-0003 | `v0.3.0-alpha` | Complete |
| Knowledge | GAR-SPRINT-0004 | `v0.4.0-alpha` | Complete |
| Context | GAR-SPRINT-0005 | `v0.5.0-alpha` | Complete |
| Reasoning | GAR-SPRINT-0006 | `v0.6.0-alpha` | Complete |
| Decision | GAR-SPRINT-0007 | `v0.7.0-alpha` | Complete |
| Action | GAR-SPRINT-0008 | `v0.8.0-alpha` | Complete |
| Execution | GAR-SPRINT-0009 | `v0.9.0-alpha` | Complete |
| Engineering Governance | GAR-SPRINT-0009 | — | Complete |

## Phase 2 — Not Defined in Repository

Purpose, dependencies, expected outcomes, and sprint estimates for Phase 2 require Chief Systems
Architect authorization. GAR-SPRINT-0010 planning is the next approved activity — specification not
yet in repository.

**Status:** Awaiting approved sprint mission specification.

## Phase 3 — Not Defined in Repository

Future platform capabilities (persistence, orchestration, runtime execution, services layer) may
appear in Phase 3 only through constitutional evolution. No Phase 3 scope is authorized from this
document.

**Status:** Not planned in repository.

## Phase 4 — Complete Garuda Operating System

Long-term vision: a complete constitutional operating system for intelligent autonomous systems.

**Status:** Vision only — not authorized for implementation.

---

# Part IX — Architectural Dependency Graph

## Completed Foundation Chain

```
                    ┌─────────────────────┐
                    │    Platform Core    │
                    │  packages/objects   │
                    │   v0.2.0-alpha      │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Memory Foundation  │
                    │  packages/memory    │
                    │   v0.3.0-alpha      │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │Knowledge Foundation │
                    │ packages/knowledge  │
                    │   v0.4.0-alpha      │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Context Foundation  │
                    │  packages/context   │
                    │   v0.5.0-alpha      │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │Reasoning Foundation │
                    │ packages/reasoning  │
                    │   v0.6.0-alpha      │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Decision Foundation │
                    │  packages/decision  │
                    │   v0.7.0-alpha      │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Action Foundation  │
                    │   packages/action   │
                    │   v0.8.0-alpha      │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │Execution Foundation │
                    │ packages/execution  │
                    │   v0.9.0-alpha      │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Future Foundations │
                    │  (Not authorized)   │
                    └─────────────────────┘
```

## Dependency Rules

- Every foundation inherits Platform Core object identity, validation, and serialization contracts
- Every foundation preserves all prior foundations unchanged
- Cross-foundation coexistence verified in each Golf certification mission
- Contracts are descriptive — they never invoke runtime behavior in current releases
- Workspaces depend on their foundation's core object but remain process-local and non-persistent

---

# Part X — Current Priorities

> **Live operational state:** [`GARUDA_CONTEXT.md`](GARUDA_CONTEXT.md) is authoritative for
> day-to-day status. This section is updated at release milestones.

## Today

```
GAR-SPRINT-0010  →  Complete  →  v0.10.0-alpha prepared pending tag approval
        ↓
Future Phase II work  →  Requires separate constitutional authorization
```

| Field | Value |
| --- | --- |
| Current release | `v0.10.0-alpha` (prepared pending tag approval) |
| Completed sprint | GAR-SPRINT-0010 |
| Next sprint | Not authorized |
| Next mission | Not specified |
| Implementation authorized | No |
| Architecture authorized | Awaiting Chief Systems Architect instructions |

## Immediate Actions Available

1. Approve Git tag `v0.10.0-alpha` after review of Mission India institutional commit
2. Authorize next Phase II sprint through constitutional process (GAR-0016 ACP if required)

---

# Part XI — Lessons Learned

Institutional wisdom from nine sprints of constitutional engineering.

## Why Constitutional Engineering Works

Separating **what** (GAR Constitutions) from **how** (Engineering Governance) from **when**
(Sprint missions) prevents architecture drift. Implementation engineers cannot accidentally
redesign the system because architecture changes require explicit constitutional approval.

## Why Deterministic Architecture Matters

Every foundation produces identical outputs for identical inputs. This enables certification,
reproducible tests, and reviewable commits. Non-determinism would make cross-foundation
certification meaningless.

## Why Governance Was Separated from Architecture

`AGENTS.md` and the GARUDA handbook govern engineering behavior without modifying constitutional
law. Engineering Governance v1.0 could be established during Sprint 9 without reopening GAR-0001
through GAR-0016.

## Why Every Sprint Ends with Certification (Golf)

Golf missions add no production functionality. They prove that the new foundation coexists with
Platform Core and every prior foundation. Certification failures block release.

## Why Every Mission Ends with Review

Architecture review confirms scope compliance, constitutional compliance, and repository health.
Mission India adds release documentation only — no code changes — preserving the integrity of
Alpha through Hotel work.

## Why Mission India Is Documentation-Only

Release preparation must not introduce last-minute code changes. VERSION, CHANGELOG, release notes,
and closure reports are the only Mission India deliverables. Tests and packages remain unchanged.

## Why One Mission, One Commit

Traceability. Every commit maps to exactly one approved mission. Reviewers can audit scope by
reading a single diff.

## Why AI Agents Are Implementation Engineers

Architecture invention by coding agents caused drift in early AI-assisted projects. Garuda assigns
architecture to the Chief Systems Architect and implementation to Cursor/Codex-class agents with
explicit approval gates.

## Why Workspaces Are Process-Local

Persistence introduces storage architecture decisions that belong in future approved sprints.
Process-local workspaces prove object identity and reference operations without premature
infrastructure commitment.

## Why Contracts Do Not Execute

Strategy, chain, index, and query contracts describe structure. Execution behavior belongs in
future runtime layers approved through separate constitutional and sprint processes. Mixing
description and execution would violate foundation boundaries.

---

# Part XII — Bootstrap for New Threads

## For Architecture Threads (ChatGPT / Human Architects)

**Start here:**

1. Read **`PROJECT_GARUDA_MASTER.md`** (this document)
2. Read [`GARUDA_CONTEXT.md`](GARUDA_CONTEXT.md) for live state
3. Read applicable GAR Constitutions (external)
4. Read approved sprint mission specification when available
5. Wait for founder direction before generating new architecture

Do not repeat historical discussions unless needed. The repository is the source of truth.

## For Implementation Threads (Cursor / AI Coding Agents)

**Start here:**

1. Read [`BOOTSTRAP.md`](BOOTSTRAP.md)
2. Complete the seven-step bootstrap sequence
3. Read approved sprint mission
4. Produce implementation plan
5. Wait for architecture approval
6. Implement only approved scope

## Role Boundaries

| Role | May Do | Must Not Do |
| --- | --- | --- |
| Chief Systems Architect | Design sprints, missions, constitutions; review | Implement production code |
| Implementation Engineer | Implement approved scope; test; document | Invent architecture; skip approval |
| Founder | Vision; approve releases and direction | — |

## Quick Reference Commands

```bash
# Local development setup (not AI bootstrap)
make bootstrap

# Full validation
.venv/bin/python scripts/run_checks.py

# Complete test suite
.venv/bin/python -m unittest discover tests
```

---

# Document Maintenance

| Part | Update Frequency |
| --- | --- |
| Part II, Part X | Every sprint / release |
| Part V, Part VI | At sprint completion |
| Part VIII | When architect approves roadmap changes |
| Part I, Part XI | Occasionally — architect/founder |
| Part IV | When GAR documents change |
| Part III, VII, IX, XII | Rare |

Version 1.0 target expansion: deepen Part IV GAR summaries, Part VIII phased roadmap, and Part V
foundation chapters toward 40–60 pages as approved content becomes available.

---

End of PROJECT_GARUDA_MASTER.md
