from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.catalog.models import Product


class Inventory(Base):
    __tablename__ = "inventory"
    #     product_id — foreign key referencing products.id
    # quantity — integer, default 0
    # A database constraint ensuring quantity >= 0
    # A one-to-one relationship with Product
    # created_at
    # updated_at
    __table_args__ = (
        CheckConstraint(
            "quantity >= 0",
            name="ck_inventory_quantity_nonnegative",
        ),
    )
    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
    )
    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id"),
        unique=True,
        nullable=False,
    )
    # 1 to 1 relationship
    product: Mapped[Product] = relationship(
        back_populates="inventory_record",
    )
    quantity: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, onupdate=func.now()
    )
