# Manuscript Style Profile Contract

This contract records how a named Study applies a manuscript-style profile.
It is a bounded metadata contract, not a style manual, writer, journal-policy
retriever, compliance assessment, or submission decision.

## Why Keep This Record

A manuscript can have three different requirement sources:

1. a baseline style profile for the discipline;
2. a research-type reporting guideline or comparable standard; and
3. the requirements of a selected target journal.

They solve different problems. A style profile controls presentation choices;
a reporting guideline identifies information that should be reported; a target
journal sets the requirements for its own route. Recording them together makes
their relationship inspectable without treating any one source as proof that
the manuscript is correct or ready to submit.

## Scope And Precedence

For a medical or health manuscript, a locally maintained profile may declare
an AMA-derived default such as `ama_11_default`. This public System does not
bundle, quote, retrieve, license, or verify any AMA source. It only recognizes
the caller-supplied profile identifier and its declared boundary.

Use the following precedence rule:

```text
confirmed project facts and authoritative results
  -> applicable reporting-guideline content requirements
  -> current selected-journal requirements
  -> active discipline style profile
```

The target journal controls when its current instruction conflicts with the
style profile. A journal formatting preference does not silently remove an
applicable reporting requirement. If a current journal instruction and a
reporting guideline appear to conflict, record the conflict and stop the
affected decision for accountable-human resolution.

No profile may rewrite a protocol fact, an approved analysis boundary, an
authoritative result, a confirmed declaration fact, or a source-supported
claim. A profile also does not establish that a guideline is applicable, a
journal instruction is current, a manual is accessible, or a manuscript is
compliant.

## Activation Boundary

For an existing Study manuscript, revision, table, figure, reference, or
submission-preparation task, the System may use only the named Study-local
requirement stack after the caller has supplied the exact Study root. The
default local location is:

```text
<Study>/09_manuscript/drafting_requirement_stack.yaml
```

The stack must identify its active profile, profile source boundary, reporting
guidance status, target-journal requirement status, and unresolved conflicts.
A Study-specific accountable-human decision reference is required when a human
selects a non-default profile; it is not required merely because a documented
local default applies. A missing, stale, conflicting, or
manual-verification-required record is a visible gap; it is not permission to
invent a rule or claim full style compliance.

The public template and schema use a JSON interchange record so the bundled
validator needs no YAML parser. A private System may maintain the same fields
in its canonical YAML stack and export a caller-named JSON copy for structural
validation. The validator never reads either form unless the caller supplies
one explicit JSON file.

## Public Boundary

This capability does not automatically select a discipline, enable an AMA
profile, obtain a journal instruction, download a manual, follow a URL, inspect
a Study, determine a reporting guideline, access a subscription, or modify a
manuscript. It does not replace a target journal's current instructions or an
accountable human's decision.

`assets/manuscript-style-profile.template.json`,
`system/09_schemas_records_and_templates/manuscript_style_profile.schema.json`,
and `scripts/validate_manuscript_style_profile.py` validate only one
caller-named metadata record. References must remain project-relative strings;
the validator never resolves or opens them.
