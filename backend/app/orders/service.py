"""Transactional guest-checkout implementation.

Checkout invariants:
1. Load and lock every referenced inventory row in a deterministic order.
2. Reject missing products, duplicates, invalid quantities, or insufficient stock.
3. Read authoritative prices from the database; never accept client totals.
4. Snapshot catalog and price data onto order lines.
5. Create the order and decrement stock in the same short transaction.
6. Make the idempotency key unique and return the existing result on replay.
"""

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.catalog.models import Product
from app.inventory.models import Inventory
from app.orders.models import Order, OrderLine
from app.orders.schemas import CreateOrderRequest, OrderReceipt


class CheckoutError(Exception):
    """Base error for an expected checkout failure."""


class DuplicateProductError(CheckoutError):
    """The same product appeared more than once."""


class ProductNotFoundError(CheckoutError):
    """A requested product does not exist."""


class InsufficientInventoryError(CheckoutError):
    """A product does not have enough inventory."""


def _to_order_receipt(order: Order) -> OrderReceipt:
    return OrderReceipt(
        id=order.id,
        createdAt=order.created_at,
        total=order.total,
        customerEmail=order.customer_email,
    )


def create_order(
    session: Session,
    request: CreateOrderRequest,
    idempotency_key: str,
) -> OrderReceipt:
    """Create an order and reduce inventory in one transaction."""

    with session.begin():
        existing_order = session.scalar(
            select(Order).where(Order.idempotency_key == idempotency_key)
        )

        if existing_order is not None:
            return _to_order_receipt(existing_order)

        product_ids = []
        for line in request.lines:
            product_ids.append(line.productId)

        if len(product_ids) != len(set(product_ids)):
            raise DuplicateProductError("Each product may appear only once")

        statement = (
            select(Product, Inventory)
            .join(
                Inventory,
                Inventory.product_id == Product.id,
            )
            .where(Product.id.in_(product_ids))
            .order_by(Product.id)
            .with_for_update(of=Inventory)
        )

        rows = session.execute(statement).all()
        locked_products = {}

        for product, inventory in rows:
            locked_products[product.id] = (product, inventory)

        if len(locked_products) != len(product_ids):
            raise ProductNotFoundError("One or more products do not exist")
        for line in request.lines:
            product, inventory = locked_products[line.productId]

            if inventory.quantity < line.quantity:
                raise InsufficientInventoryError(f"Not enough inventory for '{product.name}'")

        subtotal = Decimal("0.00")

        for line in request.lines:
            product, inventory = locked_products[line.productId]
            subtotal += product.price * line.quantity

        if subtotal >= Decimal("150.00"):
            shipping = Decimal("0.00")
        else:
            shipping = Decimal("12.00")

        tax = Decimal("0.00")
        discount = Decimal("0.00")

        total = subtotal + shipping + tax - discount

        order = Order(
            idempotency_key=idempotency_key,
            customer_email=request.checkout.email,
            customer_name=request.checkout.fullName,
            address=request.checkout.address,
            city=request.checkout.city,
            postal_code=request.checkout.postalCode,
            country=request.checkout.country,
            subtotal=subtotal,
            shipping=shipping,
            tax=tax,
            discount=discount,
            total=total,
            currency="SGD",
        )

        for line in request.lines:
            product, inventory = locked_products[line.productId]
            line_total = product.price * line.quantity

            order_line = OrderLine(
                product_id=product.id,
                product_slug=product.slug,
                product_name=product.name,
                quantity=line.quantity,
                unit_price=product.price,
                tax=Decimal("0.00"),
                discount=Decimal("0.00"),
                line_total=line_total,
                currency=product.currency,
            )

            order.lines.append(order_line)
            inventory.quantity -= line.quantity

        session.add(order)
        session.flush()

        return _to_order_receipt(order)
