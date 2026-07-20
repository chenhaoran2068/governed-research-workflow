# Release Notes Source: v0.8.1 Dependency And Lifecycle Maintenance

Status: candidate-only release-notes source. It does not establish publication,
installation eligibility, C4 authorization, or runtime identity. Verify a
selected version through its exact annotated tag and matching GitHub Release.

## Purpose

v0.8.1 is a maintenance source for the historical v0.8.0 bounded capability
scope. It corrects dependency wording, current-versus-historical lifecycle
wording, and selected-Release `system_version` semantics.

## Intended Changes

- state that explicitly invoked structural validators require the existing
  direct `jsonschema==4.26.0` dependency only;
- retain v0.8.0 Gate, evidence, rights-review, release-control, and notes as
  historical pre-C4 snapshots rather than current source identity;
- preserve exact tag plus matching GitHub Release verification for any selected
  public version; and
- record the selected Release's declared `system_version` without requiring it
  to be textually identical to the Git tag.

## What Does Not Change

No capability, dependency version, validator behavior, schema, template,
profile, Framework contract, helper, role, agent runtime, network action, data
action, CI architecture, scientific decision, compliance decision, project
Gate, submission action, or local runtime behavior changes.
