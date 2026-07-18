# Release Status Verification

Status: current release-verification rule plus `v0.5.0` release-source
boundary. The published `v0.4.0` tag/Release is the historical public baseline
for this worktree. This record does not assert that a hosted `v0.5.0` Release
or runtime update exists.

## Normal Public Installation Rule

A normal public installation target exists only when all of the following can
be verified for the selected version:

1. an exact annotated Git tag exists;
2. a matching GitHub Release exists for that same tag;
3. the tag resolves to the reviewed source commit; and
4. the installation follows `INSTALL_UPDATE_ROLLBACK.md` and records its own
   local receipt.

Never infer a live release from `main`, another mutable branch, a local
worktree, a capability ledger, a green CI run, a historical gate/evidence
document, or an AI statement. Use Git and the GitHub Releases page/API to
verify the exact tag and matching Release at the time of installation.

## v0.5.0 Release-Source Scope

- This release source contains one accountable-human-admitted metadata-only
  Data And Provenance Register Set capability. Admission is not a tag, GitHub
  Release, installation target, runtime claim, or C4 authorization.
- A v0.5.0 checkout becomes a normal public installation target only if the
  normal public installation rule is later satisfied for its exact final
  commit.
- A hosted release must not be inferred from `main`, a branch, a green CI run,
  a capability ledger, or an AI statement.

## v0.4.0 Historical Public Baseline

- The published `v0.4.0` release defines the governance-and-records baseline.
- The canonical capability ledger records ten accountable-human-admitted
  capabilities and one explicit exclusion. Admission is not a hosted-release,
  installation, runtime, or C4 claim.
- A selected `v0.4.0` checkout is an installation target only if the normal
  public installation rule above is satisfied for the exact selected commit.
- The release-control record, C4 authorization, and post-release verification
  remain distinct evidence classes. They cannot substitute for one another.

## Historical Records

- `v0.3.0` and `v0.3.1` candidate, gate, evidence, material-review, and
  release-note documents are retained as historical snapshots.
- `V0_3_2_RELEASE_STATE_CORRECTION_CANDIDATE.md` is an unpublished historical
  local candidate retained as input to `v0.4.0`; it is not a current candidate
  identity or an installation target.
- Historical records explain past decisions. They do not override the live
  tag-and-Release verification rule, the capability ledger, or an exact
  release record.

## Identity Boundary

This file describes only the public package worktree and its release-state
verification rule. It does not prove that a private skill source or an
installed Codex runtime has been updated. Those identities require their own
source record, controlled-copy receipt, and verification.
