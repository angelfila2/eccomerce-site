from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.accounts.models import Cart, CartItem, User
from app.catalog.models import Product
from app.catalog.service import _to_product_response
from app.inventory.models import Inventory


def set_quantity(session: Session, user_id: str, product_id: str, quantity: int) -> dict:
    if type(quantity) is not int or not 0 <= quantity <= 100:
        raise ValueError("Quantity must be between 0 and 100")
    owner, item_id = UUID(user_id), UUID(product_id)
    try:
        # Lock the owner to serialize concurrent cart creation/updates per user.
        if session.scalar(select(User).where(User.id == owner).with_for_update()) is None:
            raise HTTPException(404, "User not found")
        product = session.get(Product, item_id)
        if product is None:
            raise HTTPException(404, "Product not found")
        inventory = session.scalar(select(Inventory).where(Inventory.product_id == item_id))
        if quantity and (inventory is None or quantity > inventory.quantity):
            raise HTTPException(409, "Requested quantity exceeds stock")
        cart = session.scalar(select(Cart).where(Cart.user_id == owner))
        if cart is None and quantity:
            cart = Cart(user_id=owner)
            session.add(cart)
            session.flush()
        line = session.scalar(select(CartItem).where(CartItem.cart_id == cart.id,
                              CartItem.product_id == item_id)) if cart else None
        if quantity == 0:
            if line is not None:
                session.delete(line)
        elif line is None:
            session.add(CartItem(cart_id=cart.id, product_id=item_id, quantity=quantity))
        else:
            line.quantity = quantity
        session.commit()  # A cart update never decrements inventory.
    except Exception:
        session.rollback()
        raise
    return {"product_id": product_id, "quantity": quantity}


def get_cart(session: Session, user_id: str) -> list[dict]:
    statement = (select(CartItem).join(Cart).where(Cart.user_id == UUID(user_id))
                 .options(selectinload(CartItem.product).selectinload(Product.category),
                          selectinload(CartItem.product).selectinload(Product.inventory_record))
                 .order_by(CartItem.id))
    return [{"product": _to_product_response(line.product).model_dump(mode="json"),
             "quantity": line.quantity} for line in session.scalars(statement)]
