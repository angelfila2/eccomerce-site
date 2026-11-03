# Backend implementation plan

Implement in this order. Use the next unchecked items as the daily roadmap and keep the
application as one deployable modular monolith.

## 1. Database foundation

- [x] Create the SQLAlchemy engine and request-scoped session dependency in `app/db/session.py`.
- [x] Add Alembic configuration and an initial migration.
- [x] Read all secrets from settings; never commit database credentials.
- [x] Configure Supabase PostgreSQL for development.

## 2. Catalog

- [x] Add `Category` and `Product` SQLAlchemy models with UUID primary keys and timestamps.
- [x] Use `NUMERIC`/`Decimal` for prices and an explicit three-letter currency code.
- [x] Implement repository queries behind the catalog module's existing interface.
- [x] Implement list/detail handlers, category and search filters, pagination, and 404 errors.
- [x] Add seed data matching the frontend contract.
- [x] Manually verify the catalog endpoints against the frontend contract.
- [x] Add product image object keys/URLs; do not store image bytes in PostgreSQL.

## 3. Inventory and cart

- [x] Model inventory separately from catalog presentation.
- [x] Add database constraints preventing negative inventory.
- [x] Keep anonymous carts browser-local; the current frontend needs no cart endpoint.
- [x] Skip backend cart persistence unless future requirements change.

## 4. Orders and checkout

- [x] Add `Order` and `OrderLine` models with explicit state enums.
- [x] Snapshot SKU, product name, unit price, currency, tax and discount on each order line.
- [x] In one short transaction, lock inventory rows, validate quantities, create the order and decrement stock.
- [x] Give checkout an idempotency key with a unique database constraint.
- [x] Never trust prices or totals sent by the browser; calculate them from locked database rows.
- [x] Implement `POST /api/v1/orders` according to the existing Pydantic schema.
- [ ] Switch the frontend from the mock gateway to FastAPI and manually verify checkout.
- [ ] Manually verify idempotency replay and expected checkout failures.
- [ ] Add concurrent checkout tests proving inventory cannot be oversold.

## 5. Payments and reliable side effects

- [ ] Add a payment provider only after order transactions are correct.
- [ ] Verify webhook signatures and make webhook processing idempotent.
- [ ] Add an outbox table for email/payment events that must survive process crashes.
- [ ] Introduce a worker/queue only when these durable jobs exist.

## 6. Operations

- [ ] Add structured logs with request/correlation IDs.
- [ ] Add readiness checks that verify database connectivity.
- [ ] Add production CORS, proxy, HTTPS and secret-manager configuration.
- [ ] Add CI for Ruff, mypy, pytest, Alembic drift and container builds.

## 7. Authentication — intentionally last

- [ ] Confirm secure same-origin, server-side sessions as the authentication strategy.
- [ ] Add account models in PostgreSQL with normalized unique emails and secure password hashes.
- [ ] Add registration, login and logout endpoints.
- [ ] Store opaque session records in Redis with expiration and revocation support.
- [ ] Send session IDs only through `HttpOnly`, `Secure` and appropriate `SameSite` cookies.
- [ ] Use Redis to rate-limit repeated login attempts; do not treat Redis as the account database.
- [ ] Add email verification and password-reset flows.
- [ ] Add CSRF protection for cookie-authenticated mutations.
- [ ] Add admin roles/permissions; do not rely on a client-provided role.
- [ ] Attach past guest orders to a verified account without exposing other customers' orders.

## 8. Personalised recommendations — after authentication and sufficient usage data

- [ ] Define privacy, consent and retention rules before collecting behavioural history.
- [ ] Record product-view, cart-add and completed-order events without storing raw sensitive data.
- [ ] Support anonymous browser IDs and safely attach their history after verified login.
- [ ] Start with explainable fallbacks: featured products, popular products and matching categories.
- [ ] Add item-to-item recommendations based on products viewed or purchased together.
- [ ] Train a collaborative-filtering model only after enough real interaction data exists.
- [ ] Keep training offline; store versioned recommendation results instead of training during requests.
- [ ] Add `GET /api/v1/recommendations` with cold-start fallbacks for new visitors.
- [ ] Cache generated recommendations in Redis with a short expiration time.
- [ ] Measure recommendation clicks and purchases while guarding against feedback loops.

