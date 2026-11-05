# Pawchase FastAPI backend

Current workflow: [backend learning guide](../BACKEND_LEARNING_GUIDE.md),
[roadmap](../LEARNING_ROADMAP.md), and [task cards](../docs/learning/TASKS.md).
New business logic and ML code are learner-owned scaffolds; start with BE-001.
Authentication is now milestone 6, superseding the historical auth-last plan.
This is not production-ready.

From this directory, with `.venv` active:

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest tests/test_health.py tests/test_foundation.py -q
python -m pytest tests/learning/test_backend.py::test_BE_001 -q
```

The final command deliberately fails until you implement BE-001. The root README
documents environment templates, Docker, optional ML packages and test limitations.

The health, PostgreSQL-backed catalog and transactional guest-checkout endpoints are implemented. Payments and authentication remain future phases.

## Development

```bash
uv sync --dev
uv run uvicorn app.main:app --reload
uv run pytest
uv run ruff check .
```

Alternatively, with a standard virtual environment:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Configuration

Create `backend/.env` and keep it private. It is ignored by Git.

```env
APP_ENVIRONMENT=development
APP_DATABASE_URL=postgresql+psycopg://USER:PERCENT_ENCODED_PASSWORD@HOST:5432/postgres?sslmode=require
APP_CORS_ORIGINS=["http://localhost:5173"]
```

For Supabase, copy the direct or session-pooler connection URI, replace its leading
`postgresql://` with `postgresql+psycopg://`, and percent-encode reserved characters in the
password. Never put real credentials in this README.

## Seed the catalog

After applying the database migrations, run this command from the `backend` folder:

```powershell
.\.venv\Scripts\python.exe -m scripts.seed_catalog
```

The command inserts the starter catalog or updates matching records when it is run again.

Read the current learning roadmap before implementing. [TODO.md](TODO.md) is historical.

