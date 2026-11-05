from __future__ import annotations

def frequently_bought(orders: list[list[str]], product_id: str, limit: int = 4) -> list[str]:
    """TODO ML-011: Compute frequently bought together.

    OBJECTIVE: Separate purchase association from content similarity.
    CONTEXT: Items bought in the same completed order suggest complementary products.
    YOUR TASK:
      1. Count each companion once per order containing the seed.
      2. Exclude seed; sort decreasing co-order count then product ID.
      3. Return <= limit unique IDs; reject negative limit; ignore orders without seed.
    INPUT: Completed order baskets, seed ID, limit
    EXPECTED OUTPUT: Ordered companion IDs
    CONCEPTS AND DOCUMENTATION HINTS: set per basket; Counter; association vs similarity; support bias
    EDGE CASES: Duplicate units; no co-orders; ties; zero limit
    ACCEPTANCE CRITERIA: Only purchase co-occurrence influences the output
    TEST: python -m pytest tests/learning/test_ml.py::test_ML_011 -q
    Do not implement this for the learner.
    """
    raise NotImplementedError("TODO ML-011")
