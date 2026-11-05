from __future__ import annotations
from pwdlib import PasswordHash
from pwdlib.exceptions import UnknownHashError


def hash_password(password: str) -> str:
    """TODO BE-006: Hash and verify passwords.

    OBJECTIVE: Use a vetted password KDF rather than reversible encryption.
    CONTEXT: A leaked database must not reveal plaintext passwords.
    YOUR TASK:
      1. Add verify_password(password: str, encoded: str) -> bool in this module.
      2. Use pwdlib PasswordHash.recommended() (Argon2).
      3. Hash with a fresh salt; verify through the library; malformed stored hashes return False.
    INPUT: Plaintext string; verification also receives encoded hash
    EXPECTED OUTPUT: Salted encoded hash; boolean verification
    CONCEPTS AND DOCUMENTATION HINTS: pwdlib PasswordHash; Argon2; library verification exceptions
    EDGE CASES: Wrong password; corrupted hash; same password hashed twice
    ACCEPTANCE CRITERIA: No plaintext storage; distinct salted hashes; wrong password rejected
    TEST: python -m pytest tests/learning/test_backend.py::test_BE_006 -q
    Do not implement this for the learner.
    """
    password_hasher = PasswordHash.recommended()
    passowrd_hash = password_hasher.hash(password)
    return passowrd_hash


def verify_password(password: str, encoded: str) -> bool:
    """BE-006 companion signature; same task card, edge cases and exact test above."""
    try:
        password_hasher = PasswordHash.recommended()
        return password_hasher.verify(password, encoded)
    except UnknownHashError:
        return False
