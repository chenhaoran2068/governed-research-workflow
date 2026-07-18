# Release Notes: v0.5.1 Release-State Maintenance

## Purpose

v0.5.1 is a maintenance revision for the published v0.5.0 metadata-only Data
And Provenance Register Set. It corrects current-source wording that could
mistakenly describe the already published v0.5.0 tag and GitHub Release as
unreleased or non-installable.

## What Changed

- marks v0.5.0 as the published provenance-register capability baseline;
- makes the exact annotated-tag plus matching-GitHub-Release check the stable,
  version-neutral installation rule;
- separates current guidance from retained pre-C4 v0.5.0 gate, evidence,
  rights-review, admission, release-note, and synthetic-assurance snapshots;
- updates supported-version and capability-ledger wording; and
- adds regression coverage against reintroducing current-facing false
  "unreleased", "no Release", or "not an installation target" statements for
  an already published version.

## What Did Not Change

v0.5.1 does not alter `GRW-CAP-050-01`, the provenance-register-set validator,
schemas, fixtures, `jsonschema==4.26.0` direct dependency, data-access
boundary, permissions, workflow architecture, CI architecture, role-card
exclusion, or local runtime installation behavior.

## Installation And Verification

Install only a selected version whose exact annotated tag and matching GitHub
Release resolve to the same reviewed commit. Do not install `main`, an
untagged candidate branch, or an unreceipted local copy. Public installation
does not prove a private canonical source or installed Codex runtime identity.

## Historical v0.5.0 Note

The immutable v0.5.0 Release retains the pre-C4 wording that prompted this
maintenance revision. It is not rewritten. Its actual release identity is
verified from its annotated tag and matching GitHub Release, not from the
historical draft text.
