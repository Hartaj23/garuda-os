# Styles

## Mission 001 — Phase C — Implementation

| Field | Value |
| --- | --- |
| Authorization | [MISSION-001-PHASE-C-IMPLEMENTATION-AUTHORIZATION.md](../../docs/governance/MISSION-001-PHASE-C-IMPLEMENTATION-AUTHORIZATION.md) |
| Tokens source | [../brand/tokens/design-tokens.yaml](../brand/tokens/design-tokens.yaml) |
| Page specification | [../brand/CANONICAL-PAGE-SPECIFICATION-v1.0.md](../brand/CANONICAL-PAGE-SPECIFICATION-v1.0.md) |

CSS derived exclusively from approved Design Tokens v1.0.

Built copies are published to `pages/assets/styles/` by the site builder.

---

## Files

| File | Purpose |
| --- | --- |
| [tokens.css](tokens.css) | CSS custom properties from design tokens |
| [main.css](main.css) | Canonical page layout and component styles |

---

## Build

```bash
.venv/bin/python website/scripts/build_site.py
```

---

End of Styles Documentation
