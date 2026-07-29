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

For exact capability-contract status, consult
`system/00_manifest_and_profiles/capability_truth_ledger.json`. A planned,
forbidden, unknown, or contradictory ledger entry does not
authorize a behavior. The ledger does not replace the accountable-human
approval required for consequential work.

For live public installation identity, historical release records, and the
exact-tag and matching-Release verification rule, consult
`system/11_distribution_installation_and_release/CURRENT_RELEASE_STATUS.md`.
Do not infer an installed runtime version from a public tag, mutable branch,
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

For a selected released version that admits `GRW-CAP-111-01`, read
`references/future-study-execution-and-reproducibility.md` before discussing a
future Study's execution contract, formal run, result authority, or QA record.
Those records are metadata-only controls; they do not authorize a run, data
access, dependency change, result approval, or scientific claim.

For an explicitly requested `experience_vocabulary_control_review`, first
resolve the selected version to its exact public tag and matching GitHub
Release, then check the capability ledger for an admitted `GRW-CAP-120-01`
or `GRW-CAP-140-01` record. Only if both conditions hold, read
`references/controlled-experience-vocabulary.md`. Require the caller to name
each vocabulary registry, source inventory, reference index, mapping-decision,
and (when used) L1 decision-register JSON file permitted for structural review,
and to state the requested structural outcome. The L1 register can represent a
final human `mapped`, `not_mapped`, `deferred`, or `blocked` disposition; it
does not make that decision or turn it into promotion. Do not discover files
from a directory, resolve a source pointer, read source content, infer a term,
create a real mapping, administer the vocabulary, promote an experience,
modify a rule, or continue across an unknown boundary. This route is read-only
request routing, not a helper, writer, agent, delegated authority, or
human-decision mechanism.

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

Specialist role cards, delegated authority, parallel-agent orchestration,
hidden background work, and agent runtime remain excluded. The v0.8 source
also contains two non-runnable role-contract records. A role contract only
defines a bounded review perspective; it is not a second agent, a tool grant,
M53 authorization, helper admission, or per-run write confirmation. One Codex conversation
may switch review perspective when useful, but that is not a
multi-agent deployment or an additional permission.

Do not offer a v0.8 role-contract or helper-admission route as a released
capability unless the selected exact tag and matching GitHub Release exist and
the capability ledger marks the relevant record as permitted. When those
conditions are met, read `references/role-contracts.md` or
`references/controlled-helper-admission.md` before using the named bounded
review perspective or discussing the bootstrap admission boundary.

For generic data provenance metadata, use
`references/data-provenance-register.md`. A source pointer, template, task
authorization, or unknown status does not authorize data access, copying,
processing, sharing, publication, or release.

For an explicitly requested **set** of metadata-only provenance records, use
`references/data-provenance-register-set.md`. Invoke its validator only when
the user supplies one explicit index path and requests structural validation.
The validator reads metadata JSON only; it does not open source locators or
data files, grant access, or determine compliance.

For an explicitly requested workflow/evidence-control bundle, first resolve
the selected version to its exact public tag and matching GitHub Release, then
check the capability ledger for an admitted `GRW-CAP-060-01` record. Only if
both conditions hold, use
`references/workflow-evidence-control-records.md` and invoke its validator
only with one explicit review root, bundle path, and optional baseline path.
The validator is read-only and metadata-only: it does not open pointers,
access data, establish source support, verify a human identity or real
authorization, advance a Gate, or make a scientific/compliance/submission/
release decision. A source file, branch, admission record, or unadmitted ledger
state is not permission to offer this route as a released capability without
the selected version's exact tag and matching GitHub Release.

For an explicitly requested lesson-promotion control bundle, first resolve the
selected version to its exact public tag and matching GitHub Release, then
check the capability ledger for an admitted `GRW-CAP-070-01` record. Only if
both conditions hold, use `references/lesson-promotion-control-records.md` and
invoke its validator only with one explicit review root and bundle path. The
validator is read-only and metadata-only: it neither opens project material nor
follows a reference; it does not verify a human identity or actual authority,
automatically promote or integrate a lesson, modify a target, or decide any
scientific, compliance, Gate, submission, or release question.

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

## Synthetic Exchange-Pilot Route

Use the v0.10.1 exchange-pilot route only after the user explicitly asks for a
self-controlled **synthetic** private-pilot check, the selected exact public
tag and matching GitHub Release exist, and the capability ledger admits
`GRW-CAP-101-01` for that version. Read
`references/synthetic-experience-exchange-pilot.md` before invoking the named
read-only validator. Stop if a real package, external contributor, public
intake, identity/rights claim, actual transfer, or Computer B claim is
requested. Do not create a repository, upload material, or execute a
correction/withdrawal merely because a receipt validates structurally.

No user-contribution intake route is implemented. A future, explicitly
consented minimal candidate may be sent to Chenhaoran only through a
human-specified channel, for manual rights/sensitivity screening, curation, and
separate approval of any public-safe derivative. Do not create repository
access, upload/download, automatic de-identification, automatic review, or
automatic promotion from this statement.

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
- Optional blank manuscript-governance templates:
  references/manuscript-governance-templates.md
- Generic public knowledge-governance experiences, not a Knowledge or retrieval
  route: references/knowledge-governance-experience-collection.md
- Project retrospective learning and lesson promotion:
  references/retrospective-learning.md
- Metadata-only lesson-promotion control records, when admitted for the
  selected release: references/lesson-promotion-control-records.md
- Explicit empty-workspace creation:
  references/controlled-bootstrap.md
- Future-Study execution and reproducibility records, when admitted for the
  selected release: references/future-study-execution-and-reproducibility.md
- Controlled experience-vocabulary and reference-index review, when admitted
  for the selected release: references/controlled-experience-vocabulary.md
- Public/private separation and legacy boundaries:
  references/portability-and-release-boundaries.md
- Metadata-only workflow/evidence control records, when admitted for the
  selected release:
  references/workflow-evidence-control-records.md
- Bounded non-runnable role contracts, when admitted for the selected release:
  references/role-contracts.md
- Controlled bootstrap-helper admission, when admitted for the selected
  release: references/controlled-helper-admission.md
- Self-controlled synthetic experience-exchange pilot, when admitted for the
  selected release: references/synthetic-experience-exchange-pilot.md

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
