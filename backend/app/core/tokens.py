from __future__ import annotations

import jwt

def issue_token(user_id: str, secret: str, now: int, ttl: int = 900) -> str:
    """TODO BE-007: Issue and validate expiring JWTs.

    OBJECTIVE: Verify token integrity, subject and expiration.
    CONTEXT: A claimed identity is trustworthy only after signature and claim checks.
    YOUR TASK:
      1. Add decode_token(token, secret, now) -> str returning the subject.
      2. Require a nonempty subject, exp and standard iat; use HS256 with an explicit allowed algorithm list.
         iat is Unix seconds: require an integer (not bool), with iat <= now < exp.
         Use the supplied now for time validation rather than the computer's clock.
      3. Use supplied now for deterministic expiry checks; reject expired/tampered/wrong-key tokens with ValueError.
      4. Keep secrets in environment configuration; never log tokens.
    INPUT: User ID, secret, Unix time, TTL seconds
    EXPECTED OUTPUT: JWT; decoder returns subject or raises ValueError
    CONCEPTS AND DOCUMENTATION HINTS: PyJWT encode/decode; algorithms allowlist; exp/iat claims; deterministic clock
    EDGE CASES: Expiry boundary now >= exp; empty subject; wrong signature; missing claims
    ACCEPTANCE CRITERIA: Signed claims verified, no algorithm chosen from untrusted header
    TEST: python -m pytest tests/learning/test_backend.py::test_BE_007 -q
    Do not implement this for the learner.
    """
    payload = {
        "sub": user_id,
        "iat": now,
        "exp": now + ttl,
    }
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token


def decode_token(token: str, secret: str, now: int) -> str:
    """Verify the signature and required claims using the caller's Unix time."""
    try:
        decoded = jwt.decode(
            token,
            secret,
            algorithms=["HS256"],
            options={
                "require": ["sub", "iat", "exp"],
                # Check time below with `now`, keeping boundary tests deterministic.
                # These options do not disable signature verification.
                "verify_exp": False,
                "verify_iat": False,
            },
        )
    except jwt.PyJWTError as error:
        raise ValueError("Invalid token") from error

    if not isinstance(decoded["sub"], str) or not decoded["sub"]:
        raise ValueError("Invalid subject claim")
    # bool is an int subclass in Python, but is not a valid timestamp here.
    if type(decoded["iat"]) is not int:
        raise ValueError("Invalid iat claim")
    if type(decoded["exp"]) is not int:
        raise ValueError("Invalid expiration claim")
    if decoded["iat"] > now:
        raise ValueError("Token issued in the future")
    if now >= decoded["exp"]:
        raise ValueError("Token has expired")
    return decoded["sub"]
