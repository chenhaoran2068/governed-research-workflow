# v0.5.0 Metadata-Only Provenance Register-Set Release Gate

Status: historical pre-C3 candidate gate. This document defined evidence before
an accountable human can consider a later `v0.5.0` publication. It does not
authorize a commit, push, merge, tag, GitHub Release, installation, runtime
update, or public capability claim.

## Intended Scope

The only proposed `v0.5.0` capability is `GRW-CAP-050-01`: a metadata-only
Data And Provenance Register Set. It adds a register index for v0.4-compatible
single-entry metadata records and an explicitly invoked, read-only structural
validator.

The validator may read only its explicit index, package-bundled schemas, and
regular metadata JSON files named by the index. It checks structural schema
validity, safe relative paths, unique identities, and declared reciprocal
lineage. A `valid` result means only that this bounded structure was valid.
It does not establish data existence, access, permission, ethical approval,
DUA status, privacy, provenance truth, scientific fitness, or compliance.

The release must not claim data-content access, source-locator or URL access,
network activity, credential use, hashing, cleaning, analysis, clinical
handling, ethics/DUA/privacy/compliance certification, scientific conclusions,
Gate progression, submission authority, agent runtime, delegated authority,
or a technically immutable GitHub Release unless the particular claim is
separately true and recorded.

## Required Gates

### P50-G1: Exact Candidate Identity

- A clean exact candidate commit exists on the reviewed candidate route.
- Candidate version, commit, intended `v0.5.0` tag, intended GitHub Release,
  source snapshot, and candidate-to-`v0.4.0` diff resolve to one identity.
- `git status`, whitespace checks, object-integrity checks, and the exact diff
  are recorded.

### P50-G2: Capability Admission And Scope Truth

- The canonical capability ledger is current for the exact candidate commit.
- `GRW-CAP-050-01` is explicitly admitted or excluded for the named release;
  no candidate state is inherited as public availability.
- README, roadmap, SKILL, manifest, module descriptions, tests, and Release
  notes match the ledger's promise, non-promise, interface, evidence, and
  accountable-human approval owner.
- Capability admission remains separate from C4 release authorization.

### P50-G3: Public Material, Rights, And Privacy Boundary

- The exact tracked tree, newly reachable history, Git LFS objects, submodules,
  generated archives, and planned Release assets are reviewed.
- No credential, private key, private local path, real project material,
  restricted data, unpublished manuscript, unreviewed third-party payload, or
  unresolved rights issue is included.
- The accountable human confirms authority to publish the exact tree under the
  declared Apache-2.0 license.

### P50-G4: Documentation, Installation, And Compatibility

- README, SKILL, roadmap, manifest, module index, Release notes, dependency
  record, and install/update/rollback guidance consistently label `v0.5.0` as
  future until its exact tag and matching GitHub Release exist.
- Installation names only a verified exact tag and matching GitHub Release,
  never `main` or a mutable candidate branch.
- The package states Python `3.11+`, direct `jsonschema==4.26.0` validation
  dependency, and framework contract/validation boundaries without a broader
  agent, data, or compliance compatibility claim.

### P50-G5: Technical And Cross-Repository Evidence

- The complete local suite passes from the exact candidate commit with no
  skipped required checks.
- Positive, refusal, and synthetic integration tests cover the proposed
  capability, including malformed JSON, unsafe paths, duplicate identities,
  non-reciprocal lineage, dependency mismatch, symlink/reparse refusal when
  supported, and no access to an unlisted sentinel.
- The framework-integrated profile validates against Workspace Framework
  `v0.1.1` at commit `b0e32d7710b70299e633df1316b6924cd87b647b`.
- The exact intended release commit receives successful GitHub CI on Windows,
  Ubuntu, and macOS for Python 3.11 and 3.14.

### P50-G6: Release Integrity And Hosted-Control Posture

- Action references, dependency changes, workflow permissions, and public
  source authority are reviewed for the exact candidate.
- Available branch protection, immutable-release, and SHA-pinning controls are
  checked or marked unknown with an explicit limitation; unavailable controls
  are never claimed as enabled.
- The direct dependency pin is recorded as version pinning only, not as a
  hash-locked complete supply-chain claim.

### P50-G7: C4 And Post-Release Verification

- Only after P50-G1 through P50-G6 are complete may the accountable human
  authorize one exact commit, tag, Release notes, and GitHub Release action.
- After publication, independently verify tag-to-commit resolution, GitHub
  Release identity, generated source archives, Release notes, current status,
  and the immutable-release result. Record a defect as a corrective candidate
  or transparent withdrawal path, never as a silent rewrite.

## Pre-C3 Snapshot State

This gate is prepared before an exact v0.5 candidate commit exists. Its stated
tests and reviews are preparation requirements, not completed release proof.
Candidate implementation, exact identity, final material review, cross-platform
CI, accountable-human capability admission, C4 authorization, and post-release
verification remain separate decisions.
