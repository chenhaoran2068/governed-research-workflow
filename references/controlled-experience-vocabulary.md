# Controlled Experience Vocabulary And Reference Index

## Purpose

This route provides generic, metadata-only contracts for four separate
objects: a controlled vocabulary, a bounded source inventory, a recorded human
mapping decision, and a reference index. They help a caller state which
controlled terms may be relevant to a named record without turning a label into
evidence, maturity, permission, approval, promotion, integration, or authority.

The route is not a source library, retrieval service, Knowledge package, RAG
system, graph service, automatic classifier, mapping service, automatic
promotion route, intake channel, or writer. It does not open source pointers,
inspect project material, contact an external service, or establish that a
human identity, decision, or source claim is real.

## Four Separate Records

1. A vocabulary registry defines preferred labels, aliases, confused terms,
   boundaries, controlled tags, and historical terminology relationships.
2. A source inventory records only bounded source identities and metadata. It
   deliberately carries no path, URL, hash, payload, excerpt, credential, or
   access assertion.
3. A mapping-decision record represents a named accountable-human disposition:
   `map`, `hold`, `decline`, or `needs_review`. Representation is not identity
   verification or authority verification.
4. A reference index links a source identifier and controlled term identifiers
   only when the caller separately supplies a matching `map` decision record.

Each record answers a different question. A term can be accepted while an
experience remains unreviewed. A source identifier does not authorize source
access. A valid index entry does not prove a source supports a rule or that the
experience is reusable.

## Explicit Read-Only Review

The caller must name every JSON file that may be read. Use
`validate_controlled_experience_vocabulary.py` with one registry and one source
inventory. Use `validate_experience_reference_index.py` with one registry, one
index, and zero or more explicitly named mapping-decision records. Both tools
read UTF-8 JSON only, reject duplicate keys and unsafe or indirect paths, and
write nothing.

Stop rather than continue when a request asks to read a source body, resolve a
pointer, discover files in a workspace, create or edit a real mapping, choose a
term by inference, administer a vocabulary, promote an experience, integrate a
rule, or act on an unknown boundary. Those actions require separately governed
work and accountable-human decisions.

## Terminology Lifecycle

`candidate` and `accepted` terms use preferred labels. `deprecated`, `merged`,
and `renamed` terms retain only historical aliases and point to a successor;
their former labels must not remain canonical. This preserves retrieval context
without silently treating an old name as a current standard.

New vocabulary terms, aliases, and mappings must be reviewed as semantic
changes. Under M48, any correction requires a new review of affected tests,
documentation, and claims. Under M54, prior valid records and review evidence
remain preserved rather than overwritten.
