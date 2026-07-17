# Metadata-Only Data And Provenance Register

## Purpose

This register records metadata about a data object or source pointer: what it
is, where it came from, who is responsible, what restrictions are known, and
what downstream metadata records depend on it. It does not import, read, copy,
hash, clean, analyze, store, share, or otherwise process data content.

The canonical public record is
`assets/data-provenance-register.template.json`, validated by
`system/09_schemas_records_and_templates/data_provenance_register.schema.json`.
It must contain placeholders, redacted locators, relative examples, or public
source pointers only. Never put credentials, real local paths, patient
identifiers, research values, images, tables, or clinical records in a public
register entry.

## Generic Core

Use one record per metadata object. Record the stable ID, object class, role,
lifecycle layer, safe source pointer, owner, relationships, lineage,
standardization state, criticality, sharing and overwrite policy, integrity
method, audit record, and last verification date.

An external database normally appears as an `external_source_pointer`, not a
copied database. A project-specific source snapshot or analysis-ready dataset
may be registered as metadata, but this public system does not create or read
such files.

## Unknown Is Not Approval

`unknown` is an accurate record of uncertainty. It permits planning that does
not access data content, preparing empty templates, and retrieving public
source rules. It does not permit copying, uploading, sharing, publishing,
releasing, processing, or claiming access to data.

A labelled verification hypothesis may say that a named source may have terms
or conditions requiring confirmation. It must remain `unverified` and state
that it is not an authorization. A claimed data-access or sharing status needs
a `data_access_or_share_evidence_reference`, such as a source rule, DUA,
documented condition, or accountable-human confirmation.

## Relationship To Task Authorization

R40-02 task authorization answers whether an AI may attempt a narrowly defined
task. This register answers what is known about a data object's source and
restriction/share state. Neither record substitutes for the other. A task that
would use data content needs both the task authorization and applicable data
access/share evidence; an unknown data state limits the task to non-data
planning.

## Optional Restricted Or Clinical Awareness

The optional extension can record awareness that a source may be patient-
derived, clinical, restricted, credentialed, subject to a DUA, or governed by
privacy, consent, or online-service conditions. It is not an ethics, consent,
DUA, privacy, institutional, clinical, legal, or regulatory determination.

## Stop Conditions

Stop consequential data actions when source, access, restriction, sharing, or
online-service conditions are unknown or conflict. Report the known evidence,
unknown facts, feasible verification options, and the next accountable-human
decision. Do not manufacture a permission claim to unblock work.
