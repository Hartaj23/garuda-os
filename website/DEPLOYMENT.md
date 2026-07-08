# Public Deployment

## Hosting Environment Selection

| Field | Value |
| --- | --- |
| Founder Decision | [HOSTING-ENVIRONMENT-SELECTION-FOUNDER-DECISION.md](../docs/governance/HOSTING-ENVIRONMENT-SELECTION-FOUNDER-DECISION.md) |
| Deployment authorization | [MISSION-001-PUBLIC-DEPLOYMENT-AUTHORIZATION.md](../docs/governance/MISSION-001-PUBLIC-DEPLOYMENT-AUTHORIZATION.md) |
| Mission closure | [MISSION-001-CLOSURE.md](../docs/governance/MISSION-001-CLOSURE.md) |
| Platform | Cloudflare Pages (Git integration) |
| Pages project | `drgaruda` |
| Repository | `Hartaj23/garuda-os` |
| Production branch | `master` |
| Public domain | `drgaruda.com` |
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

Cloudflare Pages runs the same build command during Git-triggered deploys.

---

## Local Preview

```bash
.venv/bin/python website/scripts/build_site.py
python -m http.server 8000 --directory website/public
```

Open `http://localhost:8000/`

---

## Public Deployment — Cloudflare Pages Git Integration

Deployment is triggered by Cloudflare when changes are pushed to `master`.

Cloudflare clones the repository, runs the build command, and publishes `website/public/`.

No Wrangler CLI step is required. No GitHub Actions deploy workflow is required.

### One-time Cloudflare setup

1. Sign in to [Cloudflare Dashboard](https://dash.cloudflare.com/).
2. Go to **Workers & Pages** → **Create application** → **Pages** → **Connect to Git**.
3. Click **Get started** and select **GitHub**.
4. If the Cloudflare GitHub App is not yet installed, authorize it on GitHub, then return to Cloudflare.
5. Select repository **`Hartaj23/garuda-os`**.
6. Configure the project:

| Setting | Value |
| --- | --- |
| Project name | `drgaruda` |
| Production branch | `master` |
| Framework preset | None |
| Build command | `python3 website/scripts/build_site.py` |
| Build output directory | `website/public` |
| Root directory | `/` (repository root) |

7. (Optional) Environment variable: `PYTHON_VERSION` = `3.11`
8. Save and deploy.
9. Open project **`drgaruda`** → **Custom domains** → add **`drgaruda.com`**.
10. Ensure DNS for **`drgaruda.com`** is managed by Cloudflare and shows **Active**.

### After setup

Each push to `master` that Cloudflare monitors triggers a new build and deploy automatically.

Monitor builds in Cloudflare: **Workers & Pages** → **`drgaruda`** → **Deployments**.

### Verify deployment

1. Visit `https://drgaruda.com/`.
2. Read the homepage once on the live domain.
3. Confirm repository links resolve (e.g. `https://drgaruda.com/docs/institutional/PUBLIC-WELCOME.md`).

---

## Institutional Commitments

- The website introduces the institution.
- The repository remains the canonical authority.
- Hosting is infrastructure — not governance authority.

---

End of Public Deployment Documentation
