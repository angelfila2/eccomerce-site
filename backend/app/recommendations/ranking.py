"""Explainable hybrid scoring and recommendation reranking."""

from dataclasses import dataclass
from uuid import UUID

import numpy as np


@dataclass(frozen=True)
class RankedCandidate:
    product_id: UUID
    score: float
    similarity_score: float
    category_match_score: float
    popularity_score: float


def rank_candidates(
    *,
    all_product_ids: list[UUID],
    interested_product_ids: list[UUID],
    product_meaning_vectors: list[list[float]],
    product_categories: list[str],
    product_popularity_scores: list[float],
) -> list[RankedCandidate]:
    """BE-013 ranking subtask (legacy recommendations-3); preserve the existing attempt.

    Objective/context: Finish explainable session ranking before API integration.
    Steps: normalize product vectors; compare against the existing interest mean;
    exclude seeds; compute the documented category/popularity signals; sort with
    deterministic UUID ties. Compare this earlier weighted scheme with ML-010 RRF
    before extending to incompatible model scores. Do not average raw model scales.
    Input: aligned IDs, vectors [P,D], categories and bounded popularity signals.
    Output: descending RankedCandidate list, scores bounded to [0,1].
    Hints: np.linalg.norm; zero-vector guards; dot product; set membership.
    Edge cases: empty/invalid seeds, mismatched array lengths, zero vectors, ties.
    Acceptance: keep the learner's existing mean-vector work; no seed candidates;
    finite scores and deterministic ranking, plus BE-013 service stock filtering.
    Test: python -m pytest tests/learning/test_backend.py::test_BE_013 -q
    Add direct ranking tests for these subtask invariants when BE-013 becomes active.
    Full task card: docs/learning/TASKS.md, BE-013. Do not solve for the learner.
    """
    # 1. Average the vectors of products the user liked into one interest vector.
    interested_id_set = set(interested_product_ids)
    interested_product_indexes = []

    for index, product_id in enumerate(all_product_ids):
        if product_id in interested_id_set:
            interested_product_indexes.append(index)

    if not interested_product_indexes:
        return []

    all_product_vectors = np.asarray(product_meaning_vectors, dtype=np.float32)
    interested_product_vectors = all_product_vectors[interested_product_indexes]
    user_interest_vector = interested_product_vectors.mean(axis=0)
    vector_length = np.linalg.norm(user_interest_vector)

    if vector_length == 0:
        return []

    user_interest_vector = user_interest_vector / vector_length

    # 2. Compare every product with the user's interest vector.
    similarity_by_product: dict[UUID, float] = {}
    for index, product_id in enumerate(all_product_ids):
        product_vector = all_product_vectors[index]
    # 3. Exclude products already used to build the user's interests.
    # 4. Combine 0.70 semantic + 0.20 category + 0.10 popularity.
    # 5. Clamp the final score to [0, 1] and sort descending.
    raise NotImplementedError
