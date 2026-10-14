# Southall Stories link integrity and evidence register

This public register records broken, blocked, archived and intentionally missing links in published Southall Stories articles. The original URL is immutable evidence; do not overwrite it when recording a replacement.

## Fields
- id: stable identifier
- original_url: exact URL reported
- affected_post: published page or Micro.blog edit URL
- audit_date: date of audit
- audit_result: reported HTTP outcome, not independently verified
- classification: broken | blocked | redirected | archived | malformed | intentional | unresolved
- replacement_url: candidate or verified destination
- archive_url: preserved snapshot
- decision: proposed action
- status: pending | verify | intentional | resolved
- notes: provenance and verification caveats

A 403 or 999 is not proof that a document is gone. Never automatically replace live source URLs with archive URLs. Verify equivalence before a 301. Do not redirect security-probe paths. Archive captures must retain source provenance and capture date. Repairs to blog content belong in Micro.blog; theme/feed/redirect changes belong in the Southall Stories theme repository. Sensitive or unpublished material belongs in private Southall Research.

Dated audit imports are immutable snapshots; the cumulative register tracks subsequent decisions.
