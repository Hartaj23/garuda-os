# Hosting Environment Selection — Founder Decision

| Field | Value |
| --- | --- |
| Decision ID | HOSTING-ENVIRONMENT-SELECTION |
| Status | **Ratified** |
| Decision date | 2026-07-08 |
| Institution state | **Institutional HOLD** |
| Mission 001 closure | [MISSION-001-CLOSURE.md](MISSION-001-CLOSURE.md) |
| Deployment authorization | [MISSION-001-PUBLIC-DEPLOYMENT-AUTHORIZATION.md](MISSION-001-PUBLIC-DEPLOYMENT-AUTHORIZATION.md) |
| Recommendation | [FOUNDER-RECOMMENDATION-HOSTING-ENVIRONMENT-SELECTION.md](../institutional/FOUNDER-RECOMMENDATION-HOSTING-ENVIRONMENT-SELECTION.md) |

This decision selects the institution's permanent public hosting environment only.

It creates no constitutional, architectural, sprint, or engineering authority beyond approved hosting selection.

It does not modify the accepted Public Foundation, site architecture, or deployment build.

---

## Founder Decision

The Founding Generation hereby ratifies the Hosting Environment Selection for the Project Garuda Public Foundation.

---

## Hosting Environment

**Cloudflare Pages** is adopted as the hosting platform for the Public Foundation.

The hosting platform is operational infrastructure only.

It possesses no constitutional, governance, or architectural authority.

The repository remains the institution's canonical source of truth.

---

## Public Domain

The Public Foundation shall be published at:

**garuda.foundation**

Should operational requirements require future migration, the institution may change hosting providers without affecting its constitutional authority, governance history, repository integrity, or public identity.

Infrastructure serves the institution.

The institution does not serve the infrastructure.

---

## Selected Configuration

| Field | Value |
| --- | --- |
| Platform | Cloudflare Pages |
| Primary domain | `garuda.foundation` |
| Public URL | `https://garuda.foundation/` |
| Source repository | `Hartaj23/garuda-os` |
| Deploy branch | `master` |
| Build command | `python website/scripts/build_site.py` |
| Output directory | `website/public` |
| Workflow | `.github/workflows/deploy-public-site.yml` |

---

## Operational Direction

Implementation shall proceed through the previously approved deployment pipeline, adapted only as necessary to target the approved hosting environment.

No architectural, design, governance, or institutional modifications are authorized through this decision.

---

## Institutional Commitments

- The website introduces the institution.
- The repository remains the canonical authority.
- Hosting is infrastructure — not governance.
- The accepted Public Foundation shall not be altered by this decision.

---

## Success Criteria

Hosting selection shall be considered complete when:

- `https://garuda.foundation/` resolves to the accepted Public Foundation,
- HTTPS is active,
- repository links function correctly,
- the experience matches the accepted Mission 001 implementation.

---

## Closing Declaration

Mission 001 remains accepted and closed.

This decision concerns only the institution's public address.

With this ratification, the Founding Generation selects the permanent home from which Project Garuda shall welcome the world.

May that home reflect the same clarity, restraint, legitimacy, and stewardship through which the institution itself was built.

---

End of Hosting Environment Selection — Founder Decision
