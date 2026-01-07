# AGENTS.md - Claudipedia

> Universal guide for AI coding agents (Claude, Codex, Gemini, Cursor)

## Project Overview

**Claudipedia** is an AI-powered knowledge platform for collaborative research and truth-seeking.

| Aspect | Details |
|--------|---------|
| Type | Full-stack web application |
| Frontend | Next.js 15, React 19, TypeScript, Tailwind |
| Backend | FastAPI (Python 3.13), Neo4j |
| Database | Neo4j graph database |
| Deployment | Vercel (frontend), Docker (backend) |

## Quick Commands

```bash
# Full development stack
docker-compose up -d neo4j    # Start database
cd backend && ./start.sh      # Backend: http://localhost:8000
cd web && npm run dev         # Frontend: http://localhost:3001

# Testing
cd backend && pytest          # Backend tests
cd web && npm run build       # Frontend build check

# Database
docker-compose up -d neo4j    # Start Neo4j
# Browser: http://localhost:7474 (neo4j/claudipedia)
```

## Project Structure

```
claudipedia/
├── web/                    # Next.js 15 frontend
│   ├── app/               # App Router pages
│   ├── components/        # React components
│   └── lib/               # API client, types, utils
├── backend/                # FastAPI backend
│   ├── main.py            # API endpoints
│   ├── models/            # Pydantic models
│   └── services/          # Business logic
├── src/core/               # Neo4j integration
├── docs/                   # Documentation
└── docker-compose.yml      # Infrastructure
```

## Code Style Guidelines

### TypeScript (Frontend)
```typescript
// Use explicit types
interface ResearchProfile {
  id: string;
  name: string;
  domain: string;
  contexts: ResearchContext[];
}

// Named exports
export function ProfileCard({ profile }: { profile: ResearchProfile }) {
  return <div>{profile.name}</div>;
}
```

### Python (Backend)
```python
# Use Pydantic models
from pydantic import BaseModel

class ClaimCreate(BaseModel):
    content: str
    confidence: float
    source_id: str | None = None

# Type hints everywhere
async def create_claim(claim: ClaimCreate) -> Claim:
    ...
```

## Key Patterns

### 1. Offline Mode Support
Frontend must work without backend using mock data:
```typescript
// web/lib/api/client.ts
const useMockData = process.env.NEXT_PUBLIC_USE_MOCK_DATA === 'true';

export async function fetchProfiles() {
  if (useMockData) return MOCK_PROFILES;
  return fetch(`${API_URL}/profiles`).then(r => r.json());
}
```

### 2. Neo4j Queries
All graph queries go through services:
```python
# backend/services/graph.py
async def get_connected_claims(claim_id: str) -> list[Claim]:
    query = """
    MATCH (c:Claim {id: $id})-[e:Edge]-(related:Claim)
    RETURN related, e
    """
    return await db.run(query, {"id": claim_id})
```

## Don't

- Add backend dependencies to frontend or vice versa
- Skip type definitions for API responses
- Hardcode API URLs (use environment variables)
- Commit credentials or .env files
- Mix Neo4j queries with route handlers

## Pre-Commit Checklist

- [ ] Backend: `cd backend && pytest`
- [ ] Frontend: `cd web && npm run build`
- [ ] Types match between frontend and backend
- [ ] Mock data updated if API changed
- [ ] Environment variables documented

---

**Last Updated**: 2026-01-08
