# Public Deployment

## Hosting Environment Selection

| Field | Value |
| --- | --- |
| Founder Decision | [HOSTING-ENVIRONMENT-SELECTION-FOUNDER-DECISION.md](../docs/governance/HOSTING-ENVIRONMENT-SELECTION-FOUNDER-DECISION.md) |
| Deployment authorization | [MISSION-001-PUBLIC-DEPLOYMENT-AUTHORIZATION.md](../docs/governance/MISSION-001-PUBLIC-DEPLOYMENT-AUTHORIZATION.md) |
| Mission closure | [MISSION-001-CLOSURE.md](../docs/governance/MISSION-001-CLOSURE.md) |
| Platform | Cloudflare Pages |
| Pages project | `drgaruda` |
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

The workflow builds the site and publishes `website/public/` to Cloudflare Pages project **`drgaruda`**.

### GitHub repository secrets

Configure these secrets before the first deploy:

| Secret | Purpose |
| --- | --- |
| `CLOUDFLARE_API_TOKEN` | API token with Cloudflare Pages edit permission |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare account identifier |

### Cloudflare Pages project — create if missing

If project **`drgaruda`** does not exist yet:

1. Sign in to [Cloudflare Dashboard](https://dash.cloudflare.com/).
2. Go to **Workers & Pages** → **Create application** → **Pages** → **Connect to Git** (or **Upload assets** if using CI-only deploy).
3. For CI deploy via GitHub Actions, create an empty project:
   - **Workers & Pages** → **Create application** → **Pages** → **Import an existing Git repository** is optional;
   - Alternatively: **Create application** → **Pages** → **Upload assets** → name the project **`drgaruda`** → deploy a placeholder, then subsequent CI deploys overwrite it.
   - Simplest path when using Wrangler from GitHub Actions: run the workflow once with secrets set; Wrangler creates the project **`drgaruda`** on first successful deploy if it does not exist.
4. Open project **`drgaruda`** → **Custom domains** → **Set up a custom domain**.
5. Add **`drgaruda.com`** (and `www.drgaruda.com` if desired).
6. Ensure DNS for **`drgaruda.com`** is managed by Cloudflare and shows **Active** for the Pages binding.

### Verify deployment

1. Re-run **Deploy Public Site** in GitHub Actions after secrets are configured.
2. Visit `https://drgaruda.com/`.
3. Confirm repository links resolve (e.g. `https://drgaruda.com/docs/institutional/PUBLIC-WELCOME.md`).

---

## Institutional Commitments

- The website introduces the institution.
- The repository remains the canonical authority.
- Hosting is infrastructure — not governance authority.

---

End of Public Deployment Documentation
