"""Isolated SQLite unit fixtures; never connect to the configured application DB."""

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

import app.catalog.models  # noqa: F401
import app.inventory.models  # noqa: F401
import app.orders.models  # noqa: F401
import app.accounts.models  # noqa: F401
import app.interactions.models  # noqa: F401
from app.db.base import Base


@pytest.fixture
def db():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False},
                           poolclass=StaticPool)

    @event.listens_for(engine, "connect")
    def foreign_keys(connection, _):
        connection.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    with Session(engine, expire_on_commit=False) as session:
        yield session
        session.rollback()
    Base.metadata.drop_all(engine)
    engine.dispose()
