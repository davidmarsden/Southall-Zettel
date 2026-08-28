# Knowledge layer implementation checkpoint

Phases 1–3 of roadmap issue #1 have their first working implementation on `main`.

## Phase 1 — candidate discovery

- `scripts/discover_candidates.py`
- `generated/entity-candidates.json`
- `indexes/entity-candidates.md`
- `config/entity-candidate-ignore.txt`
- candidates never auto-promote into `entities/`

The current queue surfaces useful review candidates including Ealing Community Independents, Blair Peach Primary School, Southall Broadway, Tony Pidgley, Norwood Green, Minni Dogra, Southall Community Alliance, Jeremy Corbyn, Johnson Street, Jags Sanghera and South Road.

## Phase 2 — reviewed relationships

- `relationships/reviewed.yml`
- `generated/entity-relationships.json`
- `indexes/relationships.md`
- reviewed edges in `generated/graph.json`

Seeded reviewed edges: Peter Mason → Ealing Council (`leader_of`), Henry Construction → Norwood Road (`developer_of`), Southall Gasworks → Southall (`located_in`), Southall Green → Southall (`located_in`).

## Phase 3 — curated source records

- `sources/` schema documented in `docs/knowledge-layer.md`
- `generated/curated-sources.json`
- `indexes/source-records.md`
- source-record nodes/edges in `generated/graph.json`

First source records cover the 2021–22 Council Performance report, the Southall Market Car Park ModernGov decision record and the archived affordable-homes performance dashboard.

## Current graph

- 69 posts
- 16 curated entities
- 10 topics
- 4 reviewed entity relationships
- 3 curated source records
- 295 graph nodes
- 1,288 graph edges

Next: human review/promote the strongest candidate entities, deepen reviewed relationships and source records, then define `generated/commons.json` from real curated examples.
