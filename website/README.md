# Project Garuda — Public Website

## Phase A — Site Architecture

| Field | Value |
| --- | --- |
| Mission | Mission 001 — Launch the Public Foundation |
| Phase | Phase A — Site Architecture |
| Status | **Complete (Approved — Closed)** |
| Closure | [MISSION-001-PHASE-A-CLOSURE.md](../docs/governance/MISSION-001-PHASE-A-CLOSURE.md) |
| Authorization | [MISSION-001-PHASE-A-FOUNDER-DECISION.md](../docs/governance/MISSION-001-PHASE-A-FOUNDER-DECISION.md) |

This directory creates no constitutional, architectural, sprint, or engineering authority.

The repository remains the institution's canonical source of truth.

---

## Purpose

The `website/` directory is the **public communication layer** — separate from:

- `docs/` — institutional, governance, architecture, and engineering documentation
- `packages/` — authorized engineering foundations
- `apps/` — application implementations

Public communication is not constitutional authority.

It introduces the institution.

The repository governs it.

---

## Directory Structure

```
website/
├── README.md                 # This file — implementation documentation
├── config/
│   ├── site.yaml             # Site metadata and phase record
│   ├── navigation.yaml       # Information architecture and navigation hierarchy
│   └── reading-journey.yaml  # Public reading journey sequence
├── content/                  # Markdown source content (Phase A)
│   ├── home.md
│   ├── manifesto.md
│   ├── vision.md
│   ├── principles.md
│   ├── constitutional-engineering.md
│   ├── invitation.md
│   ├── institution/          # Institution section gateways
│   └── library/              # Library section gateways
├── pages/                    # Future page rendering layer (not authorized)
├── components/               # Future UI components (not authorized)
├── assets/                   # Future static assets (not authorized)
└── styles/                   # Future styles (not authorized — Phase B)
```

---

## Information Architecture

### Top-Level Sections

| Section | Purpose | Phase A Status |
| --- | --- | --- |
| Home | Five-minute introduction | Content gateway |
| About | Manifesto, Vision, Principles | Content gateways |
| Constitutional Engineering | Discipline introduction | Content gateway |
| The Institution | Framework overview | Structural gateways |
| Library | Preservation Series volumes | Structural gateways |
| Research | Academic publications | Placeholder only — Phase D unauthorized |
| News | Institutional updates | Placeholder only — Phase D unauthorized |
| Contact | Inquiry pathway | Placeholder only — Phase D unauthorized |

Full hierarchy: see [config/navigation.yaml](config/navigation.yaml).

---

## Public Reading Journey

The intentional reading order for first-time visitors:

1. Home
2. Manifesto
3. Vision
4. Principles
5. Constitutional Engineering
6. Invitation to the World
7. Research (placeholder)
8. Repository

Defined in [config/reading-journey.yaml](config/reading-journey.yaml).

This sequence minimizes cognitive load and gradually introduces deeper ideas.

---

## Linking Strategy

### Repository-First

Every public page that references institutional authority shall link to the **canonical repository path**, not paraphrase authoritative text.

| Content type | Link target |
| --- | --- |
| Institutional literature | `docs/institutional/` |
| Constitutional artifacts | Repository root (`GAR-*.md`) or `docs/governance/` |
| Architecture | `docs/architecture/`, `docs/adr/` |
| Engineering | `docs/engineering/`, `packages/` |
| Preservation Series | `docs/institutional/book-one/`, `atlas/`, etc. |

### Relative Paths

Content files use relative paths from `website/content/` to repository artifacts.

Example: `../../docs/institutional/MANIFESTO.md`

### No Authority Duplication

Website content provides orientation.

It does not replace or amend repository artifacts.

Where differences arise, the repository prevails.

---

## Phase Authorization Record

| Phase | Scope | Status |
| --- | --- | --- |
| A | Site architecture | **Complete (Closed)** — [Closure](../../docs/governance/MISSION-001-PHASE-A-CLOSURE.md) |
| B | Brand foundation | **Complete (Closed)** — [Closure](../../docs/governance/MISSION-001-PHASE-B-CLOSURE.md) |
| — | Implementation Readiness Review | **Complete** — [Review](../../docs/governance/IMPLEMENTATION-READINESS-REVIEW-MISSION-001.md) |
| C | Implementation | **Complete (Closed)** — [Closure](../docs/governance/MISSION-001-PHASE-C-CLOSURE.md) |
| — | Final Acceptance Review | **Complete** — [Review](../docs/governance/FINAL-ACCEPTANCE-REVIEW-MISSION-001.md) |
| — | Mission 001 | **Closed** — [Closure](../docs/governance/MISSION-001-CLOSURE.md) |
| — | Public deployment | **Authorized** — [Authorization](../docs/governance/MISSION-001-PUBLIC-DEPLOYMENT-AUTHORIZATION.md) |
| D | Research & News | Not authorized |
| — | Public deployment | Not authorized |
| — | Custom domain | Not authorized |

---

## Success Criteria (Phase A)

Phase A is complete when:

- [x] `website/` directory structure established
- [x] Information architecture documented
- [x] Navigation hierarchy defined in config
- [x] Public reading journey defined
- [x] Repository linking strategy documented
- [x] Core content gateways created
- [x] Institution and Library structural gateways created
- [x] Founder review of Phase A structure — **Approved 2026-07-08**

Mission 001 is **accepted and closed**. Public deployment is **authorized**.

Build: `.venv/bin/python website/scripts/build_site.py`

Preview: `python -m http.server 8000 --directory website/public`

Deployment: [DEPLOYMENT.md](DEPLOYMENT.md)

---

## Reflection Period

Before Phase B authorization, review the structure without expansion.

Ask: *If someone had never seen Garuda before, would this architecture naturally teach them how to think?*

See [MISSION-001-PHASE-A-CLOSURE.md](../docs/governance/MISSION-001-PHASE-A-CLOSURE.md).

---

## Next Steps (Require Founder Authorization)

- **Phase B** — Brand identity (logo, palette, typography)
- **Phase C** — Full content integration
- **Phase D** — Research and News sections
- **Hosting decision** — after structure review

---

End of Website Phase A Documentation
