# v0.7.0 Lesson Promotion Control Release Gate

Status: historical pre-C4 v0.7 release-source gate. It defines the evidence
that had to be reviewed before C4 publication. It does not establish a selected
tag, GitHub Release, local installation, runtime update, or public capability
claim.

## Intended Scope

The only proposed v0.7.0 capability is `GRW-CAP-070-01`, Human-Reviewed Lesson
Promotion Control Records: one metadata-only JSON bundle schema, blank
template, synthetic fixture, explicit read-only structural validator,
documentation, and tests.

The bundle distinguishes observations, lesson candidates, represented
accountable-human decisions, integration verification, and correction,
withdrawal, or supersession events. It does not include project content; prove
human identity or authority; automatically promote, reject, integrate, or
change a lesson; change a target rule; or decide science, compliance, Gate,
submission, or release status.

## Required Gates

### P70-G1: Exact Source And Compatibility Identity

- A clean exact source commit exists for C4 review.
- The v0.6.1 public baseline, intended `v0.7.0` tag, source snapshot, diff,
  and source preparation record resolved to one explicit identity.
- Released v0.4-v0.6 schemas, templates, fixtures, and historical release
  records remain valid without migration or rewrite.

### P70-G2: Capability Admission And Claim Truth

- `GRW-CAP-070-01` is admitted only for the named v0.7.0 release scope; this
  admission remains distinct from public availability and C4 authorization.
- README, ROADMAP, SKILL, manifest, module map, guidance, tests, and notes
  distinguish release-source scope from selected-version tag/Release status.
- Capability admission is distinct from C4 authorization.

### P70-G3: Metadata, Privacy, Rights, And Boundary Review

- The exact tracked tree, newly reachable history, Git LFS objects, submodules,
  generated archives, and planned Release assets are reviewed.
- No credential, private local path, real project material, restricted data,
  unpublished manuscript, identity record, or unreviewed third-party payload
  is included.
- The accountable human confirms Apache-2.0 publication authority for the
  exact generic tree.

### P70-G4: Validator And Documentation Integrity

- Positive and refusal tests cover duplicate keys, unsafe paths, symbolic links
  or reparse points where supported, automatic-promotion declarations, invalid
  candidate/decision/integration links, missing supersession evidence, and no
  unlisted-file read or output creation.
- The validator reads only an explicit root and one explicit relative JSON
  bundle; it does not enumerate a workspace, follow references, or write.
- Documentation states that represented human decisions do not verify identity
  or real authority and that integration verification does not prove target
  correctness.

### P70-G5: Technical And Cross-Repository Evidence

- The complete local suite passes for the exact source with no required check
  silently skipped.
- The `framework_integrated` profile validates against Workspace Framework
  `v0.1.2` at `97fbd1f4f3cbaabb2cdbb3e106c91a6c9fd8b3a8`.
- The exact intended source commit receives successful GitHub CI on Windows,
  Ubuntu, and macOS with Python 3.11 and 3.14.

### P70-G6: C4 And Post-Release Verification

- An exact C4 package names the reviewed source commit, target tag, Release
  notes, CI evidence, capability admission, material review, residual risks,
  and post-release checks.
- Only after a separately recorded accountable-human C4 decision may an
  immutable `v0.7.0` tag and matching GitHub Release be created.
- Publication is followed by independent tag/Release/archive/documentation
  verification. Local runtime adoption remains a separate controlled action.
