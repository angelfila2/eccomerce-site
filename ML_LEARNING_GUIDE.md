# Machine learning learning guide

Do not start these tasks until you are ready for their milestone. All fixtures are tiny synthetic development examples. Passing them demonstrates correctness of a contract, not useful real-world recommendation quality.

## Data path and notation

Browser signals → validated PostgreSQL interactions → time-bounded offline export → training-only feature/ID mappings → model artifact → inference candidates → hybrid business rules → product objects. Purchases come from committed orders. Synthetic data, artifacts and reports must be labeled as such; no real-world performance is claimed.

`U` = users, `P` = products, `V` = vocabulary size, `B` = batch size, `H` = history length, `D` = learned embedding dimension, `T` = description-vector dimension. A tensor shape lists the size of each axis; `[B,D]` means one D-dimensional vector per example.

## Popularity — ML-001

**What?** A weighted count of recent product interactions.

**Why?** New visitors and model failures need a deterministic baseline.

**How?** Each event contributes `weight × 0.5^(age/half_life)`. An event one half-life old contributes half as much. Start with view=1, click=2, cart=5, purchase=10; these are configurable hypotheses, not optimized weights.

**Implement:** Accumulate scores per product, ignore future/unknown events and sort deterministically. Filtering current stock belongs in serving.

**Research:** Exponential decay, weighted counts, stable tie-breaking and popularity bias.

**Verify:** ML-001 compares identical signals at different times, empty data and invalid half-life. Add a hand-calculated purchase-versus-view example during review.

## TF-IDF — ML-002

**What?** A sparse description of words that distinguish a product from the catalogue.

**Why?** A lamp can be recommended near another reading lamp before any user has purchased either.

**How?** Term frequency represents occurrences within a document; inverse document frequency reduces the influence of words appearing almost everywhere. `fit_transform` returns `[P,V]`. Sparse storage keeps zero entries implicit. Preserve the row-to-product mapping.

**Implement:** A fitted vectorizer and product matrix. Decide explicitly how title, description, category and brand form the text. Do not fit a different vocabulary for every query.

**Research:** [Scikit-learn text feature extraction](https://scikit-learn.org/stable/modules/feature_extraction.html), tokenization, lowercase handling, empty vocabulary and sparse matrix APIs.

**Verify:** ML-002 expects identical rows for identical documents and no overlap for disjoint words. Blank catalogues raise a documented error that the orchestrator can turn into a fallback.

## Cosine similarity — ML-003

**What?** The normalized dot product: similarity measures vector direction rather than raw length.

**Why?** Longer descriptions should not automatically be more similar to every product.

**How?** Compare one seed row `[1,V]` with the product matrix `[P,V]`; the result has P scores. Remove the seed before top-k selection. A zero vector needs defined behavior.

**Implement:** Sorted neighbor row indices, excluding the seed, with deterministic ties and explicit bounds validation.

**Research:** [Scikit-learn pairwise metrics](https://sklearn.org/stable/modules/metrics.html), cosine similarity, sparse slicing and ranking versus regression.

**Verify:** ML-003 uses vectors with an obvious nearest neighbor. Add tie and zero-vector cases during review.

## Semantic embeddings and pgvector — ML-004

**What?** A local language model encodes product meaning into dense vectors. pgvector stores/query-indexes those vectors in PostgreSQL.

**Why?** Semantically related products may use different words.

**How?** The existing MiniLM helper encodes P descriptions as `[P,384]`. Compute offline, store a model version and text hash, and query current vectors by cosine distance. Model downloads require network access once; inference can then use a local cache. Keep download/training out of requests.

**Implement:** The vector model, encoding logic and `nearest_vectors` query. The assistant handles the vector-table/extension migrations, backfills and command scaffolding. Do not replace the existing completed embedding helper.

**Research:** `SentenceTransformer.encode`, normalized embeddings, pgvector dimensions/cosine operators/HNSW, model version invalidation and local model paths.

**Verify:** ML-004 checks invalid shape and non-finite inputs without downloading anything. Valid ranking and extension/index DDL require a disposable PostgreSQL integration test; the local guard test alone cannot complete this task.

## Collaborative filtering — ML-005

**What?** Recommendations from relationships between users' interaction histories.

**Why?** Similar descriptions miss behavioral connections, such as a shopper buying a lamp and organizer together.

**How?** Build a nonnegative sparse matrix `[U,P]` of weighted signals. Item columns describe who interacted with each item. Item-to-item cosine produces `[P,P]`; multiply a user row by it to obtain `[1,P]` scores. Zero seen scores. Item-based collaborative filtering is a practical initial implicit-feedback algorithm; factorization can follow once the baseline works.

**Implement:** Validate the matrix, calculate item similarities and score one user's unseen items. The deliberately small fixture can be dense; a large catalogue needs bounded neighbor retrieval rather than a full dense P-by-P matrix.

**Research:** CSR matrices, transposes, implicit feedback confidence, sparsity, cold users and item-neighborhood models.

**Verify:** ML-005 expects an unseen item sharing a neighbor to outrank an isolated item. No-history users return zeros so the serving layer can use popularity.

## Two-tower forward propagation — ML-006

**What?** Two trainable encoders map a user and a product into the same D-dimensional space.

**Why?** Retrieval becomes a vector comparison while representations can learn from both behavior and catalogue features.

**How?** `nn.Embedding` maps integer IDs to learned rows. The user encoder combines an ID vector and masked mean history vector. The product encoder combines product/category/brand embeddings, normalized price and text features, then projects to D. Normalize each tower output. A similarity score is their dot product. Learn feature scalers and ID mappings on training data only; reserve an unknown-ID policy for inference.

**Implement:** Your own `nn.Module`, not a prebuilt recommender. Inputs: IDs `[B]`, history `[B,H]` with -1 padding, price `[B,1]`, text `[B,T]`. Outputs: user `[B,D]`, product `[B,D]`. Mask padding before mean pooling; never pass -1 to an embedding lookup.

**Research:** `nn.Module`, `nn.Embedding`, `nn.Linear`, `torch.cat`, broadcasting, padding masks, normalization and autograd. Start with the [official PyTorch tutorials](https://docs.pytorch.org/tutorials/).

**Verify:** ML-006 checks a two-example batch including an empty history, finite normalized vectors and gradient flow. Add individual feature-sensitivity and per-tower gradient assertions before completion.

## Negative sampling — ML-007

**What?** Sampling products without observed positive feedback as contrastive alternatives.

**Why?** Implicit logs rarely contain explicit dislikes.

**How?** Choose from the unseen candidate set using a local seeded RNG. Unobserved does not mean disliked; sampling is an approximation. A fully seen catalogue must terminate with a clear error rather than loop forever.

**Implement:** N unique unseen indices from P products, without changing the caller's set or global randomness.

**Research:** `random.Random`, sampling without replacement, false negatives and popularity-aware sampling as a later extension.

**Verify:** ML-007 checks reproducibility, uniqueness, exclusion, unchanged state and impossible requests.

## Training, validation and inference — ML-008

**What?** Training adjusts parameters; validation measures held-out behavior without changing them; inference only scores candidates.

**Why?** Random initial embeddings do not encode useful preferences.

**How?** A batch of user/product embeddings yields logits `[B,B]`; the matching pair lies on its diagonal. Contrastive cross-entropy rewards those pairs. Duplicate positive products need masking or deduplication so one positive is not incorrectly labeled a negative. Use `train`, zero gradients, forward, loss, backward and optimizer step. Validation uses `eval` and `no_grad`; save the best state and its feature/ID metadata.

**Implement:** A reproducible CPU training/validation loop with configurable settings and checkpoints. Use ML-007 samples in a later explicit-negative extension; do not confuse that sampler with in-batch contrastive negatives. Add a separate inference loader and offline command, never a training HTTP endpoint.

**Research:** Adam, learning rate, weight decay, CrossEntropyLoss, seeds, temperature, `state_dict`, `torch.save`, safe local checkpoint loading and experiment configs.

**Verify:** ML-008 checks finite histories, parameter updates and checkpoint presence. Before completion, add repeat-run reproducibility, checkpoint score roundtrip, validation-no-update and invalid-config tests. Loading a file alone is insufficient evidence.

## Time splits and ranking evaluation — ML-009

**What?** Offline ranking metrics compare recommendations against future held-out positives.

**Why?** A low training loss can coexist with poor retrieval or data leakage.

**How?** Train timestamps are `< train_end`; validation is `[train_end, validation_end)`; test is `>= validation_end`. Fit vocabularies, scalers, mappings and co-occurrence statistics on training data only. Construct each user's history using only events available at the evaluated instant.

Recall@k is retrieved relevant items / relevant items. Precision@k uses denominator k. Hit Rate@k is whether at least one relevant item was retrieved. NDCG@k discounts a hit at rank r by `1/log2(r+1)` and divides by the ideal ranking's DCG. Coverage is unique recommended catalogue IDs / catalogue size. Average user metrics across users with nonempty truth, counting missing predictions as empty.

**Implement:** The split function and metric report, comparing identical splits/candidate rules against popularity. Label synthetic development data; save real experiments locally with data cutoff, configuration and model version.

**Research:** Chronological evaluation, leakage, negative candidate bias, cold-start cohorts, precision denominators and duplicate predictions.

**Verify:** ML-009 uses a hand-computable two-user ranking and exact split boundaries. Add duplicate predictions, empty catalogue, cold users and invalid split bounds before completion.

## Hybrid ranking — ML-010

**What?** Candidate generation from multiple models followed by a common ranking and business rules.

**Why?** A raw neural logit and a popularity count have incompatible scales.

**How?** Reciprocal rank fusion sums `1/(60+rank)` for each candidate, where rank starts at 1. Filter stock and purchased items, break ties deterministically and encourage category variety. If a model is unavailable, continue with available candidates, including popularity.

**Implement:** Fusion, filtering and a two-per-category first pass, followed by ranked fill if diversity leaves slots. Preserve existing session ranking work; compare its earlier weighted scheme with fusion during review rather than silently deleting it.

**Research:** Candidate recall versus final ranking quality, RRF, score calibration, diversity and repeat-purchase policy.

**Verify:** ML-010 checks deterministic ties, duplicate candidates, stock/purchase exclusions, diversity and empty sources.

## Frequently Bought Together — ML-011

**What?** Association based on products sharing completed order baskets.

**Why?** Complementary products need not resemble one another in wording or embeddings.

**How?** Deduplicate units within each basket, count companions only in orders containing the seed, then rank by count. Later evaluate minimum support, confidence or lift to reduce popularity bias.

**Implement:** Pure order co-occurrence, excluding the seed. Serving separately checks current availability.

**Research:** Basket support, association versus semantic similarity and co-occurrence leakage across the time cutoff.

**Verify:** ML-011 includes duplicate units, missing seeds and no co-orders. Content similarity must not influence the result.

## Commands and optional dependencies

From `backend/`, install the optional packages only when needed: `python -m pip install -r requirements-ml.txt` or `uv sync --dev --extra ml`. Run one task's command from the roadmap. `python -m pytest tests/learning/test_ml.py -q` runs all ML contracts, which are deliberately red until implemented. Torch tests skip if Torch is absent; a skip never counts as task completion. No model downloads occur in the acceptance tests.
