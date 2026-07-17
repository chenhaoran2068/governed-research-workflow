# v0.3.2 Release-State Correction Candidate

Status: historical local maintenance candidate, superseded as a release input
by the local `v0.4.0` candidate. It has no public tag, GitHub Release, or
normal installation status. The locally recorded current published patch
baseline remains `v0.3.1`.

## Purpose

Correct stale v0.3.1 publication wording without rewriting the immutable
published v0.3.1 tag. This candidate updates current-facing package guidance
and labels v0.3.1 candidate-time records as historical snapshots.

## Scope

- set the source version to `0.3.2` without changing the `0.1.0` Workspace
  Framework contract or the v0.1.1 exact validation target;
- state that v0.3.1 is published and that normal installation selects an exact
  published tag with a matching GitHub Release;
- preserve v0.3.1 pre-release gate, evidence, rights-review, candidate, and
  release-note content with unambiguous historical labels; and
- replace regression checks that enforced obsolete v0.3.1 release-gated
  wording with checks for the current/historical distinction.

This candidate adds no research execution, data processing, network access,
credential handling, clinical processing, compliance determination, agent
runtime, migration, automatic release, or submission capability.

## Required Evidence Before Any Release Decision

1. The full local regression suite passes with exact Workspace Framework
   `v0.1.1` integration validation.
2. Documentation and tests distinguish current installation guidance from
   historical v0.3.1 candidate-time records without erasing either.
3. A fresh public-material, rights, and secret review covers the exact final
   candidate tree and newly reachable history.
4. The exact final candidate commit receives the required cross-platform CI
   evidence.
5. An accountable human separately approves or rejects any merge, tag, or
   GitHub Release action.

No item in this file authorizes those actions.

## Release Disposition

The accountable maintainer decided not to publish v0.3.2 as a separate public
release. This local candidate remains unmerged and unpushed as a reviewed
input to a future v0.4.0 candidate. No v0.3.2 tag, GitHub Release, or public
installation claim may be created. Until a later v0.4.0 release is approved,
v0.3.1 remains the current published patch baseline.
