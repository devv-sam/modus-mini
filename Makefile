-include .env
export

.PHONY: dev-backend dev-frontend test lint

dev-backend:
	cd backend && uv run uvicorn app.main:app --reload

dev-frontend:
	cd frontend && npm run dev

test:
	cd backend && uv run pytest

lint:
	cd backend && uv run ruff check . ../evals && uv run ruff format --check . ../evals
