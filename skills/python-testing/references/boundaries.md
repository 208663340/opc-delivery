# Test Boundaries

Use clear test-level names:

- Unit: domain behavior or a use case with controlled collaborators.
- Repository integration: real database adapter and migration-created schema.
- Composition: application dependency wiring, middleware, and configuration.
- End-to-end: critical complete user flows.

SQLite is useful for database-agnostic adapter checks, but it cannot validate PostgreSQL-specific SQL, JSON, locks, types, upserts, or transaction behavior. Test dialect-specific code against an ephemeral instance of the production database.

Share expensive immutable infrastructure such as an engine or container if needed. Give each test an isolated session and transaction, then roll it back or clean it reliably. Query through a fresh session after a commit when the contract requires durable visibility.

Test framework configuration that you own, including dependency injection, auth, transactions, and middleware. Do not test framework internals.
