from __future__ import annotations

def collaborative_scores(interactions, user_index: int) -> list[float]:
    """TODO ML-005: Score implicit collaborative feedback.

    OBJECTIVE: Infer preferences from overlapping user-item histories.
    CONTEXT: Shoppers with similar histories provide evidence that product text cannot.
    YOUR TASK:
      1. Accept nonnegative CSR-compatible [U,P] weighted feedback.
      2. Compute item-item cosine similarities from interaction columns; zero the diagonal.
      3. Score items using the selected user's weighted history times that similarity matrix.
      4. Zero seen item scores; validate user bounds and reject negative feedback; all-zero history returns zeros.
    INPUT: Nonnegative [U,P] matrix and user row index
    EXPECTED OUTPUT: P finite nonnegative scores
    CONCEPTS AND DOCUMENTATION HINTS: scipy.sparse; transpose; cosine_similarity; implicit vs explicit ratings
    EDGE CASES: Sparse cold users; unseen items; zero columns; negative values
    ACCEPTANCE CRITERIA: Unseen item shared by neighboring histories outranks isolated item
    TEST: python -m pytest tests/learning/test_ml.py::test_ML_005 -q
    Do not implement this for the learner.
    """
    raise NotImplementedError("TODO ML-005")
