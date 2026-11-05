from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from app.accounts.router import current_user
from app.cart.service import get_cart, set_quantity
from app.db.session import get_session

router = APIRouter(prefix="/cart", tags=["cart"])


class QuantityInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    quantity: int = Field(ge=0, le=100, strict=True)


@router.get("")
def read_cart(session: Annotated[Session, Depends(get_session)], user=Depends(current_user)):
    return get_cart(session, user["id"])


@router.put("/items/{product_id}")
def update_item(product_id: UUID, payload: QuantityInput,
                session: Annotated[Session, Depends(get_session)], user=Depends(current_user)):
    return set_quantity(session, user["id"], str(product_id), payload.quantity)


@router.delete("/items/{product_id}")
def remove_item(product_id: UUID, session: Annotated[Session, Depends(get_session)],
                user=Depends(current_user)):
    return set_quantity(session, user["id"], str(product_id), 0)
