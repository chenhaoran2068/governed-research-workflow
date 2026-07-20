# v0.8.1 Dependency And Lifecycle Maintenance Release Gate

Status: candidate-only release-gate record. It defines the evidence required
before a later C4 decision. It does not identify a candidate commit, authorize
C4, create a tag or GitHub Release, or establish an installation/runtime
identity.

## Intended Scope

v0.8.1 is maintenance-only. It may:

- clarify that explicitly invoked structural validators require the existing
  direct `jsonschema==4.26.0` dependency and no Framework or shared-service
  dependency;
- distinguish current v0.8.1 maintenance guidance from historical v0.8.0
  pre-C4 snapshots; and
- clarify selected-Release `system_version` recording without weakening the
  exact-tag-and-matching-GitHub-Release rule.

It must not add or alter a capability, dependency version, validator behavior,
schema, template, profile, Framework contract, helper, role, agent runtime,
network action, data action, CI architecture, scientific decision, compliance
decision, project Gate, submission, or local runtime.

## Required Evidence Before C4

1. exact clean ancestry from immutable `v0.8.0` and an allowlisted diff;
2. local positive and negative maintenance regressions with cache hygiene;
3. public-material, rights, privacy, secret, dependency, license, and release
   integrity reviews for the exact candidate;
4. exact-candidate CI on Windows, Ubuntu, and macOS after separate remote
   authorization; and
5. a separate C4 decision naming the exact protected-main commit, tag,
   release notes, and GitHub Release action.
