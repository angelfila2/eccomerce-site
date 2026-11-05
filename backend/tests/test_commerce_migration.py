from datetime import datetime, timezone
from uuid import uuid4

from alembic import command
from sqlalchemy import create_engine, event, inspect, text

from tests.test_account_migration import migration_config


def test_complete_migration_chain_preserves_legacy_orders():
    engine = create_engine("sqlite://")

    @event.listens_for(engine, "connect")
    def postgres_clock_compatibility(connection, _):
        # Historical revisions use PostgreSQL now(); SQLite needs a test adapter.
        connection.create_function("now", 0, lambda: datetime.now(timezone.utc).isoformat())

    with engine.begin() as connection:
        config = migration_config()
        config.attributes["connection"] = connection
        # Unlike the account-only fixture, build the real historical schema.
        command.upgrade(config, "8d74b92a61ef")
        order_id = uuid4().hex
        connection.execute(text("""INSERT INTO orders
            (id,status,idempotency_key,customer_email,customer_name,address,city,postal_code,
             country,subtotal,shipping,tax,discount,total,currency,created_at,updated_at)
            VALUES (:id,'confirmed','legacy-key','guest@example.com','Guest','Street','City','123',
                    'SG',20,0,0,0,20,'SGD',:now,:now)"""),
                           {"id": order_id, "now": datetime.now(timezone.utc)})
        command.upgrade(config, "head")
        row = connection.execute(text("SELECT id, user_id, request_fingerprint FROM orders")).one()
        assert row[0] == order_id and row[1] is None and row[2] is None
        assert "interactions" in inspect(connection).get_table_names()
        command.downgrade(config, "8d74b92a61ef")
        assert "interactions" not in inspect(connection).get_table_names()
        assert connection.scalar(text("SELECT id FROM orders")) == order_id
        command.upgrade(config, "head")
        assert connection.scalar(text("SELECT id FROM orders")) == order_id
    engine.dispose()
