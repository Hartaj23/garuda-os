# Institutional Strategic Lifecycle v1.0

| Field | Value |
| --- | --- |
| Document ID | INSTITUTIONAL-STRATEGIC-LIFECYCLE-v1.0 |
| Classification | Institutional governance model |
| Authority | Descriptive — adopted by Founder Decision (Architecture 5) |
| Version | 1.0 |
| Adopted | 2026-07-08 |
| Repository baseline | `v0.12.0-alpha` |

## Reference Principle

This document describes the institutional lifecycle exactly as adopted after Architecture 5. It is
descriptive rather than normative. Where conflict exists, GAR constitutions, ADRs, approved sprint
specifications, and the committed repository always take precedence.

This document does not authorize work.

---

## Governance Vocabulary

| Term | Meaning |
| --- | --- |
| **Decision** | What the Founder has concluded |
| **Recommendation** | What institutional assessment proposes |
| **Authorization** | Permission to begin work on a governance artifact |
| **Ratification** | Founder approval of a completed governance artifact |

A decision about direction does not imply authorization to begin work.

---

## Constitutional Evolution Gates (Layer 0 → Layer 1)

When a Governance Cycle identifies constitutional evolution as necessary, two Founder gates apply:

| Stage | Purpose | Authority |
| --- | --- | --- |
| **Gate A** | Whether constitutional evolution is necessary | Founder Decision |
| **Recommendation** | Identify appropriate next governance artifact | Institutional assessment |
| **Gate B** | Authorize drafting of that artifact | Founder Decision |
| **Drafting** | Produce constitutional proposal | Chief Systems Architect |
| **Ratification** | Accept, amend, or reject completed constitution | Founder |

Gate A answers **whether** evolution is needed. Gate B answers **whether work may begin**. Neither
gate authorizes ADR, sprint, or engineering work.

---

## Repository and Institution

Project Garuda distinguishes two complementary concepts:

| Concept | Role |
| --- | --- |
| **Repository** | Institutional memory — constitutions, ADRs, sprint specifications, code, tests, certification, SDK, releases, tags |
| **Institution** | Active governance — vision, sequencing, priorities, constitutional evolution, roadmap, release philosophy |

The repository is static at a release baseline. The institution pauses, reviews, and decides what the
repository will become next.

---

## Two Institutional Assets

Project Garuda now contains two independent but complementary assets:

| Asset | Description |
| --- | --- |
| **Garuda OS** | The software platform — foundations, packages, tests, SDK |
| **Garuda Constitutional Engineering** | The institutional method by which the platform evolves |

Garuda OS is built through Layer 2 Engineering. Garuda Constitutional Engineering governs Layers 0
and 1.

---

## Three Institutional Layers

### Layer 0 — Institution

Determines what Garuda becomes. No engineering authority exists at this layer.

```
Institutional HOLD
        ↓
Architecture Review
        ↓
Repository Strategic Review
        ↓
Founder Decision
```

**Outputs:** Institutional decisions only.

**Current position (Governance Cycle 6):** Institutional HOLD — Gate A complete (constitutional
evolution required). GAR-0020 recommended. Gate B pending (drafting not authorized).

---

## Governance Cycle Naming

Institutional reviews use **Governance Cycle N** as the Layer 0 process name.

| Term | Role |
| --- | --- |
| **Governance Cycle N** | Layer 0 institutional process between engineering releases |
| **Architecture N** | Specific repository strategic review within a cycle (when produced) |

A Governance Cycle may conclude that no constitutional amendment, ADR, or sprint is required. That is
a valid and complete outcome.

**Cycle history:**

| Cycle | Review artifact | Outcome |
| --- | --- | --- |
| Governance Cycle 5 | Architecture 5 | Governance model adopted — `4a9a2b1` |
| Governance Cycle 6 | Pending | Gate A complete — GAR-0020 recommended; Gate B pending |

---

### Layer 1 — Governance

Converts institutional decisions into engineering authority.

```
Constitution (if required)
        ↓
ADR
        ↓
Sprint Authorization
```

**Outputs:** Ratified constitutions, approved ADRs, authorized sprint specifications.

**Handoff:** Sprint Authorization is the boundary between governance and engineering.

---

### Layer 2 — Engineering

Determines how one authorized foundation is delivered.

```
Sprint Authorization
        ↓
Mission Planning
        ↓
Implementation
        ↓
Mission Review
        ↓
Certification
        ↓
SDK
        ↓
Release
        ↓
Git Tag
        ↓
Institutional HOLD
```

**Outputs:** Code, tests, certification records, SDK documentation, release artifacts, tags.

Certification is a **permanent named phase** between Mission Review and SDK. It is not optional
testing and not folded into Release. Repository practice from GAR-SPRINT-0010 through
GAR-SPRINT-0012 established:

```
Implementation → Mission Review → Certification → SDK → Release
```

not `Implementation → Release`.

---

## Institutional HOLD

**Institutional HOLD** replaces **Repository HOLD** for Layer 0 governance language.

The repository never pauses — it records the current institutional baseline. Governance pauses
between cycles. People and authority pause; the repository remains static.

Historical release and sprint closure documents may retain the phrase "Repository HOLD" as
period-accurate records. Live institutional context documents use **Institutional HOLD**.

---

## Cycle Closure

The full institutional cycle:

```
Layer 0: Institutional HOLD → … → Founder Decision
Layer 1: Constitution → ADR → Sprint Authorization
Layer 2: Engineering → Git Tag → Institutional HOLD
```

Layer 2 Git Tag returns authority to Layer 0 Institutional HOLD.

---

## Authority Invariant

This lifecycle model makes explicit what Sprint 0012 proved in practice. It does **not** alter
constitutional authority order:

1. GAR Constitutions
2. Architecture Decision Records
3. Approved Sprint Specifications
4. Committed Repository State

---

## Related Documents

- [GOVERNANCE-CYCLE-6-FOUNDER-DECISION.md](GOVERNANCE-CYCLE-6-FOUNDER-DECISION.md)
- [ARCHITECTURE-5-FOUNDER-DECISION.md](ARCHITECTURE-5-FOUNDER-DECISION.md)
- [GAR-ROADMAP.md](GAR-ROADMAP.md)
- [Architecture 5 Review](../architecture/ARCHITECTURE-5-repository-strategic-review.md)
- [GAR-REFERENCE-0001.md](../../GAR-REFERENCE-0001.md)

---

End of INSTITUTIONAL-STRATEGIC-LIFECYCLE-v1.0
