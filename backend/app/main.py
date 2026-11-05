from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.redis_client import create_redis_client


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:
    application.state.redis = create_redis_client()
    try:
        yield
    finally:
        application.state.redis.close()


app = FastAPI(
    title="Pawchase Commerce API",
    version="0.1.0",
    description="Pawchase backend with Redis-backed authentication and explicit ML-free recommendation fallbacks.",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,  # BE-008 uses bearer headers; cookies are a separate design.
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Idempotency-Key", "Authorization", "X-Anonymous-ID"],
)
app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/health", tags=["operations"])
def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}


@app.get("/ready", tags=["operations"])
def ready(request: Request):
    from fastapi.responses import JSONResponse
    from redis.exceptions import RedisError
    try:
        request.app.state.redis.ping()
    except RedisError:
        return JSONResponse({"status": "unavailable", "redis": "unavailable"}, status_code=503)
    return {"status": "ok", "redis": "ok"}

