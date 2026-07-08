# Governance Cycle 6 — Founder Decision Record

| Field | Value |
| --- | --- |
| Decision ID | GOVERNANCE-CYCLE-6-FOUNDER-DECISION |
| Cycle | Governance Cycle 6 |
| Prior cycle | Governance Cycle 5 — Architecture 5 (closed at `4a9a2b1`) |
| Repository baseline | `v0.12.0-alpha` (tag `bd29741`) |
| Decision date | 2026-07-08 |
| Institution state | **Institutional HOLD** |

## Authority Constraint

This document records Layer 0 institutional **decisions**. It creates no engineering, sprint,
implementation, certification, SDK, or release authority.

---

## Governance Vocabulary

These terms are used consistently across the governance corpus:

| Term | Meaning |
| --- | --- |
| **Decision** | What the Founder has concluded |
| **Recommendation** | What institutional assessment proposes |
| **Authorization** | Permission to begin work on a governance artifact |
| **Ratification** | Founder approval of a completed governance artifact |

A **decision** about direction does not imply **authorization** to begin work. Each transition
requires an explicit governance event.

---

## Decision 1 — Adopt Governance Cycle Naming

**Status:** Adopted (Founder Decision)

Future institutional reviews shall be named **Governance Cycle N**, not Architecture N.

| Term | Scope |
| --- | --- |
| **Governance Cycle N** | Layer 0 institutional process — may conclude without constitutional amendment, ADR, or sprint |
| **Architecture N** | Specific repository strategic review artifact within a cycle (when produced) |

**Retroactive mapping:**

```
Governance Cycle 5
        ↓
Architecture 5 (Repository Strategic Review)
        ↓
Founder Decision (adopted — `4a9a2b1`)
        ↓
Institutional HOLD
```

---

## Gate A — Constitutional Evolution Required

**Status:** Complete (Founder Decision)

**Gate A question:** Does Governance Cycle 6 require constitutional evolution?

**Founder Decision:** **Yes.** Constitutional evolution is required before a new foundation, ADR, or
sprint may be authorized.

Gate A determines **whether** evolution is needed. It does not authorize drafting, ratification, ADR
work, sprint work, or engineering.

---

## Institutional Recommendation — Next Governance Artifact

**Status:** Recommendation (not authorization)

Following Gate A, institutional assessment recommends **GAR-0020** — Third External Capability
Expansion Constitutional Extension — as the appropriate next governance artifact for Founder
consideration.

This is a **recommendation**, not permission to begin drafting.

| Stage | Purpose | Authority | Cycle 6 status |
| --- | --- | --- | --- |
| Gate A | Whether constitutional evolution is necessary | Founder Decision | **Complete** |
| Recommendation | Identify appropriate next governance artifact | Institutional assessment | **GAR-0020 recommended** |
| Gate B | Authorize drafting of that artifact | Founder Decision | **Pending** |
| GAR-0020 drafting | Produce constitutional proposal | Chief Systems Architect | Not authorized |
| Ratification | Accept, amend, or reject GAR-0020 | Founder | Not applicable — no draft |
| ADR-0014 | Architectural interpretation (if warranted) | Separate authorization | Not authorized |
| GAR-SPRINT-0013 | Implementation mission (if warranted) | Separate authorization | Not authorized |
| Engineering | Repository work | Separate authorization | Not authorized |

---

## Gate B — GAR-0020 Drafting Authorization

**Status:** Pending (Founder Decision not yet recorded)

**Gate B question:** Does the Founder authorize GAR-0020 drafting to begin?

Until Gate B is explicitly recorded, the Chief Systems Architect shall not produce GAR-0020 text.
The institution remains at **Institutional HOLD**.

---

## What Gate A Authorizes

| Action | Status |
| --- | --- |
| Record that constitutional evolution is required | **Complete** |
| Identify GAR-0020 as recommended next artifact | **Complete** (recommendation) |
| Governance documentation updates | **Authorized** (this record) |

---

## What Gate A and Gate B Do Not Authorize

| Action | Status |
| --- | --- |
| GAR-0020 drafting | **Not authorized** — Gate B pending |
| GAR-0020 ratification | Not applicable — no draft |
| ADR-0014 | Not authorized |
| GAR-SPRINT-0013 | Not authorized |
| Mission Alpha or any implementation | Not authorized |
| Modification of GAR-0017, GAR-0018, GAR-0019 | Not authorized |
| Modification of completed foundations or Sprint 0012 artifacts | Not authorized |

---

## GAR-0020 Scope (Recommendation Context — Not Draft Text)

If Gate B is authorized, drafted, and ratified, GAR-0020 is expected to address (per Architecture 5):

1. Post-Runtime candidate domain analysis (Orchestration first, per GAR-0017 naming)
2. Descriptive vs operational Orchestration (Runtime re-derivation precedent)
3. Exhaustiveness record for constitutionally plausible third domains
4. Single-foundation authorization or explicit epoch pause declaration
5. Preservation of GAR-0017, GAR-0018, GAR-0019, and all predecessor law

GAR-0020 must not authorize implementation, ADR drafting, or sprint work directly.

---

## Current Institutional Position

| Domain | State |
| --- | --- |
| **Repository** | `v0.12.0-alpha` — stable institutional memory |
| **Governance framework** | Architecture 5 — closed and adopted |
| **Governance cycle** | Cycle 6 — active |
| **Gate A** | **Complete** — constitutional evolution required |
| **Recommendation** | GAR-0020 |
| **Gate B** | **Pending** — Founder authorization to begin drafting |
| **Institution** | **Institutional HOLD** |
| **Engineering authority** | **None** |

---

## Related Documents

- [INSTITUTIONAL-STRATEGIC-LIFECYCLE-v1.0.md](INSTITUTIONAL-STRATEGIC-LIFECYCLE-v1.0.md)
- [GAR-ROADMAP.md](GAR-ROADMAP.md)
- [ARCHITECTURE-5-FOUNDER-DECISION.md](ARCHITECTURE-5-FOUNDER-DECISION.md)
- [Architecture 5 Review](../architecture/ARCHITECTURE-5-repository-strategic-review.md)

---

End of Governance Cycle 6 Founder Decision Record
