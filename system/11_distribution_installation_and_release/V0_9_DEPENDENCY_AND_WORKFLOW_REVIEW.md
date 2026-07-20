# v0.9.0 Dependency, Workflow, And Source-Authority Review

Status: candidate release-preparation review. It records observed boundaries
for a later exact candidate and does not establish C4, a hosted Release, or
installed runtime identity.

## Direct Dependency And Validator Boundary

- The only direct runtime dependency remains `jsonschema==4.26.0`.
- `validate_integrity_audit_bundle.py` checks that exact installed version
  before schema validation and returns `not_assessed` when it is unavailable or
  different.
- The validator accepts one explicit absolute bundle path, reads that bundle
  and the bundled schema only, emits JSON to standard output, and returns a
  nonzero status for invalid or refused input.
- It has no networking client, Git invocation, directory enumeration, report
  file, cache, temporary file, recovery action, or write-capable helper path.

## Workflow And Platform Boundary

- `.github/workflows/test-bootstrap.yml` is read-only (`contents: read`) and
  pins `actions/checkout` and `actions/setup-python` by full commit SHA.
- The required matrix is Windows, Ubuntu, and macOS with Python 3.11 and 3.14.
- Framework-integrated tests remain bound to Workspace Framework `v0.1.2` at
  `97fbd1f4f3cbaabb2cdbb3e106c91a6c9fd8b3a8`; v0.9 adds no Framework runtime
  dependency and does not widen public profile support.
- The repository's protected `main` route currently requires all six named CI
  contexts, requires up-to-date branches and resolved conversations, and
  disallows force pushes and deletions.

## Integrity And Residual Risk

An observed prior immutable GitHub Release (`v0.8.1`) confirms that the
repository's release policy can produce immutable Releases. Each later Release
must still be checked independently for immutability, exact tag/commit
identity, and matching Release object. Repository secret scanning and push
protection are enabled; Dependabot security updates are currently disabled and
remain a visible residual risk rather than a pass.

The exact final candidate must refresh all observations above after any change
to dependencies, workflow, source, Release preparation, or protected-main
state.
