from __future__ import annotations
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.accounts.models import User

def get_user_by_email(session, email: str):
    """TODO BE-004: Query a user by normalized email.

    OBJECTIVE: Write a read-only SQLAlchemy ORM query.
    CONTEXT: Login must retrieve the account before password verification.
    YOUR TASK:
      1. Normalize the supplied email with strip and casefold.
      2. Use the User model from BE-003 in a SELECT predicate.
      3. Return one User or None; do not commit.
    INPUT: Session and email string
    EXPECTED OUTPUT: User | None
    CONCEPTS AND DOCUMENTATION HINTS: sqlalchemy.select; Session.scalar; consistent normalization at registration
    EDGE CASES: Missing email; whitespace and mixed case; SQL metacharacters
    ACCEPTANCE CRITERIA: Matching normalized account; no record for unknown email
    TEST: python -m pytest tests/learning/test_backend.py::test_BE_004 -q
    Do not implement this for the learner.
    """
    normalized_email = email.strip().casefold()
    statement = select(User).where(User.email == normalized_email)
    user = session.scalar(statement)
    return user
