"""Shared Redis infrastructure: rate limits, JWT revocation and cache generations."""
from hashlib import sha256
from time import time

import jwt
from fastapi import HTTPException, Request
from redis import Redis
from redis.exceptions import RedisError

from app.core.config import settings


def create_redis_client():
    return Redis.from_url(settings.redis_url, decode_responses=True,
                          socket_connect_timeout=1, socket_timeout=1,
                          max_connections=20, health_check_interval=30)


def get_redis(request: Request):
    # Created once in FastAPI lifespan, reused by all request handlers.
    return request.app.state.redis


def token_key(token: str) -> str:
    return "auth:revoked:" + sha256(token.encode()).hexdigest()


def check_login_limit(client, email: str) -> None:
    key = "auth:login:" + sha256(email.encode()).hexdigest()
    try:
        # Atomic increment + expiring window; expiry is set only on first attempt.
        count = client.eval("local n=redis.call('INCR',KEYS[1]); "
                            "if n==1 then redis.call('EXPIRE',KEYS[1],ARGV[1]) end; return n",
                            1, key, 60)
    except RedisError as error:
        raise HTTPException(503, "Authentication storage unavailable") from error
    if count > 20:
        raise HTTPException(429, "Too many login attempts", headers={"Retry-After": "60"})


def is_revoked(client, token: str) -> bool:
    try:
        return bool(client.exists(token_key(token)))
    except RedisError as error:
        # Never silently bypass revocation when its backing store is unavailable.
        raise HTTPException(503, "Authentication storage unavailable") from error


def revoke_token(client, token: str, secret: str) -> None:
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.PyJWTError as error:
        raise HTTPException(401, "Invalid credentials") from error
    ttl = max(1, payload["exp"] - int(time()))
    try:
        client.setex(token_key(token), ttl, "1")
    except RedisError as error:
        raise HTTPException(503, "Authentication storage unavailable") from error


def catalogue_version(client) -> str:
    try:
        return str(client.get("recommendations:catalogue-version") or "0")
    except RedisError:
        return "offline"


def invalidate_recommendations(client) -> None:
    try:
        client.incr("recommendations:catalogue-version")
    except RedisError:
        # Serving also checks current stock, so an outage cannot advertise sold-out items.
        pass
