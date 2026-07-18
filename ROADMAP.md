# Roadmap

This roadmap records expected sequence, not delivery dates or promises. The
current worktree is an unreleased v0.6 candidate; the current published patch
is v0.5.1 and must be verified by its exact tag and matching GitHub Release.

## v0.5.1 (published release-state maintenance)

This maintenance revision corrects current-facing release-state wording after
the immutable `v0.5.0` publication. It does not alter the provenance-register
set validator, schemas, dependency, data boundary, permissions, or CI
architecture. A selected version is an installation target only after its own
exact annotated tag and matching GitHub Release are externally verified.

## v0.6.0 (unreleased workflow/evidence-control candidate)

The local v0.6 candidate proposes one metadata-only capability,
`GRW-CAP-060-01`: an opt-in six-record Workflow And Evidence Control Bundle,
optional canonical JSON baseline comparison, blank templates, synthetic
fixtures, and an explicitly invoked read-only structural validator.

It records declared assertions, evidence references, relationships, scoped
verification, human decision records, and revision/downstream-impact states.
It does not read data or source content, open URLs, establish semantic source
support, verify a human identity or actual authorization, prevent a process
with equivalent write authority from changing both a bundle and baseline, or
make a scientific, compliance, Gate, submission, or release decision.

The capability is not admitted in the ledger, not published, and not an
installation target. Exact candidate review, capability admission, remote CI,
C4 authorization, immutable tag/Release, and post-release verification remain
separate required steps.

## v0.5.0 (published metadata-only provenance register set)

This published baseline contains one accountable-human-admitted capability,
`GRW-CAP-050-01`: a bounded register index for v0.4-compatible metadata
records and an explicitly invoked read-only structural validator. It checks
only the supplied index and listed metadata JSON entries for schema shape,
safe paths, unique identities, and reciprocal declared lineage relationships.

The capability does not read data content, locate a source, resolve a URL,
contact a service, use credentials, calculate a data hash, infer permission,
or decide provenance truth, access, ethics, consent, DUA, privacy, legal,
clinical, scientific, Gate, submission, or release status. It requires the
fixed direct dependency `jsonschema==4.26.0` only for JSON Schema validation.

`GRW-CAP-050-01` is verified and admitted for the published v0.5.0 scope. Its
capability record is not an installed-runtime claim. The v0.5.0 tag and
matching GitHub Release must still be verified at the time of any installation;
future maintenance releases require their own exact-commit review, CI, C4,
immutable tag/Release, and post-release verification.

The immutable v0.5.0 Release retains some pre-C4 static wording. This v0.5.1
maintenance revision records that limitation and corrects the current-source
guidance without modifying the historical tag.

## Planned After v0.5.0 (not current capability)

- `v0.5.x`: corrective or compatibility maintenance only for the released
  v0.5.0 contract.
- `v0.7.x`: human-reviewed project learning and knowledge promotion; no
  automatic promotion from a project observation to a shared rule.
- `v0.8.x`: portable profiles, stable interfaces, bounded role contracts, and
  controlled-tool admission; no delegated authority or multi-agent runtime.
- `v0.9.x`: evidence-integrity and supervisory-architecture audit; no
  perfect-truthfulness claim or AI final academic approval.
- `v0.10.x`: opt-in multi-machine learning and contribution-governance pilot;
  no hidden telemetry, automatic upload, or automatic rule promotion.
- `v0.11.x+`: pre-v1 scope closure and stabilization. `v1.0.0` is a later
  evidence-and-stability threshold, not an automatic feature deadline.

## v0.4.0 (published governance-and-records baseline)

`v0.4.0` introduced the R40 capability truth ledger, release-state boundary,
bounded-autonomy authorization record, metadata-only single-entry provenance
register, release-control record contract, and synthetic assurance route. It
explicitly excludes named specialist role cards and agent runtime.

The release's capability admission, gate, evidence, rights review, and release
notes remain historical snapshots under
`system/11_distribution_installation_and_release/`. They explain the v0.4.0
decision but do not override the current exact-tag and matching-Release
verification procedure.

At every point in the release lifecycle, determine a normal installation
target using the exact-tag and matching-Release verification procedure in
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
as an input to the v0.4.0 release source, not as the current source identity
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
