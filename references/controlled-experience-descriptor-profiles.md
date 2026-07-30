# Controlled Experience Descriptor Profiles

## Purpose

This route provides generic, metadata-only structures for describing a
human-reviewed experience with controlled retrieval context. It keeps five
facets separate: domain, record kind, task trigger, target object, and scope.
An optional exact topic-term list can remain separate from those facets.

The route provides neither an approved public descriptor catalogue nor a
classification service. A local owner may maintain a caller-named catalogue;
the package supplies only a blank structure and a read-only validator.

## Four Separate Objects

1. A controlled descriptor catalogue defines allowed values for the five
   facets and their cardinality.
2. A represented descriptor decision records an accountable-human final
   disposition for one named source identity. It may be described, deferred,
   or blocked.
3. A descriptor index carries only entries derived from described decisions.
4. An optional controlled experience vocabulary can supply exact topic terms.
   Topic terms are more precise than the five descriptor facets, but neither
   type of label is evidence or authority.

The catalogue answers retrieval-context questions. It does not establish
whether an experience is true, current, approved, mature, reusable, promoted,
integrated, owned, accessible, or authorized. A descriptor decision represents
the recorded final human choice; structural validation cannot verify that the
choice, person, or source is real.

## Explicit Read-Only Validation

Use validate_experience_descriptor_profiles.py only when the caller names
four absolute JSON inputs: one vocabulary registry, one descriptor catalogue,
one descriptor-decision register, and one descriptor index. The validator also
reads its four bundled schemas. It rejects indirect or non-JSON inputs,
duplicate JSON keys, unknown accepted descriptor values, inconsistent
catalogue identities, non-described index entries, and mismatched decision
metadata digests.

It does not read a source inventory, source body, pointer, locator, path,
source hash, project directory, or external service. It does not discover
files, infer a descriptor, create or edit a decision, create an index entry,
promote experience, modify a rule, or contact a network service.

## Lifecycle Boundary

Describe an authorized-read experience only after accountable-human review.
If a source may be stale, sensitive, ambiguous, or likely to be misused, use a
stricter currentness and boundary review before a descriptor decision. If an
experience might change a rule, template, checklist, or skill, use the
separate promotion and M48 re-review route. A descriptor association alone
never causes promotion or integration.

Preserve earlier decisions under M54. Correct a descriptor by recording a
later accountable-human decision and revalidating the affected derived index;
do not silently rewrite historical evidence.
