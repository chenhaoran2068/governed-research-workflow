# v0.3.0 System Foundation Release Gate

Status: historical pre-release gate. It prepared the published `v0.3.0`
release and is retained for traceability; it is not the current gate for the
unreleased `v0.3.1` candidate.

## Purpose

Define the evidence required before `v0.3.0-system-foundation` may merge into
`main`, receive tag `v0.3.0`, and receive a public GitHub Release.

## Historical Closure Note

`v0.3.0` was subsequently published on `2026-07-15`. Its annotated tag
resolves to `dae037aa1ce939c9403aa04959f63709c50ac4ea`, and the corresponding
GitHub Release is available at
`https://github.com/chenhaoran2068/governed-research-workflow/releases/tag/v0.3.0`.

The candidate and pending wording below preserves the pre-release gate state
as historical evidence. It must not be read as the live status of the
published v0.3.0 release or of the separate v0.3.1 candidate.

This gate is deliberately narrower than a claim that the package is a complete
research system. It governs a bounded **system foundation** release: a thin
human-governed entry skill, a documented module map, explicit profiles and
boundaries, blank public-safe assets, controlled bootstrap behavior, and
validated framework integration.

## Release Claim

If accepted, `v0.3.0` may claim only that it:

- provides a Codex-first thin entry skill and generic research-work routing;
- provides a 13-module system map that distinguishes active baseline material
  from deferred foundation-only modules;
- supports the documented `standalone` and `framework_integrated` profiles;
- validates `framework_integrated` against Workspace Framework `v0.1.0`;
- creates an empty standalone project scaffold only through its existing
  explicit, preview-and-confirm bootstrap helper; and
- remains human-governed for consequential research, compliance, and release
  decisions.

It must not claim a complete agent suite, clinical-data processing, external
data access, autonomous scientific judgment, submission authority, complete
journal knowledge, or automatic system installation.

## Versioning Rule

`v0.3.0` remains a pre-1.0 release. The public interface for this release is:

- `SKILL.md` trigger and stop behavior;
- documented bootstrap CLI arguments and receipt schema;
- root `SYSTEM_MANIFEST.yaml` fields;
- documented profile names and the `framework_integrated` compatibility value;
- public template paths named in documentation; and
- release/install/rollback instructions.

A backward-compatible bug fix after release uses a later `0.3.x` patch. A new
public feature or any material public-contract change uses `0.4.0`, even if it
is backward compatible. A new release must replace rather than alter a
published tag.

## Module Admission Policy

The following may remain **foundation-only** in `v0.3.0`, provided their
module records say so clearly and the release claim excludes their capability:

- `05_data_and_provenance`: no public clinical-data handling implementation;
- `08_agent_contracts`: no runnable specialist-agent implementation; and
- any unimplemented extension within `10_assurance_evaluation_and_audit`.

All remaining modules must have an accurate ownership boundary, public-safe
entry point or explicit existing surface, and no wording that implies an
unimplemented capability is available.

## Required Gates

The candidate evidence and operating records for these gates live beside this
file. They prepare a release decision; they do not replace R30-G6 human
authorization or R30-G7 post-release verification.

### R30-G1: Scope and Contract Freeze

Required evidence:

- `README.md`, `ROADMAP.md`, `system/INDEX.md`, and `SYSTEM_MANIFEST.yaml`
  agree on release name, public scope, profiles, limitations, and deferred
  modules;
- every public CLI, template, manifest field, and supported runtime is listed
  or linked as part of the public interface;
- each active module identifies owner, allowed output, stop condition, and
  validation surface; and
- a reviewer confirms that no release text presents a foundation-only module as
  an active capability.

Stop release when the claimed feature set cannot be stated in bounded language.

### R30-G2: Public Material and Rights Boundary

Required evidence:

- full tracked-tree scan for private paths, real project identifiers, patient
  material, credentials, unpublished material, and prohibited source copies;
- review of every newly admitted public document, template, script, and test
  fixture for provenance and redistribution rights;
- review of `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, and `.gitignore`; and
- no dependency on a private checkout, account, absolute local path, or private
  system for a supported profile.

Stop release for any unresolved privacy, copyright, DUA, credential, or
project-confidentiality issue.

### R30-G3: Installation and Profile Contract

Required evidence:

- a documented manual installation, update, and rollback procedure for both
  `standalone` and `framework_integrated` use;
- an explicit statement that no automatic system installer is included in
  `v0.3.0`;
- root-level `SYSTEM_MANIFEST.yaml` installed at the documented framework path;
- exact framework compatibility recorded as `0.1.0`; and
- failure behavior for missing, mismatched, unsafe, or unregistered workspace
  records.

Stop release if a new user cannot distinguish a safe installation step from a
research-project bootstrap, or cannot recover from a failed installation.

### R30-G4: Behavioral and Compatibility Evidence

Required evidence:

- skill structural validation;
- complete local test suite with and without framework-integration environment
  variables;
- GitHub Actions matrix success on Windows, Ubuntu, and macOS with Python 3.11
  and 3.14;
- cross-repository test that checks out the exact released framework `v0.1.0`
  tag,
  creates an empty framework workspace, installs only synthetic public package
  material, registers the system, and validates a synthetic project binding;
- negative tests for unsafe paths, wrong profile, mismatched compatibility, and
  unregistered primary system; and
- an explicit statement of what each test does not establish.

Stop release if any required matrix cell fails, skips a required scenario, or
depends on private material.

### R30-G5: Release Integrity and Security Review

Required evidence:

- action references are pinned to reviewed immutable commit SHAs or an
  equivalent documented policy;
- dependency and secret review results are recorded, including any accepted
  limitations;
- the release candidate has no unreviewed generated artifacts or untracked
  changes;
- release notes identify scope, compatibility, validation, deferred modules,
  known limitations, and upgrade/rollback information; and
- a documented decision on GitHub immutable releases: enable it, or record why
  it is deferred and what integrity controls remain in force.

Stop release for unresolved high-severity dependency, secret, provenance, or
tag-integrity issues.

### R30-G6: Human Release Decision

Required evidence:

- candidate branch is reviewed against `main` with all prior gates marked
  passed or explicitly deferred;
- a named accountable maintainer explicitly authorizes merge, tag, and release;
- `main` is tested at the exact intended release commit; and
- tag `v0.3.0` and GitHub Release are created only after the final CI result is
  successful.

The AI may assemble evidence and recommend a decision. It must not merge,
tag, or publish merely because the checklist is green.

### R30-G7: Post-Release Verification

Required evidence:

- release tag resolves to the intended `main` commit;
- GitHub Release notes and download source correspond to that tag;
- the candidate branch is retained or retired only through an explicit
  maintainer decision; and
- a new issue, defect, or compatibility observation becomes a reviewed
  candidate for a later version rather than a silent alteration of `v0.3.0`.

## Evidence Record Template

Record one row or section per gate:

```text
gate_id:
status: pass | fail | deferred
evidence:
  - command, artifact path, CI URL, or reviewed record
limitations:
owner_or_approver:
decision_date:
next_action:
```

`deferred` is permitted only for a capability explicitly excluded from the
`v0.3.0` release claim. It cannot defer a privacy, rights, integrity, profile,
or human-approval failure.

## Candidate Evidence Files

- `INSTALL_UPDATE_ROLLBACK.md`: manual profile lifecycle and refusal behavior.
- `PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.3.0.md`: candidate tracked-tree, privacy,
  provenance, and redistribution review.
- `RELEASE_INTEGRITY_POLICY_v1.md`: pinned-action, dependency, tag, and
  immutable-release decision.
- `RELEASE_NOTES_v0.3.0.md`: draft GitHub Release text with scope,
  compatibility, limitations, validation placeholders, and rollback route.
- `V0_3_RELEASE_EVIDENCE.md`: gate-by-gate evidence status. R30-G6 and
  R30-G7 remain pending until an accountable maintainer authorizes and then
  verifies an actual release.

## External Design Basis

- [Semantic Versioning 2.0.0](https://semver.org/) requires a declared public
  API and treats `0.y.z` as initial development, so this gate explicitly
  defines the smaller public contract rather than implying 1.0 stability.
- [GitHub releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
  are tag-based deployment artifacts; this gate therefore binds final CI,
  release notes, and post-release verification to one exact commit.
- [GitHub immutable releases](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases)
  protect tags and assets after publication; the gate requires an explicit
  adoption or deferral decision rather than silently assuming the setting.
- [GitHub build-security guidance](https://docs.github.com/en/code-security/tutorials/implement-supply-chain-best-practices/securing-builds?learn=end_to_end_supply_chain&learnProduct=code-security)
  emphasizes immutable releases, provenance, and protected workflow changes.

## Non-Goals

This gate does not set the future `1.0.0` threshold, create a specialist agent,
admit clinical-data processing, or authorize any real research project. Those
require independent scope, safety, rights, and evaluation decisions.
