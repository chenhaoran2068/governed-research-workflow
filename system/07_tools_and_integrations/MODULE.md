# Tools And Integrations

Status: active controlled bootstrap tool; external integrations are foundation
only.

Current executable tooling is limited to the explicit empty-workspace bootstrap
helper and its regression tests. It uses no network, credentials, data import,
or external connector.

Any future integration must declare its inputs, outputs, permissions, source
boundary, confirmation behavior, failure mode, audit record, and tests. A skill
or system package cannot grant underlying source-system access.
