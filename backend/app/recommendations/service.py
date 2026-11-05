"""Serving orchestration with explicit model-free fallbacks while ML is unfinished."""
from collections import Counter
from hashlib import sha256
import json
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.catalog.models import Product
from app.catalog.service import _to_product_response
from app.core.redis_client import catalogue_version
from app.interactions.models import Interaction
from app.orders.models import Order, OrderLine, OrderStatus
from app.recommendations.cache import cached_recommendations
from app.recommendations.schemas import RecommendationItem, RecommendationResponse


def recommend_products(*, session: Session, seed_product_ids: list[UUID], limit: int,
                       mode: str = "personalized", user_id: str | None = None,
                       redis_client=None) -> RecommendationResponse:
    if not 1 <= limit <= 100:
        raise ValueError("Limit must be between 1 and 100")
    products = session.scalars(select(Product).options(selectinload(Product.category),
                              selectinload(Product.inventory_record)).order_by(Product.name, Product.id)).all()
    available = {product.id: product for product in products
                 if product.inventory_record and product.inventory_record.quantity > 0}
    seeds = set(seed_product_ids)
    purchased = set()
    if user_id:
        owner = UUID(user_id)
        history = session.scalars(select(Interaction.product_id).where(Interaction.user_id == owner,
                    Interaction.product_id.is_not(None)).order_by(Interaction.created_at.desc()).limit(30)).all()
        seeds.update(history)
        purchased.update(session.scalars(select(OrderLine.product_id).join(Order)
                         .where(Order.user_id == owner, Order.status == OrderStatus.CONFIRMED)))
    seed_categories = {product.category_id for product in products if product.id in seeds}
    counts = Counter()
    if mode == "frequently_bought" and seed_product_ids:
        baskets = session.scalars(select(OrderLine.order_id).join(Order).where(
            OrderLine.product_id == seed_product_ids[0], Order.status == OrderStatus.CONFIRMED)).all()
        if baskets:
            # Count each companion once per completed order, never text similarity.
            pairs = session.execute(select(OrderLine.order_id, OrderLine.product_id)
                                    .where(OrderLine.order_id.in_(baskets)).distinct())
            counts.update(product_id for _, product_id in pairs if product_id not in seeds)
    candidates = [p for p in available.values() if p.id not in seeds and p.id not in purchased]
    strategy = "featured_fallback"
    reason = "Featured catalogue selection; learning models are not trained yet"
    if mode == "frequently_bought":
        candidates = [p for p in candidates if counts[p.id] > 0]
        candidates.sort(key=lambda p: (-counts[p.id], p.name, str(p.id)))
        strategy, reason = "order_cooccurrence", "Bought in the same completed orders"
    elif seed_categories and mode != "trending":
        candidates.sort(key=lambda p: (p.category_id not in seed_categories, not p.featured, p.name, str(p.id)))
        strategy, reason = "category_fallback", "Matches a category you explored; ML fallback"
    else:
        candidates.sort(key=lambda p: (not p.featured, p.name, str(p.id)))
    # Current DB stock/category state forms part of the cache version. Serving
    # never trusts cached availability after a checkout or external stock change.
    signature = [(str(p.id), str(p.updated_at), p.inventory_record.quantity) for p in products if p.inventory_record]
    generation = catalogue_version(redis_client) if redis_client is not None else "uncached"
    key = "recommendations:v1:" + sha256(json.dumps([generation, mode, user_id, sorted(map(str, seeds)),
                 sorted(map(str, purchased)), limit, signature, sorted((str(k), v) for k,v in counts.items())],
                 sort_keys=True).encode()).hexdigest()
    def compute():
        return RecommendationResponse(items=[RecommendationItem(product=_to_product_response(p),
                   score=1 / (index + 1), reason=reason) for index, p in enumerate(candidates[:limit])],
                   strategy=strategy, modelVersion="baseline-serving-v1").model_dump(mode="json")
    payload = cached_recommendations(redis_client, key, compute) if redis_client is not None else compute()
    response = RecommendationResponse.model_validate(payload)
    # Refresh product objects from authoritative rows even on a cache hit.
    response.items = [item.model_copy(update={"product": _to_product_response(available[item.product.id])})
                      for item in response.items if item.product.id in available
                      and item.product.id not in seeds and item.product.id not in purchased]
    return response
