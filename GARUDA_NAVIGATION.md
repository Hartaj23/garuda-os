# PROJECT GARUDA

# GARUDA_NAVIGATION.md

Repository Navigation & Engineering Document Hierarchy

Version: 1.0

Last Updated: 2026-07-06

Document Owner: Project Garuda Engineering Governance

Change Frequency: Rare

---

# Purpose

This document serves as the entry point into Project Garuda.

Every engineer, AI coding agent, reviewer, or contributor should begin here before navigating deeper into the repository.

---

# Engineering Document Hierarchy

The engineering governance documents shall be read in the following order.

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

# Repository Structure

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
| `docs/` | Architecture and engineering documentation |
| `packages/` | Production source code |
| `tests/` | Repository test suite |

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
```

Future foundations shall extend this sequence.

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
7. Other Engineering Documentation

---

# Quick Start for AI Engineers

1. Read `AGENTS.md`
2. Read `GARUDA_CONTEXT.md`
3. Read `GARUDA_WORKFLOW.md`
4. Read `GARUDA_GLOSSARY.md`
5. Read approved sprint mission
6. Produce implementation plan
7. Wait for architecture approval

Never begin implementation before approval.

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
