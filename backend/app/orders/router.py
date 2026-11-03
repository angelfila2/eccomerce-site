from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.orders import service
from app.orders.schemas import CreateOrderRequest, OrderReceipt

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post(
    "",
    response_model=OrderReceipt,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    request: CreateOrderRequest,
    session: Annotated[Session, Depends(get_session)],
    idempotency_key: Annotated[
        str,
        Header(
            alias="Idempotency-Key",
            min_length=1,
            max_length=100,
        ),
    ],
) -> OrderReceipt:
    try:
        order = service.create_order(
            session=session,
            request=request,
            idempotency_key=idempotency_key,
        )
    except service.DuplicateProductError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(error),
        ) from error
    except service.ProductNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    except service.InsufficientInventoryError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

    return order
