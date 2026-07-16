# v0.3.1 Release Evidence Record

Status: historical pre-release evidence snapshot. It prepared the published
`v0.3.1` annotated tag and matching GitHub Release on `2026-07-16`. The
candidate-time wording below is preserved for traceability and is not the
current release status.

## Intended Release

| Field | Value |
| --- | --- |
| Version | `v0.3.1` |
| Release type | patch-level compatibility and release-governance maintenance |
| Source branch | `main` release-gated source |
| Framework contract version | `0.1.0` |
| Exact framework validation target | Workspace Framework `v0.1.1` |
| Public package contents | generic documents, blank templates, tests, standard-library helper, and Apache-2.0 license |

The exact final commit, annotated tag object, GitHub Release URL, final matrix
run URLs, and post-release verification must be recorded in the GitHub Release
and local release-review record after R31-G6 and R31-G7. They must not be
invented or prefilled in this source snapshot.

## Evidence Required Before R31-G6

- `PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.3.1.md` records the public-boundary and
  rights review.
- `INSTALL_UPDATE_ROLLBACK.md` defines exact-tag installation, update, and
  rollback behavior.
- `RELEASE_INTEGRITY_POLICY_v1.md` defines annotated-tag, CI, action-pin,
  human-approval, immutable-release, and post-release controls.
- The final local test suite and the final cross-platform CI matrix pass for
  the exact final commit.
- The accountable human reviews this exact scope and approves or rejects the
  specific tag and Release action.

## Release Boundary

This evidence supports only the stated generic package boundary. It does not
certify clinical handling, ethics, DUA compliance, research quality, results,
claims, external service behavior, or a fully locked supply chain.
