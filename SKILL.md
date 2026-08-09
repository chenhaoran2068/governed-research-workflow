---
name: governed-research-workflow
description: Mandatory first-response System for any ordinary-language request to start, plan, explore, or propose a possible new research Study. Use it before giving research methods, design, sources, citations, links, data-access suggestions, or project-creation instructions. Do not use it for an explicit request to read, understand, or appraise a specific scholarly paper unless the user also asks to start, plan, or create a new Study. It also routes governed existing-study, manuscript, reviewer-revision, declaration, citation, feasibility, and retrospective work; humans retain consequential decisions.
---

# Governed Research Workflow

Use this Research System to route and structure research work. Its `SKILL.md`
is a Codex entry adapter, not a scientific execution engine, clinical decision
tool, compliance authority, or submission service.

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

When ordinary language indicates a possible new Study, including an incomplete
idea, unknown topic, unknown data, or an ordinary-language request to start or
plan research, the navigator is the mandatory first substantive response.
Before giving a method, design recommendation,
lifecycle plan, external source, citation, link, data-access suggestion, or
project-creation instruction, read
`references/new-study-navigator-and-route-recommendation.md` and return only
its human-confirmable recommendation. The first response must state one route,
begin with the literal form `Route: <recommendation-code>`, and state visible
facts, material unknowns, route-limiting risks, why the result is
non-decisional, and the user's four choices: accept, revise, defer, or reject.
It does not create a Study, select a design, infer governance, or authorize
work. Do not enter detailed lifecycle routing until the user makes one of those
choices.

An explicit request to read, understand, annotate, discuss, or critically
appraise a specific scholarly paper is not a possible new Study merely because
it uses research language. Unless the same request clearly asks to start, plan,
explore, or create a Study, do not begin with `Route:`. Do not read a paper or
invoke another Skill automatically. For an explicitly requested paper-reading
task, use `references/research-paper-reading-bridge.md` only to state the
optional handoff boundary; the reading Skill's own source, retention, and
configuration checks remain separate.

For a stated causal or treatment-effect question, return only
`v1_8_with_specialist_review`, name the need for a separate causal-design or
target-trial-emulation review, and stop for the user's decision. Do not give
estimators, models, weighting methods, eligibility rules, or external sources
at this stage. For a prospective researcher-assigned or randomized study,
return only `specialist_module_required`, name the specialist trial route, and
stop for the user's decision.

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

For a selected released version that admits `GRW-CAP-180-01`, read
`references/future-study-lifecycle-design-governance-and-analysis-state.md`
after the user confirms the navigator's lifecycle route, or when the caller
explicitly asks for future-Study lifecycle, design classification, governance
readiness, or analysis-state/freeze guidance. Read only the blank record
relevant to the named task. Do not infer a study type, ethics/access/registration
status, freeze, human decision, or execution approval from a template or
structural validation result. This is optional generic guidance, not automatic
project discovery, persistent memory, a bootstrap executor, a research executor,
or an authority route.

For a selected released version that admits `GRW-CAP-200-01`, only after the
user confirms a future-Study lifecycle route and explicitly requests China
Mainland ethics or medical-research-registration material preparation, read
`references/research-ethics-preparation-bridge.md`. The caller must name one
compatible module, one exact Study root, one material mode, and the specific
protocol/compliance inputs permitted for the preparation task. Do not discover
a module or Study, scan a workspace, follow a reference, invoke a Skill
automatically, infer a governance fact, create an application, submit/upload,
or advance a lifecycle state. A module manifest, generated draft, blank
template, structural validation, or preparation request does not prove ethics
approval, registration, access, institutional compliance, human authorization,
or readiness to process real material. Causal/treatment-effect and prospective,
researcher-assigned, randomized, interventional, product, device, IVD, and
non-China routes remain outside this bridge and require their existing
specialist or future Charter routes.

For a selected released version that admits `GRW-CAP-210-01`, use
`references/research-paper-reading-bridge.md` only when the user explicitly
requests help with one specified scholarly paper. It may identify
`research-paper-reading` as an optional compatible Skill, but it must not
discover or invoke that Skill, read a source, download or copy a PDF, inspect a
reference manager, create a reading record, configure a Framework knowledge
service, infer a retention choice, or treat reading as a new Study. The user
must separately choose and activate the reading route.

For a selected released version that admits `GRW-CAP-220-01`, use
`references/managed-reading-knowledge-service-bridge.md` only when the user
explicitly asks an existing Study to receive a metadata-only handoff from one
named managed reading knowledge service. The caller must name the exact Study,
service, permitted metadata fields, handoff purpose, and accountable-human
decision reference. Do not discover a service or Study, inspect a manager,
open a paper, dossier, knowledge card, or PDF, synchronize a reference
manager, create a handoff, infer relevance, or make a design, governance,
source-support, or result-authority claim. The reading Skill owns any service
configuration and source/retention decision; this System can only consume a
caller-supplied metadata handoff after separate human approval.

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

For an explicitly requested `experience_descriptor_profile_review`, first
resolve the selected version to its exact public tag and matching GitHub
Release, then check the capability ledger for an admitted
`GRW-CAP-140-02` record. Require the caller to name one vocabulary
registry, one descriptor catalogue, one descriptor-decision register, and one
descriptor index JSON input. Read
`references/controlled-experience-descriptor-profiles.md` before
invoking the validator. Do not discover files, read a source inventory or
source body, infer descriptors, create a decision or index entry, promote an
experience, modify a rule, or continue across an unknown boundary.

For an explicitly requested `public_safe_experience_guidance` task, first
resolve the selected version to its exact public tag and matching GitHub
Release, then check the capability ledger for an admitted `GRW-CAP-160-01`
or `GRW-CAP-170-01` record. Read
`references/public-safe-shared-experience-derivatives.md`, then read
`assets/public-experience-derivatives/public_experience_catalogue.json` only
to locate a potentially relevant public card. Read a selected card or named
public collaboration-guidance document only when the caller's stated task
makes it relevant. Do not load all cards, infer relevance from an undisclosed
source, resolve a private source, treat a card or guidance document as current
external guidance or approval, create a mapping, promote an experience, modify
a rule, or continue across an unknown boundary. This route is selective public
guidance, not a retrieval service, recommendation engine, task executor, or
authority mechanism.

For existing-study, legacy-project, manuscript, or revision work, require an
exact workspace path or project root before reading project-local records. A
pasted excerpt may clarify the task after the root is identified; it does not
replace the project location.

For a selected released version that admits `GRW-CAP-150-01`, read
`system/03_workflows/MANUSCRIPT_OPERATIONAL_CHECKLISTS.md` only when the caller
explicitly asks for generic operational guidance within an existing manuscript,
revision, declaration, or submission task. Read
`system/03_workflows/RESEARCH_PROGRAM_BOUNDARY_AND_SHARED_MATERIALS_CONTROL.md`
only when the caller explicitly asks to review a stated boundary or proposed
relationship among named research work units. These are optional guidance
documents, not a new request class or an automatic read. They do not establish
facts, permissions, authorship, compliance, source access, result authority,
or submission readiness.

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
- Public-safe shared-experience derivative guidance, when admitted for the
  selected release: references/public-safe-shared-experience-derivatives.md
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
- Controlled experience-descriptor profile review, when admitted for the
  selected release: references/controlled-experience-descriptor-profiles.md
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
