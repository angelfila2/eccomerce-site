"""Real HTTP commerce flows on isolated SQLite, with explicit Redis test double."""
from decimal import Decimal
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import func, select

import app.main as main
from app.catalog.models import Category, Product
from app.core.config import settings
from app.db.session import get_session
from app.interactions.models import Interaction
from app.inventory.models import Inventory
from app.orders.models import Order


@pytest.fixture
def commerce(db, monkeypatch):
    redis = MagicMock()
    redis.eval.return_value = 1
    redis.exists.return_value = 0
    redis.get.return_value = None
    monkeypatch.setattr(main, "create_redis_client", lambda: redis)
    monkeypatch.setattr(settings, "jwt_secret", "unit-test-only-secret-at-least-32-characters")
    main.app.dependency_overrides[get_session] = lambda: db
    category = Category(name="Workspace", slug="workspace")
    products = []
    for index in range(3):
        product = Product(name=f"Item {index}", slug=f"item-{index}", description="Product",
                          details=[], price=Decimal("20"), image_url="/item.png", category=category)
        product.inventory_record = Inventory(quantity=5)
        db.add(product)
        products.append(product)
    db.commit()
    try:
        with TestClient(main.app) as client:
            yield client, db, redis, products
    finally:
        main.app.dependency_overrides.clear()


def account(client, index):
    email = f"learner{index}@example.com"
    password = "a-long-example-password"
    response = client.post("/api/v1/auth/register", json={"email": email, "password": password, "name": "Learner"})
    assert response.status_code == 201
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    return {"Authorization": "Bearer " + response.json()["access_token"], "X-Anonymous-ID": str(uuid4())}


def checkout_body(products):
    return {"lines": [{"productId": str(product.id), "quantity": 1} for product in products],
            "checkout": {"email": "guest@example.com", "fullName": "Guest Buyer",
                         "address": "123 Test Street", "city": "Singapore",
                         "postalCode": "123456", "country": "Singapore"}}


def test_owned_cart_checkout_order_history_and_purchase_events(commerce):
    client, db, redis, products = commerce
    first, second = account(client, 1), account(client, 2)
    path = f"/api/v1/cart/items/{products[0].id}"
    assert client.put(path, json={"quantity": 2}, headers=first).status_code == 200
    assert client.get("/api/v1/cart", headers=second).json() == []
    assert client.put(path, json={"quantity": 6}, headers=first).status_code == 409
    assert client.put(path, json={"quantity": -1}, headers=first).status_code == 422
    assert client.put(path, json={"quantity": 1}).status_code == 401
    body = checkout_body(products[:2])
    headers = {**first, "Idempotency-Key": str(uuid4())}
    receipt = client.post("/api/v1/orders", json=body, headers=headers)
    assert receipt.status_code == 201, receipt.text
    replay = client.post("/api/v1/orders", json=body, headers=headers)
    assert replay.json() == receipt.json()
    assert client.get("/api/v1/cart", headers=first).json() == []
    orders = client.get("/api/v1/orders", headers=first).json()
    assert [order["id"] for order in orders] == [receipt.json()["id"]]
    assert client.get("/api/v1/orders", headers=second).json() == []
    assert db.scalar(select(func.count()).select_from(Interaction).where(Interaction.kind == "purchase")) == 2
    db.rollback()
    # A second account cannot obtain the original receipt by reusing its key.
    assert client.post("/api/v1/orders", json=body, headers={**second, "Idempotency-Key": headers["Idempotency-Key"]}).status_code == 409
    assert redis.incr.called


def test_guest_scope_events_and_recommendation_endpoints(commerce):
    client, db, redis, products = commerce
    anonymous = str(uuid4())
    headers = {"X-Anonymous-ID": anonymous, "Idempotency-Key": str(uuid4())}
    body = checkout_body(products[:2])
    assert client.post("/api/v1/orders", json=body, headers=headers).status_code == 201
    assert client.post("/api/v1/orders", json=body, headers={**headers, "X-Anonymous-ID": str(uuid4())}).status_code == 409
    assert client.post("/api/v1/orders", json=body, headers={"Idempotency-Key": str(uuid4())}).status_code == 422
    event = {"event_id": str(uuid4()), "kind": "view", "product_id": str(products[0].id)}
    assert client.post("/api/v1/interactions", json=event, headers=headers).status_code == 202
    assert client.post("/api/v1/interactions", json=event, headers=headers).status_code == 202
    assert client.post("/api/v1/interactions", json={**event, "user_id": str(uuid4())}, headers=headers).status_code == 422
    assert client.post("/api/v1/interactions", json={**event, "kind": "purchase"}, headers=headers).status_code == 422
    assert client.post("/api/v1/interactions", json={"event_id": str(uuid4()), "kind": "search", "query": "lamp"}, headers=headers).status_code == 202
    for path in ("", "/personalized", "/trending", f"/similar/{products[0].id}",
                 f"/frequently-bought/{products[0].id}", f"/you-may-like/{products[0].id}"):
        response = client.get("/api/v1/recommendations" + path)
        assert response.status_code == 200, response.text
        assert response.json()["modelVersion"]
    together = client.get(f"/api/v1/recommendations/frequently-bought/{products[0].id}").json()
    assert [item["product"]["id"] for item in together["items"]] == [str(products[1].id)]
    assert redis.setex.called


def test_checkout_conflict_and_stock_rollback(commerce):
    client, db, _, products = commerce
    headers = {"X-Anonymous-ID": str(uuid4()), "Idempotency-Key": str(uuid4())}
    body = checkout_body(products[:1])
    assert client.post("/api/v1/orders", json=body, headers=headers).status_code == 201
    body["lines"][0]["quantity"] = 2
    assert client.post("/api/v1/orders", json=body, headers=headers).status_code == 409
    body["lines"][0]["quantity"] = 6
    assert client.post("/api/v1/orders", json=body, headers={**headers, "Idempotency-Key": str(uuid4())}).status_code == 409
    assert db.scalar(select(Inventory.quantity).where(Inventory.product_id == products[0].id)) == 4
    assert db.scalar(select(func.count()).select_from(Order)) == 1
