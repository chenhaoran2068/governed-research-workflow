# v0.7.1 Release-State And Control-Hardening Maintenance Contract

Status: maintenance-source contract. This record defines a narrow current
source navigation, roadmap correction, and read-only control hardening. It does
not itself prove a hosted tag, GitHub Release, installation target, installed
runtime, or C4 approval.

## Scope

This revision corrects current source records that still listed v0.7 as a
future candidate after the immutable v0.7.0 publication. It makes future
roadmap wording begin after v0.7, marks v0.7.0 capability material as
historical, aligns source metadata and module navigation, adds regression
checks against restoring stale wording, rejects supplied review roots with
symbolic-link or Windows-reparse-point ancestors, and adds a backward-compatible
schema `1.1.0` form for separately represented correction review.

## Non-Goals

This revision does not add data-content access, external-service action, a
write helper, automatic promotion, target mutation, a role card, agent runtime,
new dependency, or local Codex runtime installation behavior. It preserves the
five record types and historical schema `1.0.0` readability while strengthening
the existing validator and adding schema `1.1.0`-only correction-review fields.
It does not modify the immutable v0.7.0 tag or GitHub Release.

## Stable Rule

For every selected version, a normal public installation target exists only
when an exact annotated tag and matching GitHub Release resolve to the selected
source commit. Source documents, mutable branches, green CI, a capability
ledger, historical evidence, or an AI statement cannot substitute for that
check.

## Repair Rule

Historical release records retain their labeled past state and must not be
rewritten. If a current-source navigation or release-state defect is found
after an immutable release, correct it through a separately reviewed
maintenance version and repeat affected documentation, regression tests,
public-material review, CI, C4, and post-release verification.
