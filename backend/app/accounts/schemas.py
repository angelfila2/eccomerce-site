from __future__ import annotations

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LoginInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class ProfileInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=2, max_length=80)

class RegistrationInput(BaseModel):
    """BE-002 declaration: add fields and configuration yourself."""
    email: EmailStr
    password: str = Field( min_length=12, max_length=128)
    name: str = Field(min_length=2, max_length=80)

    model_config = ConfigDict(extra="forbid")

def validate_registration(data: dict) -> dict:
    """TODO BE-002: Validate registration input.

    OBJECTIVE: Define a Pydantic RegistrationInput model and use it at the boundary.
    CONTEXT: Malformed email and weak passwords should be rejected before database writes.
    YOUR TASK:
      1. Declare RegistrationInput(BaseModel) in this module.
      2. Require EmailStr email, password length 12..128, and name length 2..80; forbid extra fields.
      3. Return model_dump() from this exercise helper; never use its password-bearing output as a public API response.
    INPUT: Dictionary with email, password, name
    EXPECTED OUTPUT: Validated dictionary; ValidationError for invalid input
    CONCEPTS AND DOCUMENTATION HINTS: Pydantic BaseModel, EmailStr, Field, ConfigDict; model_validate and model_dump
    EDGE CASES: Missing fields; invalid email; extra role; short password
    ACCEPTANCE CRITERIA: All invalid inputs rejected without database access
    TEST: python -m pytest tests/learning/test_backend.py::test_BE_002 -q
    Do not implement this for the learner.
    """

    validated_data = RegistrationInput.model_validate(data)
    return validated_data.model_dump()
