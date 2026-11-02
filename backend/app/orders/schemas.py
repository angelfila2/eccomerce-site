from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class OrderLineInput(BaseModel):
    productId: UUID
    quantity: int = Field(ge=1, le=100)


class CheckoutInput(BaseModel):
    email: EmailStr
    fullName: str = Field(min_length=2, max_length=160)
    address: str = Field(min_length=3, max_length=240)
    city: str = Field(min_length=2, max_length=120)
    postalCode: str = Field(min_length=2, max_length=30)
    country: str = Field(min_length=2, max_length=80)


class CreateOrderRequest(BaseModel):
    lines: list[OrderLineInput] = Field(min_length=1, max_length=100)
    checkout: CheckoutInput


class OrderReceipt(BaseModel):
    id: UUID
    createdAt: datetime
    total: Decimal = Field(ge=0)
    customerEmail: EmailStr

