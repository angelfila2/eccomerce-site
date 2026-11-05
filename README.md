# Pawchase — Python backend and ML learning branch

React/Vite storefront and FastAPI/PostgreSQL commerce API. All BE task
implementations are supplied; ML exercises remain unfinished for the next session.
The frontend defaults to visibly labeled demo data and simulated orders.

## Implemented backend

- Registration, Argon2 password hashing, JWT login, profile/name updates and logout.
- Redis login rate limits, token revocation, recommendation caching and readiness.
- Catalogue/categories, owned carts and paginated order history.
- Atomic simulated checkout, inventory checks, owner/session-scoped request
  fingerprints and safe idempotent retries; purchases recorded only on commit.
- Validated, deduplicated user/anonymous interaction events.
- Personalized/similar/trending/you-may-like routes with explicit model-free
  featured/category fallbacks; Frequently Bought Together queries completed orders.
- Alembic migrations for catalogue/inventory/orders, accounts/carts, interactions,
  ownership and retry metadata. Existing guest orders retain unverified NULL
  ownership; no email-based backfill silently claims them for an account.

[Function | code with comments table](docs/BACKEND_FUNCTION_REFERENCE.html)

[Task progress](LEARNING_PROGRESS.md) · [ML guide](ML_LEARNING_GUIDE.md)

## What is intentionally unfinished

ML-001..011 are still exercises: popularity decay, TF-IDF, cosine/semantic vector
retrieval, collaborative filtering, two-tower training/evaluation and hybrid ranking.
The older ranking/explanation exercises also remain deferred. The running backend
uses explicit fallbacks and does not claim that a model is trained or personalized
ML is active. Baseline order co-occurrence is provided by the backend SQL query.
No paid API or real payment is involved.

## Frontend

```powershell
cd frontend
npm ci
Copy-Item .env.example .env.local
npm run dev
```

Open http://localhost:5173. `VITE_USE_MOCKS=true` keeps the existing storefront in
sample-data mode. To use the catalogue/guest-checkout/recommendation HTTP gateway,
set it to false and `VITE_API_URL=http://localhost:8000/api/v1`; restart Vite.
The gateway supplies a persistent anonymous UUID for guest checkout. Backend auth
routes are implemented; a frontend account-login UI is not part of this snapshot.

## Backend setup

Python 3.11+; locally verified using Python 3.13. From the repository root:

```powershell
Copy-Item .env.example .env
cd backend
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
```

Set backend `APP_JWT_SECRET` to a random secret of at least 32 bytes. Keep real
secrets out of Git. `APP_DATABASE_URL`, `APP_REDIS_URL`, `APP_ENVIRONMENT` and
`APP_CORS_ORIGINS` are shown in the environment template. Keep database credentials
aligned with root `.env`; percent-encode reserved URL characters.

Start local services from the repository root with Docker Desktop running:

```powershell
docker compose --env-file .env -f infrastructure/compose.yaml up -d db redis
```

From `backend/`, with its Python environment active:

```powershell
python -m alembic upgrade head
python -m scripts.seed_catalog
python -m uvicorn app.main:app --reload
```

Alternatively run the API in Docker from the root:

```powershell
docker compose --env-file .env -f infrastructure/compose.yaml up -d --build api
docker compose --env-file .env -f infrastructure/compose.yaml run --rm api python -m scripts.seed_catalog
```

The API container runs migrations before starting. Compose binds published ports
to loopback. Stop with `docker compose --env-file .env -f infrastructure/compose.yaml down`
to retain the PostgreSQL volume. No accounts are seeded with default passwords.

## API and Redis

Interactive documentation: http://localhost:8000/docs. Groups are `/api/v1/auth`,
`/users`, `/products`, `/categories`, `/cart`, `/orders`, `/interactions` and
`/recommendations` (all prefixed with `/api/v1`).

Send `Authorization: Bearer <token>` for owned operations. Guest checkout requires
`X-Anonymous-ID: <UUID>` and `Idempotency-Key: <unique key>`; only identical payloads
from the same owner/session can replay a receipt. Interaction events also require
the anonymous UUID. Client-supplied user IDs and purchase events are rejected.

Redis is actively called by HTTP authentication and cache routes: login counters
expire after 60 seconds, logout stores a token digest until its JWT expires, and
protected routes check revocation. Authentication returns 503 on Redis outage;
recommendations compute a safe uncached fallback instead. `/health` is liveness;
`/ready` pings Redis. One pooled Redis client is created/closed per application
lifespan. Cache keys include user/seeds/model and authoritative catalogue state;
checkout bumps the generation and serving refreshes stock from the database.

## Verification

From `backend/`:

```powershell
python -m pytest tests --ignore=tests/learning/test_ml.py -q
```

Observed: **38 passed, 2 skipped**. The skips are real PostgreSQL migration/concurrency
checks. Set `TEST_POSTGRES_URL` to run them in generated disposable schemas. Local
SQLite tests cover the complete migration chain, legacy-order preservation,
constraints, checkout rollback/replay, ownership and full HTTP commerce flows.
PostgreSQL DDL compilation also passes. Redis behavior uses explicit test doubles.
Frontend `npm run build` passes.

Docker Desktop was unavailable, so live PostgreSQL/Redis services and production
concurrency were not verified. This is a development application, not a verified
production deployment. ML tests are intentionally excluded because their
implementations are deferred; running the entire learning suite is still red.

## ML dependencies and next session

Install optional packages when ready: `python -m pip install -r requirements-ml.txt`
or `uv sync --dev --extra ml` from `backend/`. Training scripts/algorithms are
unfinished; no working training CLI or performance report is claimed. Use
chronological splits, training-only feature fitting, Recall/Precision/NDCG/Hit
Rate@10 and coverage, compared with popularity. Synthetic fixtures are correctness
examples only. Historical learning guides describe the original exercises;
LEARNING_PROGRESS.md and this README reflect the current delivered state.
