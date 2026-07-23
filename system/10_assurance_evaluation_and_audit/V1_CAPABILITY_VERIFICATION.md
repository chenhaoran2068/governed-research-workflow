# V1 Capability Verification Map

## Purpose

`v1_capability_verification_map.json` maps every capability in the canonical
ledger to the test files and review types required for the v1 interface freeze.
It preserves each capability's historical release record while requiring
current regression evidence for the frozen v1 contract.

It does not alter a capability promise, make a forbidden capability permitted,
establish a GitHub Release, establish an installed runtime, prove facts, verify
rights, or replace accountable-human approval.

## Candidate Evidence Status

Before the full v1 local regression has run, every map item is `pending` and
the map is `pending_local_full_regression`. After the exact candidate tree
passes the full local suite, a separately reviewed update may mark the map and
every entry `locally_verified_candidate`. That state remains local candidate
evidence only, not C4 authorization, a tag, a GitHub Release, or a runtime
installation claim.

## Reading One Entry

- `expected_claim_status` must match the ledger. The role/runtime exclusion
  `GRW-CAP-040-03` remains forbidden.
- `verification_test_paths` identifies existing source tests that must run.
- `required_review_types` forces interface, negative-boundary, and complete
  regression review rather than treating one green unit test as complete proof.

A missing map entry, missing test path, claim conflict, or unverifiable
release/install identity stops the affected public claim until a human reviews
repair options.
