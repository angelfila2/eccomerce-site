from __future__ import annotations

def vectorize(texts: list[str]):
    """TODO ML-002: Fit product TF-IDF features.

    OBJECTIVE: Convert product descriptions to comparable numeric features.
    CONTEXT: Content similarity works without other shoppers' histories.
    YOUR TASK:
      1. Build text from title, description, category and brand in the calling pipeline.
      2. Fit sklearn TfidfVectorizer with lowercase=True; return fitted vectorizer and sparse matrix.
      3. Keep input order and return one row per text; reject empty/all-blank input with ValueError.
    INPUT: P product text strings
    EXPECTED OUTPUT: Tuple (vectorizer, CSR-compatible matrix [P, V])
    CONCEPTS AND DOCUMENTATION HINTS: TfidfVectorizer.fit_transform; sparse matrices; document frequency
    EDGE CASES: Repeated terms; empty vocabulary; identical documents
    ACCEPTANCE CRITERIA: Identical texts have identical rows; reproducible feature dimensions
    TEST: python -m pytest tests/learning/test_ml.py::test_ML_002 -q
    Do not implement this for the learner.
    """
    raise NotImplementedError("TODO ML-002")
