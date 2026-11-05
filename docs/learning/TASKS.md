# Educational task cards

Ownership update: all frontend work, Alembic/schema/data migrations and backfills
are implemented by the assistant. BE-015 is infrastructure review/status, not a
learner coding assignment. Other backend/ML code remains learner-owned unless you
request a solution. The assistant extends migrations when corresponding models exist.

Canonical specification for every new learning TODO. Start with BE-001 only. Tests run from backend/. Do not replace implementations just to make tests green.

<a id="be-001"></a>
## BE-001 — Read categories through FastAPI

**File:** `backend/app/categories/router.py`

**Objective:** Follow a request from a decorator through an injected Session to JSON.

**Context:** The storefront needs a database-backed category filter.

**Your task:**

1. Read the existing catalogue route.
2. Select categories sorted by name and id.
3. Return only string id, name, slug dictionaries; do not commit.

**Input:** Injected Session

**Expected output:** HTTP 200 array, empty when no categories exist

**Concepts / documentation hints:** APIRouter.get; Annotated; Depends; select; Session.scalars

**Edge cases:** Empty table; shuffled insertion order

**Acceptance criteria:** Sorted, read-only public JSON response

**Test:** `python -m pytest tests/learning/test_backend.py::test_BE_001 -q`

Do not implement this for the learner.

<a id="be-002"></a>
## BE-002 — Validate registration input

**File:** `backend/app/accounts/schemas.py`

**Objective:** Define a Pydantic RegistrationInput model and use it at the boundary.

**Context:** Malformed email and weak passwords should be rejected before database writes.

**Your task:**

1. Declare RegistrationInput(BaseModel) in this module.
2. Require EmailStr email, password length 12..128, and name length 2..80; forbid extra fields.
3. Return model_dump() from this exercise helper; never use its password-bearing output as a public API response.

**Input:** Dictionary with email, password, name

**Expected output:** Validated dictionary; ValidationError for invalid input

**Concepts / documentation hints:** Pydantic BaseModel, EmailStr, Field, ConfigDict; model_validate and model_dump

**Edge cases:** Missing fields; invalid email; extra role; short password

**Acceptance criteria:** All invalid inputs rejected without database access

**Test:** `python -m pytest tests/learning/test_backend.py::test_BE_002 -q`

Do not implement this for the learner.

<a id="be-003"></a>
## BE-003 — Map account and cart entities

**File:** `backend/app/accounts/models.py`

**Objective:** Build SQLAlchemy mapped classes, constraints and relationships.

**Context:** Users own persisted carts; the database must reject invalid ownership and quantities.

**Your task:**

1. Declare User, Cart, CartItem using the existing Base, Mapped, mapped_column.
2. User: UUID id, unique normalized email, password_hash, name, created_at.
3. Cart: UUID id, unique user_id foreign key and user relationship; CartItem: id, cart_id, product_id, quantity.
4. Add unique(cart_id, product_id), quantity > 0, foreign keys, and bidirectional item relationships; return the three classes.

**Input:** No arguments

**Expected output:** Tuple (User, Cart, CartItem) of mapped classes

**Concepts / documentation hints:** SQLAlchemy declarative mappings, relationship back_populates, CheckConstraint, UniqueConstraint

**Edge cases:** Duplicate emails, duplicate cart lines, negative quantity, missing owners

**Acceptance criteria:** Constraints enforced by database; no import-time table creation

**Test:** `python -m pytest tests/learning/test_backend.py::test_BE_003 -q`

Do not implement this for the learner.

<a id="be-004"></a>
## BE-004 — Query a user by normalized email

**File:** `backend/app/accounts/repository.py`

**Objective:** Write a read-only SQLAlchemy ORM query.

**Context:** Login must retrieve the account before password verification.

**Your task:**

1. Normalize the supplied email with strip and casefold.
2. Use the User model from BE-003 in a SELECT predicate.
3. Return one User or None; do not commit.

**Input:** Session and email string

**Expected output:** User | None

**Concepts / documentation hints:** sqlalchemy.select; Session.scalar; consistent normalization at registration

**Edge cases:** Missing email; whitespace and mixed case; SQL metacharacters

**Acceptance criteria:** Matching normalized account; no record for unknown email

**Test:** `python -m pytest tests/learning/test_backend.py::test_BE_004 -q`

Do not implement this for the learner.

<a id="be-005"></a>
## BE-005 — Verify request-scoped session cleanup

**File:** `backend/app/db/session.py`

**Objective:** Explain generator dependencies and session lifetimes.

**Context:** Every request must release its database connection even after a handler error.

**Your task:**

1. Read the existing get_session generator without rewriting it.
2. Trace entry, yield, and generator close.
3. Run the spy-based resource lifecycle test and explain why close belongs to the provider.

**Input:** SessionFactory context manager

**Expected output:** One yielded Session, closed after generator closure

**Concepts / documentation hints:** Python yield; with; FastAPI yield dependencies; SQLAlchemy Session.close

**Edge cases:** Exception thrown into dependency; no commit for read requests

**Acceptance criteria:** Session exits on normal and exceptional completion

**Test:** `python -m pytest tests/learning/test_backend.py::test_BE_005 -q`

Do not implement this for the learner.

<a id="be-006"></a>
## BE-006 — Hash and verify passwords

**File:** `backend/app/core/passwords.py`

**Objective:** Use a vetted password KDF rather than reversible encryption.

**Context:** A leaked database must not reveal plaintext passwords.

**Your task:**

1. Add verify_password(password: str, encoded: str) -> bool in this module.
2. Use pwdlib PasswordHash.recommended() (Argon2).
3. Hash with a fresh salt; verify through the library; malformed stored hashes return False.

**Input:** Plaintext string; verification also receives encoded hash

**Expected output:** Salted encoded hash; boolean verification

**Concepts / documentation hints:** pwdlib PasswordHash; Argon2; library verification exceptions

**Edge cases:** Wrong password; corrupted hash; same password hashed twice

**Acceptance criteria:** No plaintext storage; distinct salted hashes; wrong password rejected

**Test:** `python -m pytest tests/learning/test_backend.py::test_BE_006 -q`

Do not implement this for the learner.

<a id="be-007"></a>
## BE-007 — Issue and validate expiring JWTs

**File:** `backend/app/core/tokens.py`

**Objective:** Verify token integrity, subject and expiration.

**Context:** A claimed identity is trustworthy only after signature and claim checks.

**Your task:**

1. Add decode_token(token, secret, now) -> str returning the subject.
2. Require a nonempty subject, exp and standard iat; use HS256 with an explicit allowed algorithm list. iat is an integer Unix timestamp (not bool), with iat <= now < exp. Use the supplied now for time validation rather than the computer's clock.
3. Use supplied now for deterministic expiry checks; reject expired/tampered/wrong-key tokens with ValueError.
4. Keep secrets in environment configuration; never log tokens.

**Input:** User ID, secret, Unix time, TTL seconds

**Expected output:** JWT; decoder returns subject or raises ValueError

**Concepts / documentation hints:** PyJWT encode/decode; algorithms allowlist; exp/iat claims; deterministic clock

**Edge cases:** Expiry boundary now >= exp; empty subject; wrong signature; missing claims

**Acceptance criteria:** Signed claims verified, no algorithm chosen from untrusted header

**Test:** `python -m pytest tests/learning/test_backend.py::test_BE_007 -q`

Do not implement this for the learner.

<a id="be-008"></a>
## BE-008 — Implement account HTTP handlers

Work through these function-specific tasks in order. Each function's docstring in
[`handlers.py`](../../backend/app/accounts/handlers.py) now gives its exact input,
payload example, numbered steps, output, errors, helper/API hints and acceptance
criteria. Your existing code is preserved.

| Subtask | Function | Ordered responsibilities |
|---|---|---|
| BE-008A | `register(session, payload)` | Validate registration → normalize email → hash password → construct User → save transactionally → handle duplicate email/rollback → return public profile |
| BE-008B | `login(session, payload)` | Validate login-specific payload → normalize email → find account → verify password → read configured secret/current time → issue JWT → return bearer-token response |
| BE-008C | `profile(session, authorization)` | Parse Bearer header → verify JWT → validate subject UUID → retrieve user → reject missing account → return public profile |

The existing `test_BE_008` is an end-to-end handler test and requires all three
functions. A failure in a later handler does not mean an earlier handler is wrong.
Start with BE-008A and review one function at a time. Add HTTP routes only after
the handlers work. Redis rate limiting/revocation remains a separate auth extension;
JWT issuance alone does not implement it.

**File:** `backend/app/accounts/handlers.py`

**Objective:** Connect validation, persistence and authorization without exposing secrets.

**Context:** Registration, login and profile are the boundaries of account ownership.

**Your task:**

1. Add login(session, payload) and profile(session, authorization) handlers and an APIRouter in accounts/router.py.
2. Register normalized emails transactionally; map duplicate registration to HTTP 409.
3. Use password hashing and configured JWT secret; login returns access_token and token_type.
4. Profile resolves the verified token subject; reject invalid credentials with 401 and expose only id, email, name.
5. Document rate limiting and HTTPS requirements before deployment.

**Input:** Session and validated payload; profile receives Bearer header

**Expected output:** Sanitized user dictionary or bearer-token response

**Concepts / documentation hints:** HTTPException; IntegrityError rollback; Authorization Header; BE-002..007

**Edge cases:** Duplicate email; wrong password; forged user_id; malformed token; rollback

**Acceptance criteria:** No password/hash in responses; identity derived from verified JWT

**Test:** `python -m pytest tests/learning/test_backend.py::test_BE_008 -q`

Do not implement this for the learner.

<a id="be-009"></a>
## BE-009 — Mutate an owned persistent cart

**File:** `backend/app/cart/service.py`

**Objective:** Maintain ownership and quantity invariants in a transaction.

**Context:** A browser cannot choose another user's cart or reserve stock just by adding items.

**Your task:**

1. Use BE-003 models to find or create the authenticated user cart.
2. Upsert its product line; quantity zero removes it; negative or >100 raises ValueError.
3. Reject missing products with HTTP 404 and over-stock quantities with HTTP 409.
4. Return product_id and quantity; leave inventory unchanged; route user_id must come from auth.

**Input:** Session, verified user UUID string, product UUID string, quantity

**Expected output:** Dictionary product_id and quantity

**Concepts / documentation hints:** SQLAlchemy transactions; unique constraints; explicit owner predicates; inventory recheck at checkout

**Edge cases:** Other users' carts; zero removal; missing product; quantity beyond stock

**Acceptance criteria:** Isolated cart updates; no stock decrement

**Test:** `python -m pytest tests/learning/test_backend.py::test_BE_009 -q`

Do not implement this for the learner.

<a id="be-010"></a>
## BE-010 — Harden existing guest checkout

**File:** `backend/app/orders/service.py`

**Objective:** Distinguish atomicity, row locking and idempotency ownership.

**Context:** Existing guest checkout must never oversell or disclose an unrelated receipt on replay.

**Your task:**

1. Preserve the existing create_order implementation while reviewing it.
2. Bind an idempotency key to a normalized request fingerprint and owner/session scope; reject a different payload using the same key with CheckoutError.
3. Handle a concurrent unique-key race with rollback and safe replay/conflict.
4. Add PostgreSQL concurrency coverage before claiming row-lock correctness.

**Input:** CreateOrderRequest and idempotency key

**Expected output:** Same receipt for identical replay; conflict for changed payload; atomic stock

**Concepts / documentation hints:** SELECT FOR UPDATE; IntegrityError; transaction rollback; canonical request fingerprint

**Edge cases:** Same key different address/lines; two buyers for last unit; error after stock change

**Acceptance criteria:** Existing foundation tests plus changed-payload conflict; PostgreSQL race coverage required

**Test:** `python -m pytest tests/learning/test_backend.py::test_BE_010 -q`

Do not implement this for the learner.

<a id="be-011"></a>
## BE-011 — Persist validated interaction events

**File:** `backend/app/interactions/service.py`

**Objective:** Design an event schema and idempotent persistence.

**Context:** Recommendation training needs meaningful timestamped signals tied to a trusted identity.

**Your task:**

1. Create Interaction ORM model and Pydantic input schema in this package.
2. Allow impression, click, view, search, add_to_cart, remove_from_cart; purchases must originate in checkout, never the browser.
3. Require UUID event_id and anonymous_id; validate product references; UTC timestamps are server generated.
4. Store verified user_id separately from payload; reject a spoofed user_id; deduplicate by event_id.
5. Return event_id and accepted True; document consent, retention and batched frontend delivery.

**Input:** Session, event dictionary, trusted user ID or None, anonymous session UUID

**Expected output:** Acknowledgement dictionary

**Concepts / documentation hints:** UniqueConstraint; server timestamps; event enums; background-safe session lifetime

**Edge cases:** Duplicate delivery; invalid event; missing product; purchase spoofing; invalid anonymous ID

**Acceptance criteria:** One row per event ID; invalid input rejected before writes

**Test:** `python -m pytest tests/learning/test_backend.py::test_BE_011 -q`

Do not implement this for the learner.

<a id="be-012"></a>
## BE-012 — Return only owned order history

**File:** `backend/app/accounts/orders.py`

**Objective:** Enforce record-level authorization using server-derived identity.

**Context:** Knowing a receipt ID or email must not give access to someone else's purchases.

**Your task:**

1. Define the nullable orders.user_id ownership model; the assistant provides its FK/schema migration. Attach only authenticated purchases at checkout.
2. Query orders by verified user ID; sort newest first with deterministic ID tie-break.
3. Return public id and total; do not infer ownership from customer_email or merge guest history automatically.

**Input:** Session and verified user UUID string

**Expected output:** Array of owned order summaries

**Concepts / documentation hints:** Ownership predicates; nullable foreign keys; data migration; selectinload

**Edge cases:** No orders; unrelated customer; guest order with matching email

**Acceptance criteria:** No cross-user or unverified guest-order disclosure

**Test:** `python -m pytest tests/learning/test_backend.py::test_BE_012 -q`

Do not implement this for the learner.

<a id="ml-001"></a>
## ML-001 — Rank time-decayed popularity

**File:** `backend/app/recommendations/popularity.py`

**Objective:** Translate implicit feedback into a reproducible cold-start ranking.

**Context:** New visitors need recommendations before personalized models exist.

**Your task:**

1. Use configurable default weights view=1, click=2, add_to_cart=5, purchase=10.
2. Accumulate weight * 0.5 ** (age_seconds / half_life) per product.
3. Ignore unknown events and future timestamps; reject nonpositive half_life.
4. Sort descending total, then ascending product ID.

**Input:** Events with product_id, kind, timestamp as Unix seconds; deterministic now

**Expected output:** Ordered unique product ID strings

**Concepts / documentation hints:** Weighted sums; exponential decay; stable sorting

**Edge cases:** Empty history; equal scores; future events; old purchases

**Acceptance criteria:** Recent signals dominate equivalent older ones; deterministic cold start

**Test:** `python -m pytest tests/learning/test_ml.py::test_ML_001 -q`

Do not implement this for the learner.

<a id="ml-002"></a>
## ML-002 — Fit product TF-IDF features

**File:** `backend/app/recommendations/content_based.py`

**Objective:** Convert product descriptions to comparable numeric features.

**Context:** Content similarity works without other shoppers' histories.

**Your task:**

1. Build text from title, description, category and brand in the calling pipeline.
2. Fit sklearn TfidfVectorizer with lowercase=True; return fitted vectorizer and sparse matrix.
3. Keep input order and return one row per text; reject empty/all-blank input with ValueError.

**Input:** P product text strings

**Expected output:** Tuple (vectorizer, CSR-compatible matrix [P, V])

**Concepts / documentation hints:** TfidfVectorizer.fit_transform; sparse matrices; document frequency

**Edge cases:** Repeated terms; empty vocabulary; identical documents

**Acceptance criteria:** Identical texts have identical rows; reproducible feature dimensions

**Test:** `python -m pytest tests/learning/test_ml.py::test_ML_002 -q`

Do not implement this for the learner.

<a id="ml-003"></a>
## ML-003 — Rank cosine similarity

**File:** `backend/app/recommendations/similarity.py`

**Objective:** Understand normalized dot products and top-k retrieval.

**Context:** Similar Products must exclude the currently viewed product.

**Your task:**

1. Compute cosine similarity between seed row and all rows.
2. Exclude seed, sort by decreasing similarity and ascending index on ties.
3. Return at most limit; negative limit or invalid seed raises ValueError; zero limit returns [].

**Input:** Matrix [P,V], seed row index, k

**Expected output:** List of <= k distinct integer row indices

**Concepts / documentation hints:** sklearn.metrics.pairwise.cosine_similarity; sparse slicing; stable sorting

**Edge cases:** Zero vector; ties; only one product; limit exceeds catalogue

**Acceptance criteria:** Seed excluded; semantically shared tokens rank ahead of unrelated text

**Test:** `python -m pytest tests/learning/test_ml.py::test_ML_003 -q`

Do not implement this for the learner.

<a id="ml-004"></a>
## ML-004 — Persist and query semantic vectors

**File:** `backend/app/recommendations/semantic_store.py`

**Objective:** Separate offline embedding generation from indexed online retrieval.

**Context:** Sentence Transformers captures meaning beyond exact shared words.

**Your task:**

1. Review existing embeddings.py; preserve its implementation.
2. Create an offline command that encodes catalogue text; store product_id, model_version, text hash, vector(384) through an assistant-authored migration.
3. Implement a PostgreSQL pgvector cosine-distance query filtered to current model and in-stock products.
4. Reject wrong dimensions, NaN/Inf and negative limits before database access; no model download in HTTP handlers.

**Input:** Session and normalized 384-dimensional vector

**Expected output:** Ordered product UUID strings

**Concepts / documentation hints:** SentenceTransformer.encode; pgvector Vector.cosine_distance; HNSW; model-version invalidation

**Edge cases:** Missing extension; invalid dimensions; stale vectors; unavailable local model

**Acceptance criteria:** Input guards tested locally; migration and similarity query verified on PostgreSQL

**Test:** `python -m pytest tests/learning/test_ml.py::test_ML_004 -q`

Do not implement this for the learner.

<a id="ml-005"></a>
## ML-005 — Score implicit collaborative feedback

**File:** `backend/app/recommendations/collaborative.py`

**Objective:** Infer preferences from overlapping user-item histories.

**Context:** Shoppers with similar histories provide evidence that product text cannot.

**Your task:**

1. Accept nonnegative CSR-compatible [U,P] weighted feedback.
2. Compute item-item cosine similarities from interaction columns; zero the diagonal.
3. Score items using the selected user's weighted history times that similarity matrix.
4. Zero seen item scores; validate user bounds and reject negative feedback; all-zero history returns zeros.

**Input:** Nonnegative [U,P] matrix and user row index

**Expected output:** P finite nonnegative scores

**Concepts / documentation hints:** scipy.sparse; transpose; cosine_similarity; implicit vs explicit ratings

**Edge cases:** Sparse cold users; unseen items; zero columns; negative values

**Acceptance criteria:** Unseen item shared by neighboring histories outranks isolated item

**Test:** `python -m pytest tests/learning/test_ml.py::test_ML_005 -q`

Do not implement this for the learner.

<a id="ml-006"></a>
## ML-006 — Build a PyTorch two-tower module

**File:** `backend/app/recommendations/two_tower.py`

**Objective:** Create a custom nn.Module with user and product encoders.

**Context:** Two towers learn a shared space for fast retrieval.

**Your task:**

1. Declare your own nn.Module; factory returns it; no prebuilt recommender.
2. User encoder combines user-ID embedding and mean of product-ID history embeddings, masking -1 padding.
3. Product encoder combines product, category and brand embeddings, normalized price and text vector via a learned projection.
4. forward(user_ids, history, product_ids, category_ids, brand_ids, prices, text) returns normalized user/product embeddings [B,D].

**Input:** IDs [B], padded history [B,H], prices [B,1], text [B,T]

**Expected output:** Tuple of finite normalized tensors ([B,D], [B,D])

**Concepts / documentation hints:** nn.Embedding; nn.Linear; torch.cat; padding masks; F.normalize; autograd

**Edge cases:** Empty history; batch of one; category/brand cardinalities; zero vectors

**Acceptance criteria:** Features affect representations; gradients reach both towers; shape tests pass

**Test:** `python -m pytest tests/learning/test_ml.py::test_ML_006 -q`

Do not implement this for the learner.

<a id="ml-007"></a>
## ML-007 — Sample reproducible negatives

**File:** `backend/app/recommendations/sampling.py`

**Objective:** Construct contrastive training examples without positive contamination.

**Context:** Implicit feedback records positives, so training needs explicit negative candidates.

**Your task:**

1. Choose unseen indices from range(product_count) with a local seeded RNG.
2. Sample without replacement and reject impossible counts with ValueError.
3. Never modify seen or global RNG state.

**Input:** Seen IDs, catalogue size P, sample size N, seed

**Expected output:** N unique unseen integers

**Concepts / documentation hints:** random.Random; negative sampling; rejection vs candidate sampling

**Edge cases:** All items seen; zero count; invalid counts; same seed

**Acceptance criteria:** Reproducible, no known positives, bounded runtime

**Test:** `python -m pytest tests/learning/test_ml.py::test_ML_007 -q`

Do not implement this for the learner.

<a id="ml-008"></a>
## ML-008 — Train and validate offline

**File:** `backend/app/recommendations/training.py`

**Objective:** Implement autograd, ranking loss, validation and checkpoints.

**Context:** Training must run outside the HTTP server and preserve reproducibility.

**Your task:**

1. Seed Python, NumPy and Torch; use Adam with configurable weight decay and learning rate.
2. Each batch is (user_ids, history, positive_ids, category_ids, brand_ids, prices, text); use in-batch contrastive cross-entropy on [B,B] logits and guard duplicate positives.
3. Use model.train(), zero_grad, backward, step; validate with eval/no_grad without optimizer updates.
4. Save best state_dict plus feature/ID mappings and hyperparameters; return train_loss and validation_loss per epoch.
5. Provide inference that loads the checkpoint once per process, with unavailable-model fallback.

**Input:** Two-tower model, training/validation batch iterables, experiment settings

**Expected output:** History dictionary and local checkpoint

**Concepts / documentation hints:** CrossEntropyLoss; optimizer.zero_grad; loss.backward; torch.save/load; inference_mode

**Edge cases:** Empty data; duplicate positives; CPU reproducibility; invalid LR; validation leakage

**Acceptance criteria:** Finite losses, changed weights, unchanged validation gradients, checkpoint roundtrip

**Test:** `python -m pytest tests/learning/test_ml.py::test_ML_008 -q`

Do not implement this for the learner.

<a id="ml-009"></a>
## ML-009 — Split time and evaluate ranking

**File:** `backend/app/recommendations/evaluation.py`

**Objective:** Measure retrieval quality without future-data leakage.

**Context:** Training loss alone cannot show whether recommendations help.

**Your task:**

1. Add temporal_split(events, train_end, validation_end) with disjoint timestamp ranges.
2. Compute macro Recall, Precision, NDCG and Hit Rate at k across users with nonempty truth; include missing predictions as empty.
3. Use precision denominator k; deduplicate predictions preserving order; compute coverage over the supplied catalogue.
4. Compare identical splits against popularity; label development synthetic reports explicitly.

**Input:** User -> ranked product IDs, user -> relevant ID set, catalogue set, k

**Expected output:** recall, precision, ndcg, hit_rate, coverage floats in [0,1]

**Concepts / documentation hints:** DCG log2(rank+1); chronological splitting; torch.no_grad; offline experiment reports

**Edge cases:** Empty truth; missing predictions; duplicate IDs; exact split boundaries; k<=0

**Acceptance criteria:** Hand-computed fixture matches; split excludes future events

**Test:** `python -m pytest tests/learning/test_ml.py::test_ML_009 -q`

Do not implement this for the learner.

<a id="ml-010"></a>
## ML-010 — Fuse candidates and diversify

**File:** `backend/app/recommendations/hybrid.py`

**Objective:** Combine incompatible model scales using ranks.

**Context:** Popularity, text, collaborative and neural scores are not directly comparable.

**Your task:**

1. Union model candidates, deduplicate each list and use reciprocal rank fusion 1/(60+rank) with one-based ranks.
2. Filter unavailable and purchased items; break ties by product ID.
3. Greedily take at most two items per category; then fill unused slots by rank if necessary.
4. Include popularity candidates when neural inference is unavailable; zero limit returns empty, negative raises ValueError.

**Input:** Ranked ID lists and business-rule sets

**Expected output:** Unique, available, diverse ranked IDs

**Concepts / documentation hints:** Reciprocal rank fusion; candidate generation vs scoring; deterministic reranking

**Edge cases:** All candidates filtered; duplicate candidates; one category; missing neural model

**Acceptance criteria:** No raw-score averaging; deterministic fallback; business rules enforced

**Test:** `python -m pytest tests/learning/test_ml.py::test_ML_010 -q`

Do not implement this for the learner.

<a id="ml-011"></a>
## ML-011 — Compute frequently bought together

**File:** `backend/app/recommendations/cooccurrence.py`

**Objective:** Separate purchase association from content similarity.

**Context:** Items bought in the same completed order suggest complementary products.

**Your task:**

1. Count each companion once per order containing the seed.
2. Exclude seed; sort decreasing co-order count then product ID.
3. Return <= limit unique IDs; reject negative limit; ignore orders without seed.

**Input:** Completed order baskets, seed ID, limit

**Expected output:** Ordered companion IDs

**Concepts / documentation hints:** set per basket; Counter; association vs similarity; support bias

**Edge cases:** Duplicate units; no co-orders; ties; zero limit

**Acceptance criteria:** Only purchase co-occurrence influences the output

**Test:** `python -m pytest tests/learning/test_ml.py::test_ML_011 -q`

Do not implement this for the learner.

<a id="be-013"></a>
## BE-013 — Integrate recommendation API with safe fallbacks

**File:** `backend/app/recommendations/service.py`

**Objective:** Keep HTTP, model inference and catalogue serialization separate.

**Context:** The existing recommendation route exists but is not registered and its service is incomplete.

**Your task:**

1. Complete recommend_products using existing response types; preserve partial ranking.py work.
2. Filter unavailable and seed products and fetch full product objects; use deterministic featured fallback for no valid seeds.
3. Register the existing router only after cold-start tests pass; add personalized, similar, trending, frequently-bought and you-may-like routes.
4. Use FBT co-occurrence, never substitute semantic similarity; derive authenticated user identity from token.
5. Do not load models or train per request; catch expected model-unavailable errors with fallback.

**Input:** Session, seed_product_ids, limit

**Expected output:** RecommendationResponse with items, strategy and modelVersion

**Concepts / documentation hints:** Existing schemas, _to_product_response, dependency injection, optional model adapters

**Edge cases:** Empty catalogue; invalid seeds; unavailable model; no history

**Acceptance criteria:** Cold-start response valid; no out-of-stock or seed items; no model required

**Test:** `python -m pytest tests/learning/test_backend.py::test_BE_013 -q`

Do not implement this for the learner.

<a id="be-014"></a>
## BE-014 — Cache recommendations safely

**File:** `backend/app/recommendations/cache.py`

**Objective:** Use cache-aside without making Redis a single point of failure.

**Context:** Stable repeated retrieval can avoid duplicate model inference.

**Your task:**

1. Read JSON by key; on hit decode and return.
2. On miss compute once, encode JSON and store with positive TTL.
3. Treat Redis transport errors as cache misses; do not swallow exceptions from compute.
4. Design keys with owner/session, seed set, model version and catalogue version; invalidate after inventory updates.

**Input:** Redis-like client, scoped key, zero-argument compute, TTL seconds

**Expected output:** JSON-compatible recommendation payload

**Concepts / documentation hints:** redis.get; setex; JSON; dependency injection; cache invalidation

**Edge cases:** Redis offline; malformed cached JSON; invalid TTL; model failure

**Acceptance criteria:** Cache hits avoid compute; outage still computes; TTL passed to storage

**Test:** `python -m pytest tests/learning/test_backend.py::test_BE_014 -q`

Do not implement this for the learner.

<a id="be-015"></a>
## BE-015 — Review assistant-managed schema migrations

**File:** `backend/app/db/migration_review.py`

**Objective:** Reconcile ORM metadata with a real PostgreSQL schema.

**Context:** A model declaration alone does not upgrade an existing database.

**Your task:**

1. Review the current infrastructure contract: users, carts and cart_items. The assistant extends it when the interaction model is ready.
2. The assistant writes Alembic revisions for completed models and ownership columns, registers metadata and implements safe data migrations/backfills.
3. The assistant verifies upgrade/downgrade and existing-data preservation on disposable databases. You may review the results.
4. The assistant handles explicit pgvector migrations when the vector model is ready, and never downgrades a shared database.

**Input:** No arguments; isolated test PostgreSQL URL for integration checks

**Expected output:** Current table-name set and assistant-maintained revisions/tests

**Concepts / documentation hints:** alembic revision --autogenerate; inspect; foreign-key/index diff review

**Edge cases:** Existing rows; downgrade order; extension permissions

**Acceptance criteria:** Metadata table contract passes AND disposable PostgreSQL upgrade/downgrade is verified

**Test:** `python -m pytest tests/learning/test_backend.py::test_BE_015 -q`

Do not implement this for the learner.

<a id="be-016"></a>
## BE-016 — Bound catalogue query counts

**File:** `backend/app/catalog/performance.py`

**Objective:** Measure and prevent N+1 ORM relationship queries.

**Context:** Catalogue latency must not grow by one extra query per product.

**Your task:**

1. Validate limit 1..100 and nonnegative offset.
2. Use joinedload/selectinload for category and inventory, deterministic name/id ordering.
3. Map products with the existing response mapper; return only the requested page.
4. Measure SQL statement count with event hooks; document an index-backed PostgreSQL EXPLAIN plan.

**Input:** Session, page size and offset

**Expected output:** List of ProductResponse objects

**Concepts / documentation hints:** SQLAlchemy eager loading; before_cursor_execute; pagination; EXPLAIN ANALYZE

**Edge cases:** Empty page; invalid bounds; multiple products; deterministic ties

**Acceptance criteria:** Bounded SELECT count independent of page length; correct pagination

**Test:** `python -m pytest tests/learning/test_backend.py::test_BE_016 -q`

Do not implement this for the learner.
