# v1.4.0 Release Notes

Status: pre-C4 prepared notes. These notes do not assert that a tag or GitHub
Release exists.

## Added

- GRW-CAP-140-02: generic, metadata-only controlled experience-descriptor
  profiles and faceted retrieval metadata.
- Blank descriptor-catalogue, descriptor-decision-register, and
  descriptor-index templates and schemas.
- A caller-named read-only validator with synthetic positive and negative
  fixtures for five descriptor facets.

## Boundaries

- Descriptor facets classify retrieval context only: domain, record kind, task
  trigger, target object, and scope.
- The package supplies no real descriptor value, source, inventory, decision,
  mapping, or index entry.
- The validator does not read sources, pointers, locators, paths, hashes, or
  external services; it does not infer labels, create decisions, promote
  experience, alter rules, or update a local runtime.
- Descriptor profiles complement and do not replace exact topic terms, final
  human review decisions, currentness checks, evidence, approvals, promotion,
  or M48/M54 re-review.
