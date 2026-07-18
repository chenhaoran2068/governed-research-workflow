# Release Notes: v0.5.0 Release-Source Draft

Status: release-source draft. These are not published GitHub Release notes and
do not authorize a tag, GitHub Release, installation, or C4. They must be
reconciled with the exact final-commit evidence and C4 decision before
publication.

## Intended Scope

v0.5.0 has one accountable-human-admitted bounded capability:
`GRW-CAP-050-01`, a metadata-only Data And Provenance Register Set. It
provides a register-index schema, blank index template, synthetic valid and
invalid examples, compatibility guidance, and an explicitly invoked read-only
structural validator for v0.4-compatible metadata entries.

The validator checks only declared metadata structure: JSON/schema validity,
safe relative paths, duplicate identities, and reciprocal declared lineage. It
returns `valid`, `invalid`, or `not_assessed`; `valid` does not mean that a
dataset exists, is accessible, is authorized, is compliant, or is scientifically
appropriate.

## Intended Boundaries

The release source does not read data content, locate a source, resolve a URL,
contact a service, use credentials, hash, copy, clean, analyse, upload, or
share data. It does not decide data permission, ethics, consent, DUA, privacy,
legal compliance, provenance truth, scientific suitability, project state,
Gate status, journal requirements, submission, or release status.

It adds no agent runtime, specialist role card, multi-agent orchestration,
delegated authority, hidden background work, or automatic local runtime
installation. It requires Python `3.11+` and the direct validation dependency
`jsonschema==4.26.0`; this is not a hash-locked full supply-chain claim.

## Validation To Be Recorded Before Publication

- exact clean candidate commit and reviewed diff from `v0.4.0`;
- complete local suite with exact dependency and Workspace Framework `v0.1.1`
  integration evidence;
- GitHub CI on Windows, Ubuntu, and macOS for Python 3.11 and 3.14 on the
  exact intended release commit;
- final material/rights, dependency, workflow, public-surface, and
  release-integrity review;
- accountable-human admission or exclusion decision for `GRW-CAP-050-01`; and
- accountable-human C4 authorization for the exact commit, tag, notes, and
  GitHub Release.

## Installation And Rollback

After publication, users must install only the exact `v0.5.0` tag and matching
GitHub Release. They must not install `main`, an untagged candidate branch, or
this draft. Update and rollback behavior remains governed by
`INSTALL_UPDATE_ROLLBACK.md`; neither action may alter project data, workspace
state, or private bindings.
