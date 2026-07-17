# OmLang Compiler web app

This repository now includes a minimal backend (FastAPI) and frontend (Next.js) skeleton to turn the CLI compiler into a web app.

What I added
- backend/: FastAPI service that wraps om-core and exposes /compile
- frontend/: Minimal Next.js app for editing source and calling /compile

Next steps for you
1. In Vercel, deploy the frontend by pointing to the `frontend/` directory (set the root to frontend in the project settings) and set NEXT_PUBLIC_API_URL to your backend URL.
2. Deploy the backend to a host that supports Python/asyncpg (Render, Railway, Fly, Cloud Run, or a Docker container). Set NEON_DATABASE_URL in the backend environment variables.
3. Set CORS origins: set ALLOW_ORIGINS in backend environment to your Vercel frontend URL (or leave empty to allow all origins during testing).

Notes
- I kept om-core unchanged and used the existing "init" methods. For a cleaner codebase, convert init to __init__ and repr to __repr__ in om-core modules.
- Do not expose NEON_DATABASE_URL in the frontend. Only backend should have DB credentials.

If you want, I can create a GitHub Action to build and deploy the frontend to Vercel automatically, or prepare a Docker image and deployment manifest for the backend.
