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

Directories are created by the importer as they become needed; empty folders are not committed.

## Baseline

The first source corpus is the Micro.blog export supplied on **27 August 2026**. Initial inspection found 69 journalistic posts spanning July 2018 to May 2026, with useful front matter including titles, dates, summaries, categories, Micro.blog IDs, canonical URLs and media metadata.

## First workflow

```bash
python -m pip install -r requirements.txt
python scripts/import_microblog.py /path/to/microblog-export
```

The importer copies dated posts into `posts/YYYY/MM/DD/`, preserves their source text, and writes a machine-readable inventory to `generated/posts.json` plus simple Markdown indexes.

Future imports should be run against a fresh Micro.blog export. Git then becomes the audit trail for additions and changes to the published corpus.

## Status

Early baseline build. The priority is a clean, reproducible corpus before entity extraction or AI-generated cross-linking is added.
