from typing import Annotated

from fastapi import APIRouter, Depends, Header, Response
from sqlalchemy.orm import Session

from app.accounts import handlers
from app.accounts.schemas import LoginInput, ProfileInput, RegistrationInput, TokenResponse, UserResponse
from app.core.redis_client import get_redis
from app.db.session import get_session

router = APIRouter(tags=["accounts"])
Database = Annotated[Session, Depends(get_session)]
Authorization = Annotated[str | None, Header()]


def current_user(session: Database, authorization: Authorization = None, client=Depends(get_redis)):
    return handlers.profile(session, authorization or "", client)


def optional_user(session: Database, authorization: Authorization = None, client=Depends(get_redis)):
    return handlers.profile(session, authorization, client) if authorization is not None else None


@router.post("/auth/register", response_model=UserResponse, status_code=201)
def register(payload: RegistrationInput, session: Database):
    return handlers.register(session, payload.model_dump())


@router.post("/auth/login", response_model=TokenResponse)
def login(payload: LoginInput, session: Database, client=Depends(get_redis)):
    return handlers.login(session, payload.model_dump(), client)


@router.post("/auth/logout", status_code=204)
def logout(session: Database, authorization: Authorization = None, client=Depends(get_redis)):
    handlers.logout(session, authorization or "", client)
    return Response(status_code=204)


@router.get("/users/me", response_model=UserResponse)
def profile(user=Depends(current_user)):
    return user


@router.patch("/users/me", response_model=UserResponse)
def update_profile(payload: ProfileInput, session: Database, user=Depends(current_user)):
    from uuid import UUID
    from app.accounts.models import User
    account = session.get(User, UUID(user["id"]))
    account.name = payload.name
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
    return handlers.public_user(account)
