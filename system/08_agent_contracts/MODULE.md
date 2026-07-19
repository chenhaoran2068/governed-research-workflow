# Specialist Agent-Contract Boundary

Status: v0.8 pre-C4 release source. This directory contains two release-scope-admitted, non-runnable role contract records.
No runnable specialist agent is defined here.
This is not a runnable specialist-agent surface.
No role card, agent runtime, delegated authority, external-retrieval worker,
coordinator, or parallel-agent orchestration is defined here.

The two records are `record_validation_reviewer` and
`audit_boundary_reviewer`. Each defines purpose, owner, trigger, authoritative
inputs, allowed outputs, prohibited actions, stop conditions, human decision
points, audit record, tool/action boundary, memory boundary, non-claims, and
tests. They are generic records, not software actors.

The current interaction model remains one Codex conversation that may change
review perspective as needed. A role description alone does not authorize
autonomous research, clinical, compliance, release, submission, data access,
network retrieval, or file action.

The records do not replace M53 bounded-autonomy authorization, controlled
helper admission, a per-run write confirmation, data/share evidence, C4, or
any accountable-human decision. A later role card, coordinator, external
evidence retrieval role, runtime, or multi-agent design requires a separate
scope, threat model, tools boundary, tests, and human review.

Keep Codex UI metadata in `agents/openai.yaml`; do not place it here. The root
`SKILL.md` is the current thin entry and routing contract, not a specialist
agent implementation.
