# apps/web

## Purpose

Provides the first Next.js and TypeScript frontend shell for Garuda.

## Owner

Founding Team.

## Dependencies

Minimal frontend shell, typed API client helpers and backend API contracts.

## Related Documents

- GAR-0003
- GAR-0003A
- GAR-SPRINT-0001

## AI Implementation Notes

The initial frontend shell remains limited to infrastructure concerns and a landing dashboard. Authentication, trading, portfolio, AI UI and other business features are intentionally out of scope.

## Frontend Configuration

Copy [.env.example](.env.example) to .env.local and adjust values if you need to point the dashboard at a different backend URL.

## Backend Integration

Run the backend locally:

```bash
cd ../..
source .venv/bin/activate
python -m uvicorn services.backend.app:app --host 127.0.0.1 --port 8000
```

Then run the frontend:

```bash
cd apps/web
cp .env.example .env.local
npm install
npm run dev
```

The frontend dashboard calls the backend health and version endpoints over HTTP and expects the backend to allow the frontend origin configured by GARUDA_ALLOWED_ORIGINS.

