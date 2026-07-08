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

This document records Layer 0 institutional decisions. It creates no engineering, sprint,
implementation, certification, SDK, or release authority.

---

## Decision 1 — Adopt Governance Cycle Naming

**Status:** Adopted

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

**Forward model:**

```
Governance Cycle 6
        ↓
Repository Assessment
        ↓
Founder Decision
        ↓
GAR-0020 (if required)
        ↓
ADR-0014
        ↓
GAR-SPRINT-0013
```

Not every cycle reaches GAR-0020, an ADR, or a sprint. A cycle is complete when the Founder Decision
is recorded.

---

## Decision 2 — Constitutional Evolution Required

**Status:** Adopted

Governance Cycle 6 requires **constitutional evolution** before a new foundation, ADR, or sprint may
be authorized.

The institution has determined that analysis and drafting of **GAR-0020** — Third External Capability
Expansion Constitutional Extension — is the next governance artifact.

---

## What This Decision Authorizes

| Action | Status |
| --- | --- |
| GAR-0020 drafting (Chief Systems Architect) | **Next authorized governance artifact** |
| Founder ratification of GAR-0020 | Pending draft completion |
| Governance documentation updates | Authorized (this record) |

---

## What This Decision Does Not Authorize

| Action | Status |
| --- | --- |
| GAR-0020 ratification | Not authorized — draft does not exist |
| ADR-0014 | Not authorized |
| GAR-SPRINT-0013 | Not authorized |
| Mission Alpha or any implementation | Not authorized |
| Modification of GAR-0017, GAR-0018, GAR-0019 | Not authorized |
| Modification of completed foundations or Sprint 0012 artifacts | Not authorized |

---

## GAR-0020 Scope (Institutional Direction — Not Draft Authorization Text)

If drafted and ratified, GAR-0020 is expected to address (per Architecture 5):

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
| **Institution** | Institutional HOLD — Governance Cycle 6 active |
| **Governance Cycle** | Cycle 6 — Founder Decision recorded |
| **Next artifact** | GAR-0020 (constitutional drafting) |
| **Engineering** | No active sprint |

---

## Related Documents

- [INSTITUTIONAL-STRATEGIC-LIFECYCLE-v1.0.md](INSTITUTIONAL-STRATEGIC-LIFECYCLE-v1.0.md)
- [GAR-ROADMAP.md](GAR-ROADMAP.md)
- [ARCHITECTURE-5-FOUNDER-DECISION.md](ARCHITECTURE-5-FOUNDER-DECISION.md)
- [Architecture 5 Review](../architecture/ARCHITECTURE-5-repository-strategic-review.md)

---

End of Governance Cycle 6 Founder Decision Record
