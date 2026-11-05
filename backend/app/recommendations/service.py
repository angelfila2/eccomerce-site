"""Recommendation orchestration independent of HTTP concerns."""

from uuid import UUID

from sqlalchemy.orm import Session

from app.recommendations.schemas import RecommendationResponse


def recommend_products(
    *,
    session: Session,
    seed_product_ids: list[UUID],
    limit: int,
) -> RecommendationResponse:
    """Generate personalized products or a deterministic cold-start fallback."""
    # TODO(recommendations-5): Implement this after embeddings.py and ranking.py.
    # Fetch the complete in-stock catalog, create/reuse product embeddings, call
    # rank_candidates(), build explanations, and return at most `limit` items.
    # With no valid seeds, return featured in-stock products using strategy
    # "featured_fallback" and modelVersion "semantic-session-v1".
    raise NotImplementedError
