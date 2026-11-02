"""Transactional order module implementation.

TODO: Implement create_order(session, request, idempotency_key).

Required invariants:
1. Load and lock every referenced inventory row in a deterministic order.
2. Reject missing products, duplicates, invalid quantities, or insufficient stock.
3. Read authoritative prices from the database; never accept client totals.
4. Snapshot catalog and price data onto order lines.
5. Create the order and decrement stock in the same short transaction.
6. Make the idempotency key unique and return the existing result on replay.
7. Publish external effects through an outbox after the database transaction.
"""

