# Accounts — learner-owned milestone 6

The current roadmap supersedes the historical auth-last sequencing below.
BE-002..004 cover validation/models/queries; BE-006..008 cover password hashing,
expiring bearer JWTs and handlers. The scaffold does not implement authentication.
Follow the full [task cards](../../../../docs/learning/TASKS.md) and
[backend guide](../../../../BACKEND_LEARNING_GUIDE.md).

The remaining notes are historical context for production alternatives, not the
current exercise specification. Do not replace working code to support the demo.

Authentication is intentionally not wired into the application.

After anonymous catalog and checkout are production-ready:

1. Choose secure same-origin session cookies or an external OIDC provider.
2. Model accounts independently from customer/order contact details.
3. Add authorization at both router dependencies and use-case interfaces.
4. Add CSRF protection before enabling credentialed browser requests.
5. Provide a verified process for attaching guest orders to accounts.

Do not recreate the previous custom access-token/refresh-token flow without a concrete external-client requirement.

