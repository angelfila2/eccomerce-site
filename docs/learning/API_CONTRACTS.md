# API contracts and staged integration

All paths use `/api/v1` to preserve the existing frontend client. The earlier `/api` examples describe the same groups, not a request to break this repository's versioned contract.

| Path | Status now | Owner / expected contract |
|---|---|---|
| GET `/health` | Existing | `{status, environment}` |
| GET `/products` | Existing | Product array; category/search/limit/offset; defaults to 10 rows |
| GET `/products/{slug}` | Existing | Product object or 404 |
| POST `/orders` | Existing guest workflow | Checkout + lines; required Idempotency-Key; receipt; BE-010 hardening pending |
| GET `/categories` | BE-001 standalone router, not registered in main | Array of `{id, name, slug}`, alphabetic |
| POST `/auth/register` | Learner BE-008 | `{email, name, password}` → `{id, email, name}`; 409 duplicate |
| POST `/auth/login` | Learner BE-008 | `{email, password}` → `{access_token, token_type: "bearer"}`; 401 invalid |
| GET/PATCH `/users/me` | Learner BE-008 extension | Verified identity → safe public profile; validate mutable fields |
| GET `/cart` | Learner BE-009 route extension | Only authenticated owner's product lines |
| PUT `/cart/items/{product_id}` | Learner BE-009 | `{quantity}`; zero removes; stock unchanged |
| DELETE `/cart/items/{product_id}` | Learner BE-009 extension | Owned line removal; idempotent empty result |
| GET `/orders` | Learner BE-012 | Owned summaries; never use supplied customer email as identity |
| POST `/interactions` | Learner BE-011 | `{event_id, kind, product_id?, query?}` + session header → `{event_id, accepted}` |
| GET `/recommendations` | Existing router/service scaffold; not registered | Existing RecommendationResponse; query seed_product_ids, limit |
| GET `/recommendations/personalized` | Learner BE-013 | Trusted identity/history or cold-start fallback |
| GET `/recommendations/similar/{product_id}` | Learner BE-013 | Content/semantic candidates, seed excluded |
| GET `/recommendations/trending` | Learner BE-013 | Time-decayed popularity, in stock |
| GET `/recommendations/frequently-bought/{product_id}` | Learner BE-013 | Order co-occurrence, never text substitution |
| GET `/recommendations/you-may-like/{product_id}` | Learner BE-013 | Hybrid candidates |

Existing ProductResponse: UUID `id`, `slug`, `name`, `category`, `description`, `details`, Decimal `price` (JSON string accepted by the existing client contract), integer `inventory`, `imageUrl`, `accent`, `featured`. Extend contracts deliberately when adding brand/currency metadata; keep both clients and tests aligned.

RecommendationResponse: `{items: [{product, score, reason}], strategy, modelVersion}`. Scores are bounded 0..1. Empty valid results are arrays, not missing values. No model training is required for fallback responses.

For authenticated operations, clients send `Authorization: Bearer <token>`. The server derives user IDs from verified credentials; input user IDs or roles are not trusted. Before enabling these requests, the learner must extend CORS allowed headers/methods and verify the chosen token-storage policy. The current application has no functioning auth routes.

Frontend integration sequence: leave `VITE_USE_MOCKS=true` → pass one API contract → test the HTTP gateway for that feature → opt into real APIs locally. The current switch selects the entire gateway, so do not claim per-feature switching exists. Add explicit capability flags or a composed gateway as an integration task if some endpoints are still unfinished. Do not silently fall back to mocks on a real checkout error.

The frontend is the existing React/TypeScript/Vite storefront. Retaining TypeScript avoids replacing working code merely to match the earlier JavaScript example. No backend endpoints have been completed to support the demo.

## Extra route contracts before milestone completion

The executable task tests are the starting acceptance suite. In the active task, extend them with HTTP 422 schema errors, 401/403 ownership failures, rollback on database errors and missing records. BE-008 handler tests do not replace HTTP routing tests; BE-009 unit tests do not prove route ownership; BE-013 cold-start tests do not prove every future recommendation section.
