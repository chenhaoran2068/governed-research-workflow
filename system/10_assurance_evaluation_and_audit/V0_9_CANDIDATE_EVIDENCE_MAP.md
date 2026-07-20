# v0.9 Local Candidate Evidence Map

Status: local candidate implementation record. It is not a public capability
admission, an exact candidate commit, a hosted CI result, a GitHub Release, or
an installed-runtime record.

## Candidate Scope

| Candidate capability | Candidate interface | Local evidence required before later review |
| --- | --- | --- |
| GRW-CAP-090-01 Metadata-only integrity-audit bundle | Schema, synthetic template, explicit read-only validator. | Positive, negative, path-refusal, duplicate-key, no-write, checker/fixture identity, and harness-scope tests. |
| GRW-CAP-090-02 Correction and reassessment linkage | Typed link between a prior finding, later identity, disposition reference, and re-review outcome. | Closure-with-link and closure-without-link refusal tests. |
| GRW-CAP-090-03 Operational-integrity preflight records | Metadata-only post-install outer-change and worktree-preflight records. | Active/locked/unknown stop and prunable/missing preflight refusal tests. |

## Exact Limits

The local candidate accepts one caller-selected absolute physical JSON bundle.
It reads that file and the bundled schema only. It does not enumerate a root,
follow a declared reference, inspect Git state, contact a host, read private
source/runtime or receipts, create output files, repair a worktree, or carry
out a correction.

Any passing result is limited to the named checker, supplied synthetic or
caller-supplied metadata, and stated structural rules. It does not establish
truth, a genuine human decision, hosted Release state, data access, compliance,
scientific validity, Gate readiness, submission readiness, or tamper-proof
history.

## Later Evidence Still Required

Before any capability admission or public release, later review must establish
the exact candidate commit, full local regression result, public-material and
rights review, dependency/license review, exact Windows/Ubuntu/macOS CI,
framework-integrated evidence, release-control evidence, accountable-human
admission, and a separate C4 decision. None is established by this file.

## Local Verification Snapshot

This snapshot covers an uncommitted local candidate on branch
`v0.9.0-integrity-audit-candidate`, based on public v0.8.1 commit
`9439983971e0d5f8299a337b683055aa469e0a5f`. It is local implementation
evidence only, not an exact-commit, hosted-CI, public-Release, or installed
runtime statement.

- interpreter: Python 3.13.14;
- validator dependency: `jsonschema==4.26.0`;
- focused v0.9 and ledger tests: 32 passed;
- full local regression suite: 187 passed, with 3 framework-integration tests
  skipped because their explicit integration environment was not configured;
- cache scan after tests: no `__pycache__` or `.pyc` artifact in the candidate;
- reviewed refusal coverage: absolute/relative and link path rejection,
  duplicate JSON keys and record identities, declared-input mismatch,
  closed-finding linkage, checker/harness mismatch, variable-budget refusal,
  worktree preflight stop rules, no-write sentinel, and public-material marker
  checks.

The next evidence boundary is an exact committed candidate plus independently
authorized remote CI. This snapshot cannot substitute for it.
