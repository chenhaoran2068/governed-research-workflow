---
name: governed-research-workflow
description: Start or continue governed research and manuscript work. Use for new or existing studies, manuscript drafting, reviewer revisions, declaration or AI-use work, citation control, feasibility planning, and research retrospectives. Classify the request, use the relevant local records and templates, keep humans in control of consequential decisions, and stop before unsupported scientific, clinical, compliance, or submission actions.
---

# Governed Research Workflow

Use this skill to route and structure research work. It is a process layer, not
a scientific execution engine, clinical decision tool, compliance authority, or
submission service.

Do not infer missing study facts, create a final scientific conclusion, certify
compliance, or release or submit material.

For exact local candidate capability status, consult
`system/00_manifest_and_profiles/capability_truth_ledger.json`. A planned,
candidate, forbidden, unknown, or contradictory ledger entry does not
authorize a behavior. The ledger does not replace the accountable-human
approval required for consequential work.

For current public installation identity, historical release records, and the
local candidate boundary, consult
`system/11_distribution_installation_and_release/CURRENT_RELEASE_STATUS.md`.
Do not infer an installed runtime version from a public tag, candidate branch,
or capability-ledger entry.

For a future release review, consult
`system/11_distribution_installation_and_release/RELEASE_CONTROL.md`.
Candidate-review acceptance does not authorize C4 publication or establish
post-release verification.

## Start Safely

1. Identify the stated workspace or ask for one. Do not broadly scan disks,
   accounts, drives, or unrelated folders.
2. Identify the request class before substantive work:
   new study, existing-study continuation, legacy-project bridge, manuscript
   continuation, reviewer revision, declarations or AI-use, citation work, or
   retrospective learning.
3. State known facts, unknowns, source records available, and the next allowed
   action.
4. Read only the reference and blank asset needed for the selected route.

For a new study or other consequential research work, ask the user to confirm
the collaboration mode before analysis, project creation, or substantial
generation. Human-governed interactive work is the default, but must still be
confirmed for the current study.

For an explicitly requested new empty workspace, use the controlled bootstrap
route in `references/controlled-bootstrap.md`. First run the no-write preview;
then wait for human approval of that exact plan before invoking the helper with
the matching plan ID and approval reference. Do not invoke the helper merely
because this skill triggered. The helper creates an empty scaffold only and
does not authorize consequential research work.

For existing-study, legacy-project, manuscript, or revision work, require an
exact workspace path or project root before reading project-local records. A
pasted excerpt may clarify the task after the root is identified; it does not
replace the project location.

## Collaboration Modes

Use human-governed interactive work unless the user provides an explicit,
scope-limited authorization for bounded autonomous execution.

An authorization for bounded autonomous execution must identify the task,
allowed inputs and outputs, excluded actions, evidence requirements, stop
conditions, feedback route, accountable approver, and expiration or review
point. A request for autonomy is not authorization by itself.

Use `references/bounded-autonomy-authorization.md` and the canonical JSON
authorization template when bounded autonomy is requested. The Markdown
collaboration-mode worksheet helps the human choose; it does not replace the
canonical record. The record does not authorize data access, a network action,
delegation, a release, or a submission.

The local v0.4 candidate explicitly excludes specialist role cards, delegated
authority, parallel-agent orchestration, hidden background work, and agent
runtime. One Codex conversation may switch review perspective when useful, but
that is not a multi-agent deployment or a tool grant.

For generic data provenance metadata, use
`references/data-provenance-register.md`. A source pointer, template, task
authorization, or unknown status does not authorize data access, copying,
processing, sharing, publication, or release.

## Governed Work Loop

For consequential outputs, use a bounded loop:

1. Contextualize: identify the question, governing records, source authority,
   current requirements, unknowns, and applicable boundaries.
2. Generate or analyze only within the approved scope.
3. Audit at the relevant level: overall purpose, section or module, sentence,
   variable, claim, figure, table, or code block.
4. Record a specific diagnosis when work fails review. Route that diagnosis
   back into the next context step rather than retrying blindly.
5. Stop for accountable human review before a consequential transition.

Do not treat self-review as final academic, clinical, compliance, or
publication approval.

## Mandatory Stops

Stop and request accountable evidence or approval before:

- creating or changing a protocol, eligibility rule, analysis plan, or
  consequential project state;
- treating a result as authoritative or making a final scientific claim;
- asserting ethics, consent, DUA, privacy, authorship, funding, COI, AI-use,
  availability, or journal-policy facts;
- accessing, copying, sharing, or publishing restricted, patient-derived, or
  credentialed material;
- releasing a manuscript, code, data, submission package, or public material;
- submitting to a journal;
- promoting project observations to shared or public rules.

## Route Resources

- Startup and request routing:
  references/startup-and-routing.md
- Collaboration mode, feasibility, authority, and data boundaries:
  references/governed-work-and-feasibility.md
- External evidence and citation support:
  references/evidence-and-citation-control.md
- Manuscript, revision, declaration, and submission-route work:
  references/manuscript-and-submission-control.md
- Project retrospective learning and lesson promotion:
  references/retrospective-learning.md
- Explicit empty-workspace creation:
  references/controlled-bootstrap.md
- Public/private separation and legacy boundaries:
  references/portability-and-release-boundaries.md

Use the blank assets only after explaining their role and obtaining any required
user decision. Do not populate them with invented facts.

## Response Summary

After routing, state:

- request classification;
- workspace or project status;
- records and references consulted;
- known facts and blocking unknowns;
- collaboration-mode status when relevant;
- disposition: continue, needs_user_input, blocked, or stop;
- the next allowed action.
