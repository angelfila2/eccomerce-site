# Backend learning guide

The assistant owns frontend work, Alembic schema/data migrations, backfills and
development infrastructure. You do not have to implement migrations to advance a
backend task; their verification remains the assistant's responsibility. Backend
business logic and ML remain guided exercises unless you request complete code.

Work on **BE-001 only** to begin. The roadmap describes the destination; it is not a request to implement every milestone now. Open the [task cards](docs/learning/TASKS.md) when a task becomes active.

## How we will work

1. Read one short lesson and the existing code it refers to.
2. Read its test before writing the implementation.
3. Write your attempt and run that task's exact command from `backend/`.
4. Share the attempt and failure output for review.
5. We distinguish bugs, recommended improvements and optional optimizations.
6. Mark Completed only after the acceptance criteria, required integration checks and review pass. A scaffold or a green smoke test alone is insufficient.

Hints progress from concept → relevant API → pseudocode → a small focused example. A complete implementation is provided only if you explicitly request it. Your existing implementations will not be rewritten without permission.

## 1. A FastAPI route — BE-001

**What is it?** A Python function associated with an HTTP method and URL. `@router.get("")` is a decorator: it registers the function on a router.

**Why do we need it?** Category filters should come from the catalogue database rather than another hardcoded frontend list.

**How does it work?** The test mounts your category router at `/api/v1`. FastAPI resolves `Depends(get_session)`, passes the yielded Session to `list_categories`, then serializes its returned dictionaries to JSON. An ORM object is not automatically the public API contract.

**What will I implement?** Only the body of `list_categories` in `backend/app/categories/router.py`. Query Category, order by name then id, and return dictionaries with `id`, `name`, `slug`; convert each UUID to a string. An empty table returns `[]`. Do not commit this read.

**What should I research?** Compare `backend/app/catalog/router.py` with `backend/app/catalog/service.py`. Look up [`Depends`](https://fastapi.tiangolo.com/tutorial/dependencies/), [`select()` and `Session.scalars()`](https://docs.sqlalchemy.org/en/21/orm/session_basics.html). A statement describes a query; executing it retrieves rows.

**How will I know it works?** Run `python -m pytest tests/learning/test_backend.py::test_BE_001 -q`. The test mounts the router itself and injects an isolated database. You do not need Docker, credentials, a migration, or production router registration for this first exercise.

Conceptual hint: think of three steps—describe the rows, retrieve them, shape the public response. Write your attempt before requesting a syntax hint.

## 2. Validation — BE-002

**What?** Pydantic converts untrusted input to a declared schema or reports a validation error.

**Why?** Reject malformed registration data before performing a database write.

**How?** `BaseModel`, `EmailStr`, `Field` and `ConfigDict(extra="forbid")` express the contract; `model_validate` applies it. Validation does not hash passwords or authorize a user.

**Implement:** A RegistrationInput class and the small exercise helper in `accounts/schemas.py`. Keep the helper's password-bearing dictionary internal. Public responses must use a separate safe schema.

**Research:** Pydantic model configuration, length bounds, required fields and `ValidationError`.

**Verify:** BE-002 tests valid input, missing fields, short names/passwords, invalid email and an injected role field. See its task card for the exact command.

## 3. ORM models and database constraints — BE-003

**What?** A mapped Python class describes a table; relationships connect Python objects across foreign keys.

**Why?** A user owns a cart, and each cart contains unique product lines.

**How?** `Mapped[T]` describes a mapped attribute, `mapped_column` defines its SQL storage, and `relationship` defines ORM navigation. A Python check alone cannot prevent two concurrent inserts; unique and check constraints belong in the database.

**Implement:** User, Cart and CartItem declarations in `accounts/models.py`. The factory signature is a test seam returning the three classes, not a requirement to create new classes per call. Do not create tables during application imports. Existing Category/Product/Inventory models are examples, not files to replace.

**Research:** Declarative mappings, UUID defaults, foreign keys, `back_populates`, cascades, unique/check constraints and timezone-aware timestamps.

**Verify:** BE-003 checks ownership navigation, duplicate accounts/lines and invalid quantities. Add separate assertions for invalid foreign keys and negative quantities so one constraint cannot hide another. Verify migration DDL later on PostgreSQL.

## 4. CRUD and repositories — BE-004

**What?** A repository query retrieves persistence objects without handling HTTP concerns.

**Why?** Login needs an account lookup; it should not duplicate email normalization and query construction.

**How?** Build a SQLAlchemy expression rather than interpolating strings into SQL. `Session.scalar` returns one entity or None. Consistent normalization at both registration and lookup is essential.

**Implement:** A read-only email lookup in `accounts/repository.py`.

**Research:** `select`, `where`, bound parameters, `.scalar()` versus `.scalars()`, normalization and indexes.

**Verify:** BE-004 checks existing/missing accounts, mixed case/whitespace and SQL-like input. Do not use commit to complete a read.

## 5. Dependency injection and session lifetimes — BE-005

**What?** A dependency supplies a resource to a handler. A Session tracks database work; it is not a globally shared connection.

**Why?** Connections must return to the pool after every request, including failures.

**How?** The existing `get_session` uses `with SessionFactory()` and `yield`. Execution pauses at yield while the handler uses the Session, then exits the context. A service owns the transaction; the dependency owns cleanup. A query can start an implicit transaction, so avoid nesting `session.begin()` around an already active transaction accidentally.

**Implement:** Review and explain the existing provider before changing anything. Do not rewrite working infrastructure for an exercise.

**Research:** [FastAPI dependencies with yield](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/), generator close/throw, Session autobegin and rollback.

**Verify:** BE-005 uses a context-manager spy and exercises both normal and exceptional exit. Passing it does not by itself demonstrate your understanding; explain the lifecycle during review.

## 6. Authentication and authorization — BE-006..008

**What?** Authentication establishes identity; authorization decides what that identity may access.

**Why?** Cart and profile APIs must never trust a client-supplied user ID. Existing guest checkout is not account authentication.

**How?** A password KDF uses a unique salt and deliberately expensive computation. A JWT signs claims, including subject and expiry; its signature, allowed algorithm and claims must be verified before use. JWT contents are readable, so keep secrets and personal data out of tokens. The exercise chooses short-lived bearer JWTs; production refresh, revocation and storage design remain explicit follow-up decisions.

**Implement:** First password hashing/verification, then deterministic token issuance/validation, then handlers and route wiring. Store only encoded password hashes. Registration must handle uniqueness races and roll back on failure. Return generic invalid-credential errors. Separate public profile fields from storage models.

**Research:** pwdlib/Argon2; PyJWT claims and algorithm allowlists; HTTP 401/409; `IntegrityError`; FastAPI headers/dependencies. Extend settings for environment-based secrets without a development fallback that can silently reach production.

**Verify:** BE-006..008 test salted hashing, bad passwords/hashes, expiry boundaries, wrong signatures, missing claims, duplicate registration and forged tokens. Add HTTP route tests after wiring. Before deployment add HTTPS, secret validation, login throttling, safe token storage, revocation/refresh policy and operational review. This scaffold is **not production-ready**.

## 7. Carts, atomic checkout and idempotency — BE-009..010

**What?** A transaction makes a group of database writes succeed or fail together. Idempotency makes a retry behave like the original request.

**Why?** Creating an order without decrementing inventory—or decrementing without an order—loses consistency. Reusing someone else's idempotency key must not reveal their receipt.

**How?** The existing service locks inventory rows in deterministic order and computes prices from the database. Row locking requires PostgreSQL. A unique key alone does not prove that a replay has the same owner or payload; a fingerprint and scoped ownership are separate invariants.

**Implement:** Owned cart upserts/removals, then review and harden existing checkout. Do not reserve stock when adding to a cart; recheck during checkout. Keep simulated purchases; no payment provider is part of this project.

**Research:** `Session.begin`, `SELECT FOR UPDATE`, lock ordering, unique-key races, rollback, Decimal money and canonical fingerprints.

**Verify:** Foundation tests cover sequential replay and rollback. BE-009 checks cart separation; BE-010 deliberately fails for the existing changed-payload replay behavior. PostgreSQL concurrency tests must prove that two buyers cannot purchase the last unit. SQLite tests cannot establish this.

## 8. Events and order ownership — BE-011..012

**What?** An interaction is a timestamped signal about a product or search. Event delivery is often retried.

**Why?** Models need attributable, consistent training data. A duplicate click must not double its training weight.

**How?** Unique event IDs support deduplication. Use a server timestamp, a verified optional user ID and a bounded anonymous session identifier. Client events are weak evidence: only committed checkout can create a purchase signal. Profile/order access uses owner foreign keys, never an email supplied by a browser.

**Implement:** Model, Pydantic event schema and persistence; then order ownership behavior and a filtered history query. The assistant handles the ownership-column schema/data migration. Do not automatically attach guest orders based solely on matching email. A frontend batch should deliver events without blocking navigation; its server work must use a fresh scoped Session if deferred beyond the request.

**Research:** Unique constraints, idempotent writes, UTC, event enums, pagination, data minimization, consent and retention.

**Verify:** BE-011 checks duplicate delivery, spoofing and invalid kinds; BE-012 ensures matching-email guest and other-user orders stay private. Add missing-product, search-without-product and retention tests during the task review.

## 9. Integrating inference — BE-013

**What?** An orchestration service chooses candidates, filters them and serializes product objects.

**Why?** The storefront should work when neural artifacts are absent and should never advertise unavailable products.

**How?** Keep offline training separate from request handling. Reuse an already loaded model or use a documented fallback. Existing ranking code is partially written; preserve your work when finishing it. Frequently Bought Together uses order co-occurrence, not text similarity.

**Implement:** Existing recommendation service and related ranking/explanation functions; then register routes in `api/router.py`. See [API contracts](docs/learning/API_CONTRACTS.md). Authentication-required endpoints must derive identity from verified credentials.

**Research:** Existing response schemas, eager loading, exception boundaries and candidate business rules.

**Verify:** BE-013 starts with model-free cold-start, seed exclusion and stock filtering. Add personalized, missing-model, co-occurrence and HTTP contract tests before replacing frontend mocks.

## 10. Cache and background processing — BE-014

**What?** Cache-aside stores an expensive computed result temporarily. An offline job updates model artifacts separately.

**Why?** Repeated inference should be cheap; Redis failure must not break browsing.

**How?** Read the scoped key, compute on miss, write JSON with an expiry. Treat Redis transport/decode problems separately from genuine model/database errors. A stale cache must not bypass a current inventory filter. Never share a personalized key between owners.

**Implement:** The cache helper and invalidation policy. Add a separate explicit training command only after training works; schedule it outside HTTP requests.

**Research:** Redis `get`/`setex`, TTL, cache invalidation, model/catalogue versions, process lifecycle and durable job queues only when needed.

**Verify:** BE-014 checks hits, misses, TTL and outages; add stale-stock and user-key isolation tests before enabling caching in the route.

## 11. Testing, migrations and performance — BE-015..016

**What?** Unit tests check isolated behavior; integration tests check the actual database; migrations version schema changes.

**Why?** A green unit suite cannot prove PostgreSQL lock behavior, extension installation or successful upgrades.

**How?** Each unit test gets a new in-memory SQLite database with foreign keys enabled. Tests override session dependencies rather than using `APP_DATABASE_URL`. Future model imports are inside tests so unfinished modules do not prevent collection. Use disposable PostgreSQL schemas for integration checks and never reset a shared development database. Eager loading avoids fetching category/inventory once per product.

**Implement:** Your task is the efficiently paginated catalogue query. The assistant implements and verifies Alembic schema/data migrations for completed models. You can review migrations to understand them without having to author them. Models and migrations must agree.

**Research:** Alembic upgrade/downgrade, metadata imports, SQLAlchemy event listeners, `selectinload`/`joinedload`, PostgreSQL EXPLAIN, meaningful indexes and transaction isolation.

**Verify:** BE-015 checks the table contract; disposable PostgreSQL migration roundtrips remain mandatory. BE-016 counts SELECT statements after expunging cached ORM objects so an N+1 query cannot hide in the identity map. Retain foundation regression coverage throughout the course.
