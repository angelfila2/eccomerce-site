from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from redis.exceptions import ConnectionError

import app.main as main
from app.core.config import settings
from app.db.session import get_session


@pytest.fixture
def account_client(db, monkeypatch):
    redis = MagicMock()
    redis.eval.return_value = 1
    redis.exists.return_value = 0
    monkeypatch.setattr(main, "create_redis_client", lambda: redis)
    monkeypatch.setattr(settings, "jwt_secret", "unit-test-only-secret-at-least-32-characters")
    main.app.dependency_overrides[get_session] = lambda: db
    try:
        with TestClient(main.app) as client:
            yield client, redis
    finally:
        main.app.dependency_overrides.clear()
    redis.close.assert_called_once()


def test_registration_login_profile_logout(account_client):
    client, redis = account_client
    data = {"email": "Learner@example.com", "name": "Learner",
            "password": "a-long-example-password"}
    registration = client.post("/api/v1/auth/register", json=data)
    assert registration.status_code == 201
    assert set(registration.json()) == {"id", "email", "name"}
    assert client.post("/api/v1/auth/register", json=data).status_code == 409
    assert client.post("/api/v1/auth/login", json={"email": data["email"], "password": "wrong"}).status_code == 401
    login = client.post("/api/v1/auth/login", json={"email": data["email"], "password": data["password"]})
    assert login.status_code == 200
    headers = {"Authorization": "Bearer " + login.json()["access_token"]}
    profile = client.get("/api/v1/users/me", headers=headers)
    assert profile.status_code == 200 and profile.json() == registration.json()
    assert redis.eval.called and redis.exists.called
    assert client.post("/api/v1/auth/logout", headers=headers).status_code == 204
    redis.setex.assert_called_once()
    redis.exists.return_value = 1
    assert client.get("/api/v1/users/me", headers=headers).status_code == 401


def test_redis_readiness_and_auth_failure(account_client):
    client, redis = account_client
    assert client.get("/ready").status_code == 200
    redis.ping.side_effect = ConnectionError("offline")
    assert client.get("/ready").status_code == 503
    assert client.get("/health").status_code == 200
    redis.eval.side_effect = ConnectionError("offline")
    response = client.post("/api/v1/auth/login", json={"email": "user@example.com", "password": "example"})
    assert response.status_code == 503


def test_auth_validation_and_missing_credentials(account_client):
    client, _ = account_client
    assert client.get("/api/v1/users/me").status_code == 401
    assert client.post("/api/v1/auth/register", json={"email": "invalid"}).status_code == 422
    assert client.post("/api/v1/auth/login", json={"email": "user@example.com", "password": "pw", "role": "admin"}).status_code == 422
