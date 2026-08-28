# Knowledge layer v2

This layer separates three different kinds of knowledge:

1. **Candidates** — machine-surfaced names for human review. Never assertions.
2. **Reviewed relationships** — human-approved entity-to-entity edges with evidence.
3. **Curated source records** — stable local records for high-value primary/authoritative evidence.

## Candidate entities

`python scripts/discover_candidates.py` writes:

- `generated/entity-candidates.json`
- `indexes/entity-candidates.md`

Each candidate includes a name, class hint, score, post/mention counts, first/last mention, representative posts and context snippets. Candidates are excluded if they already match a curated entity name/alias or appear in `config/entity-candidate-ignore.txt`.

Promotion is always manual: create an `entities/<type>/<slug>.md` note, then rebuild. Candidate extraction never writes to `entities/`.

## Reviewed relationships

Curated relationships live in `relationships/reviewed.yml`.

Required fields:

- `id` — stable relationship ID
- `from` / `to` — curated entity IDs
- `type` — relationship vocabulary such as `leader_of`, `developer_of`, `located_in`
- `directional` — boolean
- `evidence[]` — source post/source paths or URLs
- `confidence` — normally `high`, `medium` or `low`
- `created_by` — `human`, `rule` or `model`
- `review_status` — reviewed edges use `reviewed`

Optional fields include `valid_from`, `valid_to` and `note`.

The research builder validates referenced entity IDs and local post evidence, then writes:

- `generated/entity-relationships.json`
- `indexes/relationships.md`
- reviewed entity-to-entity edges in `generated/graph.json`

Reviewed edges are explicitly marked with `provenance: reviewed-relationship`; they are not inferred from co-occurrence.

## Curated source records

High-value evidence lives under `sources/<publisher-or-body>/<source-id>.md` with YAML front matter.

Recommended fields:

- `id`
- `title`
- `publisher`
- `source_type`
- `canonical_url`
- `archive_urls[]`
- `publication_date` / meeting date when known
- `related_entities[]`
- `related_topics[]`
- `cited_by[]`
- `review_status`
- optional local document path/checksum when preservation is appropriate

The builder writes:

- `generated/curated-sources.json`
- `indexes/source-records.md`
- source-record nodes and reviewed source/entity/topic/post edges in `generated/graph.json`

Raw outbound URLs remain in `generated/sources.json`; curated source records are deliberately selective.

## Review rule

Automation may rank, connect and regenerate deterministic data, but it must not silently promote candidates, create editorial relationships or convert arbitrary URLs into authoritative source records.
