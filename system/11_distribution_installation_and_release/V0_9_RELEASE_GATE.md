# v0.9.0 Integrity-Audit Release Gate

Status: pre-C4 release-gate record. It records required evidence and scope;
it does not authorize a tag, GitHub Release, installation, or runtime update.

## Intended Scope

The admitted v0.9.0 release-source scope contains exactly:

- `GRW-CAP-090-01`: a finite metadata-only integrity-audit bundle and explicit
  read-only structural validator;
- `GRW-CAP-090-02`: correction and reassessment linkage that preserves the
  earlier finding and requires later re-review; and
- `GRW-CAP-090-03`: metadata-only post-install and worktree-recovery preflight
  records without an executor.

It does not add hosted-state verification, data/project access, network or Git
action, credential use, agent runtime, delegated authority, recovery execution,
generic writing, scientific or compliance truth, Gate/submission readiness, or
release authority.

## Required Gates

### P90-G1: Exact Candidate And Compatibility

- Preserve v0.4-v0.8 schemas and meanings without migration or rewrite.
- Bind later remote evidence to one exact candidate commit based on immutable
  `v0.8.1` commit `9439983971e0d5f8299a337b683055aa469e0a5f`.
- Retain public `standalone` and `framework_integrated` profiles only; bind the
  latter to Workspace Framework `v0.1.2` commit
  `97fbd1f4f3cbaabb2cdbb3e106c91a6c9fd8b3a8`.

### P90-G2: Capability And Claim Truth

- Keep the capability ledger, public documentation, release notes, and test
  expectations mutually consistent.
- Capability admission is distinct from C3-remote evidence, C4, tag, matching
  GitHub Release, private source, and installed runtime identity.
- Stop an affected claim on contradiction or unknown evidence; report evidence,
  unknowns, options, costs, and residual risk to the accountable human.

### P90-G3: Public Material And Rights

- Review the exact tracked tree, reachable history, Git LFS objects, submodules,
  generated archives, and planned Release assets.
- Stop for credentials, private paths, real project material, restricted data,
  unpublished content, or unresolved rights/ownership constraints.
- Retain accountable-human Apache-2.0 publication authority for the exact
  generic tree as evidence separate from tests and platform settings.

### P90-G4: Read-Only Contract Integrity

- Refuse relative, escaping, link/reparse-point, duplicate-key, or invalid
  bundle input before an out-of-boundary read.
- Refuse duplicate/cross-type identities, bad declared-input relationships,
  unreliable harness success, unsafe worktree dispositions, and closed findings
  lacking correction/reassessment linkage.
- Test no-write behavior and preserve the distinction among observation,
  finding, machine result, unknown, human disposition, and hosted evidence.

### P90-G5: Technical And Cross-Platform Evidence

- Run the complete local suite after the final release-source change.
- Run all six required GitHub CI contexts on the exact remote candidate and on
  the protected-main commit selected for release.
- Refresh dependency, workflow, secret/privacy, license, framework, and
  release-integrity checks after any correction.

### P90-G6: Protected Main, C4, And Local Adoption

- Reach `main` through its protected pull-request route; retain CI and
  conversation-resolution evidence.
- C4 must name the exact post-merge commit, `v0.9.0` tag, release notes, and
  immutable GitHub Release operation.
- Verify the hosted tag, Release, source archive, and exact identity after
  publication. Private canonical source and Codex runtime adoption remain a
  separately controlled task with rollback, receipt/hash, and fresh-process
  validation.
