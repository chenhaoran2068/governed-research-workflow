# Bounded Non-Runnable Role Contracts

This reference describes the generic v0.8 role-contract record. A role
contract is a review-perspective boundary, not a runnable agent, scheduler,
background worker, separate AI actor, tool registry, or delegated authority.

## When It May Be Used

Use a role contract only when the caller explicitly asks for the named bounded
perspective and supplies inputs within that contract's declared input class.
The initial records are:

- `record_validation_reviewer`: structural review of one caller-supplied
  synthetic or metadata-only record against one named schema; and
- `audit_boundary_reviewer`: bounded findings about supplied public/package
  records, versions, claims, or evidence references.

The contract may produce a structural report or a bounded finding list only.
It cannot write a repair, execute a helper, retrieve external evidence, access
data, decide a conflict, or take an action because a finding was produced.

## Four Separate Controls

A role contract answers what the perspective may inspect, report, and refuse.
It cannot replace any of the following:

1. M53 bounded-autonomy authorization for a time-limited AI task;
2. controlled-helper admission for a named generic helper;
3. the exact preview, plan ID, filesystem checks, accountable-human reference,
   and per-run write confirmation required by one bootstrap run; or
4. data/share evidence, including access, sharing, ethics, DUA, release, or
   submission evidence.

If records conflict, stop the affected claim or action. Report the records,
known evidence, unknowns, safe immediate stop, realistic repair options and
tradeoffs, then await an accountable-human choice.

## Required Stops

Stop and escalate when the input is private, undisclosed, data-bearing,
out-of-boundary, missing a named schema, requires network retrieval, requests a
write or helper action, or asks for a scientific, compliance, access, Gate,
Release, or submission conclusion.

These records do not prove that an AI will always follow instructions or that
untrusted content cannot influence a conversation. Privileged actions require
their separate deterministic controls and human approval.
