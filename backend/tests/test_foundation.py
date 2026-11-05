"""Regression coverage for existing work; not proof of PostgreSQL locking."""

from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select

from app.catalog.models import Category, Product
from app.catalog.service import get_product_by_slug, list_products
from app.inventory.models import Inventory
from app.orders.models import Order
from app.orders.schemas import CreateOrderRequest
from app.orders.service import InsufficientInventoryError, create_order


@pytest.fixture
def product(db):
    category = Category(name="Workspace", slug="workspace")
    item = Product(name="Lamp", slug="lamp", description="Reading lamp", details=[],
                   price=Decimal("20.00"), image_url="/lamp.png", category=category)
    item.inventory_record = Inventory(quantity=2)
    db.add(item)
    db.commit()
    return item


def order_request(product, quantity=1):
    return CreateOrderRequest.model_validate({
        "lines": [{"productId": product.id, "quantity": quantity}],
        "checkout": {"email": "learner@example.com", "fullName": "Test Learner",
                     "address": "123 Test Street", "city": "Singapore",
                     "postalCode": "123456", "country": "Singapore"},
    })


def test_catalog_filters_and_missing_slug(db, product):
    assert list_products(db, search="lamp")[0].id == product.id
    assert list_products(db, category="Carry") == []
    assert get_product_by_slug(db, "missing") is None


def test_checkout_replay_does_not_decrement_twice(db, product):
    request = order_request(product)
    key = str(uuid4())
    receipt = create_order(db, request, key)
    assert receipt.total == Decimal("32.00")
    again = create_order(db, request, key)
    assert receipt.id == again.id
    assert db.scalar(select(Inventory.quantity)) == 1


def test_failed_checkout_rolls_back(db, product):
    request = order_request(product, quantity=3)
    with pytest.raises(InsufficientInventoryError):
        create_order(db, request, str(uuid4()))
    assert db.scalar(select(Inventory.quantity)) == 2
    assert db.scalar(select(Order)) is None
