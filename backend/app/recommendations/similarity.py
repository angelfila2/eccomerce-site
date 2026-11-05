from __future__ import annotations

def similar_indices(matrix, seed_index: int, limit: int = 4) -> list[int]:
    """TODO ML-003: Rank cosine similarity.

    OBJECTIVE: Understand normalized dot products and top-k retrieval.
    CONTEXT: Similar Products must exclude the currently viewed product.
    YOUR TASK:
      1. Compute cosine similarity between seed row and all rows.
      2. Exclude seed, sort by decreasing similarity and ascending index on ties.
      3. Return at most limit; negative limit or invalid seed raises ValueError; zero limit returns [].
    INPUT: Matrix [P,V], seed row index, k
    EXPECTED OUTPUT: List of <= k distinct integer row indices
    CONCEPTS AND DOCUMENTATION HINTS: sklearn.metrics.pairwise.cosine_similarity; sparse slicing; stable sorting
    EDGE CASES: Zero vector; ties; only one product; limit exceeds catalogue
    ACCEPTANCE CRITERIA: Seed excluded; semantically shared tokens rank ahead of unrelated text
    TEST: python -m pytest tests/learning/test_ml.py::test_ML_003 -q
    Do not implement this for the learner.
    """
    raise NotImplementedError("TODO ML-003")
