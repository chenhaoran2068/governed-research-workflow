# Current Release Status

Status: current-status record for the unreleased `v0.4.0` candidate branch. It
does not create a Git tag, GitHub Release, installation, runtime update, or
public capability claim.

## Current Public Release

- Current public release: `v0.3.1`.
- Exact local tag resolution:
  `0a16e534fb11bc5254bcdd5c2780e09f46cf81d0`.
- Locally recorded hosted-release evidence:
  `V0_3_1_RELEASE_EVIDENCE.md` and `RELEASE_NOTES_v0.3.1.md` record the
  `2026-07-16` tag and matching GitHub Release.
- Live hosted-release recheck: GitHub's `releases/latest` route resolved to
  `v0.3.1` on `2026-07-17`. This current-status observation is release-
  preparation evidence only; do not replace exact-tag verification during an
  actual installation with this local record.

Normal public installation must select an exact published tag and verify it
using `INSTALL_UPDATE_ROLLBACK.md`. It must not select `main`, an untagged
branch, an unreleased candidate branch, or a historical gate/evidence document.

## Current Unreleased Candidate Branch

- Current unreleased candidate: `v0.4.0`.
- Public candidate branch: `v0.4.0-capability-truth-ledger-candidate`.
- The branch is public for review but has no `v0.4.0` tag or GitHub Release.
- Exact candidate-commit evidence is recorded separately and must be refreshed
  after every candidate source change.
- Public tag or GitHub Release for this candidate: none.
- Installation status: not an installation target.
- Capability status: consult the capability truth ledger. It records a named
  future-release admission scope, but that admission does not create a current
  public-release claim, installation target, runtime update, or C4 authority.

## Historical Records

- `v0.3.0` and `v0.3.1` candidate, gate, evidence, material-review, and
  release-note documents are retained as historical snapshots.
- `V0_3_2_RELEASE_STATE_CORRECTION_CANDIDATE.md` is an unpublished historical
  local historical candidate retained as input to `v0.4.0`; it is not a current candidate
  identity or an installation target.
- Historical records explain past decisions. They do not override this current
  status page, the capability ledger, or a future exact release record.

## Identity Boundary

This file describes only the public package worktree and its recorded release
facts. It does not prove that a private skill source or an installed
Codex runtime has been updated. Those identities require their own source
record, controlled-copy receipt, and verification.
