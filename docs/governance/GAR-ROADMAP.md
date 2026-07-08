# GAR-ROADMAP

# Garuda Institutional Roadmap

| Field | Value |
| --- | --- |
| Document ID | GAR-ROADMAP |
| Classification | Institutional governance — descriptive only |
| Authority | **None** — this document authorizes nothing |
| Version | 1.0 |
| Governance baseline | GAR-0020 Founder Ratification — Constitutional Baseline v1.0 |
| Last updated | 2026-07-08 (GAR-0020 ratified — epoch pause) |

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
| **Governance cycle** | **Governance Cycle 6** — **closed** |
| **Constitutional law** | GAR-0020 v1.0 — **Founder Ratified** |
| **Descriptive epoch** | **Pause** — descriptive layer constitutionally complete |
| **Gate A / Gate B / Ratification** | Complete |
| **Layer 1** | No active governance chain |
| **Layer 2** | No active sprint |
| **Engineering authority** | **None** |
| **Next gate** | New Governance Cycle + explicit Founder authorization |
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
| GAR-0020 | Ratified v1.0 | External Capability Expansion — Third Derivation (epoch pause) |

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
| **Orchestration** | Not authorized (descriptive and operational) | Rejected under GAR-0020 — epoch pause |

---

## Conditional Candidates (Not Authorized)

The following are recorded for institutional awareness only. **None authorize work.**

| Candidate | GAR-0019 outcome | Notes |
| --- | --- | --- |
| External Orchestration Governance (descriptive) | REJECTED | GAR-0020 Article VII Candidate B — not admissible under current law |
| Operational Runtime | REJECTED | Remains rejected under Descriptive Before Operational |
| Orchestration (operational) | REJECTED | Remains rejected |
| Transport / Connectivity | REJECTED | Operational |
| Persistence | REJECTED | Operational |
| Authentication / Identity | REJECTED | Operational |
| Provider Abstraction | REJECTED | Technology neutrality |
| Integration re-extension | REJECTED | Integration complete and immutable |
| Universal Execution Extension | REJECTED | Phase I separation preserved |

**Constitutional fork (resolved):** GAR-0020 ratified epoch pause at `v0.12.0-alpha`. No third
descriptive foundation is authorized under current law. Future expansion requires a new governance
cycle and separate constitutional evolution if warranted.

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
| External Capability Expansion (descriptive) | Integration and Runtime complete — **epoch pause** (GAR-0020) |

---

## Institutional Strategic Lifecycle

Garuda governance operates through three layers. See
[INSTITUTIONAL-STRATEGIC-LIFECYCLE-v1.0.md](INSTITUTIONAL-STRATEGIC-LIFECYCLE-v1.0.md).

**Layer 2 engineering lifecycle (permanent):**

```
Implementation → Mission Review → Certification → SDK → Release → Tag → Institutional HOLD
```

---

## Governance Cycle 6 (Closed)

Governance Cycle 6 closed with GAR-0020 Founder ratification on 2026-07-08.

```
Gate A — constitutional evolution required          ← complete
        ↓
Recommendation — GAR-0020                           ← recorded
        ↓
Gate B — authorize GAR-0020 drafting                ← granted
        ↓
GAR-0020 drafting                                   ← submitted (`a800f7b`)
        ↓
Founder ratification                                ← complete
        ↓
Epoch pause — descriptive layer complete            ← constitutional baseline
        ↓
Institutional HOLD
```

ADR-0014, GAR-SPRINT-0013, and implementation are **not authorized**. See
[GOVERNANCE-CYCLE-6-CLOSURE.md](GOVERNANCE-CYCLE-6-CLOSURE.md).

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
- [GAR-0020-FOUNDER-RATIFICATION.md](GAR-0020-FOUNDER-RATIFICATION.md)
- [GOVERNANCE-CYCLE-6-CLOSURE.md](GOVERNANCE-CYCLE-6-CLOSURE.md)
- [GARUDA_CONTEXT.md](../../GARUDA_CONTEXT.md)
- [GAR-REFERENCE-0001.md](../../GAR-REFERENCE-0001.md)

---

End of GAR-ROADMAP
