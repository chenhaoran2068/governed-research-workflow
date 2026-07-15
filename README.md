# Governed Research Workflow

Governed Research Workflow is a thin, human-governed skill for starting and
routing research and manuscript work. It helps an AI agent identify the task,
load only relevant workflow guidance, record unknowns, and stop before
consequential decisions.

The repository is also beginning an unreleased `v0.3.0-system-foundation`
candidate. The candidate preserves this thin entry skill while establishing a
modular home for future generic system content. It does not change the scope
of the current public release.

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
system/                  # Unreleased v0.3 module architecture
```

Read `system/INDEX.md` for the 13-module public-system map and
`SYSTEM_MANIFEST.yaml` for the candidate's declared profile. Current
runtime behavior remains the released thin skill plus `references/`,
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

The unreleased `v0.3.0-system-foundation` candidate maps the complete
13-module architecture and passed CI against the exact released Workspace
Framework `v0.1.0` tag. That is release evidence, not a workflow release: it
provides no specialist agents or knowledge corpus and does not change the
released `v0.2.1` runtime contract.

The candidate's release criteria are documented in
[`system/11_distribution_installation_and_release/V0_3_RELEASE_GATE.md`](system/11_distribution_installation_and_release/V0_3_RELEASE_GATE.md).
Its candidate manual installation, update, and rollback contract is in
[`system/11_distribution_installation_and_release/INSTALL_UPDATE_ROLLBACK.md`](system/11_distribution_installation_and_release/INSTALL_UPDATE_ROLLBACK.md).
Do not install this candidate as `v0.3.0` until a matching public tag and
GitHub Release exist.

## Boundaries

Do not place restricted data, patient-derived data, credentials, unpublished
manuscripts, real project records, copyrighted source files, or personal
information in this skill or its issue tracker.

See SECURITY.md for responsible disclosure expectations and CONTRIBUTING.md
for contribution boundaries.

## License

Apache-2.0. See [LICENSE](LICENSE).
