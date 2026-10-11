# modus-mini

A data analysis agent. Upload a CSV, ask a question. The agent writes pandas code, runs it in a sandboxed subprocess, reads the output, and iterates until it can answer, citing the code cells it relied on.

## Setup

Needs Python 3.12, [uv](https://docs.astral.sh/uv/), and Node 22+.

```bash
cp .env.example .env
cd backend && uv sync
cd ../frontend && npm install
```

## Commands

```bash
make dev-backend    # http://localhost:8000/health
make dev-frontend   # http://localhost:5173
make test
make lint
```

The subprocess sandbox is not a security boundary. Run locally only.
