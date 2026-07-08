# Public Deployment

## Mission 001 — Public Deployment Authorization

| Field | Value |
| --- | --- |
| Authorization | [MISSION-001-PUBLIC-DEPLOYMENT-AUTHORIZATION.md](../docs/governance/MISSION-001-PUBLIC-DEPLOYMENT-AUTHORIZATION.md) |
| Mission closure | [MISSION-001-CLOSURE.md](../docs/governance/MISSION-001-CLOSURE.md) |
| Hosting | GitHub Pages |
| Deploy root | `website/public/` |

---

## Build

```bash
.venv/bin/python website/scripts/build_site.py
```

Generates:

- 19 gateway HTML pages
- CSS assets from approved design tokens
- Institutional Mark v1.0 (C-03 Baseline)
- `docs/` mirror for repository-first navigation

---

## Local Preview

```bash
.venv/bin/python website/scripts/build_site.py
python -m http.server 8000 --directory website/public
```

Open `http://localhost:8000/`

---

## Public Deployment

Deployment is automated via GitHub Actions on push to `master` when `website/` or `docs/` changes.

Workflow: [.github/workflows/deploy-public-site.yml](../.github/workflows/deploy-public-site.yml)

**Repository setting required:** GitHub Pages → Source → GitHub Actions.

---

## Institutional Commitments

- The website introduces the institution.
- The repository remains the canonical authority.
- Deployment grants visibility — not governance authority.

---

End of Public Deployment Documentation
