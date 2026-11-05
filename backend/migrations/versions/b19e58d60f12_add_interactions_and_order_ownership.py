"""Add interaction tracking and safe checkout retry/ownership metadata.

Revision ID: b19e58d60f12
Revises: 8d74b92a61ef
"""
from alembic import op
import sqlalchemy as sa

revision = "b19e58d60f12"
down_revision = "8d74b92a61ef"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "interactions",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("event_id", sa.Uuid(), nullable=False, unique=True),
        sa.Column("kind", sa.String(30), nullable=False),
        sa.Column("product_id", sa.Uuid(), sa.ForeignKey("products.id")),
        sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("anonymous_id", sa.Uuid(), nullable=False),
        sa.Column("query", sa.String(200)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("kind IN ('impression','click','view','search','add_to_cart','remove_from_cart','purchase')",
                           name="ck_interactions_kind"),
    )
    op.create_index("ix_interactions_anonymous_id", "interactions", ["anonymous_id"])
    op.create_index("ix_interactions_user_time", "interactions", ["user_id", "created_at"])
    op.create_index("ix_interactions_product_time", "interactions", ["product_id", "created_at"])
    with op.batch_alter_table("orders") as batch:
        batch.add_column(sa.Column("user_id", sa.Uuid(), nullable=True))
        batch.add_column(sa.Column("anonymous_id", sa.Uuid(), nullable=True))
        batch.add_column(sa.Column("request_fingerprint", sa.String(64), nullable=True))
        batch.add_column(sa.Column("owner_scope", sa.String(80), nullable=True))
        batch.create_foreign_key("fk_orders_user_id_users", "users", ["user_id"], ["id"])
        batch.create_index("ix_orders_user_id", ["user_id"])
    # Historical guest orders retain NULL ownership/fingerprints. There is no
    # verified identity or original request to backfill safely. Never guess by email.


def downgrade():
    with op.batch_alter_table("orders") as batch:
        batch.drop_index("ix_orders_user_id")
        batch.drop_constraint("fk_orders_user_id_users", type_="foreignkey")
        for column in ("owner_scope", "request_fingerprint", "anonymous_id", "user_id"):
            batch.drop_column(column)
    op.drop_table("interactions")
