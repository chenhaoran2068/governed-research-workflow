# Public System Module Index

Status: unreleased `v0.3.0-system-foundation` candidate

## Purpose

This directory is the architectural home for a future complete generic
research-collaboration system. The root `SKILL.md` remains the small AI entry
and routing layer. It must load only the module needed for the active task.

This index does not add new research capability. The active, tested `v0.2.1`
resources remain in `references/`, `assets/`, `scripts/`, and `tests/` until a
reviewed public-safe artifact is deliberately admitted to a module below.

## Module Boundaries

| Module | Owns | Does not own |
| --- | --- | --- |
| `governance/` | Generic human-control, authority, boundary, approval, and release controls. | Project facts, clinical decisions, or compliance certification. |
| `workflows/` | Reusable task sequences such as startup, feasibility, manuscript, citation, and submission work. | Project-specific execution history or final scientific conclusions. |
| `knowledge/` | Reviewed generic guidance, source pointers, provenance notes, and refresh rules. | Bundled restricted data, unlicensed source files, or permanent journal facts. |
| `agent-contracts/` | Future specialist-agent responsibilities, inputs, outputs, stop conditions, and tests. | Autonomous authority, hidden prompts, credentials, or unreviewed tool access. |
| `schemas/` | Generic, versioned record structures and validation contracts. | Live project state, patient data, or a claim that a schema is an approved protocol. |
| `examples/` | Synthetic or independently releasable demonstration material. | Real study data, unpublished text, project audit records, or identifiable case material. |

## Current Resource Map

| Existing path | Current role | Future module home when separately reviewed |
| --- | --- | --- |
| `references/` | Active route guidance used by `SKILL.md`. | `governance/`, `workflows/`, or `knowledge/` as appropriate. |
| `assets/` | Blank output templates and bootstrap assets. | Remains the output-resource location unless a future contract requires a different public-safe representation. |
| `scripts/` | Explicitly invoked deterministic helper code. | Remains executable tooling; future contracts may be documented in `agent-contracts/` or `schemas/`. |
| `tests/` | Regression and safety checks. | Remains test code; module-specific tests may be added when a module becomes active. |
| `agents/openai.yaml` | Codex-facing skill metadata. | Remains runtime metadata; it is not a specialist-agent contract. |

## Admission Rule

Do not create a module merely by copying a private rule or project artifact.
Before a new public module becomes active, it needs all of the following:

1. a reviewed generic rewrite or independently authored public artifact;
2. privacy, rights, provenance, and scope review;
3. an explicit owner, allowed use, stop conditions, and validation method;
4. a link from the appropriate route or package navigation; and
5. release approval with a versioned changelog entry.

Until then, a `MODULE.md` is a boundary definition, not an instruction to
invent missing content.

## Installation Boundary

A full public package may later be installed wherever a supported agent runtime
expects a skill package. It must remain self-contained and path-independent.
Do not require a private local checkout, private credentials, or a real project
workspace.
