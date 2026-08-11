# Future-Study Lifecycle, Design, Governance, And Analysis State

This is generic, metadata-only guidance for a future Study. It is not a
protocol, an ethics or registration decision, an access grant, a study-design
validator, an analysis executor, a result-authority mechanism, or evidence
that a real Study is ready to proceed.

## Navigator Relationship

Natural-language intent to begin a possible new Study may first use
`references/new-study-navigator-and-route-recommendation.md`. The navigator
may recommend this lifecycle as a candidate route, identify visible facts and
unknowns, and request human confirmation. It does not select this lifecycle,
create a Study, write a record, classify a design as fact, infer governance, or
authorize a feasibility probe. Only after the user confirms the route does this
guidance become relevant to detailed future-Study planning.

## Scope

The initial route supports existing individual-level observational research,
especially retrospective cohort work, for descriptive, association,
prognostic, clinical-prediction, or diagnostic questions. Potential causal or
treatment-effect questions require a separately governed causal-design or
target-trial-emulation route. Prospective recruitment, researcher-assigned
interventions, randomized trials, systematic reviews, qualitative research,
laboratory research, and specialist designs need separate modules.

## Eleven Stages

1. Clarify whether the request is a discussion, an existing-Study continuation,
   or a new Study intake.
2. Confirm collaboration mode, candidate workspace, and stop boundaries before
   an empty scaffold is created.
3. Compare research questions, external context, practical resources, and
   known unknowns.
4. Define design and feasibility: classification, population, time zero,
   measurement windows, follow-up, censoring, bias, and data/reporting fit.
5. Form a candidate, not-yet-locked protocol and separate non-real-material
   feasibility work from the governance conditions required before real
   material can be read or processed.
6. First complete a bounded decision-critical check against declared
   uncertainties and thresholds. The accountable human then decides `go`,
   `go_with_conditions`, `reframe`, or `stop`. Only a continuing decision
   permits protocol lock, analysis-state declaration, an appropriate freeze,
   and formal analysis.
7. Build a controlled result package before deriving manuscript claims.
8. Review design, governance, execution, results, claims, declarations, and
   submission material together for consistency.
9. Prepare a versioned submission package against current external
   requirements and an accountable-human decision.
10. Classify editorial/reviewer feedback and trace every accepted change to its
    affected material and renewed review.
11. Handle acceptance, proofing, rights, final archive, correction when
    needed, and project-local retrospective learning.

The route can pause, return, reframe, or stop. It never uses statistical
significance or apparent publishability as an automatic continuation rule.

`go_with_conditions` means that the work may continue only while named
conditions are resolved before their specified later gate. `reframe` returns
to the affected question, design, source, endpoint, population, timing, or
method. `stop` preserves the current reasoning and evidence without treating a
result as a reason to continue the current paper candidate. Neither `go` nor
`go_with_conditions` locks a protocol or makes a result authoritative by
itself.

## Separate Record Surfaces

| Record | Typical project-relative location | Meaning | Does not prove |
| --- | --- | --- | --- |
| `study_design_and_classification_record` | `03_protocol/` | Declared five-dimensional classification and design details. | Design validity, causal validity, feasibility, or approval. |
| `governance_readiness_record` | `02_registry/compliance/` | Declared governance status and references to externally supported evidence. | Ethics, access, registration, legal compliance, or human authorization. |
| `analysis_state_and_freeze_decision` | `00_state/lifecycle/` | Declared analysis state, freeze identity, change class, and human-decision reference. | A real freeze, approval, result authority, or scientific conclusion. |
| `analysis_execution_contract` v2 | `07_analysis/00_contract/` | Declared formal execution path and references to the preceding records. | Permission to run, install dependencies, access data, or approve results. |

`time_zero`, measurement windows, follow-up, and administrative censoring are
design details. Access, ethics, registration, jurisdiction, and institutional
requirements are governance conditions. Exploratory/validation state and
freeze identity are analysis/claim-strength controls. Do not collapse these
categories into a study-type label.

## Optional Ethics-Preparation Bridge

At Stage 5, a human may explicitly ask to prepare China Mainland ethics or
medical-research-registration materials for a compatible researcher-initiated
observational Study. The System may then classify the request only as
`eligible_for_research_ethics_v1_preparation`,
`eligible_with_institutional_or_specialist_conditions`, or
`outside_research_ethics_v1_scope`. These are navigation states, not design,
ethics, registration, access, or institutional decisions.

For the first state, the human must explicitly name a compatible module, exact
Study root, material mode, and permitted protocol/compliance inputs. The module
may prepare derived drafts under
`03_protocol/derived/ethics_preparation/<package_id>/`; it must not overwrite
the current `03_protocol/` authority. Actual applications, submitted snapshots,
approvals, waivers, consent evidence, amendments, and related evidence remain
under `02_registry/compliance/01_ethics_and_consent/`. A generated draft,
template, module manifest, or structural check never advances the governance
gate or proves an external fact.

The bridge is not automatically invoked. Causal/treatment-effect questions
remain subject to separate causal-design or target-trial-emulation review, and
prospective, researcher-assigned, randomized, interventional, product, device,
IVD, or non-China routes require an applicable specialist or future module.

## Analysis State And Change

The blank analysis-state record supports: exploratory hypothesis generation;
predictive model development with internal validation; independent validation;
confirmatory estimation; and mixed primary/exploratory work. A current freeze
requires a freeze identifier and a project-relative human-decision reference.

Later work may supersede a freeze for an implementation correction, prespecified
sensitivity analysis, new exploratory branch, new validation plan, or design
change. It must not silently overwrite the previous record or present an
exploratory result as a prespecified confirmation.

## Validator Boundary

`scripts/validate_future_study_lifecycle_records.py` accepts only four
caller-supplied JSON file paths and fixed package schemas. It performs a shape
check only. It does not discover a project, resolve a reference, read a
referenced target, edit an input, call a service, run an analysis, or determine
whether declared metadata is true.
