# Release Integrity Policy

Status: candidate policy for v0.3.0 and later releases. It defines a
maintainer-controlled process; it does not authorize an AI to publish.

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

This package has no runtime Python dependency. Historical v0.3.0
framework-integration evidence used validation-only packages declared by the
exact Workspace Framework v0.1.0 release. The release-gated v0.3.1 source
retains the v0.1.0 framework-contract version and tests the same declared
package ranges against exact Workspace Framework v0.1.1:
PyYAML>=6.0.2,<7 and jsonschema>=4.23,<5. Those ranges are not hash-locked, so
test-environment reproducibility is bounded rather than bit-for-bit. Neither
historical nor release-gated evidence may be described as a fully locked
software supply chain. A future release may add lockfiles or hash-verified test
dependencies only through a reviewed dependency-policy change.

Before release, run a tracked-tree and reachable-history secret scan using
the maintained pattern set, review all dependency and Action changes since the
previous release, and check GitHub security alerts available to the
maintainer. The public API did not expose a security_and_analysis status in
this candidate review, so this policy does not claim that GitHub Advanced
Security or any particular secret-scanning setting is enabled.

## Immutable Release Decision

Historical decision: technical immutable releases were deferred for v0.3.0.

Proposed v0.3.1 decision: retain the same deferral and immutable-by-policy
process unless the accountable maintainer explicitly enables GitHub technical
immutable releases before R31-G6. This is not a completed v0.3.1 decision
until that human approval is recorded.

Rationale:

- all prior public releases in this repository currently report as mutable;
- v0.3.0 and the proposed v0.3.1 distribute no binary assets, packages, or
  data, only a tagged source archive and documented skill/system material; and
- enabling a repository-level irreversible-release setting needs a deliberate
  maintainer operating and incident-withdrawal process, not an automatic
  change made while preparing this candidate.

Compensating controls for v0.3.0 and a deferred-v0.3.1 decision are: an
annotated exact tag, clean-tree and history checks, SHA-pinned Actions, final
matrix CI on main, explicit human authorization, published release notes with
commit identity, post-release tag verification, and a no-retag/no-silent-rewrite
policy.

This is not equivalent to GitHub technical immutability. The accountable
maintainer must reconsider enablement before every later minor release and
record either enablement or an updated deferral rationale. A future decision
to enable it does not retroactively make earlier releases technically
immutable.

## Integrity Evidence Boundary

The release evidence record may mark technical gates as passed only when it
links to concrete commands, review records, and CI runs. The applicable G6
requires human release authorization, and its G7 requires a real released tag
and GitHub Release. Neither may be simulated by a green candidate build or a
release-gated source branch.
