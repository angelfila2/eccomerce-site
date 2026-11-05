"""Executable acceptance contracts. Failures are expected until you implement tasks.

Imports stay inside tests so a missing future model cannot break test collection.
SQLite covers deterministic unit behavior, not PostgreSQL locking or pgvector.
"""
from decimal import Decimal
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy import event, inspect, select
from sqlalchemy.exc import IntegrityError

from app.catalog.models import Category, Product
from app.db.session import get_session
from app.inventory.models import Inventory


@pytest.fixture
def item(db):
    category = Category(name="Workspace", slug="workspace")
    product = Product(name="Lamp", slug="lamp", description="A lamp", details=[],
                      price=Decimal("20"), image_url="/lamp.png", category=category)
    product.inventory_record = Inventory(quantity=5)
    db.add(product)
    db.commit()
    return product


def test_BE_001(db):
    from app.categories.router import router

    app = FastAPI()
    app.include_router(router, prefix="/api/v1")
    app.dependency_overrides[get_session] = lambda: db
    client = TestClient(app)
    response = client.get("/api/v1/categories")
    assert response.status_code == 200
    assert response.json() == []
    db.add_all([Category(name="Workspace", slug="workspace"),
                Category(name="Carry", slug="carry")])
    db.commit()
    before = len(db.new), len(db.dirty), len(db.deleted)
    response = client.get("/api/v1/categories")
    assert response.status_code == 200
    rows = response.json()
    assert [row["name"] for row in rows] == ["Carry", "Workspace"]
    assert all(set(row) == {"id", "name", "slug"} for row in rows)
    assert all(isinstance(row["id"], str) for row in rows)
    assert (len(db.new), len(db.dirty), len(db.deleted)) == before


def test_BE_002():
    from app.accounts.schemas import validate_registration

    valid = {"email": "learner@example.com", "name": "Learner",
             "password": "a-long-example-password"}
    assert validate_registration(valid)["email"] == valid["email"]
    for invalid in ({**valid, "email": "invalid"}, {**valid, "password": "short"},
                    {**valid, "role": "admin"}, {**valid, "name": "X"}, {}):
        with pytest.raises(ValidationError):
            validate_registration(invalid)


def model_types(db):
    from app.accounts.models import account_model_types

    types = account_model_types()
    for model in types:
        model.__table__.create(db.get_bind(), checkfirst=True)
    return types


def test_BE_003(db, item):
    User, Cart, CartItem = model_types(db)
    user = User(email="learner@example.com", password_hash="encoded", name="Learner")
    db.add(user)
    db.flush()
    cart = Cart(user_id=user.id)
    db.add(cart)
    db.flush()
    line = CartItem(cart_id=cart.id, product_id=item.id, quantity=2)
    db.add(line)
    db.commit()
    assert line in cart.items
    assert cart.user.id == user.id
    with pytest.raises(IntegrityError), db.begin_nested():
        db.add(User(email=user.email, password_hash="other", name="Other"))
        db.flush()
    with pytest.raises(IntegrityError), db.begin_nested():
        db.add(CartItem(cart_id=cart.id, product_id=item.id, quantity=1))
        db.flush()
    with pytest.raises(IntegrityError), db.begin_nested():
        db.add(CartItem(cart_id=cart.id, product_id=uuid4(), quantity=1))
        db.flush()
    with pytest.raises(IntegrityError), db.begin_nested():
        line.quantity = -1
        db.flush()


def test_BE_004(db):
    from app.accounts.repository import get_user_by_email

    User, _, _ = model_types(db)
    user = User(email="learner@example.com", password_hash="encoded", name="Learner")
    db.add(user)
    db.commit()
    assert get_user_by_email(db, "  LEARNER@example.com ").id == user.id
    assert get_user_by_email(db, "missing@example.com") is None
    assert get_user_by_email(db, "' OR 1=1 --") is None
    assert not db.dirty


def test_BE_005(monkeypatch):
    import app.db.session as module

    for exceptional in (False, True):
        context = MagicMock()
        sentinel = context.__enter__.return_value
        monkeypatch.setattr(module, "SessionFactory", lambda: context)
        dependency = module.get_session()
        assert next(dependency) is sentinel
        if exceptional:
            with pytest.raises(RuntimeError, match="handler failed"):
                dependency.throw(RuntimeError("handler failed"))
        else:
            dependency.close()
        context.__exit__.assert_called_once()
        sentinel.commit.assert_not_called()


def test_BE_006():
    from app.core import passwords

    plain = "a-long-example-password"
    encoded = passwords.hash_password(plain)
    assert encoded != plain and encoded.startswith("$argon2")
    assert passwords.hash_password(plain) != encoded
    assert passwords.verify_password(plain, encoded)
    assert not passwords.verify_password("wrong", encoded)
    assert not passwords.verify_password(plain, "corrupt hash")


def test_BE_007():
    import jwt
    from app.core import tokens

    secret = "unit-test-only-secret-with-at-least-32-characters"
    token = tokens.issue_token("user-1", secret, now=1000, ttl=60)
    payload = jwt.decode(token, secret, algorithms=["HS256"], options={"verify_exp": False})
    assert payload["iat"] == 1000
    assert "issuedAt" not in payload
    assert tokens.decode_token(token, secret, now=1059) == "user-1"
    for candidate, key, now in ((token, secret, 1060), (token, "wrong-key", 1001),
                               ("broken.token.value", secret, 1001),
                               (jwt.encode({"sub": "user-1"}, secret, algorithm="HS256"), secret, 1001),
                               (jwt.encode({"sub": "user-1", "exp": 1060}, secret, algorithm="HS256"), secret, 1001)):
        with pytest.raises(ValueError):
            tokens.decode_token(candidate, key, now=now)


@pytest.mark.parametrize("changes", [
    {"sub": ""}, {"sub": 123}, {"iat": True}, {"iat": "1000"},
    {"iat": 1002}, {"exp": True}, {"exp": "1060"}, {"exp": 1001},
])
def test_BE_007_invalid_claims(changes):
    import jwt
    from app.core.tokens import decode_token

    secret = "unit-test-only-secret-with-at-least-32-characters"
    payload = {"sub": "user-1", "iat": 1000, "exp": 1060, **changes}
    token = jwt.encode(payload, secret, algorithm="HS256")
    with pytest.raises(ValueError):
        decode_token(token, secret, now=1001)


def test_BE_007_rejects_other_algorithm():
    import jwt
    from app.core.tokens import decode_token

    secret = "unit-test-only-secret-with-at-least-48-characters-for-HS384"
    token = jwt.encode({"sub": "user-1", "iat": 1000, "exp": 1060},
                       secret, algorithm="HS384")
    with pytest.raises(ValueError):
        decode_token(token, secret, now=1001)


def test_BE_008(db, monkeypatch):
    from app.accounts import handlers

    # Your settings extension should read APP_JWT_SECRET, never hardcode a key.
    monkeypatch.setenv("APP_JWT_SECRET", "unit-test-only-long-secret-1234567890")
    from app.core.config import settings
    monkeypatch.setattr(settings, "jwt_secret", "unit-test-only-long-secret-1234567890")
    model_types(db)
    payload = {"email": "learner@example.com", "name": "Learner",
               "password": "a-long-example-password"}
    created = handlers.register(db, payload)
    assert set(created) == {"id", "email", "name"}
    assert created["email"] == payload["email"]
    with pytest.raises(HTTPException) as duplicate:
        handlers.register(db, payload)
    assert duplicate.value.status_code == 409
    with pytest.raises(HTTPException) as invalid:
        handlers.login(db, {"email": payload["email"], "password": "wrong"})
    assert invalid.value.status_code == 401
    token = handlers.login(db, {"email": payload["email"], "password": payload["password"]})
    assert token["token_type"].lower() == "bearer"
    profile = handlers.profile(db, f"Bearer {token['access_token']}")
    assert profile == created
    with pytest.raises(HTTPException) as unauthorized:
        handlers.profile(db, "Bearer forged")
    assert unauthorized.value.status_code == 401


def test_BE_009(db, item):
    from app.cart.service import set_quantity

    User, Cart, CartItem = model_types(db)
    owners = [User(email=f"user{i}@example.com", password_hash="encoded", name="Learner")
              for i in range(2)]
    db.add_all(owners)
    db.commit()
    first = set_quantity(db, str(owners[0].id), str(item.id), 2)
    assert first == {"product_id": str(item.id), "quantity": 2}
    set_quantity(db, str(owners[1].id), str(item.id), 1)
    assert len(db.scalars(select(Cart)).all()) == 2
    db.commit()  # End the read transaction before the next service-owned write.
    with pytest.raises(ValueError):
        set_quantity(db, str(owners[0].id), str(item.id), -1)
    set_quantity(db, str(owners[0].id), str(item.id), 0)
    remaining = db.scalars(select(CartItem)).all()
    assert len(remaining) == 1 and remaining[0].quantity == 1
    assert db.get(Inventory, item.inventory_record.id).quantity == 5
    db.commit()
    with pytest.raises(HTTPException) as missing:
        set_quantity(db, str(owners[0].id), str(uuid4()), 1)
    assert missing.value.status_code == 404
    with pytest.raises(HTTPException) as unavailable:
        set_quantity(db, str(owners[0].id), str(item.id), 6)
    assert unavailable.value.status_code == 409


def test_BE_010(db, item):
    from app.orders.schemas import CreateOrderRequest
    from app.orders.service import CheckoutError, create_order

    request = CreateOrderRequest.model_validate({
        "lines": [{"productId": item.id, "quantity": 1}],
        "checkout": {"email": "learner@example.com", "fullName": "Test Learner",
                     "address": "123 Test Street", "city": "Singapore",
                     "postalCode": "123456", "country": "Singapore"},
    })
    key = str(uuid4())
    create_order(db, request, key)
    changed = request.model_copy(deep=True)
    changed.lines[0].quantity = 2
    with pytest.raises(CheckoutError):
        create_order(db, changed, key)


def test_BE_011(db, item):
    from app.interactions.service import record_event

    event_id, anonymous_id = str(uuid4()), str(uuid4())
    payload = {"event_id": event_id, "kind": "view", "product_id": str(item.id)}
    first = record_event(db, payload, None, anonymous_id)
    assert first == {"event_id": event_id, "accepted": True}
    assert record_event(db, payload, None, anonymous_id) == first
    from app.interactions.models import Interaction
    assert len(db.scalars(select(Interaction)).all()) == 1
    db.commit()
    for invalid in ({**payload, "kind": "purchase"},
                    {**payload, "user_id": str(uuid4())},
                    {**payload, "kind": "unknown"}):
        with pytest.raises((ValueError, HTTPException)):
            record_event(db, invalid, None, anonymous_id)


def test_BE_012(db, item):
    from app.accounts.orders import list_owned_orders
    from app.orders.models import Order

    User, _, _ = model_types(db)
    users = [User(email=f"history{i}@example.com", password_hash="encoded", name="Learner")
             for i in range(2)]
    db.add_all(users)
    db.flush()
    common = dict(customer_email=users[0].email, customer_name="Learner", address="Test Street",
                  city="Singapore", postal_code="123456", country="Singapore",
                  subtotal=20, shipping=0, tax=0, discount=0, total=20)
    own = Order(user_id=users[0].id, idempotency_key=str(uuid4()), **common)
    other = Order(user_id=users[1].id, idempotency_key=str(uuid4()), **common)
    guest = Order(user_id=None, idempotency_key=str(uuid4()), **common)
    db.add_all([own, other, guest])
    db.commit()
    result = list_owned_orders(db, str(users[0].id))
    assert [str(row["id"]) for row in result] == [str(own.id)]
    assert list_owned_orders(db, str(uuid4())) == []


def test_BE_013(db, item):
    from app.recommendations.service import recommend_products

    result = recommend_products(session=db, seed_product_ids=[], limit=4)
    assert result.strategy == "featured_fallback"
    assert result.model_version
    assert result.items[0].product.id == item.id
    assert result.items[0].product.inventory > 0
    assert 0 <= result.items[0].score <= 1
    seeded = recommend_products(session=db, seed_product_ids=[item.id], limit=4)
    assert seeded.items == []
    item.inventory_record.quantity = 0
    db.commit()
    empty = recommend_products(session=db, seed_product_ids=[uuid4()], limit=4)
    assert empty.items == []


def test_BE_014():
    import json
    from redis.exceptions import ConnectionError
    from app.recommendations.cache import cached_recommendations

    client, compute = MagicMock(), MagicMock(return_value={"items": ["p1"]})
    client.get.return_value = None
    assert cached_recommendations(client, "owner:model:catalogue", compute, ttl=45) == {"items": ["p1"]}
    args = client.setex.call_args.args
    assert args[:2] == ("owner:model:catalogue", 45)
    assert json.loads(args[2]) == {"items": ["p1"]}
    client.get.return_value = '{"items": ["cached"]}'
    compute.reset_mock()
    assert cached_recommendations(client, "key", compute)["items"] == ["cached"]
    compute.assert_not_called()
    client.get.side_effect = ConnectionError("offline")
    assert cached_recommendations(client, "key", compute)["items"] == ["p1"]
    compute.side_effect = RuntimeError("model failed")
    with pytest.raises(RuntimeError, match="model failed"):
        cached_recommendations(client, "key", compute)
    with pytest.raises(ValueError):
        cached_recommendations(client, "key", compute, ttl=0)


def test_BE_015(db):
    from app.db.migration_review import required_tables
    from app.accounts.models import account_model_types
    from app.db.base import Base

    account_model_types()
    assert required_tables() == {"users", "carts", "cart_items", "interactions"}
    Base.metadata.create_all(db.get_bind())
    assert required_tables() <= set(inspect(db.get_bind()).get_table_names())
    # This unit contract is not evidence that an Alembic upgrade works on PostgreSQL.


def test_BE_016(db, item):
    from app.catalog.performance import paginated_catalog

    for index in range(4):
        product = Product(name=f"Other {index}", slug=f"other-{index}", description="Item",
                          details=[], price=Decimal("10"), image_url="/item.png",
                          category_id=item.category_id)
        product.inventory_record = Inventory(quantity=1)
        db.add(product)
    db.commit()
    db.expunge_all()  # Prevent preloaded relationships from hiding N+1 queries.
    statements = []

    def collect(conn, cursor, statement, parameters, context, executemany):
        if statement.lstrip().upper().startswith("SELECT"):
            statements.append(statement)

    event.listen(db.get_bind(), "before_cursor_execute", collect)
    try:
        rows = paginated_catalog(db, limit=5, offset=0)
        assert len(rows) == 5
        assert len(statements) <= 3
        assert paginated_catalog(db, limit=5, offset=10) == []
        with pytest.raises(ValueError):
            paginated_catalog(db, limit=101, offset=0)
    finally:
        event.remove(db.get_bind(), "before_cursor_execute", collect)
