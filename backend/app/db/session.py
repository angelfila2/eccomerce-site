"""Synchronous SQLAlchemy engine and request-scoped session dependency.

Keep the database interface small:

    def get_session() -> Iterator[Session]

Routers pass the session to module use cases. A use case owns its transaction;
repository helpers do not commit independently.
"""

from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)


SessionFactory = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def get_session() -> Iterator[Session]:
    with SessionFactory() as session:
        yield session
