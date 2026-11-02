# Pawchase

A FastAPI-ready ecommerce revamp with a block-built corgi mascot. The React storefront is complete and uses an in-browser mock adapter by default. The FastAPI backend defines the intended module structure and endpoint contracts, with implementation work marked as `TODO`.

## Structure

```text
frontend/  React + TypeScript + Vite storefront
backend/   FastAPI contract skeleton and TODOs
docs/      Architecture research and decisions
```

## Run the frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend defaults to mock mode. Cart state is persisted in browser storage.

## Run the backend skeleton

```bash
cd backend
uv sync --dev
uv run uvicorn app.main:app --reload
```

The health endpoint works. Commerce endpoints deliberately return `501 Not Implemented` until their TODOs are completed.

## Connect the frontend to FastAPI

Create `frontend/.env.local`:

```env
VITE_USE_MOCKS=false
VITE_API_URL=http://localhost:8000/api/v1
```

Implement the backend TODO endpoints, then restart Vite. Authentication is intentionally deferred until the final phase.

