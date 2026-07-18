# Release Integrity Policy

Status: active maintainer policy for v0.3.0 and later releases. It defines a
maintainer-controlled process; it does not authorize an AI to publish.

## Current-Status Routing

`CURRENT_RELEASE_STATUS.md` is the current-facing release-verification route.
It separates the live exact-tag and matching-Release check from retained
historical records and the unreleased local `v0.5.0` candidate. A candidate-
review record, passing test, local branch, or source tree is not an
installation target, GitHub Release, or installed-runtime identity.

## Release Identity

Each public release must be an annotated Git tag that resolves to one exact
tested main commit. The corresponding GitHub Release must use that same tag
and state its commit identifier, public scope, compatibility, validation,
deferred modules, known limitations, installation route, and rollback route.

Do not publish from an untagged branch tip. Do not force-update, delete and
replace, or silently alter a published version. A correction requires a new
version and a new release note. A security or rights issue may require a
withdrawal notice or later corrective release, but never a hidden rewrite.

## Candidate-To-Release Controls

1. Keep a release candidate either on a separate branch or explicitly marked
   as release-gated source on `main` until the applicable release gate's G1
   through G5 have evidence and an accountable maintainer performs its G6
   approval. A merge to `main` does not itself authorize a tag or GitHub
   Release.
2. Check the final candidate tree for a clean status, whitespace errors,
   dangling Git objects, prohibited material, and unreviewed generated files.
3. Run the full local test suite and the GitHub Actions matrix. The final
   intended main commit must receive its own successful matrix run before tag
   creation.
4. Create an annotated tag only after the maintainer approves the exact
   release commit. Create the GitHub Release only after the tag and its CI
   evidence are verified.
5. Verify the published tag, GitHub Release, source archive, and release
   notes after publication. Record any follow-up as a new issue or candidate,
   not as a release mutation.

## Workflow And Dependency Review

The public workflow is intentionally small and has read-only repository
permissions. Its actions/checkout and actions/setup-python references are
pinned to reviewed full commit SHAs. Any change to an Action reference must
identify the upstream release it represents, review the new immutable SHA, and
rerun the complete matrix.

Historical v0.3.0 framework-integration evidence used validation-only packages
declared by the exact Workspace Framework v0.1.0 release. The published v0.3.1
patch retained the v0.1.0 framework-contract version and tested the same
declared package ranges against exact Workspace Framework v0.1.1.

The v0.5 candidate adds direct runtime dependency `jsonschema==4.26.0` for
the explicitly invoked metadata-only register-set validator. It is pinned at
the direct-dependency level in `requirements.txt`, but its platform-specific
transitive dependency resolution is not hash-locked. The candidate must not be
described as a fully locked software supply chain. The exact resolved local and
CI environments must be recorded in v0.5 release evidence. Any dependency,
range, extra, lockfile, or runtime-use change requires a reviewed candidate
change and M48 revalidation.

Before release, run a tracked-tree and reachable-history secret scan using
the maintained pattern set, review all dependency and Action changes since the
previous release, and check GitHub security alerts available to the
maintainer. The public API did not expose a security_and_analysis status in
this candidate review, so this policy does not claim that GitHub Advanced
Security or any particular secret-scanning setting is enabled.

## Immutable Release Decision

Historical v0.3.0 decision: technical immutable releases were deferred.

Historical v0.3.1 decision: retain the same deferral and immutable-by-policy
process. GitHub technical immutable releases were not enabled before the
human-approved v0.3.1 release decision.

Historical v0.3 rationale:

- v0.1.x through v0.3.1 public releases then reported as mutable;
- v0.3.0 and v0.3.1 distribute no binary assets, packages, or
  data, only a tagged source archive and documented skill/system material; and
- enabling a repository-level irreversible-release setting needs a deliberate
  maintainer operating and incident-withdrawal process, not an automatic
  change made while preparing this candidate.

Compensating controls for v0.3.0 and the deferred v0.3.1 decision are: an
annotated exact tag, clean-tree and history checks, SHA-pinned Actions, final
matrix CI on main, explicit human authorization, published release notes with
commit identity, post-release tag verification, and a no-retag/no-silent-rewrite
policy.

The v0.3 compensating controls were not equivalent to GitHub technical
immutability. Their historical deferral does not prevent later enablement and
does not retroactively make v0.3 releases technically immutable.

## Integrity Evidence Boundary

The release evidence record may mark technical gates as passed only when it
links to concrete commands, review records, and CI runs. The applicable G6
requires human release authorization, and its G7 requires a real released tag
and GitHub Release. Neither may be simulated by a green candidate build or an
untagged source branch.

For the released `v0.4.0` scope, `RELEASE_CONTROL.md` remains the bounded
candidate-review record contract that was used before its exact C4 decision.
It is historical preparation material and did not itself authorize a tag,
GitHub Release, hosted-control change, or public claim.

On `2026-07-17`, the accountable human enabled GitHub technical immutable
releases for this repository. GitHub technical immutable releases are enabled
for future Releases. The setting applied to future Releases and is
part of the published `v0.4.0` release posture; it does not retroactively
change earlier v0.3.0/v0.3.1 Releases. Before any v0.5 C4 decision, the
release evidence must verify that the setting remains enabled and record the
result against the exact final candidate.
