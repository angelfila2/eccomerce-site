"""Database seam.

TODO: Create a synchronous SQLAlchemy 2 engine and request-scoped Session dependency.
Start synchronous. Move to async only if load measurements demonstrate a benefit.

The eventual interface should be small:

    def get_session() -> Iterator[Session]

Routers should pass the session to module use cases. A use case owns its transaction;
repository helpers must not commit independently.
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
