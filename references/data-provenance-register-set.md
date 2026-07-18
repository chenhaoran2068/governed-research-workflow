# Metadata-Only Data And Provenance Register Set

## Purpose

This optional register set organizes a bounded list of metadata-only
`data_provenance_register_entry` files. It can check that the listed JSON
entries match the released v0.4 entry schema and that their declared
upstream/downstream identifiers agree with each other.

It is a metadata-structure tool. It does not open, locate, download, inspect,
hash, copy, analyse, share, upload, or publish the data described by an entry.
A `valid` result means only that the supplied metadata passed the documented
structural and declared-relation checks.

## Files

- `assets/data-provenance-register-set-index.template.json`: blank index
  template.
- `system/09_schemas_records_and_templates/data_provenance_register_set_index.schema.json`:
  index schema version `1.0.0`.
- `system/09_schemas_records_and_templates/data_provenance_register.schema.json`:
  unchanged v0.4 entry schema version `1.0.0`.
- `scripts/validate_data_provenance_register_set.py`: explicitly invoked,
  read-only validator.

The index lists `record_id` and a portable relative `entry_path` for each
entry. It never discovers files by scanning a directory. Keep each listed
entry under the index's own directory and use only `/` as a path separator.

## Install And Run

The validator requires Python 3.11+ and the reviewed direct dependency:

```powershell
python -m pip install -r requirements.txt
python scripts/validate_data_provenance_register_set.py path/to/register-index.json
```

It writes one JSON result to standard output and creates no output files. Exit
code `0` is `valid`, `1` is `invalid`, and `2` is `not_assessed`.

The index file itself and every listed entry must be regular JSON files. The
explicit index may be reached through a system-managed parent alias; the
validator resolves it to a canonical root before evaluating listed entries.
Absolute paths, `..` traversal, entry symlinks, Windows entry reparse points,
missing files, duplicate IDs, duplicate paths, self-links, duplicate links,
missing targets, and asymmetric upstream/downstream links are refused.

## Relationship Check

Each entry keeps its own lineage declarations. The validator checks only their
internal consistency:

```text
If A lists B as downstream, B must list A as upstream.
If A lists B as upstream, B must list A as downstream.
```

This proves neither the source nor the derivation is true in the real world.
It simply detects contradictions in the metadata files that were supplied.

## Unknown Is Not Approval

An entry may record an `unknown` access, restriction, sharing, or service
status. That can be structurally valid. It remains uncertainty, not evidence
that data access, copying, processing, sharing, or publication is permitted.

Data-content work requires separate task authorization and independently
evidenced data-access/share authority. This tool does not supply either.

## Boundaries

Do not put real data, patient identifiers, result values, credentials, signed
URLs, private absolute paths, network mounts, raw checksums, or confidential
approval material in a public register set. The validator will not resolve a
URL, contact a service, open a source locator, inspect an unlisted path, or
make an ethics, consent, DUA, privacy, legal, clinical, scientific, journal,
submission, or compliance decision.
