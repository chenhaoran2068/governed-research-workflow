# Schemas Module Boundary

Status: active blank-record baseline; formal generic schemas are foundation
only.

The active baseline is the set of blank human-reviewed records under `assets/`.
They are templates, not schemas and do not validate live project state. This
module may later hold versioned generic data contracts for reusable records
and their validation. A schema must document its version, required fields,
permitted values, compatibility expectation, ownership, and test fixture.

Do not store live project state, patient-derived data, private identifiers, or
facts that require study-specific approval in a public schema.
