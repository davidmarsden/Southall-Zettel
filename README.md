# Southall Zettel

A version-controlled research corpus built from **Southall Stories**.

The aim is broader than backup: preserve published journalism in its original form, then build a human-readable research layer of posts, entities, topics, sources, indexes and generated backlinks without changing the live site.

## Principles

1. **Originals are immutable.** Source exports are preserved as snapshots and are never silently rewritten.
2. **Curated knowledge is explicit.** Human-maintained entity and topic notes live separately from source material.
3. **Generated data is disposable.** Backlinks, inventories and machine-detected relationships can always be rebuilt from the corpus.
4. **Provenance matters.** Every imported post keeps its Micro.blog metadata and canonical URL.
5. **Automation should assist research, not invent facts.** Machine-generated entity matches are candidates until reviewed.

## Repository layout

```text
original/       untouched source snapshots or snapshot manifests
posts/          normalized copy of dated Southall Stories posts
entities/       curated people, organisations and places
topics/         curated issue/topic notes
sources/        source notes and eventually preserved source documents
indexes/        human-readable indexes
generated/      machine-generated inventories, backlinks and graphs
scripts/        repeatable import/build tools
docs/           archive conventions and documentation
```

## Baseline

The first source corpus is the Micro.blog export supplied on **27 August 2026**: 69 journalistic posts spanning July 2018 to May 2026. Every baseline post is preserved byte-for-byte and recorded in `generated/posts.json` with a SHA-256 digest.

## Import a fresh Micro.blog export

```bash
python -m pip install -r requirements.txt
python scripts/import_microblog.py /path/to/microblog-export
```

The importer copies dated posts into `posts/YYYY/MM/DD/`, preserves their source text, and updates the post inventory and basic indexes.

## Build the research layer

```bash
python scripts/build_research.py
```

This derives entity and topic mentions, internal backlinks, outbound-source records, a source-domain graph, a combined knowledge graph and human-readable research indexes. See [`docs/research-layer.md`](docs/research-layer.md).

Curated knowledge lives in `entities/` and `topics/`; generated relationships live in `generated/`. The GitHub Actions workflow rebuilds the derived layer automatically when posts, curated notes or the research builder change.

## Status

**Baseline corpus complete; research layer v1 active.** The next phase is iterative curation: improve aliases, add entities/topics as reporting demands, preserve high-value primary sources, and enrich reviewed relationships without altering the source corpus.
