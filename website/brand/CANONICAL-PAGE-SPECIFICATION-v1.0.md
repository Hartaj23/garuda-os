# Project Garuda

# Canonical Page Specification v1.0

## Mission 001 — Phase B (Brand Foundation)

| Field | Value |
| --- | --- |
| Document Type | Brand Foundation |
| Authority | Visual Implementation Guidance Only |
| Authorization | [MISSION-001-PHASE-B-CANONICAL-PAGE-SPECIFICATION-AUTHORIZATION.md](../../docs/governance/MISSION-001-PHASE-B-CANONICAL-PAGE-SPECIFICATION-AUTHORIZATION.md) |
| Derives from | [VISUAL-PHILOSOPHY-v1.0.md](VISUAL-PHILOSOPHY-v1.0.md), [DESIGN-LANGUAGE-v1.0.md](DESIGN-LANGUAGE-v1.0.md), [DESIGN-TOKENS-v1.0.md](DESIGN-TOKENS-v1.0.md) |
| Token reference | [tokens/design-tokens.yaml](tokens/design-tokens.yaml) |
| Version | 1.0 |

This document creates no constitutional, architectural, sprint, or engineering authority.

It does not authorize logo design, CSS, website implementation, public deployment, or external communication.

---

## Purpose

Canonical Page Specification v1.0 defines **what a Project Garuda page looks like** — in measurable detail, not in theory.

It is the institutional reference from which future website pages, research papers, preservation volumes, presentations, and public publications may derive consistent visual structure.

It is the canonical expression of Project Garuda's visual identity **before** the introduction of any institutional mark.

If the logo were removed, this page should still unmistakably feel like Project Garuda.

---

## Legitimacy Chain

```
Visual Philosophy v1.0              ✓ Recorded
        ↓
Design Language v1.0                ✓ Recorded
        ↓
Design Tokens v1.0                  ✓ Recorded
        ↓
Canonical Page Specification v1.0   ✓ Recorded (this document)
        ↓
Logo                                — not authorized
        ↓
Implementation                      — not authorized
```

---

## The Canonical Page

One page structure governs all public Garuda artifacts at this phase.

The **Canonical Page** is a gateway page: it introduces an idea, orients the reader, and points to the repository as authority.

It is not a landing page, not a dashboard, not a marketing surface.

It is a single column of reading matter on warm paper, with calm navigation above and institutional footer below.

No logo appears on the Canonical Page at this specification level. Identity emerges from structure alone.

---

## Page Canvas

### Ground

| Property | Token | Value |
| --- | --- | --- |
| Page background | `background.primary` | `#F7F5F0` — warm paper |
| Maximum site width | `layout.max-width.full` | 80rem (~1280px) |
| Content alignment | — | Centered within viewport |

The page ground is uniform warm paper. No gradient, no texture overlay, no dark-mode inversion.

### Page Width

| Region | Token | Width |
| --- | --- | --- |
| Primary reading column | `layout.max-width.prose` | 42rem (~672px) |
| Gateway content column | `layout.max-width.content` | 48rem (~768px) |
| Navigation + content shell | `layout.max-width.wide` | 72rem (~1152px) |

**Rule:** One primary reading column dominates. The Canonical Page uses the **gateway content column** (`48rem`) as its default measure — wide enough for metadata tables and repository links, narrow enough for sustained reading.

Content never spans the full site width except intentional diagram full-bleed (see Diagrams).

### Margins

| Viewport | Token | Margin |
| --- | --- | --- |
| Mobile (< 768px) | `spacing.page.margin-mobile` | 24px each side |
| Tablet (768px–1023px) | `spacing.page.margin-tablet` | 48px each side |
| Desktop (≥ 1024px) | `spacing.page.margin-desktop` | 64px each side |

**Rule:** Margins are minimum values. Content shall never touch the viewport edge. On desktop, the reading column sits within margins with visible paper on all sides.

---

## Reading Measure

| Property | Specification |
| --- | --- |
| Target characters per line | 65–75 (`layout.reading.measure-chars`) |
| Body size | `typography.size.base` — 17px |
| Body line-height | `typography.line-height.normal` — 1.6 minimum |
| Body font | `typography.role.body` — serif |

**Rule:** If body text exceeds 75 characters per line at the chosen column width, reduce effective measure or increase side margins. Reading comfort takes precedence over using available width.

Lead paragraphs may use `typography.size.lg` (19px) at the same measure.

---

## Spacing Rhythm

Base unit: **4px** (`spacing.unit`).

### Vertical section gaps

| Relationship | Token | Gap |
| --- | --- | --- |
| Between major page regions (header → body → footer) | `spacing.section.gap-lg` | 64px |
| Between content sections (h2 blocks) | `spacing.section.gap-md` | 48px |
| Between subsections (h3 blocks) | `spacing.section.gap-sm` | 32px |
| Between heading and following content | `spacing.6` | 24px |
| Between paragraph and following paragraph | `spacing.paragraph.after` | 1.25em |

### Rhythm rules

- Related elements cluster; unrelated elements separate by a full section gap.
- No two adjacent blocks shall share the same visual weight without intervening space.
- Major page divisions (title block, body, repository callout, footer) each receive `spacing.section.gap-lg` separation.
- Whitespace is **active** — it signals institutional confidence, not unfinished layout.

---

## Heading Hierarchy

All headings use serif (`typography.role.heading`). Hierarchy emerges through size and spacing — not color alone, not all-caps, not decorative weight.

| Level | Token | Size | Weight | Use |
| --- | --- | --- | --- | --- |
| Page title (h1) | `typography.size.3xl` | 32px | 600 (semibold) | One per page — the entry point |
| Section title (h2) | `typography.size.2xl` | 26px | 600 | Major content divisions |
| Subsection (h3) | `typography.size.xl` | 22px | 600 | Subordinate structure |
| Minor heading (h4) | `typography.size.lg` | 19px | 500 (medium) | Rare — metadata groupings only |

### Heading rules

- **One h1 per page.** It is the clear entry point.
- Heading levels shall not be skipped (no h1 → h3).
- No all-caps headings.
- Headings use `text.primary` — not accent color.
- Space below each heading: `spacing.6` (24px) before body content begins.
- Space above h2: `spacing.section.gap-md` (48px) when following body text.
- Space above h3: `spacing.section.gap-sm` (32px) when following body text.
- Body text remains the dominant visual weight; headings guide, they do not dominate.

### Prohibited

- Multiple elements styled as "most important."
- Display size (`typography.size.4xl`, 40px) on gateway pages — reserved for home proposition only.
- Color or weight used to shout where structure would suffice.

---

## Paragraph Rhythm

| Property | Specification |
| --- | --- |
| Body font | Serif, `typography.size.base` (17px) |
| Body color | `text.primary` (`#1C1C1A`) |
| Line-height | 1.6 minimum |
| Paragraph spacing | 1.25em after each paragraph |
| Lead paragraph | First paragraph after h1 may use `typography.size.lg` (19px), `text.secondary` optional |
| Maximum consecutive paragraphs without structure | 4 — then introduce h2, list, blockquote, or repository callout |

### Paragraph rules

- Paragraphs are left-aligned. No justified text (avoids rivers and institutional stiffness).
- No indent-first-line convention — separation is vertical, not horizontal.
- Short paragraphs preferred on gateway pages. Long-form prose lives in the repository.
- One primary idea per paragraph.

---

## Quotations

### Block quotations

Institutional quotations — from constitutions, preservation volumes, founder literature — receive distinct but restrained treatment.

| Property | Specification |
| --- | --- |
| Left border | 3px solid `border.default` (`#D4D0C4`) |
| Padding left | `spacing.4` (16px) |
| Background | None, or `background.secondary` (`#EFEDE6`) for extended quotations |
| Font | Serif, same size as body |
| Color | `text.secondary` (`#4A4A45`) |
| Attribution | Sans, `typography.size.sm`, `text.tertiary`, on separate line below with `spacing.4` gap |

### Inline quotations

| Property | Specification |
| --- | --- |
| Style | Typographic quotes — no straight ASCII quotes in rendered output |
| Emphasis | None beyond quotation marks; no italic-by-default |

### Quotation rules

- Blockquotes shall not exceed 4 lines on gateway pages without a link to full source in the repository.
- Every blockquote from an institutional source shall include attribution.
- Quotations serve comprehension — not decoration.

---

## Lists

| Property | Unordered | Ordered |
| --- | --- | --- |
| Indent | `spacing.6` (24px) from column edge | Same |
| Item spacing | `spacing.2` (8px) between items | Same |
| Marker | Disc — restrained, `text.secondary` | Decimal — `text.secondary` |
| Item font | Body serif, `typography.size.base` | Same |
| Nested levels | Maximum 2 | Maximum 2 |

### List rules

- Lists shall be short or deliberately structured. Walls of bullets are prohibited.
- Each list item should be a complete thought — not a fragment series.
- Space above list: `spacing.4` (16px). Space below list: `spacing.6` (24px).
- Lists introduce options or steps — they do not replace prose where prose is clearer.

---

## Tables

Tables serve comparison and reference — not information dumping.

| Property | Specification |
| --- | --- |
| Width | 100% of content column |
| Header row | Sans, `typography.size.sm`, weight 600, `text.primary` |
| Body rows | Serif or sans, `typography.size.sm`, `text.secondary` |
| Cell padding | `spacing.4` horizontal, `spacing.3` vertical |
| Row separator | 1px `border.subtle` (`#E5E2DA`) |
| Header separator | 1px `border.default` (`#D4D0C4`) |
| Background | Transparent, or `background.secondary` for header row only |
| Alignment | Left for text; avoid centered body text |

### Table rules

- Maximum 4 columns on gateway pages.
- If a table requires more columns, link to the repository source instead.
- Tables shall include a clear header row.
- No zebra striping with strong contrast — subtle `background.secondary` alternation permitted at most.
- Metadata tables (Website Layer, Phase, Canonical Source) follow this treatment exactly.

---

## Diagrams

Diagrams inherit Institutional Atlas discipline — explanatory, restrained, token-bound.

| Property | Token / Value |
| --- | --- |
| Default stroke | 1.5px `diagram.stroke` (`#1C1C1A`) |
| Secondary stroke | 1px `diagram.stroke-secondary` (`#6B6B63`) |
| Fill | `diagram.fill` (`#EFEDE6`) |
| Accent fill | `diagram.fill-accent` (`#E8EBF0`) |
| Arrow | `diagram.arrow` (`#2E4057`), 6px head |
| Corner radius | 2px maximum |
| Label font | Sans, `typography.size.sm` |
| Surface | `background.elevated` (`#FFFFFF`) with 1px `border.subtle` frame |

### Placement

| Context | Width |
| --- | --- |
| Inline diagram | 100% of content column |
| Full-bleed diagram | May extend to `layout.max-width.wide` — never beyond |
| Margin above/below | `spacing.section.gap-sm` (32px) each side |

### Diagram rules

- Diagram palette uses tokens only — no ad-hoc colors.
- Labels readable without legend when possible.
- No gradients, glows, or 3D effects.
- Complex ideas decomposed into simpler figures — never one overwhelming illustration.
- Caption below: sans, `typography.size.xs`, `text.tertiary`, centered or left-aligned with `spacing.2` gap.

---

## Repository References

Repository references are first-class visual elements — not footer afterthoughts.

The website introduces. The repository governs.

### Canonical source callout

Every gateway page includes a **repository callout** — a visually distinct block pointing to the canonical source.

| Property | Specification |
| --- | --- |
| Position | After primary body content, before reading journey / footer |
| Separation | `spacing.section.gap-md` (48px) above |
| Label | Sans, `typography.size.sm`, weight 600, `text.primary` — e.g. "Read the full text in the repository:" |
| Link | Mono, `typography.size.sm`, `semantic.repository` (`#2E4057`) |
| Path display | Full repository path — e.g. `docs/institutional/MANIFESTO.md` |
| Focus state | 2px `accent.primary` ring, 2px offset |
| Background | Optional `background.secondary` panel with `spacing.6` padding |

### Inline repository links

| Property | Specification |
| --- | --- |
| Font | Mono (`typography.role.code`) |
| Color | `semantic.repository` |
| Style | Underline on hover only — not by default |
| Visited | `link.visited` (`#4A3728`) |

### Repository rules

- Canonical source shall never be buried in footer gray-on-gray.
- Repository path shall be visible and readable — not hidden behind generic "click here."
- The distinction between website introduction and repository authority shall be clear in layout, not only in words.
- At least one repository reference per gateway page.

---

## Navigation Placement

Navigation is visually subordinate to content — present, calm, never louder than the idea on the page.

### Site navigation (header)

| Property | Specification |
| --- | --- |
| Position | Top of page, above content column |
| Font | Sans (`typography.role.ui`), `typography.size.sm`, weight 500 |
| Color | `text.secondary` — active item `text.primary` |
| Layout | Horizontal on desktop; collapsible on mobile |
| Width | Spans `layout.max-width.wide` — not full viewport |
| Padding below | `spacing.section.gap-sm` (32px) before page title |
| Separator | Optional 1px `border.subtle` below navigation bar |

### Reading journey (in-page)

| Property | Specification |
| --- | --- |
| Position | After repository callout, before footer |
| Format | Inline text links separated by middle dots (·) |
| Label | "Reading journey:" in sans, `text.tertiary`, `typography.size.sm` |
| Links | Sans, `typography.size.sm`, `accent.primary` |
| Emphasis | Current page unlinked; adjacent pages linked |

### Navigation rules

- No sticky navigation that consumes vertical reading space on scroll.
- No hamburger-only navigation on desktop.
- Navigation items shall not outnumber primary content sections.
- Breadcrumbs permitted as alternative to reading journey — not both on the same page.

---

## Whitespace Behavior

Whitespace is a design element — not leftover space.

| Principle | Expression |
| --- | --- |
| Confidence | Generous margins and section gaps on all viewports |
| Grouping | Related content clusters with small internal gaps |
| Separation | Unrelated content separated by section gaps (32px–64px) |
| Entry | Clear space above h1 — page title breathes |
| Exit | Clear space before footer — reader reaches a stopping point |
| Density | Gateway pages: low density. One primary purpose per page. |

### Whitespace prohibitions

- Hero sections consuming the entire viewport.
- Stacked promotional blocks competing for attention.
- Edge-to-edge content (except intentional diagram full-bleed).
- Density requiring scroll before the first complete idea.

---

## Footer Structure

The footer closes the page with institutional calm — not marketing urgency.

| Property | Specification |
| --- | --- |
| Position | Bottom of page, after `spacing.section.gap-lg` (64px) from body |
| Width | Same as content column (`layout.max-width.content`) |
| Separator | 1px `border.subtle` above footer content |
| Padding top | `spacing.8` (32px) |

### Footer contents (in order)

1. **Repository authority line** — sans, `typography.size.xs`, `text.tertiary` — e.g. "The repository remains the institution's canonical source of truth."
2. **Institutional identifier** — sans, `typography.size.xs`, `text.tertiary` — "Project Garuda" as text only (no logo at this specification level).
3. **Governance disclaimer** — sans, `typography.size.xs`, `text.tertiary` — website introduces; repository governs.

### Footer rules

- Footer text is visually quiet — it does not compete with body content.
- No social media icons, newsletter signup, or promotional links in footer at this phase.
- Footer shall remain printable and archivable without truncation.

---

## Reference Page Anatomy

The following describes the **Canonical Page** as a single structural specimen — the gateway page all public pages shall resemble.

```
┌─────────────────────────────────────────────────────────────┐
│  [viewport margin: 64px desktop]                            │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  SITE NAVIGATION (sans, sm, secondary)                │  │
│  │  ─────────────────────────────────────────────────    │  │
│  │  [32px gap]                                           │  │
│  │                                                       │  │
│  │  PAGE TITLE (h1, serif, 32px, semibold)               │  │
│  │  [24px gap]                                           │  │
│  │                                                       │  │
│  │  METADATA TABLE (optional — Website Layer, Source)      │  │
│  │  [48px gap]                                           │  │
│  │                                                       │  │
│  │  LEAD PARAGRAPH (serif, 19px, optional)               │  │
│  │  [1.25em gap]                                         │  │
│  │                                                       │  │
│  │  BODY PARAGRAPHS (serif, 17px, line-height 1.6)       │  │
│  │  [48px gap]                                           │  │
│  │                                                       │  │
│  │  SECTION HEADING (h2, serif, 26px)                    │  │
│  │  [24px gap]                                           │  │
│  │  Body content...                                      │  │
│  │  [48px gap]                                           │  │
│  │                                                       │  │
│  │  ┌ REPOSITORY CALLOUT ─────────────────────────────┐  │  │
│  │  │  Read the full text in the repository:           │  │  │
│  │  │  docs/institutional/MANIFESTO.md  (mono, slate)  │  │  │
│  │  └──────────────────────────────────────────────────┘  │  │
│  │  [48px gap]                                           │  │
│  │                                                       │  │
│  │  Reading journey: Home · Next: Vision  (sans, sm)     │  │
│  │  [64px gap]                                           │  │
│  │  ─────────────────────────────────────────────────    │  │
│  │  FOOTER (sans, xs, tertiary)                          │  │
│  │  The repository remains the canonical source...       │  │
│  │  Project Garuda                                       │  │
│  └───────────────────────────────────────────────────────┘  │
│  [viewport margin: 64px desktop]                            │
└─────────────────────────────────────────────────────────────┘
```

**Background:** `background.primary` (`#F7F5F0`) throughout.

**Column width:** `layout.max-width.content` (48rem).

**No logo.** Identity from structure, typography, spacing, and repository prominence alone.

---

## Token Demonstration Summary

| Page element | Primary tokens |
| --- | --- |
| Page ground | `background.primary` |
| Body text | `text.primary`, `typography.size.base`, serif |
| Headings | `text.primary`, `typography.size.3xl/2xl/xl`, serif |
| Links | `accent.primary`, `link.visited` |
| Repository paths | `semantic.repository`, mono, `typography.size.sm` |
| Navigation | sans, `typography.size.sm`, `text.secondary` |
| Section gaps | `spacing.section.gap-md`, `spacing.section.gap-lg` |
| Blockquote border | `border.default` |
| Diagram stroke | `diagram.stroke`, `diagram.fill` |
| Footer | `text.tertiary`, `typography.size.xs`, sans |

All values are defined in [DESIGN-TOKENS-v1.0.md](DESIGN-TOKENS-v1.0.md) and [tokens/design-tokens.yaml](tokens/design-tokens.yaml).

---

## Success Criteria

Canonical Page Specification v1.0 succeeds when:

- [ ] Visual philosophy is observable without explanation — calm, clarity, permanence, legitimacy visible in layout alone.
- [ ] Design language rules are expressed through measurable layout behavior — not deferred to color or font selection.
- [ ] Design tokens are demonstrated consistently across every page element defined herein.
- [ ] The page remains recognizably Project Garuda without requiring a logo.
- [ ] Reviewers agree that removing the institutional mark would not diminish the page's identity.

---

## Not Authorized

This specification does **not** authorize:

- Logo design or logomark
- Favicon
- Illustrations beyond the structural diagram in this document
- CSS or stylesheet implementation
- Component library or page rendering
- Website deployment or hosting
- Public announcement or external communication
- Branding collateral

Those activities remain subject to future Founder authorization.

---

## Closing Note

The page precedes the mark.

The institution precedes the brand.

When logo design is authorized, the question will not be *"What logo should Garuda have?"* but *"What mark belongs naturally on a Garuda page?"*

This specification defines the environment that mark must inhabit.

May every page offer hospitality through clarity before it asks for attention.

---

End of Canonical Page Specification v1.0
