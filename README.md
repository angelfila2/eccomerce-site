# Pawchase

A FastAPI ecommerce revamp with a block-built corgi mascot. The React storefront is complete and uses an in-browser mock adapter by default. The FastAPI backend has a PostgreSQL-backed catalog, while later commerce features remain documented as `TODO` items.

## Structure

```text
frontend/  React + TypeScript + Vite storefront
backend/   FastAPI application and implementation plan
docs/      Architecture research and decisions
```

## Run the frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend defaults to mock mode. Cart state is persisted in browser storage.

## Run the backend

```bash
cd backend
uv sync --dev
uv run uvicorn app.main:app --reload
```

The health, catalog and transactional guest-checkout endpoints are implemented. Payments and authentication remain future phases.

## Connect the frontend to FastAPI

Create `frontend/.env.local`:

```env
VITE_USE_MOCKS=false
VITE_API_URL=http://localhost:8000/api/v1
```

Restart Vite after changing its environment configuration. Authentication is intentionally deferred until the final phase.

