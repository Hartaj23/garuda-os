# Project Garuda

# Design Tokens v1.0

## Mission 001 — Phase B (Brand Foundation)

| Field | Value |
| --- | --- |
| Document Type | Brand Foundation |
| Authority | Visual Implementation Guidance Only |
| Authorization | [MISSION-001-PHASE-B-DESIGN-TOKENS-AUTHORIZATION.md](../../docs/governance/MISSION-001-PHASE-B-DESIGN-TOKENS-AUTHORIZATION.md) |
| Derives from | [VISUAL-PHILOSOPHY-v1.0.md](VISUAL-PHILOSOPHY-v1.0.md), [DESIGN-LANGUAGE-v1.0.md](DESIGN-LANGUAGE-v1.0.md) |
| Machine-readable | [tokens/design-tokens.yaml](tokens/design-tokens.yaml) |
| Version | 1.0 |

This document creates no constitutional, architectural, sprint, or engineering authority.

It does not authorize logo design, website implementation, public deployment, or external communication.

---

## Purpose

Design Tokens v1.0 translates Visual Philosophy and Design Language into reusable visual values.

Tokens are **tools** implementing **judgment**.

Typography and color serve the page — the page is the identity.

---

## Legitimacy Chain

```
Visual Philosophy v1.0              ✓ Recorded
Design Language v1.0                ✓ Recorded
Design Tokens v1.0                  ✓ Recorded (this document)
Canonical Page Specification v1.0   ✓ Recorded
Logo                                — not authorized
Implementation                      — not authorized
```

---

## Color Palette

Warm archival paper. Restrained ink. Institutional slate accent.

| Token | Value | Use |
| --- | --- | --- |
| `background.primary` | `#F7F5F0` | Page ground — warm paper |
| `background.secondary` | `#EFEDE6` | Section separation |
| `background.elevated` | `#FFFFFF` | Diagrams, elevated surfaces |
| `text.primary` | `#1C1C1A` | Body and headings |
| `text.secondary` | `#4A4A45` | Supporting prose |
| `text.tertiary` | `#6B6B63` | Metadata, captions |
| `accent.primary` | `#2E4057` | Institutional slate — links, emphasis |
| `link.visited` | `#4A3728` | Archive brown |
| `border.subtle` | `#E5E2DA` | Dividers, frames |
| `semantic.repository` | `#2E4057` | Canonical repository links |

### Color rationale

- No neon, no gradients, no dark-mode-by-default.
- Palette designed to feel like printed institutional matter on quality paper.
- Accent is authoritative, not promotional.

### Contrast (WCAG 2.1 AA)

| Pairing | Ratio | Pass |
| --- | --- | --- |
| `text.primary` on `background.primary` | ~14.5:1 | ✓ AAA body |
| `text.secondary` on `background.primary` | ~7.5:1 | ✓ AA body |
| `accent.primary` on `background.primary` | ~8.2:1 | ✓ AA body |
| `text.primary` on `background.elevated` | ~15:1 | ✓ AAA body |

---

## Typography System

| Role | Family | Rationale |
| --- | --- | --- |
| Display & headings | Serif (`Source Serif 4` stack) | University press, constitutional archive |
| Body | Serif | Reading is the primary experience |
| UI & navigation | Sans (`Source Sans 3` stack) | Clarity for wayfinding |
| Code & paths | Mono (`IBM Plex Mono` stack) | Repository references |

### Scale

| Token | Size | Use |
| --- | --- | --- |
| `4xl` | 40px | Home proposition only |
| `3xl` | 32px | Page title (h1) |
| `2xl` | 26px | Section title (h2) |
| `xl` | 22px | Subsection (h3) |
| `lg` | 19px | Lead paragraph |
| `base` | 17px | Body text |
| `sm` | 14px | Secondary, navigation |
| `xs` | 13px | Captions, disclaimers |

### Rules

- Body line-height: `1.6` minimum.
- Hierarchy through size and spacing — not color alone.
- No all-caps headings.
- Maximum one display size (`4xl`) per page.

---

## Spacing Scale

Base unit: **4px**.

| Token | Value | Typical use |
| --- | --- | --- |
| `1` | 4px | Tight inline |
| `2` | 8px | List items |
| `4` | 16px | Paragraph internal |
| `6` | 24px | Component padding |
| `8` | 32px | Section gap (small) |
| `12` | 48px | Section gap (medium) |
| `16` | 64px | Section gap (large) |
| `24` | 96px | Major page divisions |

### Page margins

| Viewport | Margin |
| --- | --- |
| Mobile | 24px |
| Tablet | 48px |
| Desktop | 64px |

Generous whitespace is mandatory — not optional decoration.

---

## Layout Grid

| Token | Value | Use |
| --- | --- | --- |
| `max-width.prose` | 42rem (~672px) | Primary reading column |
| `max-width.content` | 48rem (~768px) | Gateway pages |
| `max-width.wide` | 72rem (~1152px) | Navigation + content |
| `max-width.full` | 80rem (~1280px) | Site maximum |

### Grid

- 12 columns
- Gutter: 24px (32px at large breakpoints)
- Target measure: 65–75 characters per line for body text

### Rules

- One primary reading column dominates every page.
- Navigation is visually subordinate to content.
- Content never edge-to-edge except intentional diagram full-bleed.

---

## Diagram Styling

Aligned with Institutional Atlas discipline.

| Property | Value |
| --- | --- |
| Stroke (default) | 1.5px `#1C1C1A` |
| Stroke (secondary) | 1px `#6B6B63` |
| Fill | `#EFEDE6` |
| Fill (accent) | `#E8EBF0` |
| Arrow | `#2E4057`, 6px head |
| Corner radius | 2px maximum |
| Label font | Sans, `sm` |

### Rules

- Diagram palette uses tokens only — no ad-hoc colors.
- Labels readable without legend when possible.
- No gradients, glows, or 3D effects.

---

## Accessibility Requirements

| Requirement | Standard |
| --- | --- |
| Contrast | WCAG 2.1 AA minimum |
| Body text contrast | ≥ 4.5:1 |
| Large text contrast | ≥ 3:1 |
| Focus indicator | 2px `#2E4057` ring, 2px offset |
| Motion | Respect `prefers-reduced-motion` |
| Autoplay | Prohibited |
| Touch targets | Minimum 44px |

Repository links and navigation shall remain keyboard-accessible and screen-reader identifiable.

---

## Repository Link Treatment

Canonical repository references receive distinct but restrained styling:

- Monospace font for paths
- `semantic.repository` color
- Visible focus state
- Never buried in footer gray-on-gray

This implements Design Language Rule: website introduces, repository governs.

---

## Not Authorized

This token set does **not** authorize:

- Logo design or logomark
- CSS/stylesheet implementation in `website/styles/`
- Page rendering in `website/pages/`
- Public deployment or hosting
- Social launch or external campaigns

---

## Closing Note

These tokens implement judgment documented in Visual Philosophy and Design Language.

When implementation is authorized, tokens shall be applied consistently so that **the page** — not a logo — carries institutional identity.

---

End of Design Tokens v1.0
