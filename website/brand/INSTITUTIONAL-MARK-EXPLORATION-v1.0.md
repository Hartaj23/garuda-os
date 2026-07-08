# Project Garuda

# Institutional Mark Exploration v1.0

## Mission 001 — Phase B (Brand Foundation)

| Field | Value |
| --- | --- |
| Document Type | Brand Foundation |
| Authority | Visual Implementation Guidance Only |
| Authorization | [MISSION-001-PHASE-B-INSTITUTIONAL-MARK-EXPLORATION-AUTHORIZATION.md](../../docs/governance/MISSION-001-PHASE-B-INSTITUTIONAL-MARK-EXPLORATION-AUTHORIZATION.md) |
| Evidence | [PRINT-EXERCISE-INDEPENDENT-READER-OBSERVATION-MISSION-001-PHASE-B.md](../../docs/institutional/PRINT-EXERCISE-INDEPENDENT-READER-OBSERVATION-MISSION-001-PHASE-B.md) |
| Derives from | [CANONICAL-PAGE-SPECIFICATION-v1.0.md](CANONICAL-PAGE-SPECIFICATION-v1.0.md), [DESIGN-TOKENS-v1.0.md](DESIGN-TOKENS-v1.0.md), [DESIGN-LANGUAGE-v1.0.md](DESIGN-LANGUAGE-v1.0.md) |
| Version | 1.0 |

This document creates no constitutional, architectural, sprint, or engineering authority.

It does not authorize final mark selection, favicon design, CSS, website implementation, public deployment, or external communication.

---

## Purpose

Institutional Mark Exploration v1.0 defines **what mark belongs naturally on a Garuda page** — not what logo a brand requires.

The page has already established identity through structure, rhythm, typography, and repository prominence.

The mark shall **acknowledge** that identity.

It shall not **manufacture** it.

---

## Legitimacy Chain

```
Visual Philosophy v1.0              ✓ Recorded
        ↓
Design Language v1.0                ✓ Recorded
        ↓
Design Tokens v1.0                  ✓ Recorded
        ↓
Canonical Page Specification v1.0   ✓ Recorded
        ↓
Institutional Mark Exploration v1.0 ✓ Recorded
Institutional Mark Selection v1.0   ✓ Recorded
Institutional Mark Adoption           — not authorized
        ↓
Implementation                      — not authorized
```

---

## Terminology

| Term | Definition | Belongs to |
| --- | --- | --- |
| **Institutional mark** | A restrained visual acknowledgment of an institution already recognizable through its pages | An institution |
| **Logo** | A brand asset designed to carry identity in the absence of structural recognition | A brand |

Project Garuda explores an **institutional mark**.

It does not design a **logo**.

---

## The Design Question

### Not this question

*"What logo should Garuda have?"*

That question assumes the mark must carry identity.

The page has proven identity survives without a mark.

### This question

*"What mark belongs naturally on a Garuda page?"*

That question assumes the page is already the institution.

The mark inhabits an environment the Canonical Page Specification has defined.

---

## Evidence Basis

The print exercise ([Independent Reader Observation](../../docs/institutional/PRINT-EXERCISE-INDEPENDENT-READER-OBSERVATION-MISSION-001-PHASE-B.md)) established three institutionally significant findings:

1. **Identity survived the absence of the mark.**
2. **The repository-first relationship was perceived without explanation.**
3. **The page communicated institutional character before communicating institutional content.**

The mark must not undermine any of these findings.

If adding the mark would make the page feel more like a brand and less like an institution, the mark fails — regardless of aesthetic quality.

---

## Institutional Archetypes

The mark should belong to the same family as marks found on:

- university press colophons,
- constitutional archive seals (restrained, not heraldic),
- research institute working paper identifiers,
- preservation volume imprints,
- library finding-aid stamps.

The mark should **not** resemble marks found on:

- technology product logos,
- cryptocurrency project badges,
- SaaS application icons,
- conference sponsorship marks,
- social media avatars optimized for circular crops.

Reference character: **simple, quiet, archival, reproducible.**

---

## Evaluation Criteria

Every candidate mark shall be evaluated against these criteria.

A mark that fails any criterion is excluded from further consideration.

### 1. Acknowledgment, not manufacture

| Test | Pass condition |
| --- | --- |
| Page-without-mark test | Removing the mark does not diminish page identity (already proven) |
| Page-with-mark test | Adding the mark does not become the primary identity signal |
| Subordination | Mark is visually quieter than the page title |

### 2. Monochrome survival

| Test | Pass condition |
| --- | --- |
| Black and white | Mark reads clearly at 100% black on white paper |
| Reversed | Mark reads clearly as white on dark ink (`text.primary`) |
| No color dependency | Mark does not require palette colors to be recognizable |
| Print fidelity | Mark reproduces cleanly at 12mm width on A4 |

### 3. Canonical Page compatibility

| Test | Pass condition |
| --- | --- |
| Placement | Mark fits defined placement zones without disrupting reading measure |
| Scale | Mark at maximum specified size does not compete with h1 |
| Navigation | Mark does not replace or dominate site navigation |
| Footer | Mark may appear in footer at reduced scale without becoming the loudest element |

### 4. Token alignment

| Test | Pass condition |
| --- | --- |
| Primary color | Mark works in `text.primary` (`#1C1C1A`) — ink |
| Accent use | If accent used, only `accent.primary` (`#2E4057`) — institutional slate |
| No ad-hoc colors | Mark uses token palette only |
| Stroke weight | Consistent with diagram stroke discipline (1–1.5px at reference size) |

### 5. Design Language compliance

| Test | Pass condition |
| --- | --- |
| Simplicity | Mark decomposes to essential form — no detail that disappears below 16px |
| Restraint | No gradients, glows, 3D effects, or decorative complexity |
| No mascot | No figurative character, bird literalism, or anthropomorphized imagery |
| Permanence | Mark would remain appropriate decades from now |

### 6. Institutional character

| Test | Pass condition |
| --- | --- |
| Stranger test | Independent reader still perceives institution, not brand |
| Repository test | Repository callout remains visually prominent relative to mark |
| Scholarship test | Mark feels like it belongs on archival matter, not product packaging |

---

## Placement on the Canonical Page

The mark inhabits the environment defined in [CANONICAL-PAGE-SPECIFICATION-v1.0.md](CANONICAL-PAGE-SPECIFICATION-v1.0.md).

It shall remain **subordinate to content** in all placements.

### Primary placement — site header

| Property | Specification |
| --- | --- |
| Position | Left of site navigation, or above navigation within header region |
| Alignment | Left-aligned within `layout.max-width.wide` |
| Maximum height | 24px (1.5× navigation text cap height) |
| Maximum width | 24px square, or 32px horizontal if wordmark component |
| Separation from navigation | `spacing.4` (16px) minimum |
| Separation from page title | Header region ends with `spacing.section.gap-sm` (32px) before h1 — mark does not intrude into title space |

### Secondary placement — footer

| Property | Specification |
| --- | --- |
| Position | Left of or above institutional identifier text in footer |
| Maximum height | 16px |
| Color | `text.tertiary` (`#6B6B63`) or `text.primary` — not accent |
| Role | Quiet acknowledgment — not branding statement |

### Tertiary placement — preservation volumes and print

| Property | Specification |
| --- | --- |
| Position | Colophon area, title page imprint |
| Maximum height | 20mm on A4 |
| Color | Black only for print |
| Role | Volume identification — same mark, reduced |

### Prohibited placements

- Hero position above or replacing page title
- Centered above h1 as dominant brand statement
- Watermark across page body
- Favicon-only identity (favicon not authorized at this phase)
- Social media profile circle crop as primary design constraint

---

## Scale and Proportion

| Context | Maximum dimension | Minimum dimension |
| --- | --- | --- |
| Site header | 24px height | 16px height |
| Footer | 16px height | 12px height |
| Print colophon | 20mm | 8mm |
| Minimum readable size | — | 12px (below this, use text identifier only) |

**Rule:** When the mark falls below minimum readable size, the text identifier "Project Garuda" (`typography.role.ui`, `typography.size.xs`) replaces it.

The mark never scales larger than the page title.

---

## Mark Types Under Exploration

The following mark **types** are within exploration scope.

Specific designs are **not** authorized until Institutional Mark Selection.

| Type | Description | Institutional fit |
| --- | --- | --- |
| **Letterform mark** | Single letter or monogram derived from typographic tradition | High — university press colophon tradition |
| **Geometric mark** | Minimal abstract form — circle, line, gate, threshold | High — if restrained to single stroke weight |
| **Wordmark component** | "Garuda" or "G" set in institutional serif | Medium — must not compete with page title typography |
| **Seal variant** | Circular or rectangular border enclosing minimal form | Medium — must avoid heraldic or governmental overtones |

### Types excluded from exploration

| Type | Reason |
| --- | --- |
| Figurative bird | Literal mascot — contradicts restraint; invites brand not institution |
| AI/tech iconography | Neural networks, nodes, circuits — contradicts scholarship character |
| Animated mark | Violates Design Language — no autoplay, no motion dependency |
| Gradient mark | Violates token discipline — monochrome required |
| 3D mark | Violates diagram and Design Language prohibitions |

---

## Relationship to Typography

The mark shall harmonize with the established type system:

| Element | Relationship |
| --- | --- |
| Page title (h1) | Mark is always smaller and visually subordinate |
| Body serif | Mark may share stroke weight sensibility but not letterform |
| Navigation sans | Mark sits adjacent to navigation, not within it |
| Mono repository paths | Mark never uses monospace — repository paths remain distinct |

**Rule:** The mark shall not introduce a third typographic voice.

Typography carries the institution.

The mark acknowledges it.

---

## Monochrome and Reproduction

All exploration assumes black-and-white reproduction as the primary fidelity test.

| Medium | Requirement |
| --- | --- |
| A4 print | Clear at 12mm width, no ink bleed dependency |
| Photocopy | Survives one generation of copy degradation |
| Emboss/deboss | Single-depth — no multi-level relief |
| Screen (grayscale) | Readable without color tokens applied |
| Small digital | Recognizable at 16×16px favicon preview — design for this, but favicon not authorized |

Warm paper (`background.primary`) and ink (`text.primary`) are the canonical rendering context.

---

## Exploration Process

Institutional Mark Exploration v1.0 defines the process for when mark **candidates** are evaluated (future authorization required to create candidates).

### Phase 1 — Criteria confirmation (this document)

Evaluation criteria, placement, and constraints are defined.

No candidates are created.

### Phase 2 — Candidate development (not authorized)

Requires separate Founder authorization for Institutional Mark Selection.

Candidates shall be evaluated against all criteria in this document.

### Phase 3 — Selection (not authorized)

Requires Founder Decision on adopted institutional mark.

---

## Success Criteria

Institutional Mark Exploration v1.0 succeeds when:

- [x] The design question is reframed from brand logo to institutional acknowledgment
- [x] Evaluation criteria are measurable and derived from the Canonical Page Specification
- [x] Placement on the Canonical Page is defined without requiring the mark to carry identity
- [x] Scale, monochrome, and reproduction requirements are specified
- [x] Mark types under exploration are identified with exclusions stated
- [ ] Reviewers agree the criteria would select a mark that acknowledges identity the page has already established *(pending review)*

---

## Not Authorized

This exploration does **not** authorize:

- Final institutional mark selection or adoption
- Creation of mark files (SVG, PNG, or equivalent)
- Favicon design
- CSS or stylesheet implementation
- Component library or page rendering
- Website deployment or hosting
- Public announcement or external communication
- Branding collateral

Those activities remain subject to future Founder authorization.

---

## Closing Note

The institution has earned its mark — not because it needs one, but because it has proven it no longer depends on one.

When the mark arrives, it will be remarkably simple.

Because everything complicated has already been expressed by the page.

The mark will not need to carry the institution.

It will simply acknowledge it.

May the mark belong on the page as naturally as the repository callout belongs in the body.

---

End of Institutional Mark Exploration v1.0
