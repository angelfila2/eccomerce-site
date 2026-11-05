from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.catalog.models import Product
from app.interactions.models import Interaction
from app.interactions.schemas import EventInput


def record_event(session: Session, event: dict, user_id: str | None, anonymous_id: str) -> dict:
    parsed = EventInput.model_validate(event)
    owner = UUID(user_id) if user_id else None
    anonymous = UUID(anonymous_id)
    def replay(existing):
        if (existing.user_id, existing.anonymous_id, existing.kind, existing.product_id, existing.query) != (
                owner, anonymous, parsed.kind, parsed.product_id, parsed.query):
            raise HTTPException(409, "Event ID already used")
        return {"event_id": str(parsed.event_id), "accepted": True}
    try:
        existing = session.scalar(select(Interaction).where(Interaction.event_id == parsed.event_id))
        if existing:
            return replay(existing)
        if parsed.product_id and session.get(Product, parsed.product_id) is None:
            raise HTTPException(404, "Product not found")
        session.add(Interaction(event_id=parsed.event_id, kind=parsed.kind, product_id=parsed.product_id,
                                user_id=owner, anonymous_id=anonymous, query=parsed.query))
        session.commit()
    except IntegrityError:
        session.rollback()
        existing = session.scalar(select(Interaction).where(Interaction.event_id == parsed.event_id))
        if existing is None:
            raise
        return replay(existing)
    except Exception:
        session.rollback()
        raise
    return {"event_id": str(parsed.event_id), "accepted": True}
