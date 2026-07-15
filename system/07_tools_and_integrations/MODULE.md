# Tools And Integrations

Status: active controlled bootstrap tool; candidate framework integration is
test-only and has no installation helper.

Current executable tooling is limited to the explicit empty-workspace bootstrap
helper and its regression tests. It uses no network, credentials, data import,
or external connector.

The cross-repository integration test has no account, network, data-import, or
installation capability at runtime. Any future integration helper must declare
its inputs, outputs, permissions, source boundary, confirmation behavior,
failure mode, audit record, and tests. A skill or system package cannot grant
underlying source-system access.
