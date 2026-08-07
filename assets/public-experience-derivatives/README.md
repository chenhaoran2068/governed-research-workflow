# Public Experience Derivatives

This directory contains the public-safe experience derivative library retained
by `GRW-CAP-160-01` and the v1.7 `GRW-CAP-170-01` collaboration-guidance
derivatives.

## Contents

- `public_experience_vocabulary.json`: the current public topic vocabulary.
- `public_experience_catalogue.json`: the only current public discovery index.
- `cards/`: 41 generic public experience cards. Cards `001..038` preserve
  historical KGE backward references; cards `039..041` are new public-safe
  derivatives with no KGE predecessor.
- `schemas/`: read-only structural contracts.
- `fixtures/`: synthetic positive and negative validation inputs.

The library preserves the already-public KGE collection and adds reviewed
generic collaboration guidance. It is not a private archive, source library,
RAG corpus, current-requirement checker, approval mechanism, promotion
mechanism, automatic recommendation service, or synchronization service. Read
`../../PUBLIC_BOUNDARY.md` before using any card.

Cards are packaged with a selected System version but are not automatically
loaded, updated, or treated as authority. Use the catalogue to locate a
potentially relevant card, then read that card only within an explicitly
relevant task route and retain accountable-human review for consequential work.
