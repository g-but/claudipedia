# Claudipedia - AI-Powered Knowledge Platform

## Overview

Claudipedia is a **decoupled full-stack application** for collaborative knowledge building with AI. It features research profiles, context management, and a Neo4j-powered knowledge graph.

## Architecture

```
claudipedia/
├── web/                 # Next.js 15 frontend (port 3001)
├── backend/             # FastAPI Python backend (port 8000)
├── src/core/            # Neo4j knowledge graph logic
├── docker-compose.yml   # Infrastructure (Neo4j)
└── docs/                # Documentation
```

### Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 15, React 19, TypeScript, Tailwind CSS |
| Backend | FastAPI (Python 3.13), Pydantic, JWT auth |
| Database | Neo4j (graph), optional Redis cache |
| Testing | Pytest (backend), Playwright (frontend) |

## Quick Start

```bash
# Start Neo4j database
docker-compose up -d neo4j

# Start backend (terminal 1)
cd backend && ./start.sh
# API: http://localhost:8000
# Docs: http://localhost:8000/docs

# Start frontend (terminal 2)
cd web && npm run dev
# App: http://localhost:3001
```

## Critical Rules

### 1. Decoupled Architecture
- Frontend and backend are **independent services**
- Frontend has **offline mode** with mock data
- API changes require updates to both `backend/` and `web/lib/api/`

### 2. Code Locations

| Concern | Frontend | Backend |
|---------|----------|---------|
| API Routes | `web/lib/api/` | `backend/main.py` |
| Data Models | `web/lib/types.ts` | `backend/models/` |
| Components | `web/components/` | N/A |
| Business Logic | `web/lib/` | `backend/services/` |
| Auth | NextAuth.js | JWT (python-jose) |

### 3. Database Schema (Neo4j)

**Nodes:**
- `Claim` - Knowledge statements with confidence
- `Gap` - Knowledge gaps blocking progress
- `ResearchProfile` - User research profiles
- `ResearchContext` - Uploaded materials
- `Source` - Evidence and references

**Relationships:**
- `Edge` - Reasoning between claims
- `BLOCKS` - Gaps blocking claims
- `SUPPORTED_BY` - Claims with sources

### 4. Environment Variables

**Backend** (`backend/.env`):
```bash
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=claudipedia
JWT_SECRET=your_secret
```

**Frontend** (`web/.env.local`):
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_USE_MOCK_DATA=false  # true for offline mode
```

## Don't

- Mix frontend/backend responsibilities
- Skip mock data fallbacks in frontend
- Hardcode Neo4j queries outside `src/core/`
- Commit `.env` files

## Testing

```bash
# Backend
cd backend && pytest

# Frontend build check
cd web && npm run build

# API health
curl http://localhost:8000/health
```

---

**See `AGENTS.md` for universal agent guidelines.**
