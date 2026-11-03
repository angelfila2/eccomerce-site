from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.catalog import service
from app.catalog.schemas import ProductResponse
from app.db.session import get_session

router = APIRouter(prefix="/products", tags=["catalog"])


@router.get("", response_model=list[ProductResponse])
def list_products(
    session: Annotated[Session, Depends(get_session)],
    category: Annotated[str | None, Query(max_length=80)] = None,
    search: Annotated[str | None, Query(max_length=120)] = None,
    limit: Annotated[int, Query(gt=0, le=100)] = 10,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[ProductResponse]:
    filtered_products = service.list_products(
        session=session,
        category=category,
        search=search,
        limit=limit,
        offset=offset,
    )
    return filtered_products


@router.get("/{slug}", response_model=ProductResponse)
def get_product(slug: str, session: Annotated[Session, Depends(get_session)]) -> ProductResponse:
    specific_product = service.get_product_by_slug(session, slug)
    if specific_product is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")
    return specific_product
