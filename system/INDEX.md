# Public System Module Index

Status: v1.9.2 public System-entry and route-code maintenance source
retaining the
frozen public-interface contract, `GRW-CAP-150-01`, and the historical
`GRW-CAP-160-01` public card library. It adds `GRW-CAP-170-01` as two generic
System-owned guidance documents, three public topics, and three selectively
read public cards, and `GRW-CAP-180-01` as generic future-Study lifecycle
guidance, blank metadata records, a read-only validator, and synthetic tests.
It retains `GRW-CAP-190-01`: generic natural-language new-Study navigation,
strengthened System-entry metadata, and a human-confirmable route
recommendation beginning `Route: <recommendation-code>` before methods,
lifecycle guidance, external sources, and project creation.
It declares only the exact Workspace Framework `v0.2.0`
contract and preserves the V1 Public Interface Manifest, Capability
Verification Map, and V1 Support Scope Matrix. It adds no intake, exchange,
data, retrieval service, execution, sharing, submission, automatic loading,
or agent-runtime capability. This index does not prove that a selected version
is released:
users must verify an exact annotated tag and matching GitHub Release rather
than install `main` or another mutable branch.
See `11_distribution_installation_and_release/CURRENT_RELEASE_STATUS.md`.

## Purpose

This is the modular architecture for a generic governed research system. The
root `SKILL.md` remains the thin AI entry and routing layer. It must load only
the route and module needed for the current task.

The system has a [system manifest](../SYSTEM_MANIFEST.yaml). It supports
`standalone` and a `framework_integrated` profile whose exact `0.2.0` framework
contract is validated for this source only against the released Workspace
Framework `v0.2.0` tag and commit
`69c76f84a5b0913b26c17ea48f152dbc50b4bec6`.

## Module Status

The [V1 Support Scope Matrix](00_manifest_and_profiles/V1_SUPPORT_SCOPE.md)
is the sole machine-readable authority for module-level support posture. This
table remains a readable architecture map; it must not be used to override the
matrix, capability ledger, release-verification, installation, or project
authority records.

| ID | Module | Release status | Current public surface |
| --- | --- | --- | --- |
| `00` | manifest and profiles | v1.9.2 retains the two public profiles, declares only exact Framework v0.2.0 compatibility, and strengthens generic new-Study System entry | root `SYSTEM_MANIFEST.yaml`, module records |
| `01` | governance and authority | active baseline | `SKILL.md`, route references |
| `02` | project workspace and bootstrap | active empty bootstrap; no automatic system installation | bootstrap script and assets |
| `03` | workflows | active baseline plus v0.6 record-control scope, v0.11 blank manuscript-governance templates, v1.5 optional guidance, and v1.7 collaboration guidance | route references, blank assets, and generic guidance |
| `04` | evidence, requirements, and knowledge | active guidance plus v0.6 pointer/relation-record scope; no knowledge corpus or v0.11 source service | evidence/citation references |
| `05` | data and provenance | v0.4 metadata-only register plus published v0.5 register set; no data handling | public data boundary, provenance routes, and read-only validator |
| `06` | memory and learning | active retrospective baseline plus historical v0.7 promotion, v0.10 package-review, v0.10.1 synthetic exchange boundaries, v0.10.2 human-mediated future-direction boundary, v0.11 generic public experiences, v1.6 public-safe cards, and v1.7 public collaboration cards | retrospective/promotion, experience-pilot, and public-experience references |
| `07` | tools and integrations | active bootstrap plus explicit read-only validators; no new writer, intake, transfer, or user-facing contribution helper | `scripts/`, admission records, and tests |
| `08` | agent contracts | release-scope-admitted non-runnable role contracts; no role cards or agent runtime | two role-contract records and boundary guidance |
| `09` | schemas, records, and templates | blank-record baseline plus v0.8/v0.9 controls, v0.10 experience package, v0.10.1 synthetic exchange receipt schema, and v0.11 Markdown templates; v0.11 adds no standalone schema or validator | `assets/` templates and schemas |
| `10` | assurance, evaluation, and audit | regression baseline plus v0.10/v0.10.1 synthetic path/no-write/receipt controls, v0.10.2 wording controls, v0.11 template/experience-boundary checks, and v0.12 synthetic cross-module assurance | `tests/` |
| `11` | distribution, installation, and release | active release controls, historical v0.7.1/v0.8 records, and v0.9 release-preparation records that separate candidate review, C4, and post-release verification | package governance files, release verification, historical and active preparation records |
| `12` | synthetic examples | exact-tag integration test plus retained assurance, v0.8 synthetic-contract tests, and a v0.11 fictional manuscript-governance illustration | synthetic fixtures and assurance only; no end-to-end public research example |

## Current Resource Map

| Existing path | Current role | Module relationship |
| --- | --- | --- |
| `references/` | Active route guidance used by `SKILL.md`. | Modules `01`, `03`, `04`, `05`, `06`, and `11`. |
| `assets/` | Blank output templates and bootstrap assets. | Modules `02`, `05`, `06`, and `09`. |
| `scripts/` | Explicitly invoked deterministic helper code. | Modules `02`, `05`, and `07`. |
| `tests/` | Regression and safety checks. | Modules `05`, `10`, and `12`. |
| `agents/openai.yaml` | Codex-facing skill metadata. | Runtime metadata, not a specialist-agent contract. |

## Retained v1.5 Optional Guidance

The [manuscript operational checklists](03_workflows/MANUSCRIPT_OPERATIONAL_CHECKLISTS.md)
and [research-program boundary and shared-materials control](03_workflows/RESEARCH_PROGRAM_BOUNDARY_AND_SHARED_MATERIALS_CONTROL.md)
are generic guidance for caller-named work. They do not create a project,
access material, grant cross-work-unit access, establish a fact or authority,
or authorize submission.

## Admission Rule

Before a foundation module becomes active, it needs a reviewed generic artifact,
privacy/rights/provenance review, explicit allowed outputs and stop conditions,
validation coverage, and a versioned release decision. A module directory alone
does not create capability.

## Framework Relationship

The system is designed to remain path-independent and standalone. Its
framework-integrated profile declares only the exact `0.2.0` framework contract
for this source. The v1.6.0 source retains validation against the exact released
Workspace Framework `v0.2.0` tag and commit
`69c76f84a5b0913b26c17ea48f152dbc50b4bec6`; it must never require a private
checkout, private credential, or real project workspace.
