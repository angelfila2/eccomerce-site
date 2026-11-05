from __future__ import annotations

def nearest_vectors(session, vector: list[float], limit: int = 4) -> list[str]:
    """TODO ML-004: Persist and query semantic vectors.

    OBJECTIVE: Separate offline embedding generation from indexed online retrieval.
    CONTEXT: Sentence Transformers captures meaning beyond exact shared words.
    YOUR TASK:
      1. Review existing embeddings.py; preserve its implementation.
      2. Implement offline catalogue encoding; the assistant provides command scaffolding and schema/data migrations for product_id, model_version, text hash and vector(384).
      3. Implement a PostgreSQL pgvector cosine-distance query filtered to current model and in-stock products.
      4. Reject wrong dimensions, NaN/Inf and negative limits before database access; no model download in HTTP handlers.
    INPUT: Session and normalized 384-dimensional vector
    EXPECTED OUTPUT: Ordered product UUID strings
    CONCEPTS AND DOCUMENTATION HINTS: SentenceTransformer.encode; pgvector Vector.cosine_distance; HNSW; model-version invalidation
    EDGE CASES: Missing extension; invalid dimensions; stale vectors; unavailable local model
    ACCEPTANCE CRITERIA: Input guards tested locally; migration and similarity query verified on PostgreSQL
    TEST: python -m pytest tests/learning/test_ml.py::test_ML_004 -q
    Do not implement this for the learner.
    """
    raise NotImplementedError("TODO ML-004")
