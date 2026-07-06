# PROJECT GARUDA

# GARUDA_WORKFLOW.md

Engineering Workflow & Delivery Lifecycle

Version: 1.0

Last Updated: 2026-07-06

---

# Purpose

This document defines the standard engineering workflow for Project Garuda.

It describes how all engineering work progresses from architecture through implementation, testing, review, documentation, and release.

This workflow applies to all contributors, whether human or AI.

---

# Engineering Philosophy

Project Garuda follows Constitutional Engineering.

Every implementation must preserve architectural integrity.

Correctness always precedes speed.

Architecture always precedes implementation.

Every implementation must be reproducible.

Every implementation must be reviewable.

---

# Engineering Lifecycle

Every change follows this lifecycle:

```
Idea
↓
Architecture
↓
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
↓
Next Mission
```

No phase may be skipped.

---

# Mission Lifecycle

Every sprint is divided into missions.

Typical mission sequence:

- Alpha
- Bravo
- Charlie
- Delta
- Echo
- Foxtrot
- Golf
- Hotel
- India

Every mission is independent.

Every mission finishes with a clean repository.

---

# Architecture Phase

Before implementation:

1. Read `engineering/AGENTS.md`
2. Read `engineering/GARUDA_CONTEXT.md`
3. Read `engineering/GARUDA_WORKFLOW.md`
4. Read `engineering/GARUDA_GLOSSARY.md`
5. Read `engineering/GARUDA_NAVIGATION.md`
6. Read applicable GAR Constitutions
7. Read the approved sprint mission
8. Review current repository state

Implementation shall not begin until steps 1 through 7 are completed.

Never begin implementation without understanding architectural boundaries.

---

# Planning Phase

Every implementation begins with an Implementation Plan.

The plan shall include:

- Objective
- Deliverables
- Scope
- Explicit exclusions
- Tests
- Documentation
- Verification
- Completion criteria

No coding begins until the plan receives explicit approval.

---

# Approval Gate

Architecture approval is mandatory.

No implementation begins until approval is granted.

If approval is withheld:

- stop immediately
- do not modify repository
- wait for revised instructions

---

# Implementation Phase

Implement only the approved mission.

Never:

- expand scope
- redesign architecture
- anticipate future missions
- modify unrelated foundations

Every implementation shall be:

- deterministic
- minimal
- production quality

---

# Testing Phase

Every mission must include tests.

Execute:

- Mission tests
- Foundation tests
- Complete non-backend suite
- Repository validation
- Engineering validation
- Repository checks

Report all failures honestly.

Never suppress failures.

---

# Documentation Phase

Every mission updates documentation.

Documentation may include:

- Architecture
- Engineering
- SDK
- Certification
- Sprint reports
- Release notes

Documentation shall describe implemented behavior only.

---

# Verification Phase

Verify:

- repository integrity
- deterministic behavior
- cross-foundation compatibility
- Platform Core compatibility
- mission scope compliance

Never verify future functionality.

---

# Architecture Review

Every completed mission requires architecture review.

Review confirms:

- scope compliance
- constitutional compliance
- repository health
- explicit exclusions
- known limitations

Mission is not complete until review is approved.

---

# Git Workflow

- One mission.
- One commit.
- Repository must remain clean.
- Never combine multiple missions into one commit.
- Commit only verified work.

---

# Release Workflow

Release preparation occurs only during Mission India.

Typical release activities:

- `VERSION` update
- `CHANGELOG` update
- Release notes
- Sprint closure report
- Documentation review
- Repository health verification

Tags are created only after approval.

---

# Engineering Quality Standards

Every implementation shall be:

- deterministic
- reproducible
- immutable where appropriate
- platform neutral
- service independent
- fully documented
- fully tested

---

# Recovery Procedure

If uncertainty exists:

**Stop.**

Read:

1. `engineering/AGENTS.md`
2. `engineering/GARUDA_CONTEXT.md`
3. `engineering/GARUDA_WORKFLOW.md`
4. `engineering/GARUDA_GLOSSARY.md`
5. `engineering/GARUDA_NAVIGATION.md`
6. Applicable GAR Constitutions
7. Approved Sprint Mission

Never guess architecture.

---

# Completion Report

Every mission returns:

- Files created
- Files modified
- Commands executed
- Tests executed
- Documentation summary
- Git commit hash
- Repository status
- Architecture review summary
- Known limitations

Do not begin the next mission automatically.

---

# Change Policy

This document evolves only when the engineering process changes.

It shall not record repository state.

Repository state belongs in `engineering/GARUDA_CONTEXT.md`.

Architectural rules belong in the GAR constitutions.

---

End of GARUDA_WORKFLOW.md
