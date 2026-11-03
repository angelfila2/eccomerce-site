# Pawchase FastAPI backend

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

Read [TODO.md](TODO.md) before implementing. Authentication is the final phase by design.

