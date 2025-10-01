# Claudipedia

A first principles truth machine that enables anyone to seek truth on any topic, identifies gaps in human knowledge, and drives collaborative human-AI inquiry toward technological singularity.

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.10+
- Anthropic API key

### Setup

1. **Clone and configure**
   ```bash
   cd claudipedia
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

2. **Start Neo4j database**
   ```bash
   docker-compose up -d neo4j
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database with physics axioms**
   ```bash
   python scripts/setup_db.py
   python scripts/seed_axioms.py
   ```

5. **Start API server**
   ```bash
   uvicorn src.api.server:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Test the system**
   ```bash
   python scripts/test_queries.py
   ```

### Usage

**Query the knowledge graph:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Why do objects fall?"}'
```

**List knowledge gaps:**
```bash
curl http://localhost:8000/gaps
```

**View reasoning chain:**
```bash
curl http://localhost:8000/reasoning/{claim_id}
```

### Neo4j Browser

Access the graph database UI at: http://localhost:7474
- Username: `neo4j`
- Password: `claudipedia`

## Architecture

See `docs/ARCHITECTURE.md` for detailed system design.

## 💝 Support This Work

Building a truth machine to accelerate humanity toward singularity requires significant computational resources (Claude API subscriptions, Neo4j hosting, etc.).

**Support development:**
- **GitHub Sponsors:** [Sponsor @g-but](https://github.com/sponsors/g-but)
- **PayPal:** butaeff@gmail.com
- **Crypto (Bitcoin):** [Coming soon]
- **Crypto (Ethereum):** [Coming soon]

**What your support enables:**
- Claude Pro subscription (~$20/month minimum needed)
- Neo4j Aura cloud hosting
- Faster development velocity
- Public daily progress briefings

**Progress Transparency:**
All daily briefings are public! See real-time progress in [`docs/briefings/`](docs/briefings/) - you can track exactly how fast development moves and where your support goes.

---

## Development Status

**Phase 1 (Current): Physics Foundation**
- [x] Repository setup
- [x] Core data models
- [ ] Graph database interface
- [ ] 50 physics axioms seeded
- [ ] Claim decomposition engine
- [ ] Verification engine
- [ ] Gap detection
- [ ] Answer synthesis
- [ ] API endpoints
- [ ] Validation tests

📧 **Daily briefings:** Automatically emailed to butaeff@gmail.com at 5am daily and published to docs/briefings/

## Testing

Run unit tests:
```bash
pytest tests/
```

Run validation queries:
```bash
python scripts/test_queries.py
```

## Project Structure

```
claudipedia/
├── src/
│   ├── core/           # Data models and graph DB
│   ├── decomposition/  # Question → sub-claims
│   ├── verification/   # Claim verification
│   ├── synthesis/      # Answer generation
│   ├── gap_detection/  # Knowledge gap identification
│   └── api/            # FastAPI server
├── scripts/            # Setup and test scripts
├── tests/              # Unit and integration tests
└── docs/               # Architecture and design docs
```

## License

MIT
