# python-ml publication status

All BE-001..016 implementations are supplied. Local verification: 38 backend tests
passed; 2 real PostgreSQL gates skipped without TEST_POSTGRES_URL. The frontend
TypeScript/Vite build passed. Live PostgreSQL/Redis/Docker verification is pending.

ML-001..011 and the older ranking/explanation exercises remain deferred. Serving
uses explicit model-free fallbacks, so no trained ML inference is claimed.

Redis is explicitly used for login limiting, logout token revocation, protected
route checks, recommendation cache-aside and readiness. Redis outages fail auth
closed; recommendation serving falls back to computation. Tests use Redis doubles.

No agent instructions/configuration, real secrets, dependency caches or build
artifacts are included in the branch tree. See BACKEND_FUNCTION_REFERENCE.html
for a function | code with comments table of the current backend.
