# Bounded Autonomy Authorization

## Purpose

Human-governed interactive work is the default. A bounded-autonomy
authorization record is optional and only describes a narrow, time-limited
task that an accountable human has reviewed. It is a governance record, not an
executor, tool grant, compliance determination, or permission to use data.

The canonical structured record is
`assets/bounded-autonomy-authorization.template.json`, validated against
`system/09_schemas_records_and_templates/bounded_autonomy_authorization.schema.json`.
The Markdown intake worksheet is only a human decision aid.

## Before Requesting Bounded Autonomy

State the task, expected output, success criteria, risk level, allowed inputs,
allowed tool and action classes, output locations, excluded actions, evidence
requirements, budget, expiry, stop conditions, correction route, and
accountable approver. When a user has not supplied a field, present a small
set of relevant choices with a recommendation and tradeoff; do not silently
choose it.

Use human-governed interactive work when the task is not narrowly bounded, the
risk is unknown, a conclusion or consequential transition is requested, or a
required authorization is absent.

## Conditional Requirements

- File writes require approved directories, overwrite policy, and recovery
  route.
- Network or external-service work requires a service/source class,
  credential boundary, and explicit policy. This package supplies no automatic
  network, login, download, or retrieval executor.
- Data-bearing work requires a separate provenance or project record that
  states access, restriction, and sharing status. The task authorization and
  data-access/share evidence answer different questions and cannot substitute
  for one another.
- Unknown data restriction or access status permits only planning that does not
  access data content. It never becomes approval by inference.
- Delegation or multiple roles are prohibited for active v0.4 authorizations;
  v0.4 supplies neither role cards nor agent runtime.
- Medium or high risk requires a residual-risk statement and named review
  checkpoints.

## Status And Stop Rules

`active` means only that a human-approved record exists within its declared
boundary. It does not grant a tool, network, data, clinical, scientific,
compliance, release, submission, or publication authority.

Stop and return to the accountable human when the record is incomplete,
unapproved, expired, paused, revoked, out of scope, conflicts with another
record, requests a prohibited action, or encounters a critical unknown.
Record a specific diagnosis and route it to revision of the authorization or
the next human decision point; do not retry blindly.

## Review And Evolution

Reconsider the field set after an omission, near miss, material error, risk
increase, new tool or side effect, new external service, or relevant new
institutional, platform, data-access, journal, or legal requirement. A future
critical field does not retroactively make an earlier record compliant: the
record must be supplemented, expired, or reapproved.

## Boundary

The public v0.4 candidate contains record definitions and tests only. It does
not implement an autonomous executor, sandbox, scheduler, delegation system,
credential manager, data processor, or runtime enforcement mechanism.
