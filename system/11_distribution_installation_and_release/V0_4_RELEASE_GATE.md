# v0.4.0 Governance-And-Records Release Gate

Status: historical pre-C3 gate snapshot. It prepared a future `v0.4.0` candidate for human
review. It does not authorize a commit, push, merge, tag, GitHub Release,
runtime installation, or public claim.

## Intended Scope

The intended `v0.4.0` release is a bounded governance-and-records expansion.
It may re-admit the existing routing, empty-workspace bootstrap, profile, and
retrospective routes, and may admit the verified R40 governance records. Any
admitted capability must be named in the canonical capability ledger for the
exact release.

`GRW-CAP-040-03` remains excluded: `v0.4.0` does not provide specialist role
cards, an agent runtime, delegated authority, hidden background work, or
multi-agent orchestration.

The release must not claim real-data access or processing, clinical handling,
ethics/DUA/privacy/compliance certification, scientific analysis or final
conclusions, automated external login/download, submission authority, or a
technically immutable GitHub Release unless each claim is separately true and
recorded.

## Required Gates

### R40-G1: Exact Candidate Identity

- An exact, clean candidate commit exists on the reviewed candidate route.
- Candidate version, commit, intended `v0.4.0` tag, and intended GitHub
  Release resolve to one identity.
- `git status`, whitespace checks, object-integrity checks, and the exact
  candidate-to-baseline diff are recorded.

### R40-G2: Capability Admission And Scope Truth

- The canonical ledger is current for the exact candidate commit.
- Each verified candidate capability is explicitly admitted or excluded; no
  prior `v0.3.1` claim is inherited automatically.
- Public wording matches each admitted promise, non-promise, interface,
  evidence, and approval owner.
- The accountable human records the capability-admission decision separately
  from C4 release authorization.

### R40-G3: Public Material, Rights, And Privacy Boundary

- The exact tracked tree, newly reachable history, Git LFS objects, submodules,
  generated archives, and planned Release assets are reviewed.
- No credential, private key, private local path, real project material,
  restricted data, unpublished manuscript, unreviewed third-party payload, or
  unresolved rights issue is included.
- The accountable human confirms authority to publish the exact tree under the
  declared license.

### R40-G4: Documentation, Installation, And Compatibility

- README, SKILL, roadmap, manifest, module index, release notes, and
  install/update/rollback instructions consistently identify `v0.4.0` as a
  future exact tag until it exists.
- The normal installation route names only an existing exact tag and matching
  GitHub Release, never `main` or an untagged candidate branch.
- Supported profiles, platforms, Python boundary, and exact framework
  validation tag/commit are stated without broader compatibility claims.

### R40-G5: Technical And Cross-Repository Evidence

- The full local suite passes from the exact candidate commit with no skipped
  required checks.
- Standalone and framework-integrated evidence use Workspace Framework
  `v0.1.1` at `b0e32d7710b70299e633df1316b6924cd87b647b`.
- The exact intended `main` commit receives successful Windows, Ubuntu, and
  macOS CI results for Python 3.11 and 3.14.
- Positive, refusal, and synthetic integration evidence remains enabled for
  every proposed admitted capability.

### R40-G6: Release Integrity And Hosted-Control Posture

- Action references, dependency changes, workflow permissions, and public
  source authority are reviewed for the exact candidate.
- Available hosted security and branch/release controls are checked or marked
  unknown with an explicit limitation; no unavailable control is claimed.
- The accountable human records whether GitHub technical immutable Releases
  are enabled or deferred, with a reason and future re-evaluation trigger.

### R40-G7: C4 And Post-Release Verification

- Only after R40-G1 through R40-G6 are complete may the accountable human
  authorize one exact commit, tag, Release notes, and GitHub Release action.
- After publication, independently verify tag-to-commit resolution, GitHub
  Release identity, generated source archives, Release notes, and current
  status. Record defects as a new corrective candidate or transparent
  withdrawal path, never a silent rewrite.

## Pre-C3 Snapshot State

At the time this pre-C3 gate record was prepared, R40-00 through R40-06 had
local implementation-review evidence but no exact candidate commit was
recorded. This file remains a historical preparation snapshot after any later
C3 local commit; the current exact candidate identity must be recorded
separately in the local C3 implementation record.

No R40-G1 through R40-G7 gate passes automatically because a candidate commit
exists. C3 and C4 remain distinct: C3 may create and review an unreleased candidate
commit, while C4 requires the later exact release evidence and explicit human
authorization.
