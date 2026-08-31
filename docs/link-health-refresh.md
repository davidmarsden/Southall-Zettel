# Keeping the Southall Stories corpus current

The link-health checker operates on the Markdown snapshot in `posts/**`, not directly on the live Southall Stories site.

When links are corrected in Micro.blog, re-import or otherwise refresh the affected post Markdown in Southall-Zettel before relying on the next scheduled link-health report. The import script is `scripts/import_microblog.py` and deliberately treats imported post Markdown as the corpus source of truth.

Recommended maintenance sequence:

1. Export current Southall Stories content from Micro.blog.
2. Run `python scripts/import_microblog.py <extracted-export> --repo .`.
3. Review the resulting post changes.
4. Commit the refreshed corpus.
5. Let the normal research-layer workflow rebuild citation metadata and link health.

This prevents repaired live links from remaining as stale zombie URLs in the research corpus.
