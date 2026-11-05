# Assistant-managed database changes

The assistant owns Alembic configuration, schema revisions, data migrations,
backfills, seeds and their verification. The learner can focus on backend/ML code.

## Accounts and carts

Revision `8d74b92a61ef` follows `73a80b5bcddb` and creates `users`, `carts` and
`cart_items`. It matches the completed ORM models, with unique emails, one cart per
user, unique product lines, positive quantities and foreign keys. Account metadata
is now registered with Alembic for future drift detection.

No account/cart tables existed in the previous schema, so there is no account data
to transform. Existing catalogue, inventory and orders are left untouched. The
assistant will implement future backfills if a schema change requires them. Guest
orders and browser-local carts are not assigned to accounts by matching emails.

After activating the backend environment, the upgrade command is:

```powershell
cd backend
python -m alembic upgrade head
```

The assistant has not applied this to a live configured database: Docker Desktop
was unavailable during verification. No shared database was altered.

## Executed verification

```powershell
python -m pytest tests/test_account_migration.py tests/learning/test_backend.py::test_BE_003 tests/test_foundation.py -q
```

Result: **6 passed**. The new revision was applied, downgraded and reapplied on an
isolated SQLite database with existing catalogue data preserved. Actual migrated
unique constraints reject duplicate email/cart ownership. Foreign keys, line
uniqueness and positive-quantity constraints are inspected. PostgreSQL DDL compiles
with UUID columns, timezone-aware timestamps, cascade foreign keys and constraints.

The SQLite roundtrip starts from an ORM-created previous commerce schema; it does
not claim to replay all historical PostgreSQL migrations. Live PostgreSQL
upgrade/downgrade and drift verification remain pending. Downgrade is tested only
on a disposable database because dropping new account/cart tables removes their data.

## Future changes

When interaction/ownership/vector models are ready, the assistant supplies the
corresponding revision and any necessary data migration. Schema prerequisites do
not require the learner to implement Alembic. Frontend pages, API clients, demo
states and switching to verified endpoints are also assistant-owned.
