# Pawchase FastAPI backend

This folder is deliberately a contract skeleton. Health and routing are wired; commerce handlers return HTTP 501 until their TODOs are implemented.

## Development

```bash
uv sync --dev
copy .env.example .env
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

Read [TODO.md](TODO.md) before implementing. Authentication is the final phase by design.

