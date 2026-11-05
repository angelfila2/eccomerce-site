from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.orders.models import Order


def list_owned_orders(session: Session, user_id: str, limit: int = 50, offset: int = 0) -> list[dict]:
    if not 1 <= limit <= 100 or offset < 0:
        raise ValueError("Invalid pagination")
    # Email matching never grants ownership of guest or another account's orders.
    orders = session.scalars(select(Order).where(Order.user_id == UUID(user_id))
                             .order_by(Order.created_at.desc(), Order.id.desc()).limit(limit).offset(offset))
    return [{"id": str(order.id), "total": str(order.total), "createdAt": order.created_at,
             "status": order.status.value} for order in orders]
