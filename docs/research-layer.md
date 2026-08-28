# Research layer

The research layer turns the immutable Southall Stories corpus into a navigable knowledge graph without rewriting source posts.

## Curated notes

`entities/` and `topics/` contain human-maintained assertions. Each note has a stable `id`, display `name` and aliases used for deterministic mention matching. Entity notes also have a `type` (`person`, `organisation` or `place`).

Adding or correcting an alias is an editorial change and is therefore visible in Git history.

## Generated outputs

Run:

```bash
python scripts/build_research.py
```

The build writes:

- `generated/entity-mentions.json` — entity → matching posts, including the alias that matched
- `generated/topic-mentions.json` — topic → matching posts
- `generated/backlinks.json` — entity, topic and internal post backlinks
- `generated/sources.json` — distinct outbound URLs with citing posts and domains
- `generated/graph.json` — combined nodes and typed edges for posts, entities, topics and source domains
- `generated/research-summary.json` — build counts for sanity checking
- `indexes/entities.md`
- `indexes/topics.md`
- `indexes/backlinks.md`
- `indexes/source-graph.md`

Generated matching is deliberately conservative and explainable. It does not promote unreviewed named-entity extraction into curated entity pages.

## Graph edge types

- `entity -> post`: `mentioned-in`
- `topic -> post`: `mentioned-in`
- `post -> post`: `links-to`
- `post -> source-domain`: `cites-domain`

This is deliberately a useful minimum. Later layers can add reviewed entity-to-entity relationships, preserved source documents, source-document hashes, time-aware co-occurrence, and richer graph exports without changing the corpus model.

## Automation

The GitHub Actions workflow rebuilds the derived layer whenever posts, curated notes or the research build script change. Generated outputs do not themselves trigger the workflow, preventing commit loops.
