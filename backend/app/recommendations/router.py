"""Recommendation HTTP endpoint consumed by the React storefront."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.recommendations.schemas import RecommendationResponse
from app.recommendations.service import recommend_products

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("", response_model=RecommendationResponse)
def get_recommendations(
    session: Annotated[Session, Depends(get_session)],
    seed_product_ids: Annotated[list[UUID] | None, Query()] = None,
    limit: Annotated[int, Query(gt=0, le=12)] = 4,
) -> RecommendationResponse:
    # TODO(recommendations-6): Add request-level logging for strategy, model
    # version, seed count and latency after the service works end to end.
    return recommend_products(
        session=session,
        seed_product_ids=seed_product_ids or [],
        limit=limit,
    )
