# Governed Research Workflow

Governed Research Workflow is a thin, human-governed skill for starting and
routing research and manuscript work. It helps an AI agent identify the task,
load only relevant workflow guidance, record unknowns, and stop before
consequential decisions.

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

## Release Status

`v0.1.1` adds a generic retrospective-learning reference and a blank
project-retrospective register. It contains only routing instructions,
references, and blank templates; it has no executable helpers.

The unreleased `v0.2.0` development candidate adds an explicitly invoked
controlled empty-workspace bootstrap helper. It uses Python 3.11+ standard
library only, requires a no-write preview and matching human confirmation, and
creates only an empty generic workspace plus a receipt. It does not process
data, make research or compliance decisions, or run automatically when the
skill loads. Public release requires completed tests, public-boundary review,
and separate maintainer authorization.

## Boundaries

Do not place restricted data, patient-derived data, credentials, unpublished
manuscripts, real project records, copyrighted source files, or personal
information in this skill or its issue tracker.

See SECURITY.md for responsible disclosure expectations and CONTRIBUTING.md
for contribution boundaries.

## License

Apache-2.0. See [LICENSE](LICENSE).
