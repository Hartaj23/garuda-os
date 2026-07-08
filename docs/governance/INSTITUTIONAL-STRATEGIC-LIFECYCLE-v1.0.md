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

**Current position (post–Architecture 5):** Institutional HOLD — next constitutional cycle not
opened until Founder authorizes GAR-0020 analysis or equivalent governance work.

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

- [ARCHITECTURE-5-FOUNDER-DECISION.md](ARCHITECTURE-5-FOUNDER-DECISION.md)
- [GAR-ROADMAP.md](GAR-ROADMAP.md)
- [Architecture 5 Review](../architecture/ARCHITECTURE-5-repository-strategic-review.md)
- [GAR-REFERENCE-0001.md](../../GAR-REFERENCE-0001.md)

---

End of INSTITUTIONAL-STRATEGIC-LIFECYCLE-v1.0
