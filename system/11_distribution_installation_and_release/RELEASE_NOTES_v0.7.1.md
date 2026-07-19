# Release Notes: v0.7.1 Release-State And Control-Hardening Maintenance

Status: release-notes source. This file describes v0.7.1 scope and does not
itself establish publication, installation eligibility, C4 authorization, or
runtime identity. Verify a selected version through its exact annotated tag and
matching GitHub Release.

## Purpose

v0.7.1 is a documentation, release-state, and control-hardening maintenance
source for the historical v0.7.0 lesson-promotion control scope.

## What Changed

- corrects current source navigation that still classified v0.7 as a future
  candidate after its immutable release;
- makes the future roadmap begin after v0.7;
- updates current source metadata and module navigation to retain v0.7.0 as a
  historical capability/release fact; and
- adds regression tests that distinguish historical v0.7 assurance from the
  mutable maintenance source;
- refuses supplied review roots containing a symbolic-link or Windows
  reparse-point component, including an indirect ancestor; and
- adds a backward-compatible schema `1.1.0` representation in which a
  correction names a separate `confirm_correction` decision in the candidate's
  decision history.

## What Did Not Change

v0.7.1 does not add a new capability category, data access, external-service
action, a write helper, automatic promotion, target mutation, role card, agent
runtime, dependency, or local runtime installation behavior. It retains the
five record types and schema `1.0.0` readability.

## Installation And Verification

Install only a selected version whose exact annotated tag and matching GitHub
Release resolve to the same reviewed commit. Do not install `main`, an
untagged candidate branch, or an unreceipted local copy. A public release does
not prove a private canonical source or installed Codex runtime identity.
