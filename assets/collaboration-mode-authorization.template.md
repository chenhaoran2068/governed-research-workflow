# Collaboration-Mode Authorization Intake

This worksheet helps a human choose a collaboration mode. It is not the
canonical authorization record. A bounded-autonomy decision becomes active
only when the corresponding
`bounded-autonomy-authorization.template.json` record is complete, approved,
unexpired, and within scope.

## Request

- Project, workspace, or task reference:
- Requested by:
- Date:

## Default Choice

- [ ] `human_governed_interactive` (recommended when the work has material
  scientific, data, compliance, publication, cost, or uncertainty risk)
- [ ] Request a `bounded_autonomous_execution` record only for a narrow,
  reviewable task with explicit limits.

## Guided Choices For A Bounded Request

Choose only the entries that apply, and state why.

- Scope: one bounded task / a defined list of independent tasks / not yet
  bounded (stop and refine).
- Tool class: reasoning only / local document edits / local tests / manual
  public-rule retrieval. No tool class grants data access or network automation.
- Output location: no file output / a named empty or review directory / another
  location requiring separate approval.
- Budget: no budget is relevant / time limit / cost limit / iteration limit.
- Expiry: same-session review / fixed date-time / milestone review point.
- Stop condition: missing evidence / scope expansion / data-content request /
  external-service request / failed audit / other named condition.

## Required Human Decision

- Exact task and expected output:
- Success or acceptance criteria:
- Risk level and reason:
- Allowed inputs, tools, actions, outputs, and locations:
- Explicitly excluded actions:
- Evidence and audit record:
- Feedback and correction route:
- Expiry and next mandatory human decision:
- Accountable approver:
- Approval reference and time, if approved:

## Disposition

- [ ] remain human-governed interactive
- [ ] create or revise the canonical JSON authorization record
- [ ] decline or pause the bounded request
- Reason and next safe action:
