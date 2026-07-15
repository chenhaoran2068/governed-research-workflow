# Specialist Agent-Contract Boundary

Status: foundation only; this directory defines no runnable specialist agent.

A future specialist-agent contract must define: purpose, owner, trigger,
required authoritative inputs, allowed outputs, prohibited actions, stop
conditions, human approval points, audit record, tool dependencies, and tests.

Examples of possible future roles include citation audit, external evidence
capture, manuscript boundary review, and submission-route preparation. A role
description alone does not authorize autonomous research, clinical,
compliance, release, or submission decisions.

Keep Codex UI metadata in `agents/openai.yaml`; do not place it here. The root
`SKILL.md` is the current thin entry and routing contract, not a specialist
agent implementation.
