# Project Garuda — Public Website

## Phase A — Site Architecture

| Field | Value |
| --- | --- |
| Mission | Mission 001 — Launch the Public Foundation |
| Phase | Phase A — Site Architecture (authorized) |
| Authorization | [MISSION-001-PHASE-A-FOUNDER-DECISION.md](../docs/governance/MISSION-001-PHASE-A-FOUNDER-DECISION.md) |
| Status | Phase A — In Progress |

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
| A | Site architecture | **Authorized — In Progress** |
| B | Brand foundation | Not authorized |
| C | Content integration | Not authorized |
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
- [ ] Founder review of Phase A structure

---

## Next Steps (Require Founder Authorization)

- **Phase B** — Brand identity (logo, palette, typography)
- **Phase C** — Full content integration
- **Phase D** — Research and News sections
- **Hosting decision** — after structure review

---

End of Website Phase A Documentation
