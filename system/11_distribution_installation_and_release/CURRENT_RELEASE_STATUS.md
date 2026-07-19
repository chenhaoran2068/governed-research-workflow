# Release Status Verification

Status: active, version-neutral release-verification rule. Historical v0.5,
v0.6, and v0.7 tags/Releases are retained below as bounded facts. This record
does not prove that any selected version is installed in a private skill source
or Codex runtime.

This record never declares a latest or current public version. Its versioned
entries are bounded historical facts; the only live public-availability check
for a selected version is the exact-tag-and-matching-Release procedure below.

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

## Published v0.5.0 Baseline

- `v0.5.0` is publicly released at annotated tag
  `v0.5.0`, target commit
  `14c37ae1eecb5f12cee385a331ee5233265ca778`, with a matching immutable
  GitHub Release.
- It contains one accountable-human-admitted metadata-only Data And Provenance
  Register Set capability. Capability admission is not an installed-runtime
  claim and does not authorize a future release.
- The immutable v0.5.0 Release retains some pre-C4 source wording. That
  wording is a historical snapshot, not a current release-state authority.
  Verify the exact tag and matching Release at the time of any installation.

## v0.5.1 Maintenance Source

- v0.5.1 is published at annotated tag `v0.5.1`, target commit
  `36ad824f0df6ed73610c6886edd76c38472793ab`, with a matching immutable
  GitHub Release.
- It corrects release-state wording without changing the v0.5.0
  capability contract, validator, schemas, dependency, data boundary,
  permissions, or CI architecture.
- A selected v0.5.1 checkout is an installation target only when the normal
  public installation rule is verified at installation time. Do not infer a
  private source or Codex runtime update from the hosted Release.

## v0.6 Capability Scope

- The v0.6 release source records an accountable-human-admitted scope for
  `GRW-CAP-060-01`. Source admission is not a public Release, installation
  target, or runtime claim.
- The retained branch `v0.6.0-workflow-evidence-controls-candidate` is source
  history only. It cannot alter published identity or authorize a private
  source/runtime update.
- A selected v0.6 version becomes an installation target only when the normal
  public installation rule above is independently verified for that exact tag
  and matching GitHub Release.

## v0.7 Historical Capability Scope

- `v0.7.0` is publicly released at annotated tag `v0.7.0`, target commit
  `a1a1bba3bca87aa7fa3107f3bd6e2d8ee53af7dc`, with a matching immutable
  GitHub Release.
- It contains the metadata-only `GRW-CAP-070-01` human-reviewed
  lesson-promotion control record scope. Its admission does not establish a
  private source, installed runtime, automatic promotion, target-rule change,
  data access, or another release authorization.
- `v0.7.1` is a control-hardening maintenance source that corrects current
  navigation and roadmap wording, rejects review roots containing indirection,
  and adds a backward-compatible correction-review record form without adding
  a new capability category. It becomes a normal installation target only if
  its own exact tag and matching GitHub Release are verified at selection time.

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
