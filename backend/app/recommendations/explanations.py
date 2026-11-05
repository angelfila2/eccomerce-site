"""Human-readable explanations for recommendation results."""

from app.recommendations.ranking import RankedCandidate


def explain_candidate(candidate: RankedCandidate, category: str) -> str:
    """Explain the strongest signal without exposing internal score details."""
    # TODO(recommendations-4): Return a stable explanation such as
    # "Matches your interest in Workspace" when category affinity dominates,
    # otherwise use a semantic-similarity or popularity explanation.
    raise NotImplementedError
