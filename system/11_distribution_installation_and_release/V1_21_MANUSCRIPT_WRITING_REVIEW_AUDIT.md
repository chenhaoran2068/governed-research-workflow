# V1.21 Manuscript Writing And Linked Review Candidate Audit

## Audit Identity

- audit scope: local v1.21 manuscript-writing and linked-review candidate
- candidate base: `d8533b7b1f77d03ae102704bbd0667d8dfd30381`
- audited candidate commit: `37d110d34cb9b7dd392bd8621ea134f8c30bc011`
- audit posture: static delivery audit after implementation; not scientific,
  editorial, legal, or release approval
- excluded operations: no runtime modification, installation, tag, remote push,
  GitHub Release, publication, Study inspection, manuscript edit, or data access

## Scope Inventory

The candidate changes nine public-source paths:

1. one generic writing and linked-review reference;
2. one blank linked-review checklist;
3. one existing claim/display template;
4. three existing generic manuscript or review references;
5. the public module index;
6. one candidate control record; and
7. one regression-test module.

The candidate expresses eight generic practices: narrative weight, limitations,
information placement, eligibility, cohort flow, claim/evidence linkage, linked
candidate QA, and Results roles. It introduces no executable helper, schema
writer, data route, publication route, or external source retriever.

## Traceability And Boundary Review

| Candidate concern | Candidate surface | Static check | Audit result |
| --- | --- | --- | --- |
| Writing detail becomes mechanically uniform | generic reference and checklist | Required narrative-weight and one-paragraph-task checks | Covered |
| Results emphasis follows significance | Results-role guidance and Results-first reference | Explicit role hierarchy and no-significance-only rule | Covered |
| Limitations become hidden or repetitive | generic reference and checklist | Study-wide versus result-specific placement checks | Covered |
| Methods, Results, and displays duplicate or omit material | generic reference, checklist, and claim/display template | Information-placement and display-local interpretation checks | Covered |
| Eligibility or flow diverges from execution | generic reference and checklist | Two-layer eligibility and reconciled-flow checks | Covered |
| A claim or display changes without dependent review | generic reference, checklist, existing joint-review route | Linked claim/display table and direct-dependency re-review checks | Covered |
| Candidate wording is mistaken for journal or release authority | all new public surfaces | Explicit non-authority wording and candidate-only status | Covered |

## Verification Evidence

- Targeted regression suite: 30 tests passed.
- Full regression suite: 447 tests passed; 3 tests skipped.
- `git diff --check`: passed before the candidate commit.
- Cross-reference check: the new guidance is linked from the existing
  manuscript-and-submission control; the checklist and claim/display template
  are linked from the new guidance.
- Static public-boundary scan: no private path, named Study, credential, secret,
  real manuscript, patient data, or research result in the changed public
  documentation. Test-only forbidden-marker patterns and the generic phrase
  `patient-level data` were separately identified as expected non-sensitive
  controls or exclusions.
- Side-effect review: no new runtime helper, network client, writer, installer,
  or release command was added. The only release wording is an explicit
  prohibition.

## Findings And Remaining Gates

No blocking implementation finding was identified in this static audit.

This audit cannot establish that the eight practices fit every research type,
target journal, or reporting guideline. The System already requires a selected
review profile and allows a specialist placeholder where the default
observational profile does not fit. For a real manuscript, the accountable
human must still select the profile, verify external requirements, review
project evidence, and decide whether a candidate is acceptable.

Release and runtime adoption remain pending. This audit does not authorise a
tag, remote push, GitHub Release, publication, installation, or use by an
active local System.
