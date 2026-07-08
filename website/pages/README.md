# Pages

## Mission 001 — Phase C — Implementation

| Field | Value |
| --- | --- |
| Authorization | [MISSION-001-PHASE-C-IMPLEMENTATION-AUTHORIZATION.md](../../docs/governance/MISSION-001-PHASE-C-IMPLEMENTATION-AUTHORIZATION.md) |
| Builder | [../scripts/build_site.py](../scripts/build_site.py) |
| Source content | [../content/](../content/) |

Generated HTML gateway pages. Faithful translation of approved content and Canonical Page Specification.

**Deployment not authorized.**

---

## Build

```bash
.venv/bin/python website/scripts/build_site.py
```

Output: 19 gateway pages, assets (styles, institutional mark).

---

## Local Preview

Serve from repository root so repository links resolve:

```bash
python -m http.server 8000
```

Open `http://localhost:8000/website/pages/`

---

End of Pages Documentation
