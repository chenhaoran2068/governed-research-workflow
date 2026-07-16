# Release Notes: v0.3.1

Status: prepared release-note source. It becomes a public release statement
only if annotated tag `v0.3.1` and a matching GitHub Release are created from
the exact final tested commit.

## Scope

v0.3.1 is a patch-level compatibility and release-governance maintenance
release. It does not add research execution authority or change the system's
human-governed research boundaries.

## Changes

- Corrects source-branch wording so a release-gated source is not confused
  with an already published release.
- Distinguishes the `0.1.0` workspace-framework contract version from the exact
  Workspace Framework `v0.1.1` release used for v0.3.1 synthetic integration
  validation.
- Adds v0.3.1-specific public-material, release-gate, evidence, and release-
  note records.
- Generalizes the installation/update/rollback contract to exact released tags
  rather than mutable branches or a single historical version example.

## Validation

Before publication, the exact final commit must pass the full local regression
suite and the Windows, Ubuntu, and macOS GitHub Actions matrix with Python 3.11
and 3.14. The framework-integrated tests must use exact Workspace Framework
`v0.1.1`.

## Compatibility

- Codex-first routing skill and bounded public system foundation.
- Supports `standalone` and optional `framework_integrated` profiles.
- Retains the Workspace Framework `0.1.0` contract version.
- Uses Python 3.11+ only for the optional controlled empty-workspace bootstrap
  and test commands.

## Still Out Of Scope

- clinical decision-making or patient-data processing;
- scientific analysis, final research conclusions, or compliance certification;
- automatic external retrieval, login, download, migration, update, rollback,
  or release actions;
- agent runtime or autonomous submission capability;
- a fully hash-locked dependency supply chain; and
- GitHub technical immutable releases unless explicitly enabled and stated in
  the final GitHub Release.

## Install, Update, And Rollback

Use only an existing exact `v0.3.1` tag and matching GitHub Release after
publication. Follow `INSTALL_UPDATE_ROLLBACK.md`; do not install `main` as a
release identity. To roll back, detach to a prior reviewed exact tag and
revalidate without changing project data, workspace state, or bindings.

## Integrity

The final GitHub Release must name the exact annotated tag and commit, link to
the v0.3.1 evidence, state the technical immutable-release decision, and avoid
claims beyond the boundaries above.
