from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.catalog.models import Product
from app.catalog.service import _to_product_response


def paginated_catalog(session: Session, limit: int, offset: int) -> list:
    if not 1 <= limit <= 100 or offset < 0:
        raise ValueError("Invalid pagination")
    # Three bounded queries replace per-product category/inventory lookups.
    rows = session.scalars(select(Product).options(selectinload(Product.category),
                           selectinload(Product.inventory_record)).order_by(Product.name, Product.id)
                           .limit(limit).offset(offset))
    return [_to_product_response(product) for product in rows]
