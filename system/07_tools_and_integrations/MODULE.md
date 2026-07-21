# Tools And Integrations

Status: v0.9.0 integrity-audit source retains the historical v0.8.0 controlled
bootstrap helper and its release-scope helper-admission record. The v0.9
validator is read-only and does not add a helper admission or write surface.
Framework integration is test-only and has no installation helper.

Current executable tooling is limited to the explicit empty-workspace bootstrap
helper and its regression tests. It uses no network, credentials, data import,
or external connector.

`bootstrap_empty_workspace_helper_admission.json` records the helper's source
identity, allowed empty-scaffold action, write/recovery/confirmation boundaries,
limitations, and evidence. Admission is not a per-run approval, M53
authorization, data authority, C4 authorization, or runtime-installation
authority. Its current Python source identity uses the declared,
cross-platform `sha256_utf8_lf_v1` text rule; the helper does not become a
generic writer.

The cross-repository integration test has no account, network, data-import, or
installation capability at runtime. Any future integration helper must declare
its inputs, outputs, permissions, source boundary, confirmation behavior,
failure mode, audit record, and tests. A skill or system package cannot grant
underlying source-system access.

The v0.10 release source's experience-package validator is an explicit read-only
checker, not a helper admission or intake tool. It reads one selected manifest
and its five declared metadata records, reports to standard output, and never
writes, discovers a directory, sends a request, or handles real contribution
content.

The v0.10.1 exchange-pilot validator is also explicit and read-only. It reads
one receipt, one named package manifest, and the five records declared by that
manifest. It has no clone, fetch, upload, download, credential, transfer, or
writer capability. Any actual repository or transport action stays outside the
validator and requires separately approved human-controlled operation.
