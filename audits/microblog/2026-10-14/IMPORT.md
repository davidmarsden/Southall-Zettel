# Importing the complete 14 October 2026 Micro.blog audit

**Status: awaiting verbatim source export.** The nine findings in `evidence/link-integrity/register.csv` are a curated baseline, not a full audit. Do not reconstruct missing entries from memory.

## Source capture

Save the original Micro.blog audit report unedited alongside this document as `raw-audit.md` or `raw-audit.html` (preserve the source exactly). Then transcribe/export each individual finding into `raw-occurrences.csv` with columns:

```csv
original_url,affected_post,audit_result,section,notes
```

Include every occurrence, even when one target URL appears in multiple articles. Use `section` for broken-links, feeds, missing-paths, or another exact report section. Record absent values as blank; do not invent statuses, article associations or redirect targets.

Run:

```sh
python3 audits/microblog/import_audit.py audits/microblog/2026-10-14/raw-occurrences.csv audits/microblog/2026-10-14/occurrences.csv
```

The output preserves all input occurrences, and adds a normalized comparison key. It does **not** automatically classify, repair, or collapse records. The cumulative register remains the decision log for distinct URLs; the occurrences file is the evidence of every affected page.

## Verification checklist

- Confirm imported row count equals original report row count, by section.
- Confirm all repeated URLs retain their separate affected article references.
- Distinguish HTTP 403 bot restrictions from verified disappearance.
- Preserve deliberate 404s, notably the Dhindsa joke.
- Do not redirect vulnerability probes.
- Retain original and archived URLs together; verify equivalence before redirects.
- Treat missing pagination/month archives as separate site-routing findings, not source-document loss.
- Keep repairs in separate website/theme PRs after verification.

No full-import claim is valid until the original source is attached and counts reconcile.
