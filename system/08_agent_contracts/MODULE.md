# Specialist Agent-Contract Boundary

Status: v0.4 explicit exclusion; this directory defines no named role card,
runnable specialist agent, agent runtime, delegated authority, or parallel
agent orchestration.

A future specialist-agent contract must define: purpose, owner, trigger,
required authoritative inputs, allowed outputs, prohibited actions, stop
conditions, human approval points, audit record, tool dependencies, and tests.

Examples of possible future roles include citation audit, external evidence
capture, manuscript boundary review, and submission-route preparation. A role
description alone does not authorize autonomous research, clinical,
compliance, release, or submission decisions.

The current interaction model is one Codex conversation that may change review
perspective as needed. That convenience must not be described as an operating
role card, separate agent, or additional tool permission. A future role card
requires its own name, purpose, owner, authoritative inputs, allowed outputs,
prohibited actions, stop conditions, human approval points, audit record, tool
dependencies, and tests before a later version can consider admission.

Keep Codex UI metadata in `agents/openai.yaml`; do not place it here. The root
`SKILL.md` is the current thin entry and routing contract, not a specialist
agent implementation.
