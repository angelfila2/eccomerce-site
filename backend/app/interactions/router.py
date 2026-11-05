from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.accounts.router import optional_user
from app.db.session import get_session
from app.interactions.schemas import EventInput
from app.interactions.service import record_event

router = APIRouter(prefix="/interactions", tags=["interactions"])


@router.post("", status_code=202)
def track_event(payload: EventInput, session: Annotated[Session, Depends(get_session)],
                anonymous_id: Annotated[UUID, Header(alias="X-Anonymous-ID")], user=Depends(optional_user)):
    return record_event(session, payload.model_dump(), user["id"] if user else None, str(anonymous_id))
