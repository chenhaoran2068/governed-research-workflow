# v0.6.0 Workflow And Evidence Control Release Gate

Status: v0.6 release-source gate. It defines evidence that must be independently
reviewed before C4 publication. It does not authorize a tag, GitHub Release,
local installation, runtime update, or a public capability claim.

## Intended Scope

The only admitted v0.6.0 capability is `GRW-CAP-060-01`: a metadata-only
Workflow And Evidence Control Bundle with exactly six record types, optional
canonical baseline comparison, blank templates, synthetic fixtures, and an
explicitly invoked read-only validator.

It may validate only explicit JSON inputs under a supplied review root. A
structural result does not establish truth, source support, human identity,
actual authorization, data availability, permission, compliance, scientific
validity, Gate passage, submission readiness, release readiness, or tamper-
proof history.

## Required Gates

### P60-G1: Exact Source And Compatibility Identity

- A clean exact source commit exists for C4 review.
- Source version, base `v0.5.1` commit, intended `v0.6.0` tag, source
  snapshot, and diff resolve to one identity.
- v0.4/v0.5 schemas, templates, fixtures, and published release history remain
  unchanged and valid without migration.

### P60-G2: Capability Admission And Public Claim Truth

- `GRW-CAP-060-01` is verified and then explicitly admitted or excluded by the
  accountable human for the exact release scope.
- Until that admission, the capability ledger must not describe it as
  permitted or released.
- README, ROADMAP, SKILL, manifest, module maps, references, tests, and notes
  distinguish the v0.6 release source from published v0.5.1.
- Capability admission remains separate from C4 authorization.

### P60-G3: Input, Privacy, Rights, And Boundary Review

- The exact tracked tree, newly reachable history, Git LFS objects,
  submodules, generated archives, and planned Release assets are reviewed.
- No credential, private key, private local path, real project material,
  restricted data, unpublished manuscript, or unreviewed third-party payload
  is included.
- The accountable human confirms publication authority for the exact generic
  tree under Apache-2.0.

### P60-G4: Validator And Documentation Integrity

- Positive and refusal tests cover duplicate keys, unsafe paths, malformed
  JSON, missing/circular references, stale/unknown/invalidated prerequisites,
  AI-as-human-decision refusal, revision/downstream contradiction, baseline
  mismatch, no unlisted read, and no output creation.
- Canonical JSON identity is implemented in one tested helper, not recreated
  ad hoc in a shell command.
- Documentation states that a baseline comparison cannot prevent a process
  with equivalent write authority from changing both bundle and baseline.

### P60-G5: Technical And Cross-Repository Evidence

- The complete local suite passes for the exact source with no required
  check silently skipped.
- The framework-integrated profile validates against Workspace Framework
  `v0.1.2` at `97fbd1f4f3cbaabb2cdbb3e106c91a6c9fd8b3a8`.
- The exact intended source commit receives successful GitHub CI on Windows,
  Ubuntu, and macOS with supported Python 3.11 and 3.14.

### P60-G6: C4 And Post-Release Verification

- An exact C4 package names the reviewed source commit, target tag,
  Release notes, CI evidence, capability admission, release-control record,
  residual risks, and post-release checks.
- Only after the accountable human separately approves that exact package may
  a v0.6.0 tag and immutable GitHub Release be created.
- Publication is followed by independent tag/Release/archive/documentation
  verification. Local runtime adoption remains a separate M52 operation.
