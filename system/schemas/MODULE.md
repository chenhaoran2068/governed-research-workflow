# Schemas Module Boundary

Status: foundation only; no new public schema is admitted here yet.

This module will hold versioned generic data contracts for reusable records and
their validation. A schema must document its version, required fields,
permitted values, compatibility expectation, ownership, and test fixture.

Do not store live project state, patient-derived data, private identifiers, or
facts that require study-specific approval in a public schema.
