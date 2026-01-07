#!/usr/bin/env bash
# Claudipedia Backend Startup Script (portable)

set -euo pipefail

# Resolve script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$SCRIPT_DIR"

# Activate virtual environment if present
if [[ -d "$PROJECT_ROOT/venv" ]]; then
  # shellcheck disable=SC1091
  source "$PROJECT_ROOT/venv/bin/activate"
else
  echo "⚠️  No virtualenv found at $PROJECT_ROOT/venv — proceeding with system Python."
fi

# Set environment variables
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"
export NEO4J_URI="${NEO4J_URI:-bolt://localhost:7687}"
export NEO4J_USER="${NEO4J_USER:-neo4j}"
export NEO4J_PASSWORD="${NEO4J_PASSWORD:-claudipedia}"
export JWT_SECRET="${JWT_SECRET:-development-secret-key-change-in-production}"
export LOG_LEVEL="${LOG_LEVEL:-INFO}"

echo "Starting Claudipedia Backend API..."
echo "API will be available at: http://localhost:8000"
echo "API Docs will be available at: http://localhost:8000/docs"
echo ""

python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

