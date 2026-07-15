# Public System Module Index

Status: unreleased `v0.3.0-system-foundation` candidate.

## Purpose

This is the modular architecture for a generic governed research system. The
root `SKILL.md` remains the thin AI entry and routing layer. It must load only
the route and module needed for the current task.

The candidate has a [system manifest](../SYSTEM_MANIFEST.yaml). It supports
`standalone` and a candidate-validated `framework_integrated` profile.
Framework compatibility remains non-release evidence until the validation is
repeated against an exact released framework version.

## Module Status

| ID | Module | Candidate status | Current public surface |
| --- | --- | --- | --- |
| `00` | manifest and profiles | active candidate manifest; integration validation pending released-framework retest | root `SYSTEM_MANIFEST.yaml`, module records |
| `01` | governance and authority | active baseline | `SKILL.md`, route references |
| `02` | project workspace and bootstrap | active empty bootstrap; no automatic system installation | bootstrap script and assets |
| `03` | workflows | active baseline | route references and blank assets |
| `04` | evidence, requirements, and knowledge | active guidance; no knowledge corpus | evidence/citation references |
| `05` | data and provenance | foundation only | public data boundary |
| `06` | memory and learning | active retrospective baseline | retrospective reference and asset |
| `07` | tools and integrations | active bootstrap tool; candidate integration test only | `scripts/` and tests |
| `08` | agent contracts | foundation only | role-contract boundary |
| `09` | schemas, records, and templates | active blank-record baseline | `assets/` templates |
| `10` | assurance, evaluation, and audit | active regression baseline plus candidate cross-repository integration | `tests/` |
| `11` | distribution, installation, and release | active candidate-release controls; stable integration pending tagged-framework retest | package governance files |
| `12` | synthetic examples | candidate integration test only | no admitted system example yet |

## Current Resource Map

| Existing path | Current role | Module relationship |
| --- | --- | --- |
| `references/` | Active route guidance used by `SKILL.md`. | Modules `01`, `03`, `04`, `06`, and `11`. |
| `assets/` | Blank output templates and bootstrap assets. | Modules `02`, `06`, and `09`. |
| `scripts/` | Explicitly invoked deterministic helper code. | Modules `02` and `07`. |
| `tests/` | Regression and safety checks. | Module `10`. |
| `agents/openai.yaml` | Codex-facing skill metadata. | Runtime metadata, not a specialist-agent contract. |

## Admission Rule

Before a foundation module becomes active, it needs a reviewed generic artifact,
privacy/rights/provenance review, explicit allowed outputs and stop conditions,
validation coverage, and a versioned release decision. A module directory alone
does not create capability.

## Framework Relationship

The system is designed to remain path-independent and standalone. Its candidate
framework-integrated profile has cross-repository test evidence, but a stable
release must validate against an exact released Workspace Framework tag. It
must never require a private checkout, private credential, or real project
workspace.
