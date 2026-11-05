# Scaffold verification — 2026-11-06

## Latest delivery verification

All BE implementations were supplied at the user's request. Command:
`python -m pytest tests --ignore=tests/learning/test_ml.py -q`.
Result: **38 passed, 2 skipped**. Skips are real PostgreSQL concurrency gates
requiring `TEST_POSTGRES_URL`; Redis tests use doubles. Full SQLite migrations
preserve legacy orders across upgrade/downgrade; PostgreSQL DDL compilation passes.
Frontend `npm run build` passes. ML algorithms remain deferred. The earlier
scaffold results below are historical, not the current delivery status.

This records executed checks, not completion of learning tasks.

| Check | Observed result |
|---|---|
| Frontend `npm ci` and `npm run build` | Passed; TypeScript and Vite production bundle generated locally |
| `docker compose --env-file .env.example -f infrastructure/compose.yaml config --quiet` | Passed configuration validation only |
| Foundation pytest suite | 4 passed: health, catalogue filtering/missing slug, sequential idempotent replay, insufficient-inventory rollback |
| Combined foundation + learning pytest suite | 5 passed, 24 failed, 2 skipped; no collection errors |
| Learning failures | Unimplemented task signatures or missing prerequisites; BE-010 specifically demonstrates changed-payload replay not rejected by existing checkout |
| Optional skips | ML-006 and ML-008 because Torch is not installed |

Tests ran with Python 3.13.3. The FastAPI TestClient required execution outside the restricted sandbox; it completed there. The installed FastAPI/Starlette stack emitted an httpx TestClient deprecation warning; this did not fail the checks.

No learner algorithm was implemented to change these results. The passing BE-005 test exercises existing session infrastructure and does not mark that learning task Completed. The optional training/inference contract is collected but cannot be executed without Torch and the learner implementation.

Not verified: Docker service startup/image build, PostgreSQL connectivity/migration roundtrip/concurrency, pgvector retrieval, actual Redis integration, browser visual behavior, Python 3.11/3.12 execution or model training. Follow TESTING.md for the corresponding integration gates.
