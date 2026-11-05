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

    # BE-011/013 extension: introduce a response correlation ID with attribution
    # tests when impressions are persisted; preserve this client contract meanwhile.
