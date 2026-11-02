from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, status

from app.orders.schemas import CreateOrderRequest, OrderReceipt

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderReceipt, status_code=status.HTTP_201_CREATED)
def create_order(
    request: CreateOrderRequest,
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
) -> OrderReceipt:
    # TODO: Require the idempotency key in production, inject Session,
    # and call the single transactional orders.service.create_order use case.
    _ = (request, idempotency_key)
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, "Implement transactional checkout")

