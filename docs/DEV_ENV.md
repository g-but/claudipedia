# Development Environment

This repo contains a decoupled stack. For the backend, use `backend/requirements.txt` as the source of truth. The root `requirements.txt` is for extra/dev use only and should not be used for production backend environments.

## Backend (FastAPI)

- Primary deps: `backend/requirements.txt`
- Recommended Python: 3.11–3.13
- Local run:

```
python -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
export PYTHONPATH=$(pwd)
cd backend && ./start.sh
```

## Tests

- CI runs `tests/test_graph_db.py` using stdlib `unittest` only (no network installs).
- `tests/test_models.py` uses `pytest`; run locally if you have it installed.

## Import Paths

- Canonical backend core modules live in `src/core/*`.
- The previous duplicates under `backend/src/core` were removed to avoid drift.

## Neo4j

- Optional at import time: the code gracefully degrades if the `neo4j` package is missing so unit tests can run without it.
- To use the real DB, set `NEO4J_URI`, `NEO4J_USER`, and `NEO4J_PASSWORD`.

