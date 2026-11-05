from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class OrderStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        CheckConstraint("subtotal >= 0", name="ck_orders_subtotal_nonnegative"),
        CheckConstraint("shipping >= 0", name="ck_orders_shipping_nonnegative"),
        CheckConstraint("tax >= 0", name="ck_orders_tax_nonnegative"),
        CheckConstraint("discount >= 0", name="ck_orders_discount_nonnegative"),
        CheckConstraint("total >= 0", name="ck_orders_total_nonnegative"),
    )

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
    )
    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    anonymous_id: Mapped[UUID | None] = mapped_column(Uuid, nullable=True)
    request_fingerprint: Mapped[str | None] = mapped_column(String(64), nullable=True)
    owner_scope: Mapped[str | None] = mapped_column(String(80), nullable=True)
    status: Mapped[OrderStatus] = mapped_column(
        SqlEnum(
            OrderStatus,
            name="order_status",
            values_callable=lambda statuses: [status.value for status in statuses],
        ),
        default=OrderStatus.PENDING,
        nullable=False,
    )
    idempotency_key: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )
    customer_email: Mapped[str] = mapped_column(
        String(320),
        nullable=False,
    )
    customer_name: Mapped[str] = mapped_column(
        String(160),
        nullable=False,
    )
    address: Mapped[str] = mapped_column(
        String(240),
        nullable=False,
    )
    city: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )
    postal_code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )
    country: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )
    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    shipping: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        default=Decimal("0.00"),
        nullable=False,
    )
    tax: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        default=Decimal("0.00"),
        nullable=False,
    )
    discount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        default=Decimal("0.00"),
        nullable=False,
    )
    total: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    currency: Mapped[str] = mapped_column(
        String(3),
        default="SGD",
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        onupdate=func.now(),
    )

    lines: Mapped[list[OrderLine]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
    )


class OrderLine(Base):
    __tablename__ = "order_lines"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_order_lines_quantity_positive"),
        CheckConstraint("unit_price >= 0", name="ck_order_lines_unit_price_nonnegative"),
        CheckConstraint("tax >= 0", name="ck_order_lines_tax_nonnegative"),
        CheckConstraint("discount >= 0", name="ck_order_lines_discount_nonnegative"),
        CheckConstraint("line_total >= 0", name="ck_order_lines_total_nonnegative"),
    )

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
    )
    order_id: Mapped[UUID] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
    )
    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
    )
    product_slug: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    product_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    tax: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        default=Decimal("0.00"),
        nullable=False,
    )
    discount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        default=Decimal("0.00"),
        nullable=False,
    )
    line_total: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    currency: Mapped[str] = mapped_column(
        String(3),
        default="SGD",
        nullable=False,
    )

    order: Mapped[Order] = relationship(
        back_populates="lines",
    )
