"""Atomic simulated checkout with scoped, fingerprinted idempotent retries."""
from decimal import Decimal
from hashlib import sha256
import json
from uuid import UUID, NAMESPACE_URL, uuid4, uuid5

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.accounts.models import Cart, CartItem
from app.catalog.models import Product
from app.interactions.models import Interaction
from app.inventory.models import Inventory
from app.orders.models import Order, OrderLine, OrderStatus
from app.orders.schemas import CreateOrderRequest, OrderReceipt


class CheckoutError(Exception):
    """Expected checkout failure."""


class DuplicateProductError(CheckoutError):
    pass


class ProductNotFoundError(CheckoutError):
    pass


class InsufficientInventoryError(CheckoutError):
    pass


class IdempotencyConflictError(CheckoutError):
    pass


def _to_order_receipt(order: Order) -> OrderReceipt:
    return OrderReceipt(id=order.id, createdAt=order.created_at, total=order.total,
                        customerEmail=order.customer_email)


def request_fingerprint(request: CreateOrderRequest, scope: str) -> str:
    payload = request.model_dump(mode="json")
    payload["lines"].sort(key=lambda line: line["productId"])
    payload["checkout"]["email"] = payload["checkout"]["email"].strip().casefold()
    return sha256(json.dumps({"scope": scope, "request": payload}, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def replay_order(order: Order, fingerprint: str, scope: str) -> OrderReceipt:
    if order.owner_scope != scope or order.request_fingerprint != fingerprint:
        # Legacy orders with no fingerprint cannot establish a safe replay.
        raise IdempotencyConflictError("Idempotency key already used for another checkout")
    return _to_order_receipt(order)


def create_order(session: Session, request: CreateOrderRequest, idempotency_key: str,
                 user_id: str | None = None, anonymous_id: str | None = None) -> OrderReceipt:
    owner = UUID(user_id) if user_id else None
    anonymous = UUID(anonymous_id) if anonymous_id else None
    scope = f"user:{owner}" if owner else f"guest:{anonymous or 'legacy-direct-call'}"
    fingerprint = request_fingerprint(request, scope)
    ids = [line.productId for line in request.lines]
    if len(ids) != len(set(ids)):
        raise DuplicateProductError("Each product may appear only once")
    try:
        existing = session.scalar(select(Order).where(Order.idempotency_key == idempotency_key))
        if existing:
            result = replay_order(existing, fingerprint, scope)
            session.rollback()  # End the read-only retry transaction.
            return result
        rows = session.execute(select(Product, Inventory).join(Inventory, Inventory.product_id == Product.id)
                               .where(Product.id.in_(ids)).order_by(Product.id).with_for_update(of=Inventory)
                               .execution_options(populate_existing=True)).all()
        # A matching retry may have waited on the first request's inventory lock.
        existing = session.scalar(select(Order).where(Order.idempotency_key == idempotency_key))
        if existing:
            result = replay_order(existing, fingerprint, scope)
            session.rollback()
            return result
        products = {product.id: (product, stock) for product, stock in rows}
        if len(products) != len(ids):
            raise ProductNotFoundError("One or more products do not exist")
        if any(products[line.productId][1].quantity < line.quantity for line in request.lines):
            raise InsufficientInventoryError("Not enough inventory")
        subtotal = sum((products[line.productId][0].price * line.quantity for line in request.lines), Decimal("0.00"))
        shipping = Decimal("0.00") if subtotal >= Decimal("150.00") else Decimal("12.00")
        order = Order(status=OrderStatus.CONFIRMED, idempotency_key=idempotency_key,
                      request_fingerprint=fingerprint, owner_scope=scope, user_id=owner, anonymous_id=anonymous,
                      customer_email=str(request.checkout.email), customer_name=request.checkout.fullName,
                      address=request.checkout.address, city=request.checkout.city,
                      postal_code=request.checkout.postalCode, country=request.checkout.country,
                      subtotal=subtotal, shipping=shipping, tax=Decimal("0"), discount=Decimal("0"),
                      total=subtotal + shipping, currency="SGD")
        session.add(order)
        session.flush()  # Claim the unique idempotency key before changing stock.
        for line in request.lines:
            product, stock = products[line.productId]
            # Conditional SQL decrement also guards against concurrent last-unit sales.
            changed = session.execute(update(Inventory).where(Inventory.product_id == product.id,
                                      Inventory.quantity >= line.quantity)
                                      .values(quantity=Inventory.quantity - line.quantity)
                                      .execution_options(synchronize_session="fetch"))
            if changed.rowcount != 1:
                raise InsufficientInventoryError("Not enough inventory")
            order.lines.append(OrderLine(product_id=product.id, product_slug=product.slug,
                               product_name=product.name, quantity=line.quantity, unit_price=product.price,
                               line_total=product.price * line.quantity, tax=Decimal("0"),
                               discount=Decimal("0"), currency=product.currency))
            # Purchases are recorded only inside a successful checkout transaction.
            session.add(Interaction(event_id=uuid5(NAMESPACE_URL, f"purchase:{order.id}:{product.id}"),
                                    kind="purchase", product_id=product.id, user_id=owner,
                                    anonymous_id=anonymous or uuid4()))
        if owner:
            cart_id = session.scalar(select(Cart.id).where(Cart.user_id == owner))
            if cart_id:
                session.execute(delete(CartItem).where(CartItem.cart_id == cart_id, CartItem.product_id.in_(ids)))
        session.flush()
        result = _to_order_receipt(order)
        session.commit()  # Order, inventory, cart cleanup and purchase events are atomic.
        return result
    except IntegrityError as error:
        session.rollback()
        # A concurrent request may have claimed the same key while this one waited.
        existing = session.scalar(select(Order).where(Order.idempotency_key == idempotency_key))
        if existing is None:
            session.rollback()
            raise
        try:
            return replay_order(existing, fingerprint, scope)
        finally:
            session.rollback()
    except Exception:
        session.rollback()
        raise
