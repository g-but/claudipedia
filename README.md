# 📚 Claudipedia

**The AI-Powered Encyclopedia for Truth-Seeking**

An open knowledge platform where humans and Claude AI collaborate to build reliable, transparent knowledge through research profiles, evidence tracking, and systematic truth-seeking.

[![Status](https://img.shields.io/badge/status-operational-success)](./STATUS.md)
[![Architecture](https://img.shields.io/badge/architecture-decoupled-blue)](./docs/SYSTEM_ARCHITECTURE.md)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)

---

## 🎯 Vision

Claudipedia transforms how we discover and verify knowledge by:

1. **Research Profiles** - Organize your truth-seeking journey by domain
2. **Context Management** - Upload papers, books, data, and insights
3. **Knowledge Graph** - Connect claims with evidence and reasoning
4. **AI Collaboration** - Claude assists in verification and gap identification
5. **Transparency** - Track confidence, provenance, and verification

---

## 🏗️ Architecture

**Decoupled Modern Stack:**

```
Frontend (Next.js 15)  ←→  Backend (FastAPI)  ←→  Neo4j Graph DB
     ↓                          ↓                      ↓
 Vercel Deploy          Docker/Production      Knowledge Graph
 Offline Mode           API Endpoints          Claims & Evidence
```

**Key Features:**
- ✅ Independent service deployment
- ✅ Graceful offline mode with mock data
- ✅ Neo4j-powered knowledge graph
- ✅ Research profile system
- ✅ Context upload and management
- ✅ TypeScript end-to-end

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.13+
- Docker (for Neo4j)

### 1. Start the Backend

```bash
# Start Neo4j database
docker-compose up -d neo4j

# Start backend API
cd backend
./start.sh

# Backend available at:
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
```

### 2. Start the Frontend

```bash
# Install dependencies
cd web
npm install

# Run development server
npm run dev

# Frontend available at:
# - App: http://localhost:3000
```

### 3. Start Researching!

1. Navigate to http://localhost:3000
2. Go to **Research Profiles** (or `/research`)
3. Create your first research profile
4. Upload research contexts (papers, books, data)
5. Start your truth-seeking journey!

---

## 📖 Documentation

- **[System Status](./STATUS.md)** - Current operational status
- **[Architecture Guide](./docs/SYSTEM_ARCHITECTURE.md)** - Technical details
- **[Deployment Guide](./DEPLOYMENT.md)** - Production deployment
- **[Progress Tracker](./docs/PROGRESS.md)** - Development progress
- **[Dev Environment](./docs/DEV_ENV.md)** - Dependencies, tests, imports
- **[API Documentation](http://localhost:8000/docs)** - Interactive API docs (when running)

---

## 🎯 Core Features

### Research Profile System
- **Create Profiles** - Organize research by domain and focus area
- **Upload Context** - Papers, books, experimental data, field notes
- **Track Sessions** - Document findings with confidence scores
- **Manage Knowledge** - Build your personal knowledge graph

### Knowledge Graph (Neo4j)
- **Claims** - Statements with confidence and provenance
- **Edges** - Reasoning relationships between claims
- **Gaps** - Identified knowledge gaps blocking progress
- **Sources** - Evidence tracking and verification

### AI Collaboration
- **Claude Integration** - AI-assisted research and verification
- **Evidence Analysis** - Automatic source credibility assessment
- **Gap Detection** - Identify missing knowledge for investigation
- **Quest Generation** - Guided research paths (coming soon)

### Offline Support
- **Mock Data Mode** - Frontend works without backend
- **Graceful Degradation** - Seamless fallback when offline
- **Independent Services** - Deploy frontend and backend separately

---

## 🛠️ Development

### Project Structure

```
claudipedia/
├── backend/              # FastAPI backend
│   ├── main.py          # API endpoints
│   ├── models/          # Data models
│   ├── services/        # Business logic
│   └── start.sh         # Startup script
├── web/                 # Next.js frontend
│   ├── app/            # App routes & pages
│   ├── lib/            # API client & utilities
│   └── components/     # React components
├── src/                # Core knowledge graph
│   └── core/           # Neo4j integration
├── docs/               # Documentation
└── docker-compose.yml  # Infrastructure
```

### Tech Stack

**Frontend:**
- Next.js 15 (App Router)
- TypeScript
- Tailwind CSS
- NextAuth.js

**Backend:**
- FastAPI (Python 3.13)
- Neo4j (Graph Database)
- Pydantic (Data validation)
- JWT Authentication

**Infrastructure:**
- Docker & Docker Compose
- Neo4j with APOC plugins
- Redis (optional caching)

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
source ../venv/bin/activate
pytest
```

### Frontend Build
```bash
cd web
npm run build
# ✅ Production build successful
```

### API Tests
```bash
# Health check
curl http://localhost:8000/health

# Get API info
curl http://localhost:8000/

# Interactive docs
open http://localhost:8000/docs
```

---

## 📊 Database Schema

### Neo4j Nodes
- `Claim` - Knowledge statements with confidence
- `Gap` - Knowledge gaps blocking progress
- `ResearchProfile` - User research profiles
- `ResearchContext` - Uploaded research materials
- `ResearchSession` - Truth-seeking sessions
- `Source` - Evidence and references

### Relationships
- `Edge` - Reasoning between claims
- `BLOCKS` - Gaps blocking claims
- `SUPPORTED_BY` - Claims supported by sources
- `HAS_CONTEXT` - Profiles with contexts

---

## 🔧 Configuration

### Backend Environment

Create `backend/.env`:
```bash
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=claudipedia
ANTHROPIC_API_KEY=your_api_key  # Optional
JWT_SECRET=your_secret_key
LOG_LEVEL=INFO
```

### Frontend Environment

Create `web/.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_USE_MOCK_DATA=false  # Set true for offline mode

# Optional: Supabase for auth
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
```

---

## 🚢 Deployment

### Production Deployment

**Backend:**
```bash
# Deploy to your server
docker-compose -f docker-compose.prod.yml up -d

# Or use backend/start.sh with production env vars
```

**Frontend:**
```bash
# Deploy to Vercel
cd web
vercel --prod

# Or use GitHub Actions (configured)
git push origin main
```

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions.

---

## 🤝 Contributing

We welcome contributions! Areas to contribute:

- **Research Tools** - Enhanced context analysis and visualization
- **AI Integration** - Claude-powered research assistance
- **Knowledge Graph** - Advanced graph algorithms and queries
- **UI/UX** - Research profile enhancements
- **Documentation** - Guides and tutorials
- **Testing** - Comprehensive test coverage

---

## 📝 Roadmap

### ✅ Completed
- [x] Decoupled architecture
- [x] Research profile system
- [x] Context upload and management
- [x] Neo4j knowledge graph
- [x] Offline mode support
- [x] API documentation
- [x] TypeScript integration

### 🚧 In Progress
- [ ] Claude AI integration
- [ ] Advanced evidence viewer
- [ ] Quest generation system

### 🔮 Future
- [ ] Mobile app
- [ ] Real-time collaboration
- [ ] External knowledge sources (arXiv, PubMed)
- [ ] Advanced analytics dashboard
- [ ] Gamification system

---

## 📄 License

MIT License - see [LICENSE](./LICENSE) for details

---

## 🙏 Acknowledgments

- Built with [Claude](https://anthropic.com/claude) AI assistance
- Powered by [Neo4j](https://neo4j.com/) graph database
- Frontend by [Next.js](https://nextjs.org/)
- Backend by [FastAPI](https://fastapi.tiangolo.com/)

---

## 📞 Support

- **Documentation:** [docs/](./docs/)
- **Status:** [STATUS.md](./STATUS.md)
- **Issues:** Use GitHub Issues
- **Discussions:** Use GitHub Discussions

---

**Ready to seek truth? Start your research journey today!** 🚀

```bash
# One command to rule them all
docker-compose up -d neo4j && cd backend && ./start.sh
```
