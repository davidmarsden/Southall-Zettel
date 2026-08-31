# Southall Stories draft editorial workflow

Southall-Zettel can act as a Git-backed newsroom workspace before an article reaches Micro.blog.

## Where drafts live

Put unpublished Southall Stories articles in:

`posts/drafts/`

Subdirectories are allowed if useful.

A minimal draft can look like:

```markdown
---
title: "Working title"
categories:
  - Investigations
review_complete: false
---

Article text here.
```

Drafts are not included in the normal live-corpus sync and are not published merely because they are committed to GitHub.

## Automatic review

Whenever a draft changes, `.github/workflows/review-drafts.yml` runs `scripts/review_drafts.py`.

The review is deliberately advisory. It checks for:

- links already known to be broken/actionable in the citation-health cache;
- blocked, unreachable or not-yet-checked links, reported separately as inconclusive;
- obvious placeholders such as `TODO`, `TK`, `CHECK`, `SOURCE?` and `[citation needed]`;
- dates, figures, percentages and quotations without a nearby external citation;
- Markdown or HTML images missing alt text;
- recognised people, organisations and places from `entities/**`, including aliases;
- previously published Southall Stories articles sharing those entities.

Outputs are written to:

- `indexes/draft-review.md` — summary dashboard;
- `generated/draft-review/<draft>.md` — readable review for each draft;
- `generated/draft-review.json` — machine-readable results.

A mechanical **PASS** only means the automated blockers are clear. It does not certify factual accuracy, fairness, legal safety, tone or publication readiness.

## Human review

Use the generated report as a checklist. Resolve what matters, ignore false-positive heuristics where appropriate, and rerun by committing the edited draft or manually running **Review Southall Stories drafts** in GitHub Actions.

When satisfied, set:

```yaml
review_complete: true
```

This records editorial judgement; the automated script does not set it for you.

## Publishing

The existing reverse-publishing lane remains deliberately separate from review.

For an already-published article, use the guarded `publish_to_microblog: true` workflow documented in `docs/publishing-to-microblog.md`.

For a new article, the next publishing extension should create a Micro.blog draft from a reviewed file in `posts/drafts/**`, record the resulting Micro.blog identity/canonical URL, and then move or transform it into the normal published `posts/YYYY/MM/DD/**` corpus after verification.

The intended flow is therefore:

`Markdown Hand or editor → posts/drafts/** → automated review → human review → Micro.blog draft → final review → publish → automatic live-to-Zettel sync`

This keeps the research/archive layer, editorial judgement and production publishing distinct while allowing them to share the same Markdown source.
