# Archive model

Southall Zettel separates source material, editorial knowledge and generated analysis so that research convenience never obscures provenance.

## 1. Source corpus

`posts/` contains dated Southall Stories post files copied from Micro.blog exports. Importing must preserve the source Markdown and YAML front matter rather than rewriting it into a new house format.

The original export ZIP should be retained separately as a dated baseline backup. A manifest can record its filename, date, checksum and import statistics without requiring the binary archive itself to live in Git.

## 2. Curated research notes

`entities/` and `topics/` are deliberately human-maintained.

Suggested entity classes:

- `entities/people/`
- `entities/organisations/`
- `entities/places/`

A curated entity note should eventually record stable names/aliases, a short description, relevant source links and reviewed relationships. An entity page is an editorial assertion, so machine extraction alone should not create one automatically.

`topics/` is for recurring issues rather than named things: air pollution, local democracy, housing development, children's centres, planning, pensions and similar themes.

## 3. Sources

`sources/` is for material relied upon in reporting: council papers, ModernGov records, regulatory documents, datasets, archived web pages and other primary/secondary evidence.

Initially, source-domain and outbound-link indexes can be generated directly from posts. Full source preservation can be added incrementally where it has research value and where copyright/licensing allows.

## 4. Generated material

`generated/` may contain:

- post inventory (`posts.json`)
- detected entity mentions
- outbound-link graph
- co-occurrence data
- backlinks
- search indexes

Nothing in `generated/` should be treated as authoritative merely because it was machine-produced. It must always be possible to delete the directory and rebuild it from the corpus plus curated notes.

## 5. Backlinks

Backlinks should be computed rather than manually maintained wherever possible. A future build can answer questions such as:

- Which posts mention Peter Mason?
- Where do Berkeley Group and Southall Gasworks co-occur?
- Which reporting repeatedly cites the same council document?
- What older posts are relevant to a newly published investigation?
- Which people, places or issues form recurring clusters over time?

## 6. Future snapshots

Each fresh Micro.blog export should be imported without overwriting history outside normal Git versioning. Git diffs then provide an audit trail for new posts and edits to existing published material.

The archive is therefore both a current research corpus and a record of how the published corpus changes over time.
