# Architecture 5 — Founder Decision Record

| Field | Value |
| --- | --- |
| Decision ID | ARCHITECTURE-5-FOUNDER-DECISION |
| Review | Architecture 5 — Repository Strategic Architecture Review |
| Repository baseline | `v0.12.0-alpha` (tag `bd29741`) |
| Decision date | 2026-07-08 |
| Institution state | **Institutional HOLD** |

## Finding

Architecture 5 did not produce a new foundation. It strengthened the governance of every future
foundation by formalizing what Sprint 0012 proved in practice: Garuda operates through distinct
institutional, governance, and engineering layers.

---

## Decision 1 — Adopt Institutional Strategic Lifecycle v1.0

**Status:** Adopted

The Garuda governance model formally recognizes three institutional layers:

- **Layer 0 — Institution:** Institutional HOLD → Architecture Review → Repository Strategic Review → Founder Decision
- **Layer 1 — Governance:** Constitution → ADR → Sprint Authorization
- **Layer 2 — Engineering:** Sprint Authorization → Mission Planning → Implementation → Mission Review → Certification → SDK → Release → Git Tag → Institutional HOLD

**Artifact:** [INSTITUTIONAL-STRATEGIC-LIFECYCLE-v1.0.md](INSTITUTIONAL-STRATEGIC-LIFECYCLE-v1.0.md)

This adoption does not alter constitutional authority. It makes explicit what Sprint 0012 proved in
practice.

---

## Decision 2 — Adopt Certification as a Permanent Governance Phase

**Status:** Adopted

Certification is a permanent named phase of the Garuda Engineering System.

Engineering lifecycle:

```
Implementation
        ↓
Mission Review
        ↓
Certification
        ↓
SDK
        ↓
Release
```

Repository evidence: GAR-SPRINT-0010 through GAR-SPRINT-0012 (Mission Golf certification records).

---

## Decision 3 — Create Institutional Roadmap

**Status:** Adopted — artifact authorized

**Location:** [GAR-ROADMAP.md](GAR-ROADMAP.md)

**Authority:** Descriptive only. Records institutional direction. Authorizes nothing.

---

## Decision 4 — Adopt Institutional HOLD Terminology

**Status:** Adopted

Layer 0 governance language uses **Institutional HOLD** instead of **Repository HOLD**.

The repository records the current institutional baseline. Governance pauses between cycles.

Historical sprint and release documents are not reopened. Live context documents reflect the adopted
terminology.

---

## Decision 5 — Recognize the Garuda Engineering System

**Status:** Adopted

Project Garuda contains two complementary institutional assets:

| Asset | Role |
| --- | --- |
| **Garuda OS** | The software platform |
| **Garuda Constitutional Engineering** | The institutional method by which the platform evolves |

---

## Architecture 5 Conclusion

Architecture 5 is **closed**. Outcomes are governance improvements to the Garuda Engineering
System — not foundation work and not Sprint 0013 authorization.

---

## Next Governance Cycle (Not Authorized Here)

The following sequence may proceed only after separate Founder authorization at each gate:

```
Institutional HOLD
        ↓
Architecture 5 outcomes adopted (complete)
        ↓
GAR-ROADMAP established (complete)
        ↓
GAR-0020 (if constitution requires evolution)
        ↓
ADR-0014
        ↓
GAR-SPRINT-0013
```

Sprint 0013 remains a **consequence** of constitutional authority — not a starting point.

---

## Related Documents

- [Architecture 5 Review](../architecture/ARCHITECTURE-5-repository-strategic-review.md)
- [INSTITUTIONAL-STRATEGIC-LIFECYCLE-v1.0.md](INSTITUTIONAL-STRATEGIC-LIFECYCLE-v1.0.md)
- [GAR-ROADMAP.md](GAR-ROADMAP.md)

---

End of Architecture 5 Founder Decision Record
