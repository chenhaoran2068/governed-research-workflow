# Roadmap

This roadmap records expected sequence, not delivery dates or promises.

## v0.4.0 (unreleased governance-and-records candidate branch)

This unreleased candidate branch is not a public release or normal installation target. It
contains the R40-00 capability truth ledger, R40-01 release-state boundary,
R40-02 bounded-autonomy authorization record, R40-04 metadata-only provenance
register, R40-05 release-control record contract, and R40-06 synthetic
assurance route. R40-03 explicitly excludes named specialist role cards and
agent runtime from `v0.4.0`.

All non-excluded records remain verified candidate records with public claims
forbidden. No `v0.4.0` capability becomes publicly claimable until an exact
candidate commit is verified, the capability is admitted, the accountable
human approves the exact release, and the tag and GitHub Release are created.

v0.4.0 explicitly excludes named specialist role cards and agent runtime. A
future version needs a separately reviewed named-role design before it can
describe any role card as an available public capability.

The unreleased candidate includes metadata-only provenance records with a generic
core and optional restricted or clinical awareness extension. It does not add
data import, processing, access, compliance, or certification capability.

It includes candidate-only release-control record definitions that distinguish
candidate review, C4 authorization, and post-release verification. These
records do not create a tag, GitHub Release, hosted-control change, or public
release claim.

The candidate includes a synthetic cross-record assurance route. It checks
only candidate records, empty templates, and public documentation; it does not
establish an installed runtime, hosted Release, or release readiness.

The C3 candidate-branch push and candidate CI are complete. The historical
pre-C3 preparation records remain useful context and must remain internally
consistent: `V0_4_CAPABILITY_ADMISSION.md`,
`V0_4_RELEASE_GATE.md`, `V0_4_RELEASE_EVIDENCE.md`,
`PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.4.0.md`, and
`RELEASE_NOTES_v0.4.0.md`. They are historical preparation materials, not a substitute
for exact-commit evidence or C4 authorization.

Until final exact-release admission and C4, the normal installation target is
the exact published `v0.3.1` tag. See
`system/11_distribution_installation_and_release/CURRENT_RELEASE_STATUS.md`.

## v0.3.2 (historical local release-state correction candidate)

This unpublished historical candidate:

- corrects current-facing documents that still describe published `v0.3.1` as
  release-gated or uninstalled;
- labels v0.3.1 candidate, gate, material-review, evidence, and release-note
  files as historical pre-release snapshots; and
- replaces tests that enforce stale candidate wording with tests that separate
  current installation guidance from preserved historical evidence.

It has no public tag or Release. Its release-state correction work is retained
as an input to the unreleased `v0.4.0` candidate, not as the current source identity
or installation target.

## v0.3.1 (released 2026-07-16)

This patch does not add workflow capability. It:

- corrected v0.3.0 candidate wording that had remained in the source branch;
- validated the framework-integrated profile against the exact released
  Workspace Framework `v0.1.1` tag while retaining the `0.1.0` framework
  contract version; and
- added patch-release material-review, gate, evidence, and release-note
  records.

The pre-release records for this published version are retained as historical
snapshots. They are not the current release state or normal installation
guidance.

## v0.3.0 (released 2026-07-15)

This release establishes the module boundaries for a future complete generic
research-collaboration system while keeping `SKILL.md` as the small entry and
routing layer.

- maps all 13 public system modules: manifest and profiles; governance;
  workspace and bootstrap; workflows; evidence and knowledge; data and
  provenance; memory and learning; tools and integrations; agent contracts;
  schemas and templates; assurance; distribution; and synthetic examples;
- adds a system manifest and module-boundary records, plus synthetic
  cross-repository framework-integration validation against the exact released
  framework `v0.1.0` tag;
- retains `references/`, `assets/`, `scripts/`, and `tests/` as the active
  `v0.2.1` implementation surface;
- adds manual installation, update, rollback, public-material review,
  release-integrity policy, and release-evidence records; these records do not
  authorize a merge, tag, or release;
- adds no new specialist agent, knowledge corpus, execution authority, or
  claim of compatibility; and
- is a bounded system-foundation release, not evidence that a full public
  system already exists.

## v0.2.1 (released 2026-07-14)

Patch release:

- bound reviewed bootstrap plans to the selected root's filesystem identity;
- hardened Windows reparse-point refusal in the local and public bootstrap
  designs;
- added stable, distinct fallback workspace IDs for non-ASCII-only titles;
- added regression coverage for root replacement, Windows junctions, and
  non-ASCII titles;
- pinned CI actions to reviewed full commit SHAs and added a job timeout;
- corrected released-version wording in contributor guidance.

## v0.2.0 (released 2026-07-14)

Minor release:

- added an explicitly invoked controlled empty-workspace bootstrap helper;
- added generic workspace, initial-state, and receipt templates;
- retained no-write preview, matching human confirmation, no-overwrite, and
  no-data-copy boundaries;
- added read-only CI coverage on Windows, Ubuntu, and macOS with Python 3.11
  and 3.14;
- added no clinical decision-making, patient-data processing, scientific
  analysis, compliance certification, or autonomous release capability.

## v0.1.1 (released 2026-07-14)

Maintenance release:

- added public retrospective-learning guidance;
- added a blank project retrospective and lesson register;
- clarified retrospective routing and public/private boundaries;
- retained the human approval requirement for any lesson promotion;
- added no executable helper, real-project content, or new compatibility claim.

## v0.1.0 (released 2026-07-14)

Initial public release:

- thin routing skill;
- five focused references;
- one workspace marker and eight blank templates;
- README, contribution, security, license, and ignore-file governance;
- human-governed default and explicit stop boundaries;
- no executable helpers.

This release completed material-boundary review and clean-environment
validation. It is Codex-first and does not claim compatibility with every agent
or operating system.

## Long-Term Direction (Not Current Release Scope)

The package may evolve from a thin startup skill into a complete, installable
generic research-collaboration system. In that future design, `SKILL.md`
remains a small AI entry and routing layer while detailed generic modules live
in clearly separated rules, workflows, templates, scripts, agent contracts,
knowledge/source-pointer, example, and test areas.

This direction does not authorize copying a private research workspace into
the public repository. A public system may contain only independently
understandable, generic, rights-cleared, privacy-reviewed, and validated
materials. Real project data, unpublished artifacts, restricted materials,
credentials, project-local audit records, and private memory remain outside
the public package.

Future journal support will provide a controlled procedure for retrieving and
recording current official requirements. It will not treat bundled journal or
publisher instructions as permanently current facts.

The intended distribution model is:

- a generic public system for external users;
- separately authorized private lab distributions where needed; and
- isolated workspaces for real studies.

No release is entitled to claim this complete-system scope until its included
modules, supported runtimes, tests, and public/private boundary have been
separately reviewed and released.

## Planned Candidates

Completed planned candidates are recorded in their release sections above.
`REL-008` was completed by the released `v0.3.0` system-foundation release on
`2026-07-15`; its historical gate remains available for traceability only.

| ID | Candidate | Earliest review | Promotion conditions |
| --- | --- | --- | --- |
| REL-002 | Bounded wording, link, template-field, or installation corrections | v0.1.x | Reviewed defect or feedback, material review, regression check, and release note. |
| REL-004 | Optional structured-record helpers for mode, state, route, or source registration | v0.3.0+ review | Public data model, privacy and migration review, tests, and demonstrated user need. |
| REL-005 | Contributor issue forms and dependency or security automation | deferred | A maintainer-owned support process and safe disclosure route. |
| REL-006 | Code of conduct and citation metadata | deferred | Deliberate term selection and maintainable enforcement or credit process. |
| REL-007 | Broader compatibility statement or 1.0.0 | unscheduled | Repeated clean-install evidence, stable contract, controlled release history, and explicit maintainer decision. |

## Not Public Capability Candidates

- clinical decision support;
- patient-data processing;
- autonomous scientific analysis;
- final scientific conclusions;
- autonomous compliance approval;
- autonomous manuscript or submission release;
- bundled databases, papers, journal instructions, or third-party skills;
- real-project demonstrations or project-derived content.

Any reconsideration requires a separate scope, rights, privacy, and safety
decision. It is not an automatic roadmap promotion.
