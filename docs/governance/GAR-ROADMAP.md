# GAR-ROADMAP

# Garuda Institutional Roadmap

| Field | Value |
| --- | --- |
| Document ID | GAR-ROADMAP |
| Classification | Institutional governance — descriptive only |
| Authority | **None** — this document authorizes nothing |
| Version | 1.0 |
| Governance baseline | Architecture 5 Founder Decision — `v0.12.0-alpha` |
| Last updated | 2026-07-08 (Governance Cycle 6 Founder Decision) |

---

## Authority Constraint

**This document is descriptive only.** It records the institutional direction of Project Garuda at
the governance baseline identified above. It creates no constitutional, architectural, sprint,
implementation, certification, SDK, release, or engineering authority.

When this document conflicts with a GAR constitution, ADR, approved sprint specification, or
committed repository state, the higher-authority artifact prevails.

---

## Purpose

The institutional roadmap answers: **Where is Garuda going?**

Unlike ADRs (one architectural decision) or sprint specifications (one implementation
authorization), this roadmap records strategic position, completed milestones, conditional candidates,
and dependency law — without authorizing any work.

Maintenance: update only at governance baselines (post-release institutional reviews, Founder
Decision cycles). Do not update mid-sprint or mid-mission.

---

## Current Institutional Position

| Field | Value |
| --- | --- |
| **Repository release** | `v0.12.0-alpha` |
| **Git tag** | `v0.12.0-alpha` on `bd29741` |
| **Institution state** | **Institutional HOLD** |
| **Governance cycle** | **Governance Cycle 6** — active |
| **Gate A** | **Complete** — constitutional evolution required (Founder Decision) |
| **Recommendation** | GAR-0020 — next governance artifact for Founder consideration |
| **Gate B** | **Pending** — Founder authorization to begin GAR-0020 drafting |
| **Layer 1** | No active governance chain |
| **Layer 2** | No active sprint |
| **Engineering authority** | **None** |
| **Test baseline** | 1042 passing tests |
| **Regression floor** | 1042 (`unittest discover tests`) |

---

## Two Institutional Assets

| Asset | Description | Current state |
| --- | --- | --- |
| **Garuda OS** | Software platform — foundations, packages, tests, SDK | Published through Runtime Foundation |
| **Garuda Constitutional Engineering** | Institutional method for platform evolution | Formalized at Architecture 5 |

---

## Completed Constitutions (In Repository)

| Document | Status | Epoch / scope |
| --- | --- | --- |
| GAR-0017 | Frozen v1.0 | Phase II — Interface Foundation, Constitutional Membrane |
| GAR-0018 | Frozen v1.0 | External Capability Expansion — Integration |
| GAR-0019 | Ratified v1.0 | External Capability Expansion — Runtime (descriptive) |

**Not committed as full text in repository:** GAR-0001 through GAR-0016 (referenced throughout
engineering documents; external corpus dependency).

---

## Completed Architecture Decision Records (In Repository)

| ADR | Foundation | Release |
| --- | --- | --- |
| ADR-0011 | Interface Foundation | `v0.10.0-alpha` |
| ADR-0012 | Integration Foundation | `v0.11.0-alpha` |
| ADR-0013 | Runtime Foundation | `v0.12.0-alpha` |

**Not committed as full text in repository:** ADR-0001 through ADR-0010.

---

## Completed Foundations

| Layer | Package | Release | Constitutional authority |
| --- | --- | --- | --- |
| Platform Core | `packages/objects` | `v0.2.0-alpha` | Phase I |
| Memory | `packages/memory` | `v0.3.0-alpha` | Phase I |
| Knowledge | `packages/knowledge` | `v0.4.0-alpha` | Phase I |
| Context | `packages/context` | `v0.5.0-alpha` | Phase I |
| Reasoning | `packages/reasoning` | `v0.6.0-alpha` | Phase I |
| Decision | `packages/decision` | `v0.7.0-alpha` | Phase I |
| Action | `packages/action` | `v0.8.0-alpha` | Phase I |
| Execution | `packages/execution` | `v0.9.0-alpha` | Phase I |
| Interface (membrane) | `packages/interface` | `v0.10.0-alpha` | GAR-0017 |
| Integration | `packages/integration` | `v0.11.0-alpha` | GAR-0018 |
| Runtime | `packages/runtime` | `v0.12.0-alpha` | GAR-0019 |

**Production packages:** 12 under `packages/`.

---

## External-Capability Stack (Published)

Descriptive governance layer — complete through Runtime for constitutionally admissible domains
evaluated to date:

```
Interface Foundation (Constitutional Membrane)
        ↓ lawful consumption
Integration Foundation (external integration governance)
        ↓ lawful consumption
Runtime Foundation (external runtime governance)
```

Each layer is **descriptive only**. Registries are process-local catalogs. Validation evaluates
metadata — no live connectivity, invocation, scheduling, or persistence.

### Shared descriptive pipeline (external-capability template)

| Subsystem | Interface | Integration | Runtime |
| --- | --- | --- | --- |
| Core | ✓ | ✓ | ✓ |
| Contracts | ✓ | ✓ | ✓ (dual subordination) |
| Lifecycle / Boundary | ✓ | ✓ | ✓ |
| Semantic layer | Translation | Relationships | Classification |
| Validation | ✓ | ✓ | ✓ |
| Registry | ✓ | ✓ | ✓ |

---

## Dependency Law

```
Platform Core (packages/objects)
    ↑
Phase I cognitive foundations (memory → execution)
    ↑ (no dependency on external systems)

Interface Foundation
    ↑ lawful consumption only
Integration Foundation
    ↑ lawful consumption only
Runtime Foundation
```

- Phase I foundations do **not** import Interface, Integration, or Runtime.
- Integration subordinates to Interface.
- Runtime subordinates to Integration **and** Interface (dual subordination).
- A third external-capability foundation would likely require triple stack subordination.

---

## Release Sequence (Published)

| Version | Sprint | Foundation / milestone |
| --- | --- | --- |
| `v0.1.0-alpha` | GAR-SPRINT-0001 | Repository platform |
| `v0.2.0-alpha` | GAR-SPRINT-0002 | Platform Core |
| `v0.3.0-alpha` | GAR-SPRINT-0003 | Memory |
| `v0.4.0-alpha` | GAR-SPRINT-0004 | Knowledge |
| `v0.5.0-alpha` | GAR-SPRINT-0005 | Context |
| `v0.6.0-alpha` | GAR-SPRINT-0006 | Reasoning |
| `v0.7.0-alpha` | GAR-SPRINT-0007 | Decision |
| `v0.8.0-alpha` | GAR-SPRINT-0008 | Action |
| `v0.9.0-alpha` | GAR-SPRINT-0009 | Execution |
| `v0.10.0-alpha` | GAR-SPRINT-0010 | Interface (Phase II) |
| `v0.11.0-alpha` | GAR-SPRINT-0011 | Integration |
| `v0.12.0-alpha` | GAR-SPRINT-0012 | Runtime |

---

## GAR-0017 Named External Capability Classes

| Class | Descriptive governance status | Authority |
| --- | --- | --- |
| **Integration** | Complete | GAR-0018, ADR-0012, `v0.11.0-alpha` |
| **Runtime** | Complete (descriptive) | GAR-0019, ADR-0013, `v0.12.0-alpha` |
| **Orchestration** | Not authorized | Rejected as operational under GAR-0018 and GAR-0019 |

---

## Conditional Candidates (Not Authorized)

The following are recorded for institutional awareness only. **None authorize work.**

| Candidate | GAR-0019 outcome | Notes |
| --- | --- | --- |
| External Orchestration Governance (descriptive) | Not evaluated | Requires GAR-0020 constitutional analysis if epoch continues |
| Operational Runtime | REJECTED | Remains rejected under Descriptive Before Operational |
| Orchestration (operational) | REJECTED | Remains rejected |
| Transport / Connectivity | REJECTED | Operational |
| Persistence | REJECTED | Operational |
| Authentication / Identity | REJECTED | Operational |
| Provider Abstraction | REJECTED | Technology neutrality |
| Integration re-extension | REJECTED | Integration complete and immutable |
| Universal Execution Extension | REJECTED | Phase I separation preserved |

**Constitutional fork (unresolved):** Can External Orchestration Governance be derived as a
descriptive foundation — as Runtime was derived from Operational Runtime — or does the External
Capability Expansion epoch pause at `v0.12.0-alpha`? Resolution requires GAR-0020 (if authorized).

---

## Deferred Domains (Require Constitutional Authority)

From GAR-0019 and Sprint 0012 closure records:

- Operational runtime execution engines
- Orchestration Foundation (operational interpretation)
- Transport and connectivity layers
- Provider implementations
- Persistence beyond process-local catalogs
- Authentication, authorization, identity systems
- Scheduling and operational state transition engines

---

## Phase Status

| Phase / epoch | Status |
| --- | --- |
| Phase I (Platform Core + cognitive foundations) | Complete — `v0.9.0-alpha` |
| Phase II (Interface membrane) | Complete — `v0.10.0-alpha` |
| External Capability Expansion (descriptive) | Integration and Runtime complete — Orchestration unresolved |

---

## Institutional Strategic Lifecycle

Garuda governance operates through three layers. See
[INSTITUTIONAL-STRATEGIC-LIFECYCLE-v1.0.md](INSTITUTIONAL-STRATEGIC-LIFECYCLE-v1.0.md).

**Layer 2 engineering lifecycle (permanent):**

```
Implementation → Mission Review → Certification → SDK → Release → Tag → Institutional HOLD
```

---

## Governance Cycle 6 (Active)

**Gate A (Founder Decision):** Constitutional evolution required — **complete**.

**Recommendation (institutional assessment):** GAR-0020 — Third External Capability Expansion
Constitutional Extension.

**Gate B (Founder Decision):** Authorization to begin GAR-0020 drafting — **pending**.

```
Governance Cycle 6
        ↓
Gate A — constitutional evolution required          ← complete
        ↓
Recommendation — GAR-0020                           ← recorded
        ↓
Gate B — authorize GAR-0020 drafting                ← pending
        ↓
GAR-0020 drafting (Chief Systems Architect)
        ↓
Founder ratification of GAR-0020
        ↓
ADR-0014 (if GAR-0020 authorizes a foundation)
        ↓
GAR-SPRINT-0013 (if ADR approved)
```

GAR-0020 drafting, ADR-0014, GAR-SPRINT-0013, and implementation are not authorized. Sprint 0013
is not assumed.

---

## Known Institutional Gaps

| Gap | Impact |
| --- | --- |
| GAR-0001–GAR-0016 not in repository as full text | External corpus dependency for Phase I law |
| ADR-0001–ADR-0010 not in repository | External corpus dependency for Phase I decisions |
| `PROJECT_GARUDA_MASTER.md` Part VIII stale | Superseded for strategic navigation by this roadmap |
| `docs/architecture/overview.md` stale | Index behind committed state |
| Process-local registries | Known limitation across Interface, Integration, Runtime |

---

## Related Documents

- [INSTITUTIONAL-STRATEGIC-LIFECYCLE-v1.0.md](INSTITUTIONAL-STRATEGIC-LIFECYCLE-v1.0.md)
- [ARCHITECTURE-5-FOUNDER-DECISION.md](ARCHITECTURE-5-FOUNDER-DECISION.md)
- [Architecture 5 Review](../architecture/ARCHITECTURE-5-repository-strategic-review.md)
- [GARUDA_CONTEXT.md](../../GARUDA_CONTEXT.md)
- [GAR-REFERENCE-0001.md](../../GAR-REFERENCE-0001.md)

---

End of GAR-ROADMAP
