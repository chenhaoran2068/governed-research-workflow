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

Show the visible facts, material unknowns, route-limiting risks, and the reason
the output is only a recommendation. Do not use a numerical confidence score.
The user may accept, revise, defer, or reject the recommendation. Only then may
the System enter detailed lifecycle routing.

## Boundaries

The navigator does not create a Study, decide a design, infer ethics, access,
registration, or reporting compliance, select a method, read data, run a
feasibility probe, execute analysis, establish result authority, or grant
approval. It does not replace the controlled bootstrap, lifecycle guidance,
feasibility workflow, compliance controls, or accountable-human decisions.

For a confirmed future-Study lifecycle route, read
`references/future-study-lifecycle-design-governance-and-analysis-state.md`.
