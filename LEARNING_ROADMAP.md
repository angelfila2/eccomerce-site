# Learning roadmap

**Current responsibility boundary:** The assistant implements all frontend code,
Alembic schema/data migrations, backfills and infrastructure verification. You write
backend business logic and ML unless you explicitly request implementation. Migration
lessons are optional explanations/reviews, not work assigned to you. This overrides
earlier wording that treated migrations as learner implementation tasks.

This is a mentored project. You write backend and ML implementations; the mentor provides contracts, fixtures and progressive hints. Do one task at a time. Existing code is preserved and requires review, not automatic replacement.

Run all commands below from `backend/` with its virtual environment active. Learning tests deliberately fail until implemented. Passing an isolated smoke test is necessary but not sufficient: finish every acceptance criterion and required PostgreSQL check before marking Completed.

## Existing foundation

Already present: catalogue/inventory/order models and migrations, catalogue handlers, guest checkout, React demo and HTTP clients, semantic embedding helper, and a partially written ranking function. None is marked Completed merely because it exists. Original files remain learner-owned.

## Architecture

```text
frontend/                         React + TypeScript + Vite demo and HTTP gateway
backend/app/catalog,inventory/    Existing models and catalogue operations
backend/app/orders/               Existing guest transaction workflow
backend/app/accounts,cart/        Learner-owned identity and persistent-cart tasks
backend/app/categories/           First learner-owned API endpoint
backend/app/interactions/         Learner-owned event persistence
backend/app/recommendations/      Learner-owned retrieval, training and ranking
backend/app/db,core/              Configuration and resource infrastructure
backend/migrations/               Assistant-owned schema/data migrations and backfills
backend/tests/learning/           Red acceptance tests
infrastructure/                   Local PostgreSQL + Redis Compose setup
docs/learning/                    Complete task cards and endpoint contracts
```

The modular structure follows this repository rather than moving your work into a new architecture. Sentence Transformers/PyTorch are optional installs. No training, model download, paid service or real payment is needed to open the frontend demo.

## 1. FastAPI fundamentals

**Objectives:** Follow a request from a decorator through an injected Session to JSON.

**Prerequisites:** Python functions, imports, dictionaries and basic HTTP.

**Files:** `backend/app/categories/router.py`.

**Tasks:** [BE-001](docs/learning/TASKS.md#be-001) — Read categories through FastAPI.

**Inputs → outputs:** BE-001: Injected Session → HTTP 200 array, empty when no categories exist.

**Common mistakes:** Empty table; shuffled insertion order.

**Tests:**
- `python -m pytest tests/learning/test_backend.py::test_BE_001 -q`

**Definition of done:** Sorted, read-only public JSON response. Review your attempt and test evidence with the mentor before advancing.

## 2. Pydantic validation

**Objectives:** Define a Pydantic RegistrationInput model and use it at the boundary.

**Prerequisites:** Milestone 1; review the task-specific concepts below.

**Files:** `backend/app/accounts/schemas.py`.

**Tasks:** [BE-002](docs/learning/TASKS.md#be-002) — Validate registration input.

**Inputs → outputs:** BE-002: Dictionary with email, password, name → Validated dictionary; ValidationError for invalid input.

**Common mistakes:** Missing fields; invalid email; extra role; short password.

**Tests:**
- `python -m pytest tests/learning/test_backend.py::test_BE_002 -q`

**Definition of done:** All invalid inputs rejected without database access. Review your attempt and test evidence with the mentor before advancing.

## 3. SQLAlchemy models and relationships

**Objectives:** Build SQLAlchemy mapped classes, constraints and relationships.

**Prerequisites:** Milestone 2; review the task-specific concepts below.

**Files:** `backend/app/accounts/models.py`.

**Tasks:** [BE-003](docs/learning/TASKS.md#be-003) — Map account and cart entities.

**Inputs → outputs:** BE-003: No arguments → Tuple (User, Cart, CartItem) of mapped classes.

**Common mistakes:** Duplicate emails, duplicate cart lines, negative quantity, missing owners.

**Tests:**
- `python -m pytest tests/learning/test_backend.py::test_BE_003 -q`

**Definition of done:** Constraints enforced by database; no import-time table creation. Review your attempt and test evidence with the mentor before advancing.

## 4. PostgreSQL CRUD operations

**Objectives:** Write a read-only SQLAlchemy ORM query.

**Prerequisites:** Milestone 3; review the task-specific concepts below.

**Files:** `backend/app/accounts/repository.py`.

**Tasks:** [BE-004](docs/learning/TASKS.md#be-004) — Query a user by normalized email.

**Inputs → outputs:** BE-004: Session and email string → User | None.

**Common mistakes:** Missing email; whitespace and mixed case; SQL metacharacters.

**Tests:**
- `python -m pytest tests/learning/test_backend.py::test_BE_004 -q`

**Definition of done:** Matching normalized account; no record for unknown email. Review your attempt and test evidence with the mentor before advancing.

## 5. Dependency injection and database sessions

**Objectives:** Explain generator dependencies and session lifetimes.

**Prerequisites:** Milestone 4; review the task-specific concepts below.

**Files:** `backend/app/db/session.py`.

**Tasks:** [BE-005](docs/learning/TASKS.md#be-005) — Verify request-scoped session cleanup.

**Inputs → outputs:** BE-005: SessionFactory context manager → One yielded Session, closed after generator closure.

**Common mistakes:** Exception thrown into dependency; no commit for read requests.

**Tests:**
- `python -m pytest tests/learning/test_backend.py::test_BE_005 -q`

**Definition of done:** Session exits on normal and exceptional completion. Review your attempt and test evidence with the mentor before advancing.

## 6. Authentication and authorization

**Objectives:** Use a vetted password KDF rather than reversible encryption. Verify token integrity, subject and expiration. Connect validation, persistence and authorization without exposing secrets.

**Prerequisites:** Milestone 5; review the task-specific concepts below.

**Files:** `backend/app/core/passwords.py`, `backend/app/core/tokens.py`, `backend/app/accounts/handlers.py`.

**Tasks:** [BE-006](docs/learning/TASKS.md#be-006) — Hash and verify passwords, [BE-007](docs/learning/TASKS.md#be-007) — Issue and validate expiring JWTs, [BE-008](docs/learning/TASKS.md#be-008) — Implement account HTTP handlers.

**Inputs → outputs:** BE-006: Plaintext string; verification also receives encoded hash → Salted encoded hash; boolean verification; BE-007: User ID, secret, Unix time, TTL seconds → JWT; decoder returns subject or raises ValueError; BE-008: Session and validated payload; profile receives Bearer header → Sanitized user dictionary or bearer-token response.

**Common mistakes:** Wrong password; corrupted hash; same password hashed twice; Expiry boundary now >= exp; empty subject; wrong signature; missing claims; Duplicate email; wrong password; forged user_id; malformed token; rollback.

**Tests:**
- `python -m pytest tests/learning/test_backend.py::test_BE_006 -q`
- `python -m pytest tests/learning/test_backend.py::test_BE_007 -q`
- `python -m pytest tests/learning/test_backend.py::test_BE_008 -q`

**Definition of done:** No plaintext storage; distinct salted hashes; wrong password rejected; Signed claims verified, no algorithm chosen from untrusted header; No password/hash in responses; identity derived from verified JWT. Review your attempt and test evidence with the mentor before advancing.

## 7. Shopping cart and checkout logic

**Objectives:** Maintain ownership and quantity invariants in a transaction. Distinguish atomicity, row locking and idempotency ownership.

**Prerequisites:** Milestone 6; review the task-specific concepts below.

**Files:** `backend/app/cart/service.py`, `backend/app/orders/service.py`.

**Tasks:** [BE-009](docs/learning/TASKS.md#be-009) — Mutate an owned persistent cart, [BE-010](docs/learning/TASKS.md#be-010) — Harden existing guest checkout.

**Inputs → outputs:** BE-009: Session, verified user UUID string, product UUID string, quantity → Dictionary product_id and quantity; BE-010: CreateOrderRequest and idempotency key → Same receipt for identical replay; conflict for changed payload; atomic stock.

**Common mistakes:** Other users' carts; zero removal; missing product; quantity beyond stock; Same key different address/lines; two buyers for last unit; error after stock change.

**Tests:**
- `python -m pytest tests/learning/test_backend.py::test_BE_009 -q`
- `python -m pytest tests/learning/test_backend.py::test_BE_010 -q`

**Definition of done:** Isolated cart updates; no stock decrement; Existing foundation tests plus changed-payload conflict; PostgreSQL race coverage required. Review your attempt and test evidence with the mentor before advancing.

## 8. User interaction tracking

**Objectives:** Design an event schema and idempotent persistence. Enforce record-level authorization using server-derived identity.

**Prerequisites:** Milestone 7; review the task-specific concepts below.

**Files:** `backend/app/interactions/service.py`, `backend/app/accounts/orders.py`.

**Tasks:** [BE-011](docs/learning/TASKS.md#be-011) — Persist validated interaction events, [BE-012](docs/learning/TASKS.md#be-012) — Return only owned order history.

**Inputs → outputs:** BE-011: Session, event dictionary, trusted user ID or None, anonymous session UUID → Acknowledgement dictionary; BE-012: Session and verified user UUID string → Array of owned order summaries.

**Common mistakes:** Duplicate delivery; invalid event; missing product; purchase spoofing; invalid anonymous ID; No orders; unrelated customer; guest order with matching email.

**Tests:**
- `python -m pytest tests/learning/test_backend.py::test_BE_011 -q`
- `python -m pytest tests/learning/test_backend.py::test_BE_012 -q`

**Definition of done:** One row per event ID; invalid input rejected before writes; No cross-user or unverified guest-order disclosure. Review your attempt and test evidence with the mentor before advancing.

## 9. Content-based recommendations

**Objectives:** Translate implicit feedback into a reproducible cold-start ranking. Convert product descriptions to comparable numeric features. Understand normalized dot products and top-k retrieval. Separate offline embedding generation from indexed online retrieval.

**Prerequisites:** Milestone 8; review the task-specific concepts below.

**Files:** `backend/app/recommendations/popularity.py`, `backend/app/recommendations/content_based.py`, `backend/app/recommendations/similarity.py`, `backend/app/recommendations/semantic_store.py`.

**Tasks:** [ML-001](docs/learning/TASKS.md#ml-001) — Rank time-decayed popularity, [ML-002](docs/learning/TASKS.md#ml-002) — Fit product TF-IDF features, [ML-003](docs/learning/TASKS.md#ml-003) — Rank cosine similarity, [ML-004](docs/learning/TASKS.md#ml-004) — Persist and query semantic vectors.

**Inputs → outputs:** ML-001: Events with product_id, kind, timestamp as Unix seconds; deterministic now → Ordered unique product ID strings; ML-002: P product text strings → Tuple (vectorizer, CSR-compatible matrix [P, V]); ML-003: Matrix [P,V], seed row index, k → List of <= k distinct integer row indices; ML-004: Session and normalized 384-dimensional vector → Ordered product UUID strings.

**Common mistakes:** Empty history; equal scores; future events; old purchases; Repeated terms; empty vocabulary; identical documents; Zero vector; ties; only one product; limit exceeds catalogue; Missing extension; invalid dimensions; stale vectors; unavailable local model.

**Tests:**
- `python -m pytest tests/learning/test_ml.py::test_ML_001 -q`
- `python -m pytest tests/learning/test_ml.py::test_ML_002 -q`
- `python -m pytest tests/learning/test_ml.py::test_ML_003 -q`
- `python -m pytest tests/learning/test_ml.py::test_ML_004 -q`

**Definition of done:** Recent signals dominate equivalent older ones; deterministic cold start; Identical texts have identical rows; reproducible feature dimensions; Seed excluded; semantically shared tokens rank ahead of unrelated text; Input guards tested locally; migration and similarity query verified on PostgreSQL. Review your attempt and test evidence with the mentor before advancing.

## 10. Collaborative filtering

**Objectives:** Infer preferences from overlapping user-item histories.

**Prerequisites:** Milestone 9; review the task-specific concepts below.

**Files:** `backend/app/recommendations/collaborative.py`.

**Tasks:** [ML-005](docs/learning/TASKS.md#ml-005) — Score implicit collaborative feedback.

**Inputs → outputs:** ML-005: Nonnegative [U,P] matrix and user row index → P finite nonnegative scores.

**Common mistakes:** Sparse cold users; unseen items; zero columns; negative values.

**Tests:**
- `python -m pytest tests/learning/test_ml.py::test_ML_005 -q`

**Definition of done:** Unseen item shared by neighboring histories outranks isolated item. Review your attempt and test evidence with the mentor before advancing.

## 11. PyTorch neural recommendation systems

**Objectives:** Create a custom nn.Module with user and product encoders. Construct contrastive training examples without positive contamination. Implement autograd, ranking loss, validation and checkpoints. Measure retrieval quality without future-data leakage.

**Prerequisites:** Milestone 10; review the task-specific concepts below.

**Files:** `backend/app/recommendations/two_tower.py`, `backend/app/recommendations/sampling.py`, `backend/app/recommendations/training.py`, `backend/app/recommendations/evaluation.py`.

**Tasks:** [ML-006](docs/learning/TASKS.md#ml-006) — Build a PyTorch two-tower module, [ML-007](docs/learning/TASKS.md#ml-007) — Sample reproducible negatives, [ML-008](docs/learning/TASKS.md#ml-008) — Train and validate offline, [ML-009](docs/learning/TASKS.md#ml-009) — Split time and evaluate ranking.

**Inputs → outputs:** ML-006: IDs [B], padded history [B,H], prices [B,1], text [B,T] → Tuple of finite normalized tensors ([B,D], [B,D]); ML-007: Seen IDs, catalogue size P, sample size N, seed → N unique unseen integers; ML-008: Two-tower model, training/validation batch iterables, experiment settings → History dictionary and local checkpoint; ML-009: User -> ranked product IDs, user -> relevant ID set, catalogue set, k → recall, precision, ndcg, hit_rate, coverage floats in [0,1].

**Common mistakes:** Empty history; batch of one; category/brand cardinalities; zero vectors; All items seen; zero count; invalid counts; same seed; Empty data; duplicate positives; CPU reproducibility; invalid LR; validation leakage; Empty truth; missing predictions; duplicate IDs; exact split boundaries; k<=0.

**Tests:**
- `python -m pytest tests/learning/test_ml.py::test_ML_006 -q`
- `python -m pytest tests/learning/test_ml.py::test_ML_007 -q`
- `python -m pytest tests/learning/test_ml.py::test_ML_008 -q`
- `python -m pytest tests/learning/test_ml.py::test_ML_009 -q`

**Definition of done:** Features affect representations; gradients reach both towers; shape tests pass; Reproducible, no known positives, bounded runtime; Finite losses, changed weights, unchanged validation gradients, checkpoint roundtrip; Hand-computed fixture matches; split excludes future events. Review your attempt and test evidence with the mentor before advancing.

## 12. Hybrid recommendation ranking

**Objectives:** Combine incompatible model scales using ranks. Separate purchase association from content similarity. Keep HTTP, model inference and catalogue serialization separate.

**Prerequisites:** Milestone 11; review the task-specific concepts below.

**Files:** `backend/app/recommendations/hybrid.py`, `backend/app/recommendations/cooccurrence.py`, `backend/app/recommendations/service.py`.

**Tasks:** [ML-010](docs/learning/TASKS.md#ml-010) — Fuse candidates and diversify, [ML-011](docs/learning/TASKS.md#ml-011) — Compute frequently bought together, [BE-013](docs/learning/TASKS.md#be-013) — Integrate recommendation API with safe fallbacks.

**Inputs → outputs:** ML-010: Ranked ID lists and business-rule sets → Unique, available, diverse ranked IDs; ML-011: Completed order baskets, seed ID, limit → Ordered companion IDs; BE-013: Session, seed_product_ids, limit → RecommendationResponse with items, strategy and modelVersion.

**Common mistakes:** All candidates filtered; duplicate candidates; one category; missing neural model; Duplicate units; no co-orders; ties; zero limit; Empty catalogue; invalid seeds; unavailable model; no history.

**Tests:**
- `python -m pytest tests/learning/test_ml.py::test_ML_010 -q`
- `python -m pytest tests/learning/test_ml.py::test_ML_011 -q`
- `python -m pytest tests/learning/test_backend.py::test_BE_013 -q`

**Definition of done:** No raw-score averaging; deterministic fallback; business rules enforced; Only purchase co-occurrence influences the output; Cold-start response valid; no out-of-stock or seed items; no model required. Review your attempt and test evidence with the mentor before advancing.

## 13. Redis caching and background processing

**Objectives:** Use cache-aside without making Redis a single point of failure.

**Prerequisites:** Milestone 12; review the task-specific concepts below.

**Files:** `backend/app/recommendations/cache.py`.

**Tasks:** [BE-014](docs/learning/TASKS.md#be-014) — Cache recommendations safely.

**Inputs → outputs:** BE-014: Redis-like client, scoped key, zero-argument compute, TTL seconds → JSON-compatible recommendation payload.

**Common mistakes:** Redis offline; malformed cached JSON; invalid TTL; model failure.

**Tests:**
- `python -m pytest tests/learning/test_backend.py::test_BE_014 -q`

**Definition of done:** Cache hits avoid compute; outage still computes; TTL passed to storage. Review your attempt and test evidence with the mentor before advancing.

## 14. Automated testing and performance optimization

**Objectives:** Reconcile ORM metadata with a real PostgreSQL schema. Measure and prevent N+1 ORM relationship queries.

**Prerequisites:** Milestone 13; review the task-specific concepts below.

**Files:** `backend/app/db/migration_review.py`, `backend/app/catalog/performance.py`.

**Tasks:** [BE-015](docs/learning/TASKS.md#be-015) — Review assistant-managed schema migrations, [BE-016](docs/learning/TASKS.md#be-016) — Bound catalogue query counts.

**Inputs → outputs:** BE-015: No arguments; isolated test PostgreSQL URL for integration checks → Current table-name set and assistant-maintained revisions/tests; BE-016: Session, page size and offset → List of ProductResponse objects.

**Common mistakes:** Existing rows; downgrade order; extension permissions; Empty page; invalid bounds; multiple products; deterministic ties.

**Tests:**
- `python -m pytest tests/learning/test_backend.py::test_BE_015 -q`
- `python -m pytest tests/learning/test_backend.py::test_BE_016 -q`

**Definition of done:** Metadata table contract passes AND disposable PostgreSQL upgrade/downgrade is verified; Bounded SELECT count independent of page length; correct pagination. Review your attempt and test evidence with the mentor before advancing.
