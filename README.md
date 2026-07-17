# Governed Research Workflow

Governed Research Workflow is a thin, human-governed skill for starting and
routing research and manuscript work. It helps an AI agent identify the task,
load only relevant workflow guidance, record unknowns, and stop before
consequential decisions.

Status: release-state-neutral `v0.4.0` source. This source tree does not claim
that a hosted `v0.4.0` Release already exists. A normal public installation
target exists only when an exact annotated `v0.4.0` tag and matching GitHub
Release exist and resolve to the selected source commit. Never install a
mutable branch. This source does not add research execution authority or
expand any human-approval boundary.

For the live release-verification procedure and retained historical snapshots,
read
[`CURRENT_RELEASE_STATUS.md`](system/11_distribution_installation_and_release/CURRENT_RELEASE_STATUS.md).

## Capability Truth

This release-state-neutral source contains a single machine-checkable capability ledger at
`system/00_manifest_and_profiles/capability_truth_ledger.json`. It records
what the `v0.4.0` release source may claim, what it must not claim, its
interface, evidence, version, and required human approval. The ledger is not
a live hosted-release statement. It records the accountable-human Option A
admission of ten named capabilities for the `v0.4.0` release scope; that
admission is not a tag, GitHub Release, normal installation target, runtime
claim, or C4 authorization.

The package manifest and current installation narrative identify this source
as release-state-neutral `v0.4.0` content. The ledger's target is a planning
and verification boundary, not by itself a public release statement or
installation claim.

R40-00 through R40-06 have completed implementation review: the ledger,
current-versus-historical release boundary, bounded-autonomy authorization
record, metadata-only provenance register, release-control record contract,
and synthetic assurance route are present. The role-card and agent-runtime
route is explicitly excluded from `v0.4.0`. The remaining ten records are
admitted only for the named release scope. Exact-commit evidence, C4
authorization, tagging, and hosted-release verification are separate steps;
the live release-verification rule, rather than this paragraph, decides whether
they have occurred.

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
references/              # Active v0.2.1 route guidance
assets/                  # Blank output templates and bootstrap assets
scripts/                 # Explicitly invoked deterministic helpers
tests/                   # Safety and regression checks
agents/openai.yaml       # Codex-facing skill metadata
system/                  # Public v0.3 module architecture
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
and is retained as an input to this local `v0.4.0` candidate; it is not the
current candidate identity or an installation target.

## Public Evolution Roadmap

This is a planning summary, not a promise or a statement that a future module
is already available. The accountable maintainer may split, defer, narrow, or
supersede a band through a reviewed revision.

- `v0.4.x`: governance records and control foundations; no real-data handling,
  autonomous research, credentialed network activity, or agent runtime.
- `v0.5.x`: reviewable workflow and evidence controls; no scientific,
  compliance, journal, or submission decision by the system.
- `v0.6.x`: human-reviewed retrospective learning and knowledge promotion; no
  automatic promotion of project observations.
- `v0.7.x`: portable profiles, stable interfaces, bounded role contracts, and
  controlled-tool admission; no delegated authority or multi-agent runtime.
- `v0.8.x`: dedicated evidence-integrity and supervisory-architecture audit;
  no perfect-truthfulness claim or AI final academic approval.
- `v0.9.x`: opt-in multi-machine learning and contribution-governance pilot;
  no hidden telemetry, automatic upload, or automatic rule promotion.
- `v0.10.x+`: pre-v1 scope closure and stabilization of every admitted module.
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
