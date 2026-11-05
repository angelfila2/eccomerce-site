from __future__ import annotations

def sample_negatives(seen: set[int], product_count: int, count: int, seed: int) -> list[int]:
    """TODO ML-007: Sample reproducible negatives.

    OBJECTIVE: Construct contrastive training examples without positive contamination.
    CONTEXT: Implicit feedback records positives, so training needs explicit negative candidates.
    YOUR TASK:
      1. Choose unseen indices from range(product_count) with a local seeded RNG.
      2. Sample without replacement and reject impossible counts with ValueError.
      3. Never modify seen or global RNG state.
    INPUT: Seen IDs, catalogue size P, sample size N, seed
    EXPECTED OUTPUT: N unique unseen integers
    CONCEPTS AND DOCUMENTATION HINTS: random.Random; negative sampling; rejection vs candidate sampling
    EDGE CASES: All items seen; zero count; invalid counts; same seed
    ACCEPTANCE CRITERIA: Reproducible, no known positives, bounded runtime
    TEST: python -m pytest tests/learning/test_ml.py::test_ML_007 -q
    Do not implement this for the learner.
    """
    raise NotImplementedError("TODO ML-007")
