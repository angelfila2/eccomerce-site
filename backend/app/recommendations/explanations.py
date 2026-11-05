"""Human-readable explanations for recommendation results."""

from app.recommendations.ranking import RankedCandidate


def explain_candidate(candidate: RankedCandidate, category: str) -> str:
    """BE-013 explanation subtask (legacy recommendations-4).

    Objective/context: Help a shopper understand the strongest recommendation signal.
    Steps: inspect category, similarity and popularity evidence; choose a stable,
    truthful phrase; use deterministic precedence on ties; expose no user identifiers.
    Input: RankedCandidate and public category name. Output: nonempty reason string.
    Hints: compare named dataclass fields; keep presentation separate from ranking.
    Edge cases: equal scores, no category name, zero-valued evidence.
    Acceptance: truthful reason; no promise of purchase co-occurrence without orders.
    Test: python -m pytest tests/learning/test_backend.py::test_BE_013 -q
    Add direct reason/precedence tests during BE-013; full card: docs/learning/TASKS.md.
    Do not implement for the learner. Return a stable explanation such as
    "Matches your interest in Workspace" when category affinity dominates;
    otherwise use semantic or popularity evidence.
    """
    # Earlier example wording, retained for the learner:
    # "Matches your interest in Workspace" when category affinity dominates,
    # otherwise use a semantic-similarity or popularity explanation.
    raise NotImplementedError
