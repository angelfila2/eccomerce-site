# Test workflow

Run from `backend/` with `.venv` active. All unit tests use isolated SQLite or fakes, never the configured PostgreSQL URL. No trained artifacts or model downloads are required.

```powershell
# Existing foundation only: expected green
python -m pytest tests/test_health.py tests/test_foundation.py -q

# Your first task: expected red until you write it
python -m pytest tests/learning/test_backend.py::test_BE_001 -q

# Collection should succeed even when implementations do not exist
python -m pytest --collect-only -q

# Full learning suite: deliberately red; do not fill in code on the learner's behalf
python -m pytest tests/learning -q
```

`BE-005` checks existing infrastructure and may already pass. Its learning status remains Not Started until reviewed. ML-006/008 skip without optional Torch; skipped tests do not demonstrate completion. Tests are not xfailed or marked passing merely because a stub raises NotImplementedError.

Every task has a focused executable test and a fuller written acceptance card. Some tests necessarily depend on earlier learner code. Fix prerequisites in order; do not interpret dependent failures as separate bugs. During each active task, add adversarial cases listed in the card and guide before declaring completion.

SQLite cannot verify PostgreSQL row locks, pgvector, full migration DDL or transaction race behavior. Before those tasks are Completed, the assistant supplies and runs the migration/infrastructure integration tests on a disposable PostgreSQL database. Backend business-logic tests remain part of the guided work. This setup deliberately does not run destructive reset commands against a shared database.

| Integration gate | Required experiment |
|---|---|
| BE-003/015 | Upgrade new migrations from previous head; inspect FK/unique/check constraints; downgrade the assistant-authored revision and upgrade again on a disposable DB |
| BE-010 | Two independent Sessions start checkout for one remaining unit; exactly one succeeds, one has a stock conflict, quantity stays >=0 |
| BE-010 | Concurrent identical idempotency keys create only one order; changed owner/payload never returns another receipt |
| ML-004 | Install extension explicitly; insert known 384-dimensional vectors; query verifies cosine order, version filtering and stock exclusion |
| BE-014 | Verify TTL and inventory/model-version invalidation against actual Redis; Redis offline remains functional |
| BE-016 | Record PostgreSQL EXPLAIN with bounded pagination and measured query counts |

Fixtures must clean up only their own schema/data. Integration test infrastructure can be added with the mentor when the corresponding task starts, without implementing the task's business logic.

Security gates before deployment: HTTPS, startup secret validation, password hashing, validated JWT claims, server-derived authorization, input bounds, rate limits, safe token storage, sanitized error responses, ownership tests, transaction/concurrency tests and dependency review. The application is not production-ready.
