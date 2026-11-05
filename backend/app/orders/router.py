from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session

from app.accounts.orders import list_owned_orders
from app.accounts.router import current_user, optional_user
from app.core.redis_client import get_redis, invalidate_recommendations
from app.db.session import get_session
from app.orders import service
from app.orders.schemas import CreateOrderRequest, OrderReceipt

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderReceipt, status_code=201)
def create_order(request: CreateOrderRequest, session: Annotated[Session, Depends(get_session)],
                 idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=1, max_length=100)],
                 anonymous_id: Annotated[UUID | None, Header(alias="X-Anonymous-ID")] = None,
                 user=Depends(optional_user), client=Depends(get_redis)):
    if user is None and anonymous_id is None:
        raise HTTPException(422, "Guest checkout requires X-Anonymous-ID")
    try:
        receipt = service.create_order(session, request, idempotency_key,
                                       user["id"] if user else None, str(anonymous_id) if anonymous_id else None)
    except service.DuplicateProductError as error:
        raise HTTPException(422, str(error)) from error
    except service.ProductNotFoundError as error:
        raise HTTPException(404, str(error)) from error
    except (service.InsufficientInventoryError, service.IdempotencyConflictError) as error:
        raise HTTPException(409, str(error)) from error
    invalidate_recommendations(client)
    return receipt


@router.get("")
def order_history(session: Annotated[Session, Depends(get_session)], user=Depends(current_user),
                  limit: Annotated[int, Query(ge=1, le=100)] = 50,
                  offset: Annotated[int, Query(ge=0)] = 0):
    return list_owned_orders(session, user["id"], limit, offset)
