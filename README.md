# Governed Research Workflow

Governed Research Workflow is a thin, human-governed skill for starting and
routing research and manuscript work. It helps an AI agent identify the task,
load only relevant workflow guidance, record unknowns, and stop before
consequential decisions.

Status: `v0.7.0` release source retaining the released v0.6 workflow/evidence
control scope and adding a human-reviewed lesson-promotion control record
contract. It does not alter the v0.6 contract. This source tree does not itself
prove the release or installation identity of any selected version. A normal
public installation target exists only when an exact annotated tag and matching
GitHub Release resolve to the selected source commit. Never install a mutable
branch.

For the live release-verification procedure and retained historical snapshots,
read
[`CURRENT_RELEASE_STATUS.md`](system/11_distribution_installation_and_release/CURRENT_RELEASE_STATUS.md).

## Capability Truth

This source tree contains a single machine-checkable capability ledger at
`system/00_manifest_and_profiles/capability_truth_ledger.json`. It records
the historical `v0.4.0`, `v0.5.0`, and `v0.6.0` capability baselines, plus a
`v0.7.0` lesson-promotion scope. It records each
capability's interface, evidence, version, and required human approval. The
ledger is not an installed-runtime statement. Neither a historical admission
nor a v0.6 scope admission alone proves a local installation, runtime identity,
hosted Release, or C4 authorization.

The package manifest identifies this source as `v0.7.0` release-source content.
`GRW-CAP-060-01` remains verified for its named v0.6.0 public Release.
`GRW-CAP-070-01` is admitted only for its named v0.7.0 release scope. Neither
historical verification nor scope admission is an installation claim, hosted
Release claim, or C4 authorization. Public availability for any selected
version remains determined only by the exact-tag-and-matching-Release rule.

The v0.4 baseline includes the ledger, current-versus-historical release
boundary, bounded-autonomy authorization record, metadata-only provenance
register, release-control record contract, and synthetic assurance route. The
role-card and agent-runtime route remains explicitly excluded. The published
v0.5 baseline adds one metadata-only provenance register set with an explicit
read-only validator. Exact-final-commit evidence, C4 authorization, tagging,
and hosted-release verification remain separate for every future release; the
live release-verification rule, rather than this paragraph, decides whether a
selected version is released or installed.

README, SKILL, and module documentation explain routes and boundaries. The
ledger is the single capability truth source when those summaries conflict.

For a release decision, this source also provides a synthetic
release-control record contract at
[`RELEASE_CONTROL.md`](system/11_distribution_installation_and_release/RELEASE_CONTROL.md).
It separates candidate-review acceptance from C4 authorization of an exact
commit/tag/Release and from post-release verification. It does not publish or
certify a release.

This source also has a synthetic cross-record assurance route at
[`V0_4_SYNTHETIC_ASSURANCE.md`](system/12_synthetic_examples/V0_4_SYNTHETIC_ASSURANCE.md).
It tests only empty templates and public package records; it cannot prove
runtime parity, a hosted release, or release readiness.

It is Codex-first. The `v0.1.0` baseline was validated with the current Codex
workflow on Windows, and `v0.1.1` additionally forward-tested its new
retrospective route in an isolated Windows Codex session. It makes no
compatibility claim for every agent, platform, or operating system.

## Scope

The skill supports process routing for:

- new studies and feasibility planning;
- existing-study continuation and legacy-project bridging;
- manuscript drafting and reviewer revisions;
- declarations and AI-use documentation;
- source and citation control;
- retrospective learning.

It does not perform clinical decision-making, process patient data, certify
ethics or compliance, validate scientific results, make final conclusions, or
release or submit work. The v0.4.0 scope also explicitly excludes
specialist role cards, multi-agent orchestration, delegated authority, hidden
background work, and agent runtime. One Codex conversation remains the
interaction model; it may use different review perspectives without creating
separate agents.

The published v0.5.0 baseline additionally provides only a metadata-only
provenance register-set index and explicit structural validator. It does not read real
data, source locators, URLs, or credentials; it does not infer access,
permission, compliance, provenance truth, or scientific suitability.

The admitted v0.6 release scope adds only a metadata-only workflow/evidence
control bundle, optional baseline comparison, and read-only structural
validation. It records declared relationships and revision impact; it does not
open sources, establish semantic support, prove a human authorization, prevent
a same-authority rewrite, or decide scientific, compliance, Gate, submission,
or release status.

The v0.7 release-source scope adds only a metadata-only lesson-promotion
control bundle:
bounded observations, lesson candidates, represented human decisions, separate
integration verification, and visible correction, withdrawal, or supersession
events. It cannot automatically promote a lesson, modify any target, read
project material, or prove a human identity, actual authority, or target
correctness.

## Use

Ask the agent to use the skill when beginning or continuing a research task.
Provide a workspace path or explain that one does not yet exist. For
consequential new-study work, confirm the collaboration mode when asked.

The skill uses blank assets for an intake, collaboration-mode authorization,
feasibility brief, evidence register, claim register, reference audit,
submission route, project retrospective register, and public-boundary review.

## Package Structure

```text
SKILL.md                 # Stable AI entry and routing instructions
references/              # Active route guidance and bounded metadata controls
assets/                  # Blank output templates and bootstrap assets
scripts/                 # Explicitly invoked deterministic helpers
tests/                   # Safety and regression checks
agents/openai.yaml       # Codex-facing skill metadata
system/                  # Public 13-module architecture and release-source records
```

Read `system/INDEX.md` for the 13-module public-system map and
`SYSTEM_MANIFEST.yaml` for its declared profile. Current runtime behavior
remains the thin skill plus `references/`,
`assets/`, `scripts/`, and `tests/`. A module marked foundation is an intended
boundary, not a current capability.

## Release Status

`v0.2.1` hardens the controlled bootstrap path. A reviewed plan now binds the
selected workspace root's filesystem identity, so replacement of that root
invalidates confirmation. It also uses distinct stable fallback IDs for
non-ASCII-only titles, and CI dependencies are pinned to reviewed Action
commits.

`v0.1.1` adds a generic retrospective-learning reference and a blank
project-retrospective register. It contains only routing instructions,
references, and blank templates; it has no executable helpers.

`v0.2.0` adds an explicitly invoked
controlled empty-workspace bootstrap helper. It uses Python 3.11+ standard
library only, requires a no-write preview and matching human confirmation, and
creates only an empty generic workspace plus a receipt. It does not process
data, make research or compliance decisions, or run automatically when the
skill loads. It passed the repository CI matrix on Windows, Ubuntu, and macOS
with Python 3.11 and 3.14.

`v0.3.0` is the released bounded system-foundation baseline. Its exact
framework-integration evidence is against Workspace Framework `v0.1.0`.

`v0.3.1` is the published compatibility and release-governance maintenance
patch. It corrects earlier v0.3.0 candidate wording and validates the
framework-integrated profile against the exact released Workspace Framework
`v0.1.1` tag while retaining the `0.1.0` framework-contract version. Its
pre-release gate, material review, evidence, and release-note records are
retained as historical snapshots under
[`system/11_distribution_installation_and_release/`](system/11_distribution_installation_and_release/).

The historical local `v0.3.2` maintenance candidate separated current
installation guidance from retained historical snapshots. It was not published
and is retained as an input to the published `v0.4.0` release source; it is
not the current candidate identity or an installation target.

`v0.4.0` is the published governance-and-records release. It remains a
historical public baseline for this release source and is never modified in place.

`v0.5.0` is the published metadata-only Data And Provenance Register Set
baseline. Its historical preparation records are retained under
`system/11_distribution_installation_and_release/` and do not override the
exact-tag and matching-Release verification rule. `v0.5.1` corrects
release-state wording only; it does not change that capability contract.

`v0.5.1` is the published release-state-maintenance patch for the v0.5.0
capability contract. It is verified independently by its exact annotated tag
and matching GitHub Release; it is not evidence that this v0.6 release source,
a private source, or an installed runtime is current.

## Public Evolution Roadmap

This is a planning summary, not a promise or a statement that a future module
is already available. The accountable maintainer may split, defer, narrow, or
supersede a band through a reviewed revision.

- `v0.4.0`: published governance records and control foundations; no real-data
  handling, autonomous research, credentialed network activity, or agent
  runtime.
- `v0.5.0`: metadata-only provenance register set; no data-content handling,
  source-locator access, credentialed network activity, or permission/
  compliance decision.
- `v0.5.x`: only corrections or compatibility maintenance for the released
  `v0.5.0` contract.
- `v0.6.0`: reviewable workflow and evidence controls release source; public
  availability requires the exact-tag-and-matching-Release rule, and the
  system makes no scientific, compliance, journal, or submission decision.
- `v0.7.x`: human-reviewed retrospective learning and knowledge promotion; no
  automatic promotion of project observations.
- `v0.8.x`: portable profiles, stable interfaces, bounded role contracts, and
  controlled-tool admission; no delegated authority or multi-agent runtime.
- `v0.9.x`: dedicated evidence-integrity and supervisory-architecture audit;
  no perfect-truthfulness claim or AI final academic approval.
- `v0.10.x`: opt-in multi-machine learning and contribution-governance pilot;
  no hidden telemetry, automatic upload, or automatic rule promotion.
- `v0.11.x+`: pre-v1 scope closure and stabilization of every admitted module.
- `v1.0.0`: stable bounded public-system contract, only after its interface,
  evidence, support, and release conditions are met.
- `v1.1+`: separately reviewed post-v1 expansion; this roadmap grants no
  future capability automatically.

The detailed private planning baseline is not part of this public package.
The public package will add only generic, rights-cleared, reviewed material
for a band that has separately passed its release gate.

## Boundaries

Do not place restricted data, patient-derived data, credentials, unpublished
manuscripts, real project records, copyrighted source files, or personal
information in this skill or its issue tracker.

See SECURITY.md for responsible disclosure expectations and CONTRIBUTING.md
for contribution boundaries.

## License

Apache-2.0. See [LICENSE](LICENSE).
