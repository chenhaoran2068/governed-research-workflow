# Release Control Record

## Purpose

`release_control_record.schema.json` defines a machine-checkable candidate
review record. `assets/release-control-record.template.json` is a synthetic
example. Neither document creates a Git tag, a GitHub Release, a security or
rights certification, an installation, or authority to publish.

## Record Hierarchy

The records below answer separate questions and must not substitute for one
another:

1. The capability truth ledger says whether a capability is planned, verified,
   excluded, or admitted for an exact release.
2. A release-control record says whether a candidate has the review material
   needed to request a later human release decision.
3. An exact C4 authorization says whether the accountable human has approved
   one commit, tag, release notes, and GitHub Release action.
4. A post-release verification record says whether the tag and hosted Release
   were actually checked after publication.

Candidate-review acceptance is not C4 authorization. C4 authorization is not
post-release verification. A local or remote candidate branch is not a
released version.

## Current-State Assertion Control

Before C4, review each current-facing source document, including the README,
roadmap, manifest, module index, capability ledger, release-status rule,
release notes, and relevant tests. A current-facing source document must not
declare that an exact version is the current, latest, or otherwise live public
release. It may describe its own source scope and explicitly labeled historical
tags or releases.

The only live public-availability statement is the exact annotated-tag and
matching-GitHub-Release check for the selected version. Treat a dynamic
current-version assertion as a release-blocking documentation defect. If it is
found after an immutable release, retain the historical release and make a
separate maintenance correction; never rewrite the tag or hosted Release.

## Candidate Snapshot Completeness

Before calculating a candidate source snapshot or recording final local test
evidence, stage exactly the intended public candidate files without committing
them. Confirm that the worktree has no unstaged candidate change and no
untracked public candidate file. The tracked-source snapshot deliberately uses
`git ls-files`; it cannot prove the identity of a new file that remains
untracked. Recalculate the snapshot after staging, and repeat affected tests
after any subsequent candidate-file change.

## Candidate Review Requirements

Record the exact candidate identity, capability-ledger outcome, public and
private material reviews, source/dependency authority, framework tag and
commit when integrated behavior is claimed, integrity posture, supported
profile/platform scope, residual risks, and incident/repair route.

`admitted_capability_ids` remains empty until exact-release admission is
separately established. A candidate record may contain verified-candidate and
explicitly excluded capabilities without implying public admission. Once an
accountable human has admitted a named future-release scope, set
`candidate_outcome` to `admitted_exact_release_scope` and list those IDs.
That still does not create C4 authorization, a tag, a GitHub Release, a normal
installation target, or an installed-runtime claim.

Unknown, blocked, or revise material-review states block any release claim.
Technical immutable-release status must be `enabled`, `deferred` with a reason
and re-evaluation trigger, `unavailable` with a reason and trigger, or
`unknown`. None of those labels claims a repository setting has been changed.

## C4 And Post-Release Route

Before C4, retain `c4_release_authorization_reference` as `null`. Before a
real release exists, retain `post_release_verification_reference` as `null`.
The final release route must verify the exact commit, intended tag, release
notes, material review, capability ledger, and CI evidence; obtain C4; create
the tag and GitHub Release through a separately authorized action; then verify
the hosted tag and Release independently.

## Boundaries

The record does not run secret scanning, call GitHub, change hosted settings,
sign artifacts, inspect a private workspace, or certify security, legal,
institutional, rights, scientific, clinical, ethics, privacy, DUA, or
compliance sufficiency. It records evidence and conditions for an accountable
human to review.

## Post-Release Route

After an actual C4-authorized publication, verify that the public tag resolves
to the approved commit, the GitHub Release uses that tag, the published notes
match the reviewed notes, the source archive contains only reviewed public
material, and the current release status is updated without rewriting history.
Record any discrepancy as a corrective candidate or withdrawal path, never as
a silent mutation of a published release.
