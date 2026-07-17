# FastAPI backend for OmLang Compiler

This backend exposes a /compile endpoint that compiles and runs OmLang source using the existing om-core code in the repository. It captures VM output and (optionally) writes compile history to a NeonDB Postgres database.

Environment variables
- NEON_DATABASE_URL: Postgres connection string for Neon (optional, used to persist history)
- ALLOW_ORIGINS: comma-separated list of allowed CORS origins (optional). If not set, all origins are allowed.

Run locally
- python -m venv .venv
- source .venv/bin/activate
- pip install -r requirements.txt
- uvicorn main:app --reload --host 0.0.0.0 --port 8000

API
POST /compile
Request JSON: { "source": "...", "inputs": ["input1", "input2"] }
Response JSON: { success, bytecode, constants, runtime_output, errors }
