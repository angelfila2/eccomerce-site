from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from app.catalog.schemas import ProductResponse

router = APIRouter(prefix="/products", tags=["catalog"])


@router.get("", response_model=list[ProductResponse])
def list_products(
    category: Annotated[str | None, Query(max_length=80)] = None,
    search: Annotated[str | None, Query(max_length=120)] = None,
) -> list[ProductResponse]:
    # TODO: Inject Session and call catalog.service.list_products.
    # Keep filtering in SQL and add limit/cursor pagination before production.
    _ = (category, search)
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, "Implement catalog listing")


@router.get("/{slug}", response_model=ProductResponse)
def get_product(slug: str) -> ProductResponse:
    # TODO: Inject Session, call catalog.service.get_product_by_slug,
    # and return HTTP 404 when no active product matches.
    _ = slug
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, "Implement product detail")

