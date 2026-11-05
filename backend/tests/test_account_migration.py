"""Exercise the new revision on disposable SQLite and compile PostgreSQL DDL."""

from io import StringIO
from pathlib import Path
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, event, inspect, select
from sqlalchemy.exc import IntegrityError

import app.accounts.models  # noqa: F401
from app.catalog.models import Category
from app.db.base import Base

PREVIOUS = "73a80b5bcddb"
CURRENT = "8d74b92a61ef"
NEW_TABLES = {"users", "carts", "cart_items"}


def migration_config():
    root = Path(__file__).resolve().parents[1]
    config = Config(str(root / "alembic.ini"))
    config.set_main_option("script_location", str(root / "migrations"))
    return config


def test_account_migration_roundtrip_preserves_catalogue():
    engine = create_engine("sqlite://")

    @event.listens_for(engine, "connect")
    def foreign_keys(connection, _):
        connection.execute("PRAGMA foreign_keys=ON")

    # Existing commerce schema is the starting point. This test exercises only
    # the new revision, not historical PostgreSQL-specific data migrations.
    Base.metadata.create_all(engine, tables=[table for table in Base.metadata.sorted_tables
                                            if table.name not in NEW_TABLES | {"interactions"}])
    category_id = uuid4()
    with engine.begin() as connection:
        connection.execute(Category.__table__.insert().values(
            id=category_id, name="Existing", slug="existing"
        ))
        config = migration_config()
        config.attributes["connection"] = connection
        command.stamp(config, PREVIOUS)
        command.upgrade(config, CURRENT)
        assert NEW_TABLES <= set(inspect(connection).get_table_names())
        assert connection.scalar(select(Category.name)) == "Existing"

        users = Base.metadata.tables["users"]
        carts = Base.metadata.tables["carts"]
        user_id = uuid4()
        connection.execute(users.insert().values(
            id=user_id, email="learner@example.com", password_hash="encoded", name="Learner"
        ))
        connection.execute(carts.insert().values(id=uuid4(), user_id=user_id))
        with pytest.raises(IntegrityError), connection.begin_nested():
            connection.execute(carts.insert().values(id=uuid4(), user_id=user_id))
        with pytest.raises(IntegrityError), connection.begin_nested():
            connection.execute(users.insert().values(
                id=uuid4(), email="learner@example.com", password_hash="other", name="Other"
            ))

        items = inspect(connection)
        assert {"cart_id", "product_id"} in [set(c["column_names"])
            for c in items.get_unique_constraints("cart_items")]
        assert any(c["name"] == "ck_cart_items_quantity_positive"
                   for c in items.get_check_constraints("cart_items"))
        assert len(items.get_foreign_keys("cart_items")) == 2

        command.downgrade(config, PREVIOUS)
        assert NEW_TABLES.isdisjoint(inspect(connection).get_table_names())
        assert connection.scalar(select(Category.name)) == "Existing"
        command.upgrade(config, CURRENT)
        assert NEW_TABLES <= set(inspect(connection).get_table_names())
        assert connection.scalar(select(Category.name)) == "Existing"
    engine.dispose()


def test_account_revision_compiles_for_postgresql():
    from app.core.config import settings
    from unittest.mock import patch

    output = StringIO()
    config = migration_config()
    config.output_buffer = output
    # Override URL only for SQL compilation: no credentials, sockets or DB writes.
    with patch.object(settings, "database_url", "postgresql+psycopg://"):
        command.upgrade(config, f"{PREVIOUS}:head", sql=True)
    sql = output.getvalue()
    assert "CREATE TABLE users" in sql
    assert "TIMESTAMP WITH TIME ZONE" in sql
    assert "ON DELETE CASCADE" in sql
    assert "uq_cart_items_cart_product" in sql
    assert "quantity > 0" in sql
    assert "CREATE TABLE interactions" in sql
    assert "request_fingerprint" in sql
