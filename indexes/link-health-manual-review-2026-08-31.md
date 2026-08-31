# Link-health manual review — 31 August 2026

Manual review following the automated Monday link-health alert.

## What the review found

The automated report is checking the static Markdown corpus in `posts/**`, not the current live Southall Stories pages. Manual edits made in Micro.blog after the corpus import therefore remain in `indexes/link-health.md` until the corpus is refreshed or the corresponding Markdown is updated.

The current checker also treats every HTTP error >= 400, timeout, URL/network failure or parse failure as `unreachable`. `unreachable` can therefore mean bot blocking, throttling or a temporary fetch failure rather than a broken public link. This is especially likely for ModernGov, LinkedIn, Substack, Police.uk, archive.org and similar services.

## Live-site fixes manually confirmed

David reported replacing the first eight entries classified as `gone` in `indexes/link-health.md`. The live Southall Stories pages were checked on 31 August 2026 and show the edits rather than the stale corpus versions.

1. `http://www.aresok.org/npg/nioshdbs/calc.htm` — **Health Risks of Exposure to Benzene** — replaced on the live article.
2. `https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/337516/hpa_benzene_toxicological_overview_v2.pdf` — **Health Risks of Exposure to Benzene** — replaced on the live article.
3. `https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/522459/Benzene_IM_PHE_050516.pdf` — **Health Risks of Exposure to Benzene** — replaced on the live article.
4. `https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/561046/benzene_general_information.pdf` — **Health Risks of Exposure to Benzene** — replaced on the live article.
5. `https://docs.google.com/document/d/e/2PACX1vTtn2vpBsl8Z4Lqn1NjEOQjZIJ2JXbmnTjrflIKZTVsOMZRqy75zEoDwo205cAiMcRsCxoy2x8DogF/pub` — **Lies, Damned Lies, and Statistics?** — repaired; the current live link opens the Technical Note for Residents.
6. `https://www.ealing.gov.uk/download/downloads/id/3349/ed102_-_ealing_in_london_2_edition_2_spring_2011.pdf` — **Ealing Monopoly** — replaced with the archived PDF; the live link resolves to the Wayback copy.
7. `https://www.ealing.gov.uk/info/201033/council_and_local_decisions/516/complaints/6` — **How to Report Nuisance and Pollution in Ealing** — replaced on the live article.
8. `https://www.ealing.gov.uk/info/201065/elections/3270/find_your_polling_station` — **Sixty-Four Years On Your Side** — replaced on the live article.

## Additional live fix

The stale `https://ealing.moderngov.co.uk/` link reported for **The Meeting that Ended Local Democracy in Southall** has been replaced on the live article with:

`https://ealing.moderngov.co.uk/ieListMeetings.aspx?CId=231&Year=0`

## Recommended checker behaviour

- Treat `gone` (404/410) and `suspicious-redirect` as actionable.
- Treat `unreachable` as diagnostic/transient unless it fails repeatedly across checks.
- Do not email a newly-degraded alert for a first `unreachable` result.
- Refresh the corpus from Micro.blog, or introduce a live-link reconciliation step, before treating the static `posts/**` snapshot as authoritative for current link health.

This note is intentionally separate from the generated `indexes/link-health.md`, so the next automated rebuild will not overwrite the manual review.
