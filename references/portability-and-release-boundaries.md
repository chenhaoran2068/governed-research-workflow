# Portability And Release Boundaries

## Public And Private Separation

Keep project data, restricted materials, credentials, unpublished manuscripts,
source PDFs, reviewer correspondence, project audit records, personal memory,
and private paths outside this public skill.

Before moving any candidate material into a public package, classify it as:

- generic concept suitable for independent rewrite;
- blank template suitable for new creation;
- design reference only;
- excluded.

Use assets/public-boundary-review.template.md. Public eligibility is not
authorization to copy, publish, or release.

## Legacy Projects

Do not assume a legacy project followed this workflow from the beginning.
Before connecting it to a governed workspace, record the known history,
missing records, current authoritative sources, restrictions, and next safe
action. Selectively inventory and copy only what is justified; do not bulk
migrate or silently declare compliance.

## Retrospective Learning

Keep observations project-local until they are reviewed. For retrospective
scope, evidence, promotion, and closure controls, use
`references/retrospective-learning.md`. Do not automatically promote an
observation to shared or public guidance.

## Public Release

A public release requires material-level privacy, rights, provenance, and
boundary review; clean-environment validation; a real security-report route;
and explicit approval for repository visibility, tag, and release. A public
package must never overwrite a private workflow system or installed local
runtime.

Executable helpers require an additional review of input boundary, destination
boundary, overwrite behavior, partial-failure cleanup, tests, dependencies,
platform claims, and whether the helper could read, copy, or expose private
material. A helper must be independently written for the public package; it
must not be a wrapper around a private implementation.
