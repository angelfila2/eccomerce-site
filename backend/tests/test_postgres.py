"""Optional real PostgreSQL gates. Set TEST_POSTGRES_URL to run in a private schema."""
import os
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from uuid import uuid4

import pytest
from alembic import command
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session

from app.catalog.models import Category, Product
from app.inventory.models import Inventory
from app.orders.models import Order
from app.orders.schemas import CreateOrderRequest
from app.orders.service import InsufficientInventoryError, create_order
from tests.test_account_migration import migration_config


@pytest.fixture
def postgres_database():
    url = os.environ.get("TEST_POSTGRES_URL")
    if not url:
        pytest.skip("Set TEST_POSTGRES_URL for real PostgreSQL concurrency/migration checks")
    admin = create_engine(url)
    assert admin.dialect.name == "postgresql"
    schema = "be_test_" + uuid4().hex
    with admin.begin() as connection:
        connection.exec_driver_sql(f'CREATE SCHEMA "{schema}"')
    engine = create_engine(url, connect_args={"options": f"-csearch_path={schema}"})
    try:
        with engine.begin() as connection:
            config = migration_config()
            config.attributes["connection"] = connection
            command.upgrade(config, "head")
            command.downgrade(config, "8d74b92a61ef")
            command.upgrade(config, "head")
        yield engine
    finally:
        engine.dispose()
        # Schema is generated locally above; never drop public or shared tables.
        with admin.begin() as connection:
            connection.exec_driver_sql(f'DROP SCHEMA "{schema}" CASCADE')
        admin.dispose()


@pytest.mark.parametrize("identical_key", [False, True])
def test_postgres_last_unit_and_idempotency_race(postgres_database, identical_key):
    engine = postgres_database
    with Session(engine, expire_on_commit=False) as session:
        product = Product(name="Last item", slug="last-item", description="Item", details=[],
                          price=20, image_url="/item.png", category=Category(name="Desk", slug="desk"))
        product.inventory_record = Inventory(quantity=1)
        session.add(product)
        session.commit()
        product_id = product.id
    request = CreateOrderRequest.model_validate({
        "lines": [{"productId": product_id, "quantity": 1}],
        "checkout": {"email": "guest@example.com", "fullName": "Guest Buyer", "address": "123 Street",
                     "city": "Singapore", "postalCode": "123456", "country": "Singapore"}})
    barrier = Barrier(2)
    shared_key = str(uuid4())
    def purchase(index):
        with Session(engine) as session:
            barrier.wait(timeout=15)
            try:
                receipt = create_order(session, request, shared_key if identical_key else str(uuid4()))
                return str(receipt.id)
            except InsufficientInventoryError:
                return "stock-conflict"
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(purchase, range(2)))
    if identical_key:
        assert results[0] == results[1] != "stock-conflict"
    else:
        assert results.count("stock-conflict") == 1
    with Session(engine) as session:
        assert session.scalar(select(Inventory.quantity).where(Inventory.product_id == product_id)) == 0
        assert len(session.scalars(select(Order)).all()) == 1
