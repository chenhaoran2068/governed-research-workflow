# Governed Research Workflow

Governed Research Workflow is a thin, human-governed skill for starting and
routing research and manuscript work. It helps an AI agent identify the task,
load only relevant workflow guidance, record unknowns, and stop before
consequential decisions.

Status: local maintenance candidate version `0.3.2`. It is not a public
release or normal installation target. Install only an exact annotated tag with
a matching GitHub Release, never a mutable branch. The current published patch
baseline is `v0.3.1`; its tag and matching GitHub Release both exist. This
candidate repairs the released package's stale pre-release wording. It does not
add research execution authority or expand any human-approval boundary.

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
release or submit work.

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

The local `v0.3.2` maintenance candidate separates current installation
guidance from those retained historical snapshots. It has no public tag or
GitHub Release, and must complete its own review before any release decision.

## Boundaries

Do not place restricted data, patient-derived data, credentials, unpublished
manuscripts, real project records, copyrighted source files, or personal
information in this skill or its issue tracker.

See SECURITY.md for responsible disclosure expectations and CONTRIBUTING.md
for contribution boundaries.

## License

Apache-2.0. See [LICENSE](LICENSE).
