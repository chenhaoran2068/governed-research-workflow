# Integrity Audit Bundle

## Purpose

`integrity_audit_bundle` is an opt-in, finite, metadata-only record for
reviewing declared identity relationships, evidence limits, correction links,
and operational-preflight records. It makes structural conflicts and unknowns
visible. It does not decide which record is true or what a human should do.

## Explicit Invocation

Run the validator only for one explicit absolute physical JSON path:

```text
python scripts/validate_integrity_audit_bundle.py --bundle ABSOLUTE_PATH_TO_BUNDLE.json
```

The validator opens only that bundle and its versioned schema. It rejects
relative paths, parent traversal, symbolic links, and Windows reparse points.
It does not enumerate a directory, follow a record reference, contact a host,
run Git, write a report, repair a worktree, or change a receipt or runtime.

`valid` means only that the named checker found the supplied bundle structurally
consistent with its schema and cross-record rules. It never proves scientific
truth, human authorization, hosted Release state, tamper-proof history, data
access, compliance, Gate passage, submission readiness, or installed-runtime
identity.

## Required Record Areas

1. `audit_scope` states the finite objective, declared input IDs, named
   checker, excluded surfaces, permitted tool boundary, and non-claims.
2. `audit_observations` record bounded match, mismatch, missing, stale,
   unknown, or out-of-scope observations. They are not inferences or decisions.
3. `audit_findings` connect observations to a structural routing label and a
   required human decision. A `stop_required` finding must visibly require a
   stop.
4. `audit_harness` binds the asserted structural result to the checker,
   fixture identity and class, environment, expected claim, deterministic or
   variable evaluation mode, attempt budget where variable evaluation is used,
   validity checks, skipped checks, and blind spots. A `passed` result requires
   `validity_status: valid`; changing the checker or fixture identity requires
   a new review rather than reuse of an earlier result.
5. `correction_reassessment_links` preserve a later human disposition and
   re-review relationship. They do not overwrite the original finding or close
   it automatically.
6. `operational_integrity_records` may record either a later outer-package
   change or a worktree-recovery preflight. They cannot replace an installation
   receipt, prove a runtime installation, or execute maintenance.

## Correction And Reassessment

An earlier finding remains part of the audit trail. To represent a later
change, add a `correction_reassessment_link` that identifies the prior finding
and affected identity, records a separately supplied accountable-human
disposition reference, names the later identity and allowed write scope, lists
declared downstream obligations, and records the latest re-review outcome.

Only a link with `latest_rereview_outcome: reviewed` can structurally support a
closed finding. This does not prove that the correction was correct or that the
human reference is genuine.

## Operational Preflight Boundary

For a worktree marked `active`, `locked`, or `unknown`, the record must set
`recovery_disposition: stop`. A `prunable` worktree can be recorded as needing
separately authorized maintenance only when its physical state is `missing`.
The record is a preflight description, not permission to invoke `git worktree
prune`, `repair`, deletion, or cleanup.

For a post-install outer-package change, preserve the original receipt
reference, owner, time, prior outer and runtime identities, change reason, and
the separately declared comparison method and scope. A later event never
rewrites the original receipt and never establishes a new installation by
itself.

## Safe Use

Use the public template and test fixtures only as synthetic structural
examples. A real project must retain its own data-access, authorization,
protocol, source-control, release, and submission authority. Do not place data
content, patient material, manuscript text, credentials, private paths,
receipts, or unpublished material in a public bundle.
