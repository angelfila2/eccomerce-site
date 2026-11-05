from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.accounts.router import optional_user
from app.catalog.models import Product
from app.core.redis_client import get_redis
from app.db.session import get_session
from app.recommendations.schemas import RecommendationResponse
from app.recommendations.service import recommend_products

router = APIRouter(prefix="/recommendations", tags=["recommendations"])
Database = Annotated[Session, Depends(get_session)]
Limit = Annotated[int, Query(ge=1, le=12)]


@router.get("", response_model=RecommendationResponse)
@router.get("/personalized", response_model=RecommendationResponse)
def personalized(session: Database, seed_product_ids: Annotated[list[UUID] | None, Query()] = None,
                 limit: Limit = 4, user=Depends(optional_user), client=Depends(get_redis)):
    return recommend_products(session=session, seed_product_ids=seed_product_ids or [], limit=limit,
                              user_id=user["id"] if user else None, redis_client=client)


@router.get("/trending", response_model=RecommendationResponse)
def trending(session: Database, limit: Limit = 4, client=Depends(get_redis)):
    return recommend_products(session=session, seed_product_ids=[], limit=limit, mode="trending", redis_client=client)


def product_recommendations(session, product_id, limit, mode, client):
    if session.get(Product, product_id) is None:
        raise HTTPException(404, "Product not found")
    return recommend_products(session=session, seed_product_ids=[product_id], limit=limit, mode=mode, redis_client=client)


@router.get("/similar/{product_id}", response_model=RecommendationResponse)
def similar(product_id: UUID, session: Database, limit: Limit = 4, client=Depends(get_redis)):
    return product_recommendations(session, product_id, limit, "similar", client)


@router.get("/frequently-bought/{product_id}", response_model=RecommendationResponse)
def frequently_bought(product_id: UUID, session: Database, limit: Limit = 4, client=Depends(get_redis)):
    return product_recommendations(session, product_id, limit, "frequently_bought", client)


@router.get("/you-may-like/{product_id}", response_model=RecommendationResponse)
def you_may_like(product_id: UUID, session: Database, limit: Limit = 4, client=Depends(get_redis)):
    return product_recommendations(session, product_id, limit, "you_may_like", client)
