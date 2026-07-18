# Release Notes: v0.6.1 Release-State Maintenance

Status: release-notes source. This file describes v0.6.1 scope and does not
itself establish publication, installation eligibility, C4 authorization, or
runtime identity. Verify a selected version through its exact annotated tag and
matching GitHub Release.

## Purpose

v0.6.1 is a maintenance source for the v0.6 Workflow And Evidence Control
Bundle. It removes a dynamic statement that an older patch was the current
published version and establishes a regression control against repeating that
error.

## What Changed

- makes current roadmap guidance version-neutral;
- adds a current-state assertion control to release governance;
- adds a regression test that current-facing source documents do not identify
  an exact version as current, latest, or live; and
- updates source identity and module documentation for the maintenance scope.

## What Did Not Change

v0.6.1 does not alter `GRW-CAP-060-01`, its six record types, validator,
schemas, templates, fixtures, `jsonschema==4.26.0` dependency, data boundary,
permissions, CI architecture, agent boundary, or local runtime installation
behavior.

## Installation And Verification

Install only a selected version whose exact annotated tag and matching GitHub
Release resolve to the same reviewed commit. Do not install `main`, an
untagged candidate branch, or an unreceipted local copy. A public release does
not prove a private canonical source or installed Codex runtime identity.
