from __future__ import annotations

def popularity(events: list[dict], now: float, half_life: float = 604800, weights: dict | None = None) -> list[str]:
    """TODO ML-001: Rank time-decayed popularity.

    OBJECTIVE: Translate implicit feedback into a reproducible cold-start ranking.
    CONTEXT: New visitors need recommendations before personalized models exist.
    YOUR TASK:
      1. Use configurable default weights view=1, click=2, add_to_cart=5, purchase=10.
      2. Accumulate weight * 0.5 ** (age_seconds / half_life) per product.
      3. Ignore unknown events and future timestamps; reject nonpositive half_life.
      4. Sort descending total, then ascending product ID.
    INPUT: Events with product_id, kind, timestamp as Unix seconds; deterministic now
    EXPECTED OUTPUT: Ordered unique product ID strings
    CONCEPTS AND DOCUMENTATION HINTS: Weighted sums; exponential decay; stable sorting
    EDGE CASES: Empty history; equal scores; future events; old purchases
    ACCEPTANCE CRITERIA: Recent signals dominate equivalent older ones; deterministic cold start
    TEST: python -m pytest tests/learning/test_ml.py::test_ML_001 -q
    Do not implement this for the learner.
    """
    raise NotImplementedError("TODO ML-001")
