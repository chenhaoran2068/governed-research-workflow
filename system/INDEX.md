# Public System Module Index

Status: release-state-neutral `v0.4.0` governance-and-records source. It is
an installation target only when an exact annotated `v0.4.0` tag and matching
GitHub Release can be verified. Users must select an exact published tag rather
than `main` or another mutable branch. See
`11_distribution_installation_and_release/CURRENT_RELEASE_STATUS.md`.

## Purpose

This is the modular architecture for a generic governed research system. The
root `SKILL.md` remains the thin AI entry and routing layer. It must load only
the route and module needed for the current task.

The system has a [system manifest](../SYSTEM_MANIFEST.yaml). It supports
`standalone` and a `framework_integrated` profile whose `0.1.0` framework
contract is validated against the exact released framework `v0.1.1` tag.

## Module Status

| ID | Module | Release status | Current public surface |
| --- | --- | --- | --- |
| `00` | manifest and profiles | active manifest; exact released-framework validation passed | root `SYSTEM_MANIFEST.yaml`, module records |
| `01` | governance and authority | active baseline | `SKILL.md`, route references |
| `02` | project workspace and bootstrap | active empty bootstrap; no automatic system installation | bootstrap script and assets |
| `03` | workflows | active baseline | route references and blank assets |
| `04` | evidence, requirements, and knowledge | active guidance; no knowledge corpus | evidence/citation references |
| `05` | data and provenance | metadata-only register candidate; no data handling | public data boundary and provenance route |
| `06` | memory and learning | active retrospective baseline | retrospective reference and asset |
| `07` | tools and integrations | active bootstrap tool; exact-tag integration regression test | `scripts/` and tests |
| `08` | agent contracts | v0.4 explicit exclusion: no role cards or agent runtime | future role-contract boundary only |
| `09` | schemas, records, and templates | blank-record baseline plus release-source capability and bounded-autonomy schemas | `assets/` templates and schemas |
| `10` | assurance, evaluation, and audit | active regression baseline, cross-repository integration, and release-source synthetic assurance | `tests/` |
| `11` | distribution, installation, and release | active release controls plus a release-control record that separates candidate review, C4, and post-release verification | package governance files, release verification, v0.3.1 historical release snapshots, and historical v0.3.2/v0.4 preparation records |
| `12` | synthetic examples | exact-tag integration test plus release-source cross-record assurance record | admitted release scope; no end-to-end public research example |

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

The system is designed to remain path-independent and standalone. Its
framework-integrated profile retains a `0.1.0` framework contract and is
validated against the exact released Workspace Framework `v0.1.1` tag. It must
never require a private checkout, private credential, or real project
workspace.
