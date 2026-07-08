# Public Deployment

## Hosting Environment Selection

| Field | Value |
| --- | --- |
| Founder Decision | [HOSTING-ENVIRONMENT-SELECTION-FOUNDER-DECISION.md](../docs/governance/HOSTING-ENVIRONMENT-SELECTION-FOUNDER-DECISION.md) |
| Deployment authorization | [MISSION-001-PUBLIC-DEPLOYMENT-AUTHORIZATION.md](../docs/governance/MISSION-001-PUBLIC-DEPLOYMENT-AUTHORIZATION.md) |
| Mission closure | [MISSION-001-CLOSURE.md](../docs/governance/MISSION-001-CLOSURE.md) |
| Platform | Cloudflare Pages |
| Public domain | `garuda.foundation` |
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

The workflow builds the site and publishes `website/public/` to Cloudflare Pages.

### Cloudflare prerequisites

Configure these repository secrets before the first deploy:

| Secret | Purpose |
| --- | --- |
| `CLOUDFLARE_API_TOKEN` | API token with Cloudflare Pages edit permission |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare account identifier |

In Cloudflare:

1. Create a Pages project named `garuda-foundation` (or allow the first deploy to create it).
2. Add custom domain `garuda.foundation`.
3. Ensure DNS for `garuda.foundation` is managed by Cloudflare.

---

## Institutional Commitments

- The website introduces the institution.
- The repository remains the canonical authority.
- Hosting is infrastructure — not governance authority.

---

End of Public Deployment Documentation
