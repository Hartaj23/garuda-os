# PROJECT GARUDA

# GARUDA_NAVIGATION.md

Repository Navigation & Engineering Governance v1.0

Version: 1.0

Last Updated: 2026-07-06

Document Owner: Project Garuda Engineering Governance

Change Frequency: Rare

---

# Purpose

This document serves as the entry point into Project Garuda Engineering Governance v1.0.

Every engineer, AI coding agent, reviewer, or contributor should begin here before navigating deeper into the repository.

---

# Governance Hierarchy

```
GAR Constitutions
        ↓
Architecture Decision Records
        ↓
Sprint Specifications
        ↓
Repository
        ↓
GAR-REFERENCE-0001 (descriptive reference)
```

## GAR Constitutions

Defines what Project Garuda is.

- GAR-INDEX
- GAR-0001 through GAR-0024

**Authority:** Highest

## Engineering Handbook

Defines how Project Garuda is built.

- [`PROJECT_GARUDA_MASTER.md`](../PROJECT_GARUDA_MASTER.md) *(architectural synthesis)*
- [`ENGINEERING_GOVERNANCE_v1.0.md`](../ENGINEERING_GOVERNANCE_v1.0.md) *(frozen baseline)*
- `AGENTS.md`
- `GARUDA_CONTEXT.md`
- `GARUDA_WORKFLOW.md`
- `GARUDA_GLOSSARY.md`
- `GARUDA_NAVIGATION.md`
- [`GAR-REFERENCE-0001.md`](../GAR-REFERENCE-0001.md) *(descriptive institutional reference)*
- `PROMPTS.md` *(optional)*
- `templates/`

**Authority:** Engineering governance (GAR-REFERENCE-0001 is descriptive only; not normative)

## Repository

Defines implementation.

- `README.md`
- `VERSION`
- `CHANGELOG.md`
- `packages/`
- `tests/`
- `docs/`
- `scripts/`

**Authority:** Implementation

---

# Repository Entry Point

```
Repository Entry Point
↓
README.md
↓
AGENTS.md
↓
GARUDA_CONTEXT.md
↓
GARUDA_WORKFLOW.md
↓
GARUDA_GLOSSARY.md
↓
GARUDA_NAVIGATION.md
↓
Mission Specification
↓
Implementation
```

---

# Engineering Document Hierarchy

The engineering governance documents shall be read in the following order.

## Governance Documents

| Document | Purpose | Change Frequency |
| --- | --- | --- |
| `AGENTS.md` | AI engineering operating manual | Rare |
| `GARUDA_CONTEXT.md` | Current repository state | Every sprint |
| `GARUDA_WORKFLOW.md` | Engineering lifecycle | Rare |
| `GARUDA_GLOSSARY.md` | Canonical terminology | Occasional |
| `GARUDA_NAVIGATION.md` | Repository navigation | Rare |
| `GAR-REFERENCE-0001.md` | Constitutional engineering reference manual (descriptive) | Occasional |
| `PROMPTS.md` *(optional)* | Reusable AI prompt templates | Occasional |

---

## Level 1 — Constitutional Authority

- GAR-INDEX
- GAR-0001 through GAR-0024

**Purpose:** Defines what Project Garuda is.

These documents are the highest architectural authority.

---

## Level 2 — AI Engineering

- `AGENTS.md`

**Purpose:** Defines how AI engineers behave.

Read before performing any work.

---

## Level 3 — Repository Context

- `GARUDA_CONTEXT.md`

**Purpose:** Defines the current repository state.

Read before planning or implementation.

---

## Level 4 — Engineering Workflow

- `GARUDA_WORKFLOW.md`

**Purpose:** Defines how work progresses through planning, implementation, testing, review, and release.

---

## Level 5 — Canonical Terminology

- `GARUDA_GLOSSARY.md`

**Purpose:** Defines the canonical language of Project Garuda.

---

## Level 6 — Repository Navigation

- `GARUDA_NAVIGATION.md`

**Purpose:** Defines the engineering document hierarchy and repository entry point.

---

## Level 7 — AI Prompt Library

- `PROMPTS.md`

**Purpose:** Defines reusable AI engineering prompts.

---

## Level 8 — Engineering Document Templates

- `templates/`

**Purpose:** Defines reusable planning, review, closure, and release document templates.

**Templates:**

- `templates/mission-specification.md`
- `templates/implementation-plan.md`
- `templates/approval.md`
- `templates/architecture-review.md`
- `templates/completion-report.md`
- `templates/release-notes.md`
- `templates/sprint-closure.md`

---

# Repository Structure

```
Garuda/
├── README.md
├── VERSION
├── CHANGELOG.md
├── AGENTS.md
├── GARUDA_CONTEXT.md
├── GARUDA_WORKFLOW.md
├── GARUDA_GLOSSARY.md
├── GARUDA_NAVIGATION.md
├── GAR-REFERENCE-0001.md
├── packages/
├── tests/
├── docs/
└── scripts/
```

**Repository Root**

| Path | Purpose |
|---|---|
| `README.md` | Project introduction |
| `VERSION` | Current repository version |
| `CHANGELOG.md` | Release history |
| `AGENTS.md` | AI engineering rules |
| `GARUDA_CONTEXT.md` | Current repository state |
| `GARUDA_WORKFLOW.md` | Engineering lifecycle |
| `GARUDA_GLOSSARY.md` | Canonical terminology |
| `GARUDA_NAVIGATION.md` | Repository navigation |
| `GAR-REFERENCE-0001.md` | Constitutional engineering reference manual (descriptive) |
| `packages/` | Production source code |
| `tests/` | Repository test suite |
| `docs/` | Architecture and engineering documentation |
| `scripts/` | Repository validation and tooling scripts |

---

# Foundation Order

```
Platform Core
↓
Memory
↓
Knowledge
↓
Context
↓
Reasoning
↓
Decision
↓
Action
↓
Execution
↓
Interface Foundation (Phase II — GAR-0017)
```

Phase I cognitive foundations are complete. Interface Foundation is the first Phase II foundation.

Future foundations shall extend this sequence only through approved constitutional authority.

---

# Sprint Pattern

Every foundation sprint follows:

```
Alpha
↓
Bravo
↓
Charlie
↓
Delta
↓
Echo
↓
Foxtrot
↓
Golf
↓
Hotel
↓
India
```

---

# Engineering Lifecycle

```
Mission Specification
↓
Implementation Plan
↓
Architecture Approval
↓
Implementation
↓
Testing
↓
Documentation
↓
Verification
↓
Architecture Review
↓
Git Commit
↓
Mission Complete
```

---

# Repository Authority

When conflicts exist:

1. Constitutions
2. Approved Sprint Documents
3. Committed Repository State
4. `VERSION`
5. Release Documentation
6. `GARUDA_CONTEXT.md`
7. `ENGINEERING_GOVERNANCE_v1.0.md` *(frozen baseline)*
8. Other Engineering Documentation

---

# Repository Bootstrap Sequence

Every AI engineer shall begin with [`BOOTSTRAP.md`](BOOTSTRAP.md), then initialize work using the following order:

1. `AGENTS.md`
2. `GARUDA_CONTEXT.md`
3. `GARUDA_WORKFLOW.md`
4. `GARUDA_GLOSSARY.md`
5. `GARUDA_NAVIGATION.md`
6. Applicable GAR Constitutions
7. Approved Sprint Mission

Implementation shall not begin until this sequence has been completed.

---

# AI Engineer Workflow

```
Open Cursor
↓
Read AGENTS.md
↓
Read GARUDA_CONTEXT.md
↓
Read Mission
↓
Produce Plan
↓
Wait
↓
Approve
↓
Implement
↓
Review
↓
Commit
```

Complete the repository bootstrap sequence before beginning this workflow.

Never begin implementation before approval.

Do not begin the next mission automatically.

---

# Maintenance Policy

Update this document only when:

- repository structure changes
- governance documents change
- engineering workflow changes

Do not record repository state here.

Repository state belongs only in `GARUDA_CONTEXT.md`.

---

End of GARUDA_NAVIGATION.md
