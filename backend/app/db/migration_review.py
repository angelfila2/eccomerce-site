"""Assistant-owned migration inventory for implemented account/cart models.

Schema/data migrations and frontend are assistant responsibilities. Add newly
completed model tables here alongside their Alembic revision and migration tests.
"""

from app.accounts.models import Cart, CartItem, User
from app.interactions.models import Interaction


def required_tables() -> set[str]:
    """Return account/cart tables supported by the current migration head."""
    return {model.__tablename__ for model in (User, Cart, CartItem, Interaction)}
