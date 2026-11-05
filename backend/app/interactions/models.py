from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Interaction(Base):
    __tablename__ = "interactions"
    __table_args__ = (
        CheckConstraint("kind IN ('impression','click','view','search','add_to_cart','remove_from_cart','purchase')",
                        name="ck_interactions_kind"),
        Index("ix_interactions_user_time", "user_id", "created_at"),
        Index("ix_interactions_product_time", "product_id", "created_at"),
    )
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    event_id: Mapped[UUID] = mapped_column(Uuid, unique=True, nullable=False)
    kind: Mapped[str] = mapped_column(String(30), nullable=False)
    product_id: Mapped[UUID | None] = mapped_column(ForeignKey("products.id"), nullable=True)
    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    anonymous_id: Mapped[UUID] = mapped_column(Uuid, nullable=False, index=True)
    query: Mapped[str | None] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
