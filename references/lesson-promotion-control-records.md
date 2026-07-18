# Lesson Promotion Control Records

Status: v0.7 release-source guidance. This route is available as a public
capability only when the selected version's exact immutable tag and matching
GitHub Release exist and its ledger admits `GRW-CAP-070-01`. A branch,
template, validator, source document, or test result alone is not public
availability or authorization to promote a lesson.

## Purpose And Boundary

This optional, metadata-only bundle makes a proposed lesson traceable from a
bounded observation through accountable-human review to a separately recorded
integration verification. It is designed to prevent a project-local note, an
AI suggestion, or a test result from silently becoming a shared rule.

It does not include project content, participant data, credentials, detailed
private history, or a shared private-memory store. It does not prove an
observation is true, an accountable human is identified or authorized, a
target rule is correct, or any project is compliant, ready, or publishable.

`metadata_only` is a required authoring boundary, not automatic redaction or a
claim that the validator can recognize every sensitive fact. Do not place raw
data, names, record excerpts, unpublished results, credential material, or
restricted source text in a summary, reference, reason, or other free-text
field. If that boundary cannot be maintained, do not use this public record
contract for the material; keep it under the applicable private project rules.

## Records

| Record | Records | Does not establish |
| --- | --- | --- |
| `observation` | A bounded process observation and its declared evidence references. | Scientific truth or a global rule. |
| `lesson_candidate` | A proposed reusable behavior, limits, target, and lifecycle state. | Automatic promotion or target modification. |
| `human_decision` | A represented accountable-human disposition and stated basis. | Identity or real authority verification. |
| `integration_verification` | A declared target and evidence that a human-approved candidate was integrated. | Target correctness, future compliance, or public release. |
| `change_event` | A correction, withdrawal, or supersession with an associated human decision. | Tamper-proof history or a complete audit trail. |

Use a candidate lifecycle status exactly as declared. `under_review` must not
be treated as approved. `integrated` needs an `approve_for_integration` human
decision and a `verified` integration record. `withdrawn` and `superseded`
need the matching decision and change event. A correction, withdrawal, or
supersession must remain visible rather than silently replacing an earlier
record.

## Explicit Read-Only Validation

Invoke only for a human-supplied review root and one explicit portable relative
bundle path:

```text
python scripts/validate_lesson_promotion_control_bundle.py \
  --root <review-root> \
  --bundle <relative-json-path>
```

The validator reads only the selected JSON input and its bundled schema. It
rejects absolute paths, parent traversal, symbolic links, Windows reparse
points, non-regular files, malformed JSON, duplicate keys, wrong schema
versions, duplicate IDs, invalid references, automatic-promotion declarations,
and incompatible lifecycle/decision/integration/change-event combinations.
It neither enumerates the review root nor writes a file.

It never follows a reference, opens a URL or pointer target, reads data,
contacts a service, verifies source content, verifies a human identity or
actual authorization, decides a Gate, modifies an integration target, promotes
a lesson, or makes a science, compliance, submission, or release decision.
It also does not inspect free text for private or restricted content.

## Safe Use

Keep actual project retrospective material in the project-local retrospective
register. Use this public contract only to describe a minimal, rights-cleared
metadata representation when an accountable human chooses to review whether a
lesson can be integrated elsewhere. A real integration remains a separate
reviewed modification of its target rule, workflow, template, checklist, or
skill; this bundle does not perform it.
