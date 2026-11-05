# Learning progress

All BE implementations were completed at the user's explicit request. Completed below means code and local contracts pass; live PostgreSQL/Redis verification remains a separate pending integration gate. ML remains Not Started.
All tasks start Not Started. Existing code is not evidence of a verified learning outcome.

Allowed statuses: Not Started, In Progress, Blocked, Completed. Record actual command output and review acceptance criteria before marking Completed. Do not count scaffolding or expected failures as completion.

| Task ID | Topic | Status | Test |
|---|---|---|---|
| BE-001 | Read categories through FastAPI | Completed | User reported passing test; implementation reviewed. Optional cleanup: remove unreachable raise after return. |
| BE-002 | Validate registration input | Completed | User reported passing test; saved implementation reviewed. Optional cleanup: duplicate BaseModel import. |
| BE-003 | Map account and cart entities | Completed | Account/cart models and migrations implemented; focused constraints and SQLite migration roundtrips pass. Live PostgreSQL gate is separately pending. |
| BE-004 | Query a user by normalized email | Completed | Implementation reviewed; focused test executed: 1 passed. |
| BE-005 | Verify request-scoped session cleanup | Completed | Focused test executed: 1 passed. Reviewed yield versus return, cleanup on errors and no automatic commit. |
| BE-006 | Hash and verify passwords | Completed | Saved implementation reviewed; focused test executed: 1 passed. Argon2 hashing, salted hashes, correct/wrong passwords and unknown-hash handling verified. |
| BE-007 | Issue and validate expiring JWTs | Completed | Decoder fixed at learner's explicit request; 10 focused tests passed for signatures, algorithm restrictions, required claims, timestamp types and expiry boundaries. |
| BE-008 | Implement account HTTP handlers | Completed | Implemented at user request: registration/login/profile/update/logout, registered HTTP routes, Redis rate limiting/revocation. Handler and HTTP contracts pass in the 27-test focused suite; live Redis verification pending. |
| BE-009 | Mutate an owned persistent cart | Completed | Owned cart read/update/removal, bounds, stock checks and ownership HTTP contracts pass. |
| BE-010 | Harden existing guest checkout | Completed | Fingerprint/owner-bound replay, conditional atomic stock updates and purchase events pass local tests; real PostgreSQL concurrency gates are present but skipped without TEST_POSTGRES_URL. |
| BE-011 | Persist validated interaction events | Completed | Validated interaction persistence, UUID sessions, event deduplication and purchase-spoof rejection pass service/HTTP tests. |
| BE-012 | Return only owned order history | Completed | Owned paginated order history and cross-account isolation pass. |
| ML-001 | Rank time-decayed popularity | Not Started | Pending — `python -m pytest tests/learning/test_ml.py::test_ML_001 -q` |
| ML-002 | Fit product TF-IDF features | Not Started | Pending — `python -m pytest tests/learning/test_ml.py::test_ML_002 -q` |
| ML-003 | Rank cosine similarity | Not Started | Pending — `python -m pytest tests/learning/test_ml.py::test_ML_003 -q` |
| ML-004 | Persist and query semantic vectors | Not Started | Pending — `python -m pytest tests/learning/test_ml.py::test_ML_004 -q` |
| ML-005 | Score implicit collaborative feedback | Not Started | Pending — `python -m pytest tests/learning/test_ml.py::test_ML_005 -q` |
| ML-006 | Build a PyTorch two-tower module | Not Started | Pending — `python -m pytest tests/learning/test_ml.py::test_ML_006 -q` |
| ML-007 | Sample reproducible negatives | Not Started | Pending — `python -m pytest tests/learning/test_ml.py::test_ML_007 -q` |
| ML-008 | Train and validate offline | Not Started | Pending — `python -m pytest tests/learning/test_ml.py::test_ML_008 -q` |
| ML-009 | Split time and evaluate ranking | Not Started | Pending — `python -m pytest tests/learning/test_ml.py::test_ML_009 -q` |
| ML-010 | Fuse candidates and diversify | Not Started | Pending — `python -m pytest tests/learning/test_ml.py::test_ML_010 -q` |
| ML-011 | Compute frequently bought together | Not Started | Pending — `python -m pytest tests/learning/test_ml.py::test_ML_011 -q` |
| BE-013 | Integrate recommendation API with safe fallbacks | Completed | All recommendation endpoints serve explicit featured/category fallbacks and order-cooccurrence data; stock/seed filtering and HTTP contracts pass. Deferred ML algorithms remain unfinished. |
| BE-014 | Cache recommendations safely | Completed | Redis cache-aside with TTL/outage handling, scoped DB-state-versioned keys, checkout invalidation and current-stock refresh implemented; test doubles pass, live Redis remains unverified. |
| BE-015 | Assistant-managed schema/data migrations | Completed | Account/cart and interaction/order metadata migrations implemented. Full SQLite upgrade/downgrade preserves legacy orders; PostgreSQL DDL compiles. Live PostgreSQL gates pending infrastructure. |
| BE-016 | Bound catalogue query counts | Completed | Bounded eager-load pagination used by catalogue; SELECT-count and bounds contracts pass. |
