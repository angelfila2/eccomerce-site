"""Catalog queries and response mapping."""

from sqlalchemy import or_, select
from sqlalchemy.orm import Session, selectinload

from app.catalog.models import Category, Product
from app.catalog.schemas import ProductResponse


def get_product_by_slug(session: Session, slug: str) -> ProductResponse | None:
    """Retrieve a product by its slug."""
    statement = (
        select(Product)
        .where(Product.slug == slug)
        .options(
            selectinload(Product.category),
            selectinload(Product.inventory_record),
        )
    )
    product = session.scalar(statement)
    if product is None:
        return None
    return _to_product_response(product)


def _to_product_response(product: Product) -> ProductResponse:
    if product.inventory_record is None:
        raise ValueError(f"Product '{product.slug}' has no inventory record")
    return ProductResponse(
        id=product.id,
        slug=product.slug,
        name=product.name,
        category=product.category.name,
        description=product.description,
        details=product.details,
        price=product.price,
        inventory=product.inventory_record.quantity,
        imageUrl=product.image_url,
        accent=product.accent,
        featured=product.featured,
    )


def list_products(
    session: Session,
    category: str | None = None,
    search: str | None = None,
    limit: int = 10,
    offset: int = 0,
) -> list[ProductResponse]:
    """List products with optional category and search filters."""
    if not 1 <= limit <= 100 or offset < 0:
        raise ValueError("Invalid pagination")
    if not category and not search:
        from app.catalog.performance import paginated_catalog
        return paginated_catalog(session, limit, offset)
    statement = select(Product).options(
        selectinload(Product.category),
        selectinload(Product.inventory_record),
    )
    if category:
        statement = statement.join(Product.category).where(Category.name == category)
    if search:
        statement = statement.where(
            or_(
                Product.name.ilike(f"%{search}%"),
                Product.description.ilike(f"%{search}%"),
            )
        )
    statement = statement.order_by(Product.name, Product.id).offset(offset).limit(limit)
    products = session.scalars(statement).all()
    responses: list[ProductResponse] = []

    for product in products:
        response = _to_product_response(product)
        responses.append(response)

    return responses
