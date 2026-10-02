# IDAFAMU

IDAFAMU is an advanced AI agent backend inspired by the architecture of RAFIQ, but designed to be more modular, scalable, and production-ready.

This repository currently contains the initial backend skeleton for an AI agent platform built with FastAPI, SQLAlchemy, Pydantic, and a provider-agnostic LLM layer.

## Current backend features

- FastAPI app scaffold
- LLM provider abstraction
- Model registry and router
- Chat request / response schemas
- Tool registry foundation
- Memory service foundation
- Agent runtime placeholder
- Health and chat endpoints
- SQLite-ready database session and models

## Planned next stages

1. Add persistent chat storage and message history
2. Add tool execution layer for filesystem, shell, browser, and MCP integrations
3. Add memory / vector retrieval service
4. Add task queue and background job engine
5. Add auth and user management
6. Add frontend dashboard

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API overview

- GET `/health`
- GET `/api/v1/models`
- POST `/api/v1/chat` for streaming or standard responses
- GET `/api/v1/tools`

## Environment

Create a `.env` file based on `.env.example`.
