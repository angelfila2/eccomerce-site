"""Add accounts and persistent carts without modifying existing commerce data.

Revision ID: 8d74b92a61ef
Revises: 73a80b5bcddb
"""

from alembic import op
import sqlalchemy as sa

revision = "8d74b92a61ef"
down_revision = "73a80b5bcddb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email", sa.String(320), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("name", sa.String(80), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "carts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_table(
        "cart_items",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("cart_id", sa.Uuid(), nullable=False),
        sa.Column("product_id", sa.Uuid(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["cart_id"], ["carts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.UniqueConstraint("cart_id", "product_id", name="uq_cart_items_cart_product"),
        sa.CheckConstraint("quantity > 0", name="ck_cart_items_quantity_positive"),
    )
    # There is no earlier account/cart table to backfill. Leave guest orders and
    # browser-local carts untouched; neither proves verified account ownership.


def downgrade() -> None:
    # Explicit rollback removes only the tables introduced in this revision.
    op.drop_table("cart_items")
    op.drop_table("carts")
    op.drop_table("users")
