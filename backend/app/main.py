from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # TODO: Initialize shared clients here (not database tables).
    # Production schema changes must run through Alembic before startup.
    yield
    # TODO: Close shared clients here when they are introduced.


app = FastAPI(
    title="Pawchase Commerce API",
    version="0.1.0",
    description="Contract-first FastAPI skeleton. Authentication is intentionally deferred.",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,  # TODO(auth-last): enable only with the final cookie strategy.
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Idempotency-Key"],
)
app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/health", tags=["operations"])
def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}

