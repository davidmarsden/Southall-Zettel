# Southall-Zettel

A research corpus and civic-memory layer built from the published Southall Stories archive.

The repository keeps the original journalism corpus immutable while building a reviewed research layer around it: entities, topics, source records, relationships, backlinks, public export data, citation metadata, and link-health monitoring.

## Research layer

Generated outputs are rebuildable from the source corpus and curated records. Human-reviewed assertions remain separate from machine-generated candidates.

## Link health

External links cited by Southall Stories are checked and recorded in `generated/link-health.json`, with a human-readable report at `indexes/link-health.md`.

The report distinguishes healthy links, ordinary redirects, suspicious redirects, unreachable links, and definite 404/410 failures. It also records which Southall Stories posts contain each problem link.

A weekly full check runs through GitHub Actions. Newly degraded links can trigger a GitHub issue and email alert. The report also records links resolved since the previous check, including links that recover and links removed or replaced in the source article.

For genuine link rot, Micro.blog’s archived-link feature can be used to recover or replace the original destination while preserving the reporting context.
