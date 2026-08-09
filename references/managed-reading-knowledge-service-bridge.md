# Managed Reading Knowledge-Service Bridge

## Purpose

`GRW-CAP-220-01` defines the narrow consumer boundary by which an existing
Study may receive a separately human-approved metadata-only handoff from the
optional `scholarly-reading-knowledge` service. The reading Skill owns and
configures it through the separately maintained `research-paper-reading` Skill. The
Workspace Framework supplies only the generic optional service boundary.

This System is an optional consumer. It does not require the service for new
Studies, existing Studies, manuscript work, or any other route.

## Entry Conditions

Use this bridge only when all of the following are explicitly supplied by the
caller:

1. one named existing Study and its exact root;
2. the service identifier `scholarly-reading-knowledge`;
3. one stated handoff purpose;
4. the specific metadata fields permitted for the handoff; and
5. an accountable-human decision reference approving this handoff.

The caller must separately establish that the reading Skill and Framework
service are compatible and configured. This bridge does not inspect either
configuration or prove their installed identity.

## Allowed Metadata

An approved handoff may contain only the fields in the blank
`assets/managed-reading-knowledge-service/study-knowledge-handoff.template.json`
and its schema: opaque record references, a citation key, a persistent
identifier, title, publication year, a bounded purpose, and an accountable
human decision reference. It declares both `source_content_transferred: false`
and `source_reading_authorized: false`. These fields are navigation context
only.

Metadata does not establish that a source exists, was read correctly, supports
a claim, is current, applies to the Study, may be retained, or justifies a
design, method, conclusion, governance action, or manuscript statement.

## Refusals

Do not use this bridge to:

- discover a Study, service, manager, paper, dossier, knowledge card, or
  configuration;
- inspect or configure a reference manager or a Framework service;
- read, download, copy, parse, quote, summarize, index, or transfer a paper,
  PDF, source excerpt, reading dossier, knowledge-card body, or manager data;
- create, edit, infer, validate semantically, or approve a real handoff;
- convert a knowledge item into an experience, rule, template, checklist, or
  skill; or
- infer access, ethics, registration, source support, relevance, study type,
  result authority, or an installed runtime.

If any entry condition or required human decision is missing, conflicting, or
unknown, stop and request clarification. A structural schema result is not a
real handoff, source review, or approval.
