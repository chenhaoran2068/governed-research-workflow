# v0.3.1 Compatibility Maintenance Release Gate

Status: historical pre-release gate. It prepared the published `v0.3.1`
annotated tag and matching GitHub Release on `2026-07-16`. The gate conditions
below preserve their candidate-time meaning and are not a current release stop.

## Scope

v0.3.1 is limited to release-status/documentation corrections, explicit
release-governance records, and synthetic framework-integrated validation
against exact Governed Research Workspace Framework v0.1.1 while retaining the
v0.1.0 framework-contract version. It adds no research execution, data access,
clinical processing, compliance decision, agent runtime, migration, automatic
release, or submission capability.

## Required Gates

### R31-G1: Exact Identity And Patch Scope

- `SYSTEM_MANIFEST.yaml` declares source version `0.3.1`.
- The intended tag is `v0.3.1`, absent before creation, and points to one exact
  tested `main` commit.
- The final diff from `v0.3.0` is limited to documented compatibility and
  release-governance maintenance.

### R31-G2: Public Material, Rights, And Provenance

- The exact final tree and newly reachable history receive a fresh material,
  rights, and credential review.
- No real project, restricted data, private record, credential, or unreviewed
  third-party payload is admitted.
- The accountable human confirms publication authority for the exact tree.

### R31-G3: Installation, Update, Rollback, And Claims

- README, system index, manifest, installation contract, roadmap, and release
  notes distinguish a release-gated source from a released tag.
- Normal installation names only an existing exact tag and matching GitHub
  Release, never a mutable branch.
- Framework contract version and exact release-validation target are not
  conflated.

### R31-G4: Technical And Cross-Repository Evidence

- The full local suite passes with `FRAMEWORK_REPOSITORY_ROOT` set to the
  exact Framework v0.1.1 checkout and `FRAMEWORK_RELEASE_TAG=v0.1.1`.
- The final intended `main` commit has a successful Windows, Ubuntu, and macOS
  matrix using Python 3.11 and 3.14.
- Failure and negative-path tests remain enabled; skipped tests cannot be
  represented as passing evidence.

### R31-G5: Release Integrity And Hosted Controls

- Git tree is clean; object integrity and whitespace checks pass.
- Action references and dependency scope are reviewed.
- Hosted security, branch-protection, and release-integrity unknowns are
  recorded rather than silently assumed.
- The accountable human records either enablement of GitHub technical
  immutable releases or the v0.3.1 deferral rationale in the integrity policy.

### R31-G6: Accountable-Human Release Decision

The accountable human must explicitly approve or reject creation of annotated
tag `v0.3.1` and its matching GitHub Release from the exact final tested commit.
AI preparation, a successful branch build, or a merge to `main` cannot satisfy
this gate.

### R31-G7: Publication And Post-Release Verification

After R31-G6 only:

- create the annotated tag without rewriting an earlier tag;
- create the matching GitHub Release using the prepared release notes;
- verify the tag resolves to the approved commit, the Release identifies that
  tag, and source archives/notes are correct; and
- record any later correction as a new version, never a hidden mutation.

## Stop Rule

Any mismatch among final commit, tag, Release, scope, test evidence, rights,
or human approval stops publication. A later patch is safer than rewriting a
published release.
