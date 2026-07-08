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
| Pages root directory | `website/` |
| Deploy root | `public/` (relative to `website/`) |

---

## Why the Pages root is `website/`

The repository root contains engineering metadata (`pyproject.toml`, `package.json`) for the full Garuda monorepo. Cloudflare Pages detects those files and runs dependency installation (for example `pip install .`) before the build command.

The public website is a **static build** inside `website/`. It uses stdlib Python only via `scripts/build_site.py` and does not require installing the monorepo as a Python package.

Scoping the Cloudflare **Root directory** to `website/` tells Cloudflare to treat this subtree as the Pages project only.

Repository-side markers:

- [wrangler.toml](wrangler.toml) — Pages output directory declaration
- [.python-version](.python-version) — Python version for the static build

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

Cloudflare runs the equivalent command from the `website/` directory during Git-triggered deploys.

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

Cloudflare clones the repository, runs the build from `website/`, and publishes `website/public/`.

No Wrangler CLI deploy step is required. No GitHub Actions deploy workflow is required.

### Cloudflare project settings

| Setting | Value |
| --- | --- |
| Project name | `drgaruda` |
| Production branch | `master` |
| Root directory | `website` |
| Framework preset | None |
| Build command | `python3 scripts/build_site.py` |
| Build output directory | `public` |

### Optional safety net

If Cloudflare still attempts dependency installation, add this environment variable in **Settings → Environment variables** (Production and Preview):

| Variable | Value |
| --- | --- |
| `SKIP_DEPENDENCY_INSTALL` | `1` |

This disables automatic `pip install` / `npm install` and runs only the build command above.

### One-time Cloudflare setup

1. Sign in to [Cloudflare Dashboard](https://dash.cloudflare.com/).
2. Go to **Workers & Pages** → **Create application** → **Pages** → **Connect to Git**.
3. Select repository **`Hartaj23/garuda-os`**.
4. Apply the project settings in the table above.
5. Save and deploy.
6. Open project **`drgaruda`** → **Custom domains** → add **`drgaruda.com`** and **`www.drgaruda.com`**.
7. Ensure DNS for **`drgaruda.com`** is managed by Cloudflare and shows **Active**.

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
