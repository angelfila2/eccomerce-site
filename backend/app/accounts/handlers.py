from __future__ import annotations

import time
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.accounts.models import User
from app.accounts.repository import get_user_by_email
from app.accounts.schemas import LoginInput, validate_registration
from app.core.config import settings
from app.core.passwords import hash_password, verify_password
from app.core.redis_client import check_login_limit, is_revoked, revoke_token
from app.core.tokens import decode_token, issue_token


def public_user(user: User) -> dict:
    """Never serialize a password hash into an account response."""
    return {"id": str(user.id), "email": user.email, "name": user.name}


def jwt_secret() -> str:
    secret = settings.jwt_secret
    if not secret or len(secret.encode()) < 32:
        raise HTTPException(503, "Authentication requires APP_JWT_SECRET of at least 32 bytes")
    return secret


def register(session: Session, payload: dict) -> dict:
    validated = validate_registration(payload)
    user = User(email=validated["email"].strip().casefold(),
                password_hash=hash_password(validated["password"]), name=validated["name"])
    try:
        session.add(user)
        session.commit()  # Persist the user and generate its UUID before returning.
    except IntegrityError as error:
        session.rollback()
        existing = get_user_by_email(session, user.email)
        session.rollback()
        if existing is not None:
            raise HTTPException(409, "Email already registered") from error
        raise
    except SQLAlchemyError:
        session.rollback()
        raise
    return public_user(user)


def login(session: Session, payload: dict, redis_client=None) -> dict:
    validated = LoginInput.model_validate(payload)
    email = str(validated.email).strip().casefold()
    if redis_client is not None:
        check_login_limit(redis_client, email)
    user = get_user_by_email(session, email)
    if user is None or not verify_password(validated.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password", headers={"WWW-Authenticate": "Bearer"})
    token = issue_token(str(user.id), jwt_secret(), int(time.time()))
    return {"access_token": token, "token_type": "bearer"}


def bearer_token(authorization: str) -> str:
    parts = authorization.split() if isinstance(authorization, str) else []
    if len(parts) != 2 or parts[0].casefold() != "bearer":
        raise HTTPException(401, "Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    return parts[1]


def profile(session: Session, authorization: str, redis_client=None) -> dict:
    token = bearer_token(authorization)
    secret = jwt_secret()
    try:
        user_id = UUID(decode_token(token, secret, int(time.time())))
    except ValueError as error:
        raise HTTPException(401, "Invalid credentials", headers={"WWW-Authenticate": "Bearer"}) from error
    if redis_client is not None and is_revoked(redis_client, token):
        raise HTTPException(401, "Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(401, "Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    return public_user(user)


def logout(session: Session, authorization: str, redis_client) -> None:
    profile(session, authorization, redis_client)
    revoke_token(redis_client, bearer_token(authorization), jwt_secret())
