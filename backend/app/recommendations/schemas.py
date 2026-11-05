"""Public API contract for recommendation results."""

from pydantic import BaseModel, ConfigDict, Field

from app.catalog.schemas import ProductResponse


class RecommendationItem(BaseModel):
    product: ProductResponse
    score: float = Field(ge=0, le=1)
    reason: str


class RecommendationResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[RecommendationItem]
    strategy: str
    model_version: str = Field(alias="modelVersion")

    # TODO(recommendations): Add a request ID when recommendation impressions
    # are persisted so clicks can be attributed to this exact response.
