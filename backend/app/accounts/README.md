# Accounts — final implementation phase

Authentication is intentionally not wired into the application.

After anonymous catalog and checkout are production-ready:

1. Choose secure same-origin session cookies or an external OIDC provider.
2. Model accounts independently from customer/order contact details.
3. Add authorization at both router dependencies and use-case interfaces.
4. Add CSRF protection before enabling credentialed browser requests.
5. Provide a verified process for attaching guest orders to accounts.

Do not recreate the previous custom access-token/refresh-token flow without a concrete external-client requirement.

