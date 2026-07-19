# v0.8.0 Dependency, Workflow, And Repository-Control Review

Status: active candidate technical-review record. It records current evidence
and visible limitations for v0.8 preparation. It does not certify a hosted
setting, dependency security, C4 authorization, or publication.

## Dependency And Workflow Surface

- The candidate introduces no dependency or lockfile change. The only declared
  runtime dependency remains `jsonschema==4.26.0`.
- The candidate introduces no workflow change. The workflow keeps read-only
  `contents` permission, SHA-pinned `actions/checkout` and
  `actions/setup-python`, a ten-minute job timeout, and the six-context matrix
  of Windows, Ubuntu, and macOS with Python 3.11 and 3.14.
- Framework-integrated validation checks out the exact public Workspace
  Framework `v0.1.2` commit
  `97fbd1f4f3cbaabb2cdbb3e106c91a6c9fd8b3a8`.

## Remote Candidate Evidence

GitHub Actions run `29680656435` passed all six contexts for implementation
commit `49102f9da068b290e311f63437351d1e1ce220e7`. This evidence must be
repeated for the exact candidate named by the separate C3 record.

## Repository Controls And Known Limitations

- `main` requires a pull request, strict up-to-date status checks for all six
  CI contexts, resolved conversations, and blocks force-pushes and deletions.
- GitHub Secret Scanning and push protection are enabled. The review observed
  zero open secret-scanning alerts.
- Dependabot alerts are disabled and code scanning has no analysis configured.
  They are residual visibility limitations, not passing security controls.
- The current authenticated read-only API scope cannot independently retrieve
  the repository's immutable-release or Actions SHA-pinning settings. Their
  current settings must be reconfirmed through GitHub settings or a properly
  scoped maintainer token before C4; do not infer them from this record.

## C4 Refresh Requirement

Before C4, repeat the dependency diff, workflow diff, security-alert query,
protected-main review, source snapshot, and exact CI check for the selected
post-merge commit. Any change after that review restarts the affected checks.
