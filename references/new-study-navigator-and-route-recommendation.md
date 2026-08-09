# New-Study Navigator And Route Recommendation

## Purpose

This generic route guidance lets an AI recognize ordinary language indicating a
possible new Study and give a short, reviewable recommendation before detailed
lifecycle planning begins. It is navigation only, not an automated research
decision or project-creation mechanism.

## Trigger And Early Screen

Use this reference for a possible new-Study request such as "I want to start a
study", "I have a database research idea", or an equivalent request in another
language. Do not make it the primary route for an identified existing Study,
manuscript-only task, reviewer revision, local code task, or casual discussion
with no intent to begin research. Ask the smallest focused question when that
distinction is unclear.

An explicit request to read, understand, annotate, discuss, or critically
appraise a specific scholarly paper is a paper-reading request, not a possible
new Study request. Do not return `Route: <recommendation-code>` unless the
same request clearly asks to start, plan, explore, or create a Study.

At the early screen, summarize only visible facts and material unknowns. Do not
require a complete protocol, create a project or record, read real material,
or call the request approved, feasible, compliant, or publishable.

## Human-Confirmable Recommendation

Consider intervention allocation, object-selection design, temporal orientation,
data origin, and primary research purpose separately. Also identify visible
time-zero, data-fitness, governance, reporting, and specialist-review risks.
Return exactly one of:

| Recommendation | Meaning |
| --- | --- |
| `v1_8_primary_route_candidate` | Likely in-scope observational work using existing individual-level records for a descriptive, association, prognostic, clinical-prediction, or diagnostic question. |
| `v1_8_with_specialist_review` | The lifecycle may organize the work, but causal, treatment-effect, or another specialist review is necessary. |
| `specialist_module_required` | A prospective, researcher-assigned, randomized, systematic-review, qualitative, laboratory, or other specialist route must lead. |
| `insufficient_information` | The available facts do not support a responsible route recommendation. |

The first substantive response must begin with the literal form
`Route: <recommendation-code>`, where the code is exactly one value from the
table. A descriptive label, translated paraphrase, or heading cannot replace
the code. It must then contain exactly these six parts:

1. one recommendation code from the table;
2. visible facts;
3. material unknowns;
4. route-limiting risks;
5. why the output is a non-decisional recommendation; and
6. the user's choices to accept, revise, defer, or reject.

Do not use a numerical confidence score. For `insufficient_information`, ask
no more than two focused questions that would distinguish the route. Only after
the user accepts, revises, defers, or rejects the recommendation may the System
enter detailed lifecycle routing.

For a causal or treatment-effect request, return
`v1_8_with_specialist_review`, name the need for a separate causal-design or
target-trial-emulation review, and stop. For a prospective,
researcher-assigned, or randomized study, return `specialist_module_required`,
name the specialist trial route, and stop.

## Boundaries

The navigator does not create a Study, decide a design, infer ethics, access,
registration, or reporting compliance, select a method, read data, run a
feasibility probe, execute analysis, establish result authority, or grant
approval. Before a human route decision, it also does not provide an estimator,
model, weighting method, target-trial specification, analysis procedure,
external source, citation, link, or data-access suggestion. It does not replace
the controlled bootstrap, lifecycle guidance, feasibility workflow, compliance
controls, or accountable-human decisions.

For a confirmed future-Study lifecycle route, read
`references/future-study-lifecycle-design-governance-and-analysis-state.md`.
