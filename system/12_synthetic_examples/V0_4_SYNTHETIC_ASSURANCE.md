# V0.4 Synthetic Assurance

Status: local candidate-only synthetic assurance evidence. It is not a public
release record, C4 authorization, installed-runtime verification, or a claim
that the candidate is ready to publish.

## Scope

This route combines only empty templates, synthetic identifiers, public package
documentation, and local regression tests. It verifies that the v0.4 candidate
continues to distinguish current public release, local candidate, private
source, and installed runtime; preserves the human-governed authorization,
metadata-only provenance, role-card exclusion, and release-control boundaries;
and records an exact framework reference for the framework-integrated profile.

It does not access a real project, data, manuscript, credential, institution,
external service, installed runtime, or hosted GitHub state. Passing this route
does not prove scientific, clinical, ethics, DUA, legal, security, installation,
or release correctness.

## Candidate Snapshot Identity

- head commit: `854d6d10910677ebd7988ee61c6ca6a35519e66f`
- working-tree source snapshot SHA-256: `620efe8024b6201ef01be624b698ca31d5e3e57ecfa1a6d680b82e1309d2e66d`
- snapshot method: SHA-256 over each `git ls-files --cached --others
  --exclude-standard -z` repository source file's UTF-8 relative path, a NUL
  separator, normalized source bytes, and a final NUL separator, in byte-sorted
  path order. Text files normalize CRLF and lone-CR line endings to LF; binary
  files containing a NUL byte remain byte-for-byte. This evidence file is
  excluded so the evidence block does not hash itself. The check therefore
  requires a Git checkout and includes untracked, non-ignored candidate schema,
  template, documentation, and test files.
- framework tag: `v0.1.1`
- framework resolved commit: `b0e32d7710b70299e633df1316b6924cd87b647b`

This is a transparent uncommitted candidate snapshot, not an exact release
commit. A later C4 release decision must rerun the required checks from a clean
exact commit and update the release-control and post-release records.

## Synthetic Fixture Inventory

- `assets/bounded-autonomy-authorization.template.json`: blank bounded-task
  authorization example; no approval is granted.
- `assets/data-provenance-register.template.json`: metadata-only source pointer
  example; access/restriction status is `unknown`.
- `assets/release-control-record.template.json`: fictional candidate-review
  record; C4 and post-release verification are `null`.

All identifiers, roles, evidence references, sources, and outputs in these
fixtures are synthetic placeholders. No fixture is a project record.

## Test-Run Evidence

- command: `python -m unittest discover -s tests -v`
- operating system: `Windows`
- Python version: `3.13.14`
- test dependency provenance: `jsonschema 4.26.0`, already recorded in
  `tests/TEST_DEPENDENCY_PROVENANCE.md`; no package runtime dependency added.
- tested capability set: `GRW-CAP-040-00`, `GRW-CAP-040-01`,
  `GRW-CAP-040-02`, `GRW-CAP-040-04`, and `GRW-CAP-040-05` as verified
  candidates; `GRW-CAP-040-03` as verified excluded; `GRW-CAP-040-06` as a
  verified candidate-only assurance route.
- pass/fail/skip: `76 passed / 0 failed / 0 skipped` on the recorded local run.
- source-snapshot verification: passed; the synthetic-assurance test recomputes
  the documented snapshot from the current candidate source tree and fails if
  a source change has not been accompanied by an evidence refresh.
- framework-integrated coverage: passed against the pre-existing local,
  clean Workspace Framework checkout at the exact recorded `v0.1.1` tag and
  commit. It created only temporary synthetic workspaces and did not perform a
  network recheck or alter the framework checkout.
- manual boundary check: passed for synthetic fixture inventory, no private
  workspace markers, no real-data input, no role-card/runtime claim, and no
  publication or runtime-parity claim.
- executor label: `local deterministic unittest runner; non-agent assurance implementation`
- actions not performed: No C4 authorization, tag, GitHub Release, push, merge, or runtime installation occurred.
- known limitations: no external platform check, hosted Release check, runtime
  installation, real-project input, real-data operation, secret-scanning
  service, signing, or technical immutable-release setting verification.
- next safe action: submit the candidate-only evidence for human review. A
  later exact-release decision must refresh all evidence from a clean commit,
  rerun integrated framework tests, and obtain C4 separately.

## Refusal Cases

The integrated route refuses to turn any of the following into a capability or
release claim: a missing or expired bounded authorization; unknown data access,
restriction, sharing, or online-service state; a role-card or agent-runtime
claim; a candidate-review reference reused as C4 authorization; a missing
framework tag/commit when integrated behavior is claimed; or a public tag used
to infer installed-runtime parity.
