# v0.6.1 Release-State Maintenance Contract

Status: active maintenance-source contract. This record defines a narrow
documentation and release-control correction. It does not itself prove that
v0.6.1 has a hosted tag, GitHub Release, installation target, or installed
runtime.

## Scope

This revision removes the dynamic statement that `v0.5.1` was the current
published patch from current-facing roadmap guidance. It makes the roadmap
version-neutral and adds a release-control and regression-test rule that a
current-facing source document cannot declare an exact version to be current,
latest, or otherwise live. It also requires the exact public candidate files to
be staged before calculating a tracked-source snapshot, because an untracked
new file is outside the snapshot input set.

## Non-Goals

This revision does not alter `GRW-CAP-060-01`, its six record types, the
workflow/evidence-control validator, schemas, templates, fixtures,
`jsonschema==4.26.0` dependency, data-content boundary, permissions, workflow
behavior, CI architecture, agent boundary, or local Codex runtime.

## Stable Rule

For every selected version, a normal public installation target exists only
when an exact annotated tag and matching GitHub Release resolve to the selected
source commit. A source document, mutable branch, green CI run, capability
ledger, historical gate, or AI statement cannot substitute for that check.

## Historical Boundary And Repair Rule

Historical release records retain their labeled past state and must not be
rewritten. When a dynamic release-state assertion is discovered after an
immutable release, correct it through a separately reviewed maintenance
version, then repeat affected documentation, test, public-material, CI, C4,
and post-release checks.
