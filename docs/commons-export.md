# Civic Commons public export

`generated/commons.json` is the stable, deliberately narrow public data contract from Southall-Zettel to Ealing Civic Commons.

## Versioning

The current export uses `schema_version: 1` and is described by `schemas/commons-v1.schema.json`.

Breaking changes require a new schema version. Additive fields may be introduced within a version only when existing consumers can safely ignore them.

The export is deterministic: it contains no build timestamp or transient commit metadata, so unchanged reviewed inputs produce unchanged output bytes.

## What is exported

- curated entities: stable IDs, names, types, aliases and descriptions
- curated topics
- canonical Southall Stories post metadata and content hashes
- reviewed entity-to-entity relationships with evidence, confidence and review metadata
- deterministic entity/topic-to-post mention links
- deterministic post-to-post links found in source articles
- curated high-value source records and their reviewed entity/topic/post references

Stable public identifiers are typed:

- `entity:<local-id>`
- `topic:<local-id>`
- `post:<Micro.blog post_id>`
- `relationship:<local-id>`
- `source:<local-id>`

Consumers should use these identifiers rather than Southall-Zettel filenames or directory structure.

## What is deliberately excluded

- candidate entities or unreviewed assertions
- raw source-domain nodes
- the complete set of outbound URLs
- full Southall Stories article text
- machine-generated relationship guesses
- internal note paths and implementation-specific graph nodes

The top-level `policy` object makes these exclusions machine-readable.

## Provenance and authority

Civic Commons should distinguish the following provenance values:

- `curated-entity` / `curated-topic`: human-reviewed Southall-Zettel classifications
- `reviewed-relationship`: a human-reviewed assertion with explicit corpus evidence
- `reviewed-source-record`: a human-reviewed high-value evidence record
- `southall-stories-corpus`: immutable source-post metadata
- `deterministic-alias-match`: generated mention link based on curated names/aliases; useful enrichment, not a new editorial assertion
- `source-post-link`: a literal link between corpus posts

Only relationships with `review_status: reviewed` enter the public export.

## Consumer rules for Civic Commons

Civic Commons may treat curated entities, topics, reviewed relationships and curated source records as the authoritative Southall-Zettel layer, while preserving their provenance and evidence.

Deterministic mention links are enrichment. They may be used for discovery and "Related civic memory" features, but should not be presented as if a human separately asserted each mention relationship.

Southall Stories remains the canonical publisher of its articles. Commons should link to `posts[].url`; it should not reconstruct or republish full article bodies from this export.

The export should be optional enrichment. A Commons build or page must remain usable if Southall-Zettel cannot be reached or if it presents an unsupported `schema_version`.

## Validation

`scripts/generate_commons.py` performs semantic checks before writing the export, including:

- unique stable IDs
- valid relationship endpoints
- reviewed-only relationship/source records
- valid relationship evidence references
- valid source references to posts/entities/topics
- valid deterministic link endpoints

The rebuild workflow also parses the resulting JSON before committing generated files.

## Intended first integration

The safest first Civic Commons integration is deterministic matching by Southall Stories canonical URL. Once an item is matched, Commons can display:

- related people, organisations and places
- related topics
- earlier/later Southall Stories reporting
- reviewed entity relationships
- selected supporting primary sources

This keeps the boundary explicit:

`Southall Stories → Southall-Zettel → generated/commons.json → Ealing Civic Commons`

Suggestions or corrections from Commons may later flow back as review candidates, never as automatic curated assertions.
