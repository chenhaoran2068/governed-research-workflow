# Joint Review Profiles And Dependency Order

This is generic guidance for planning a human-AI review sequence. It is not a
Study protocol, review executor, approval record, or publication decision. It
does not discover a project, read a named reference, inspect data or code,
evaluate a result, or establish that any package is accepted.

## Choose The Review Profile First

Before deciding an order, record the selected research/reporting profile and
the accountable-human decision reference. A study may require a specialist
profile because of its design, purpose, evidence source, or external reporting
requirements. This v1 route supplies one default profile only:
`observational_empirical_original_research_v1`.

When that default does not fit, record
`additional_review_profile_required` and stop at a placeholder. Do not force
the R0-R10 order onto trials, causal-effect studies, prediction or diagnostic
model development, systematic reviews, qualitative research, methods papers,
dataset-development, case-report, or another design merely because a plan
record exists.

Candidate reporting guidance may be tracked while a profile is being planned.
Its status is not an applicability, compliance, or approval finding.

## Record Terms

A **review profile** is the selected scope and order of review, not a research
classification. A **package** is one bounded review surface in that order. An
**authority reference** is a caller-supplied project-relative pointer to the
record a package may cite; the plan and validator never follow it. A
**downstream material** effect identifies later packages that need renewed
review after a change. A **review conclusion** is only the declared package
state plus its accountable-human decision reference; it is not proof that the
underlying material is correct. A **reopen event** preserves why an accepted or
active surface requires renewed review.

## Default Package Order

For a selected observational empirical original-research profile, review in
this dependency order:

1. **R0 - profile and reporting context:** the selected profile, applicable
   guidance candidates, and declared limits of the plan.
2. **R1 - design and governance facts:** the current protocol/design and the
   human-confirmed governance facts that later materials may describe.
3. **R2 - data definition and reproducible execution:** data definitions,
   execution record, QA boundary, and reproducibility material.
4. **R3 - result authority:** the current result-authority surface and known
   uncertainty before manuscript claims are reviewed.
5. **R4 - Results work units and whole Results:** Results structure, displays,
   factual prose, result claims, and whole-Results review.
6. **R5 - Methods:** methods language against the reviewed protocol and actual
   execution record.
7. **R6 - Discussion and Conclusion:** interpretation and limits against the
   reviewed result surface.
8. **R7 - Introduction:** question, rationale, and contribution after the
   result and interpretation boundaries are known.
9. **R8 - Title, Abstract, and Keywords:** compressed manuscript claims after
   the preceding sections are stable.
10. **R9 - cross-cutting materials and submission:** citations, declarations,
    supplements, response material, and submission-facing package checks.
11. **R10 - reconciliation, revision, and archive:** whole-package
    reconciliation, change traceability, and bounded archival preparation.

This is a review order, not a mandatory journal layout. It does not forbid an
early Methods outline or local drafting. A later package cannot silently
invalidate an accepted earlier package: record a reopen event and re-review
the affected and downstream packages.

## Results Work Units

R4 can contain individual Results work units. Each unit declares one assembly
mode:

- `display_first`: the table or figure is prepared before the linked prose;
- `parallel`: verified inputs, prose, and display are developed together. This
  is the default when no documented exception makes another assembly mode more
  appropriate;
- `text_provisional`: limited factual prose is drafted from verified inputs
  while a planned display remains to be completed.

`text_provisional` is a historical state, not a label to overwrite after the
fact. It cannot support an accepted Results work unit until the planned display
reconciliation is complete. The generic control does not decide which display,
claim, or text is scientifically adequate.

## Citation And Cross-Cutting Review

Check citations while the claims that need them are written, then review the
complete citation and declaration surface in R9. That two-level approach avoids
postponing obvious support gaps while preserving a final whole-package audit.

## Reopen And Re-Review

Use a reopen event when a design/governance change, data or definition error,
implementation or QA failure, result-authority change, citation/declaration
conflict, external-requirement change, or new analysis/claim affects a review
surface. The event records affected package identifiers, downstream effect,
whether QA or rerun is required, a replacement reference if supplied, and an
accountable-human decision reference.

The event is traceability metadata only. It does not rerun work, replace an
artifact, infer a decision, or restore an earlier package to validity.

## Structural Record Boundary

`assets/joint-review-plan.template.json`,
`system/09_schemas_records_and_templates/joint_review_plan.schema.json`, and
`scripts/validate_joint_review_plan.py` organize only caller-supplied metadata.
The validator reads one named JSON plan and its package-owned schema. It does
not resolve references, discover a Study, read project material, access data,
inspect results, run code, verify a human decision, or make a scientific,
governance, submission, or release determination.
