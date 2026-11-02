# Backend implementation plan

Implement in this order. Keep the application as one deployable modular monolith.

## 1. Database foundation

- [ ] Create the SQLAlchemy engine and request-scoped session dependency in `app/db/session.py`.
- [ ] Add Alembic configuration and an initial empty migration.
- [ ] Read all secrets from settings; never commit database credentials.
- [ ] Add a PostgreSQL service for local development.

## 2. Catalog

- [ ] Add `Category` and `Product` SQLAlchemy models with UUID primary keys and timestamps.
- [ ] Use `NUMERIC`/`Decimal` for prices and an explicit three-letter currency code.
- [ ] Implement repository queries behind the catalog module's existing interface.
- [ ] Implement list/detail handlers, category and search filters, pagination, and 404 errors.
- [ ] Add seed data and tests matching the frontend contract.
- [ ] Add product image object keys/URLs; do not store image bytes in PostgreSQL.

## 3. Inventory and cart

- [ ] Model inventory separately from catalog presentation.
- [ ] Add database constraints preventing negative inventory.
- [ ] Decide whether anonymous carts remain browser-local or receive signed server IDs.
- [ ] Implement cart persistence only after that decision; the current frontend needs no cart endpoint.

## 4. Orders and checkout

- [ ] Add `Order` and `OrderLine` models with explicit state enums.
- [ ] Snapshot SKU, product name, unit price, currency, tax and discount on each order line.
- [ ] In one short transaction, lock inventory rows, validate quantities, create the order and decrement stock.
- [ ] Give checkout an idempotency key with a unique database constraint.
- [ ] Never trust prices or totals sent by the browser; calculate them from locked database rows.
- [ ] Implement `POST /api/v1/orders` according to the existing Pydantic schema.
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

- [ ] Decide between secure same-origin session cookies and an external OIDC provider.
- [ ] Add account models and authorization rules after anonymous checkout works.
- [ ] Add CSRF protection for cookie-authenticated mutations.
- [ ] Add admin roles/permissions; do not rely on a client-provided role.
- [ ] Attach past guest orders to a verified account without exposing other customers' orders.

