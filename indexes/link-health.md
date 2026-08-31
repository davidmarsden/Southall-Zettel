# Link health

Automated health checks for external links cited by the Southall Stories research corpus.

- Checked/cached links: **531**
- Actionable problems: **12**
- Inconclusive automated checks: **67**
- Newly degraded since the previous report: **0**
- Resolved/de-escalated since the previous report: **6**
- Ordinary redirects: **27**

`gone` means HTTP 404/410. `blocked` means the destination rejected the automated checker (for example 403/429). A single `unreachable` result is treated as inconclusive; it becomes actionable only after repeated scheduled failures. `suspicious-redirect` means a URL resolves successfully but appears to have been repointed to unrelated content.

For genuine link rot, Southall Stories can use Micro.blog’s archived-link feature to recover or replace the destination while preserving the original reporting context.

## Resolved or de-escalated since last check

- [https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/337516/hpa_benzene_toxicological_overview_v2.pdf](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/337516/hpa_benzene_toxicological_overview_v2.pdf) — was `gone`; removed or replaced in the Southall Stories corpus.
  - [Health Risks of Exposure to Benzene](https://southallstories.uk/2018/08/03/health-risks-of-exposure-to/)
- [https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/522459/Benzene_IM_PHE_050516.pdf](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/522459/Benzene_IM_PHE_050516.pdf) — was `gone`; removed or replaced in the Southall Stories corpus.
  - [Health Risks of Exposure to Benzene](https://southallstories.uk/2018/08/03/health-risks-of-exposure-to/)
- [LGC Awards 2027](https://awards.lgcplus.com/lgca2026/en/page/2026-shortlist) — was `suspicious-redirect`; removed or replaced in the Southall Stories corpus.
  - [Boomerang! Ten Years Sorting Out Fly-tipping](https://southallstories.uk/2026/03/01/boomerang-ten-years-sorting-out/)
  - [This Is Our Home. It's a Tip.](https://southallstories.uk/2026/04/30/this-is-our-home-its/)
- [https://docs.google.com/document/d/e/2PACX1vTtn2vpBsl8Z4Lqn1NjEOQjZIJ2JXbmnTjrflIKZTVsOMZRqy75zEoDwo205cAiMcRsCxoy2x8DogF/pub](https://docs.google.com/document/d/e/2PACX1vTtn2vpBsl8Z4Lqn1NjEOQjZIJ2JXbmnTjrflIKZTVsOMZRqy75zEoDwo205cAiMcRsCxoy2x8DogF/pub) — was `gone`; removed or replaced in the Southall Stories corpus.
  - [Lies, Damned Lies, and Statistics?](https://southallstories.uk/2018/11/02/lies-damned-lies-and-statistics/)
- [https://www.ealing.gov.uk/download/downloads/id/3349/ed102_-_ealing_in_london_2_edition_2_spring_2011.pdf](https://www.ealing.gov.uk/download/downloads/id/3349/ed102_-_ealing_in_london_2_edition_2_spring_2011.pdf) — was `gone`; removed or replaced in the Southall Stories corpus.
  - [Ealing Monopoly](https://southallstories.uk/2022/03/25/ealing-monopoly/)
- [https://www.ealing.gov.uk/news/article/1925/nearly_900_new_genuinely_affordable_homes_in_ealing_since_april_2018](https://www.ealing.gov.uk/news/article/1925/nearly_900_new_genuinely_affordable_homes_in_ealing_since_april_2018) — was `gone`; removed or replaced in the Southall Stories corpus.
  - [Look at these Bricks!](https://southallstories.uk/2021/05/03/look-at-these-bricks/)

## Needs attention

### gone: http://www.aresok.org/npg/nioshdbs/calc.htm

- Original: [http://www.aresok.org/npg/nioshdbs/calc.htm](http://www.aresok.org/npg/nioshdbs/calc.htm)
- Current destination: [https://aresok.org/npg/nioshdbs/calc.htm](https://aresok.org/npg/nioshdbs/calc.htm)
- HTTP: `404`
- Action: Use Micro.blog’s archived version or replace the source URL.
- Appears in:
  - [Health Risks of Exposure to Benzene](https://southallstories.uk/2018/08/03/health-risks-of-exposure-to/) — anchor text: `aresok.org/npg/nioshdbs/c…`

### gone: https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/561046/benzene_general_information.pdf

- Original: [https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/561046/benzene_general_information.pdf](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/561046/benzene_general_information.pdf)
- Current destination: [https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/791325/Benzene_general_information_2019.pdf](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/791325/Benzene_general_information_2019.pdf)
- HTTP: `410`
- Action: Use Micro.blog’s archived version or replace the source URL.
- Appears in:
  - [Health Risks of Exposure to Benzene](https://southallstories.uk/2018/08/03/health-risks-of-exposure-to/) — anchor text: `assets.publishing.service.gov.uk/government/upl…`

### gone: https://www.ealing.gov.uk/info/201033/council_and_local_decisions/516/complaints/6

- Original: [https://www.ealing.gov.uk/info/201033/council_and_local_decisions/516/complaints/6](https://www.ealing.gov.uk/info/201033/council_and_local_decisions/516/complaints/6)
- HTTP: `404`
- Action: Use Micro.blog’s archived version or replace the source URL.
- Appears in:
  - [How to Report Nuisance and Pollution in Ealing](https://southallstories.uk/2026/01/22/its-never-enough-until-its/) — anchor text: `the nuisance`

### gone: https://www.ealing.gov.uk/info/201065/elections/3270/find_your_polling_station

- Original: [https://www.ealing.gov.uk/info/201065/elections/3270/find_your_polling_station](https://www.ealing.gov.uk/info/201065/elections/3270/find_your_polling_station)
- HTTP: `404`
- Action: Use Micro.blog’s archived version or replace the source URL.
- Appears in:
  - [Sixty-Four Years On Your Side](https://southallstories.uk/2026/05/06/sixtyfour-years-on-your-side/) — anchor text: `Find your polling station »`

### gone: https://www.ealing.gov.uk/info/201281/council_priorities/2866/tackling_the_climate_crisis

- Original: [https://www.ealing.gov.uk/info/201281/council_priorities/2866/tackling_the_climate_crisis](https://www.ealing.gov.uk/info/201281/council_priorities/2866/tackling_the_climate_crisis)
- HTTP: `404`
- Action: Use Micro.blog’s archived version or replace the source URL.
- Appears in:
  - [Feeling the Heat](https://southallstories.uk/2026/05/25/feeling-the-heat/) — anchor text: `Climate Emergency`

### gone: https://ealingperformance.inphase.com/Detail/865_17759?s=09

- Original: [https://ealingperformance.inphase.com/Detail/865_17759?s=09](https://ealingperformance.inphase.com/Detail/865_17759?s=09)
- HTTP: `404`
- Action: Use Micro.blog’s archived version or replace the source URL.
- Appears in:
  - [Look at these Bricks!](https://southallstories.uk/2021/05/03/look-at-these-bricks/) — anchor text: `ealingperformance.inphase.com/Detail/865\_177…`

### gone: https://en.wikipedia.org/wiki/Communist_Party_of_Great_Britain_(Marxist%E2%80%93Leninist

- Original: [https://en.wikipedia.org/wiki/Communist_Party_of_Great_Britain_(Marxist%E2%80%93Leninist](https://en.wikipedia.org/wiki/Communist_Party_of_Great_Britain_(Marxist%E2%80%93Leninist)
- HTTP: `404`
- Action: Use Micro.blog’s archived version or replace the source URL.
- Appears in:
  - [Who Does Peter Mason Really Represent?](https://southallstories.uk/2026/05/07/who-does-peter-mason-really/) — anchor text: `CPGB(ML)`

### gone: https://en.wikipedia.org/wiki/Peter_Mason_(politician

- Original: [https://en.wikipedia.org/wiki/Peter_Mason_(politician](https://en.wikipedia.org/wiki/Peter_Mason_(politician)
- HTTP: `404`
- Action: Use Micro.blog’s archived version or replace the source URL.
- Appears in:
  - [Who Does Peter Mason Really Represent?](https://southallstories.uk/2026/05/07/who-does-peter-mason-really/) — anchor text: `Peter Robert Ness`

### gone: https://www.mylondon.news/news/west-london-news/ealing-school-catering-staff-paid-20380035

- Original: [https://www.mylondon.news/news/west-london-news/ealing-school-catering-staff-paid-20380035](https://www.mylondon.news/news/west-london-news/ealing-school-catering-staff-paid-20380035)
- HTTP: `404`
- Action: Use Micro.blog’s archived version or replace the source URL.
- Appears in:
  - [When is a Hustings not a Hustings?](https://southallstories.uk/2026/04/30/when-is-a-hustings-not/) — anchor text: `Ealing school catering staff were being paid £8.91 per hour`

### gone: https://www.plands.org/en/articles-speeches/articles/2023/anatomy-of-a-massacre-ed-dawayima,-hebron-district

- Original: [https://www.plands.org/en/articles-speeches/articles/2023/anatomy-of-a-massacre-ed-dawayima,-hebron-district](https://www.plands.org/en/articles-speeches/articles/2023/anatomy-of-a-massacre-ed-dawayima,-hebron-district)
- HTTP: `404`
- Action: Use Micro.blog’s archived version or replace the source URL.
- Appears in:
  - [Cactuses Never Die](https://southallstories.uk/2026/05/03/cactuses-never-die/) — anchor text: `Palestine Land Society's detailed account`

### gone: https://www.telegraph.co.uk/gift/9249993120211e2f

- Original: [https://www.telegraph.co.uk/gift/9249993120211e2f](https://www.telegraph.co.uk/gift/9249993120211e2f)
- HTTP: `404`
- Action: Use Micro.blog’s archived version or replace the source URL.
- Appears in:
  - [Who Does Peter Mason Really Represent?](https://southallstories.uk/2026/05/07/who-does-peter-mason-really/) — anchor text: `personally voted to block Andy Burnham`

### suspicious-redirect: Lamp column electric vehicle charge points (EVCP) consultation | Lamp column electric vehicle charge points (EVCP) consultation | Ealing Council

- Original: [https://www.ealing.gov.uk/info/201112/community_and_living/2916/ealing_race_equality_commission](https://www.ealing.gov.uk/info/201112/community_and_living/2916/ealing_race_equality_commission)
- Current destination: [https://www.ealing.gov.uk/info/201307/past_consultations_2022/2916/lamp_column_electric_vehicle_charge_points_evcp_consultation](https://www.ealing.gov.uk/info/201307/past_consultations_2022/2916/lamp_column_electric_vehicle_charge_points_evcp_consultation)
- HTTP: `200`
- Action: Check the Micro.blog archived version; the live URL now appears to point at unrelated content.
- Appears in:
  - [Feeling the Heat](https://southallstories.uk/2026/05/25/feeling-the-heat/) — anchor text: `Ealing Race Equality Commission`

## Inconclusive automated checks

These links are retained for retry and do not trigger an alert or imply that the citation should be edited.

- **blocked** — [https://ealing.moderngov.co.uk/ieListMeetings.aspx?CId=231&Year=0](https://ealing.moderngov.co.uk/ieListMeetings.aspx?CId=231&Year=0) — HTTP 403; streak 1
- **unreachable** — [https://archive.ph/JZAll](https://archive.ph/JZAll) — HTTP 429; streak 0
- **unreachable** — [https://archive.ph/kfpaA](https://archive.ph/kfpaA) — HTTP 429; streak 0
- **unreachable** — [https://ccrjustice.org/Corporate-Capture](https://ccrjustice.org/Corporate-Capture) — HTTP 403; streak 0
- **unreachable** — [https://ealing.cmis.uk.com/ealing/Document.ashx?czJKcaeAi5tUFL1DTL2UE4zNRBcoShgo=WQhOaubzPPxk1yVzZleRxFZb7u/GmxWvbCWE1o9prqXCN7mbG5lCZg%3D%3D&rUzwRPf%2BZ3zd4E7Ikn8Lyw%3D%3D=pwRE6AGJFLDNlh225F5QMaQWCtPHwdhUfCZ/LUQzgA2uL5jNRG4jdQ%3D%3D&mCTIbCubSFfXsDGW9IXnlg%3D%3D=hFflUdN3100%3D&kCx1AnS9/pWZQ40DXFvdEw%3D%3D=hFflUdN3100%3D&uJovDxwdjMPoYv%2BAJvYtyA%3D%3D=ctNJFf55vVA%3D&FgPlIEJYlotS%2BYGoBi5olA%3D%3D=NHdURQburHA%3D&d9Qjj0ag1Pd993jsyOJqFvmyB7X0CSQK=ctNJFf55vVA%3D&WGewmoAfeNR9xqBux0r1Q8Za60lavYmz=ctNJFf55vVA%3D&WGewmoAfeNQ16B2MHuCpMRKZMwaG1PaO=ctNJFf55vVA%3D](https://ealing.cmis.uk.com/ealing/Document.ashx?czJKcaeAi5tUFL1DTL2UE4zNRBcoShgo=WQhOaubzPPxk1yVzZleRxFZb7u/GmxWvbCWE1o9prqXCN7mbG5lCZg%3D%3D&rUzwRPf%2BZ3zd4E7Ikn8Lyw%3D%3D=pwRE6AGJFLDNlh225F5QMaQWCtPHwdhUfCZ/LUQzgA2uL5jNRG4jdQ%3D%3D&mCTIbCubSFfXsDGW9IXnlg%3D%3D=hFflUdN3100%3D&kCx1AnS9/pWZQ40DXFvdEw%3D%3D=hFflUdN3100%3D&uJovDxwdjMPoYv%2BAJvYtyA%3D%3D=ctNJFf55vVA%3D&FgPlIEJYlotS%2BYGoBi5olA%3D%3D=NHdURQburHA%3D&d9Qjj0ag1Pd993jsyOJqFvmyB7X0CSQK=ctNJFf55vVA%3D&WGewmoAfeNR9xqBux0r1Q8Za60lavYmz=ctNJFf55vVA%3D&WGewmoAfeNQ16B2MHuCpMRKZMwaG1PaO=ctNJFf55vVA%3D) — no HTTP response; streak 0
- **unreachable** — [https://ealing.cmis.uk.com/ealing/Meetings/tabid/70/ctl/ViewMeetingPublic/mid/397/Meeting/6876/Committee/3/Default.aspx](https://ealing.cmis.uk.com/ealing/Meetings/tabid/70/ctl/ViewMeetingPublic/mid/397/Meeting/6876/Committee/3/Default.aspx) — no HTTP response; streak 0
- **unreachable** — [https://Ealing.moderngov.co.uk/ieDecisionDetails.aspx?Id=958&LLL=0](https://Ealing.moderngov.co.uk/ieDecisionDetails.aspx?Id=958&LLL=0) — HTTP 403; streak 0
- **unreachable** — [https://ealing.moderngov.co.uk/Data/Pension%20Fund%20Panel/202111251900/Agenda/Appendix%202%20-%20The%20Pension%20Fund%20Newsletter%202020-21.pdf](https://ealing.moderngov.co.uk/Data/Pension%20Fund%20Panel/202111251900/Agenda/Appendix%202%20-%20The%20Pension%20Fund%20Newsletter%202020-21.pdf) — HTTP 403; streak 0
- **unreachable** — [https://ealing.moderngov.co.uk/Data/Southall%20Broadway%20Ward%20Forum/201607121900/Agenda/Southall%20Broadway%20ward%20forum%20notes%2012%20July%2016.pdf](https://ealing.moderngov.co.uk/Data/Southall%20Broadway%20Ward%20Forum/201607121900/Agenda/Southall%20Broadway%20ward%20forum%20notes%2012%20July%2016.pdf) — HTTP 403; streak 0
- **unreachable** — [https://ealing.moderngov.co.uk/documents/g6611/Public%20reports%20pack%20Tuesday%2015-Jul-2025%2019.00%20Council.pdf?T=10](https://ealing.moderngov.co.uk/documents/g6611/Public%20reports%20pack%20Tuesday%2015-Jul-2025%2019.00%20Council.pdf?T=10) — HTTP 403; streak 0
- **unreachable** — [https://ealing.moderngov.co.uk/documents/s11538/Drug%20alcohol%20services%20by%20entering%20into%20two%20new%20leases%20and%20refurbishments.pdf](https://ealing.moderngov.co.uk/documents/s11538/Drug%20alcohol%20services%20by%20entering%20into%20two%20new%20leases%20and%20refurbishments.pdf) — HTTP 403; streak 0
- **unreachable** — [https://ealing.moderngov.co.uk/documents/s1725/Council%20Performance%20Year%20End%202021-22.pdf](https://ealing.moderngov.co.uk/documents/s1725/Council%20Performance%20Year%20End%202021-22.pdf) — HTTP 403; streak 0
- **unreachable** — [https://ealing.moderngov.co.uk/documents/s1726/Southall%20Reset.pdf](https://ealing.moderngov.co.uk/documents/s1726/Southall%20Reset.pdf) — HTTP 403; streak 0
- **unreachable** — [https://ealing.moderngov.co.uk/documents/s1728/Appendix%202%20Southall%20Planning%20Baseline%20Report.pdf](https://ealing.moderngov.co.uk/documents/s1728/Appendix%202%20Southall%20Planning%20Baseline%20Report.pdf) — HTTP 403; streak 0
- **unreachable** — [https://ealing.moderngov.co.uk/documents/s1730/Appendix%204%20South%20Road%20Bridge%20Widening%20June%202022.pdf](https://ealing.moderngov.co.uk/documents/s1730/Appendix%204%20South%20Road%20Bridge%20Widening%20June%202022.pdf) — HTTP 403; streak 0
- **unreachable** — [https://ealing.moderngov.co.uk/documents/s18496/Housing%20Development%20and%20Regeneration%20Report%20to%20Scrutiny.pdf](https://ealing.moderngov.co.uk/documents/s18496/Housing%20Development%20and%20Regeneration%20Report%20to%20Scrutiny.pdf) — HTTP 403; streak 0
- **unreachable** — [https://ealing.moderngov.co.uk/documents/s18754/Waste%20and%20Recycling%20Update.pdf](https://ealing.moderngov.co.uk/documents/s18754/Waste%20and%20Recycling%20Update.pdf) — HTTP 403; streak 0
- **unreachable** — [https://ealing.moderngov.co.uk/documents/s18754/Waste+and+Recycling+Update.pdf](https://ealing.moderngov.co.uk/documents/s18754/Waste+and+Recycling+Update.pdf) — HTTP 403; streak 0
- **unreachable** — [https://ealing.moderngov.co.uk/documents/s19482/Substance%20Misuse%20Service.pdf](https://ealing.moderngov.co.uk/documents/s19482/Substance%20Misuse%20Service.pdf) — HTTP 403; streak 0
- **unreachable** — [https://ealing.moderngov.co.uk/documents/s22212/FINAL%20Ealings%20Early%20Help%20Strategy%20Childrens%20Scrutiny%20Report_v1%2014.11.25.pdf](https://ealing.moderngov.co.uk/documents/s22212/FINAL%20Ealings%20Early%20Help%20Strategy%20Childrens%20Scrutiny%20Report_v1%2014.11.25.pdf) — HTTP 403; streak 0
- **unreachable** — [https://ealing.moderngov.co.uk/documents/s23017/Council%20Plan%20Performance%20Report%20Q2%20202526.pdf](https://ealing.moderngov.co.uk/documents/s23017/Council%20Plan%20Performance%20Report%20Q2%20202526.pdf) — HTTP 403; streak 0
- **unreachable** — [https://ealing.moderngov.co.uk/documents/s23226/4.2.%20Appendix%202%20-%20LBE%20Forvis%20Mazars%20ACR%202024-25.pdf](https://ealing.moderngov.co.uk/documents/s23226/4.2.%20Appendix%202%20-%20LBE%20Forvis%20Mazars%20ACR%202024-25.pdf) — HTTP 403; streak 0
- **unreachable** — [https://ealing.moderngov.co.uk/ieListDocuments.aspx?MId=6661](https://ealing.moderngov.co.uk/ieListDocuments.aspx?MId=6661) — HTTP 403; streak 0
- **unreachable** — [https://ealing.moderngov.co.uk/mgAi.aspx?ID=6020](https://ealing.moderngov.co.uk/mgAi.aspx?ID=6020) — HTTP 403; streak 0
- **unreachable** — [https://ealing.moderngov.co.uk/mgCommitteeDetails.aspx?ID=188](https://ealing.moderngov.co.uk/mgCommitteeDetails.aspx?ID=188) — HTTP 403; streak 0
- **unreachable** — [https://ealing.moderngov.co.uk/mgIssueHistoryHome.aspx?IId=9740&Opt=0](https://ealing.moderngov.co.uk/mgIssueHistoryHome.aspx?IId=9740&Opt=0) — HTTP 403; streak 0
- **unreachable** — [https://ealing.moderngov.co.uk/mgUserInfo.aspx?UID=116](https://ealing.moderngov.co.uk/mgUserInfo.aspx?UID=116) — HTTP 403; streak 0
- **unreachable** — [https://ealing.moderngov.co.uk/mgUserInfo.aspx?UID=149](https://ealing.moderngov.co.uk/mgUserInfo.aspx?UID=149) — HTTP 403; streak 0
- **unreachable** — [https://ealing.moderngov.co.uk/mgUserInfo.aspx?UID=164](https://ealing.moderngov.co.uk/mgUserInfo.aspx?UID=164) — HTTP 403; streak 0
- **unreachable** — [https://ealingindependents.org/](https://ealingindependents.org/) — HTTP 403; streak 0
- **unreachable** — [https://ealingindependents.org/what-we-stand-for/](https://ealingindependents.org/what-we-stand-for/) — HTTP 403; streak 0
- **unreachable** — [https://www.ealingitree.online/stories/canopy-cover/0](https://www.ealingitree.online/stories/canopy-cover/0) — no HTTP response; streak 0
- **unreachable** — [https://www.economist.com/britain/2026/03/30/right-wingers-want-ice-style-mass-deportations-in-britain](https://www.economist.com/britain/2026/03/30/right-wingers-want-ice-style-mass-deportations-in-britain) — HTTP 403; streak 0
- **unreachable** — [https://www.itv.com/news/london/2026-02-25/croydon-named-englands-fly-tipping-hotspot-with-seven-boroughs-in-top-ten](https://www.itv.com/news/london/2026-02-25/croydon-named-englands-fly-tipping-hotspot-with-seven-boroughs-in-top-ten) — no HTTP response; streak 0
- **unreachable** — [https://www.jewishnews.co.uk/best-of-british-three-uk-jews-now-working-in-the-heart-of-israels-government/](https://www.jewishnews.co.uk/best-of-british-three-uk-jews-now-working-in-the-heart-of-israels-government/) — HTTP 403; streak 0
- **unreachable** — [https://www.linkedin.com/in/jags-sanghera-04722153](https://www.linkedin.com/in/jags-sanghera-04722153) — HTTP 999; streak 0
- **unreachable** — [https://www.linkedin.com/in/peter-mason-5a377941](https://www.linkedin.com/in/peter-mason-5a377941) — HTTP 999; streak 0
- **unreachable** — [https://www.linkedin.com/in/yairzivan](https://www.linkedin.com/in/yairzivan) — HTTP 999; streak 0
- **unreachable** — [https://www.london.gov.uk/who-we-are/what-london-assembly-does/questions-mayor/find-an-answer/retrofitting-homes-ealing](https://www.london.gov.uk/who-we-are/what-london-assembly-does/questions-mayor/find-an-answer/retrofitting-homes-ealing) — HTTP 403; streak 0
- **unreachable** — [https://news.sky.com/story/jeremy-corbyn-to-face-confidence-vote-from-jewish-labour-movement-11686632](https://news.sky.com/story/jeremy-corbyn-to-face-confidence-vote-from-jewish-labour-movement-11686632) — HTTP 403; streak 0
- **unreachable** — [https://onlinelibrary.wiley.com/doi/epdf/10.1111/j.1553-2712.2000.tb01889.x](https://onlinelibrary.wiley.com/doi/epdf/10.1111/j.1553-2712.2000.tb01889.x) — HTTP 403; streak 0
- **unreachable** — [https://open.substack.com/pub/southall/p/a-town-ignored-southall-after-16](https://open.substack.com/pub/southall/p/a-town-ignored-southall-after-16) — HTTP 403; streak 0
- **unreachable** — [https://open.substack.com/pub/southall/p/real-change-not-empty-consultations](https://open.substack.com/pub/southall/p/real-change-not-empty-consultations) — HTTP 403; streak 0
- **unreachable** — [https://open.substack.com/pub/southall/p/southall-deserves-better](https://open.substack.com/pub/southall/p/southall-deserves-better) — HTTP 403; streak 0
- **unreachable** — [https://open.substack.com/pub/theviewfromw5/p/demolition-of-ealing-homes-part-of-trail-chaos](https://open.substack.com/pub/theviewfromw5/p/demolition-of-ealing-homes-part-of-trail-chaos) — HTTP 403; streak 0
- **unreachable** — [https://open.substack.com/pub/theviewfromw5/p/ealing-council-hopes-to-recoup-money-from-collapse-of-henry-construction](https://open.substack.com/pub/theviewfromw5/p/ealing-council-hopes-to-recoup-money-from-collapse-of-henry-construction) — HTTP 403; streak 0
- **unreachable** — [https://open.substack.com/pub/theviewfromw5/p/ealing-delivers-16-percent-of-its-affordable-homes-target](https://open.substack.com/pub/theviewfromw5/p/ealing-delivers-16-percent-of-its-affordable-homes-target) — HTTP 403; streak 0
- **unreachable** — [https://open.substack.com/pub/theviewfromw5/p/history-of-insolvency-and-10-million-dividend](https://open.substack.com/pub/theviewfromw5/p/history-of-insolvency-and-10-million-dividend) — HTTP 403; streak 0
- **unreachable** — [https://www.police.uk/pu/your-area/metropolitan-police-service/hanwell-broadway/](https://www.police.uk/pu/your-area/metropolitan-police-service/hanwell-broadway/) — HTTP 403; streak 0
- **unreachable** — [https://www.police.uk/pu/your-area/metropolitan-police-service/southall-broadway/](https://www.police.uk/pu/your-area/metropolitan-police-service/southall-broadway/) — HTTP 403; streak 0
- **unreachable** — [https://www.police.uk/pu/your-area/metropolitan-police-service/southall-green/](https://www.police.uk/pu/your-area/metropolitan-police-service/southall-green/) — HTTP 403; streak 0
- **unreachable** — [https://www.police.uk/pu/your-area/metropolitan-police-service/walpole/](https://www.police.uk/pu/your-area/metropolitan-police-service/walpole/) — HTTP 403; streak 0
- **unreachable** — [https://www.reddit.com/r/Ealing/s/JD2n25UHIk](https://www.reddit.com/r/Ealing/s/JD2n25UHIk) — HTTP 403; streak 0
- **unreachable** — [https://register.charitycommission.gov.uk/en/charity-details/?regId=1104671](https://register.charitycommission.gov.uk/en/charity-details/?regId=1104671) — no HTTP response; streak 0
- **unreachable** — [https://www.researchgate.net/publication/308019398_The_first_one_wins_Distilling_the_primacy_effect](https://www.researchgate.net/publication/308019398_The_first_one_wins_Distilling_the_primacy_effect) — HTTP 403; streak 0
- **unreachable** — [https://www.royalalberthall.com/tickets/events/2025/ealing-together-harmony-in-diversity](https://www.royalalberthall.com/tickets/events/2025/ealing-together-harmony-in-diversity) — HTTP 403; streak 0
- **unreachable** — [https://southall.davidmarsden.info/2025/07/11/perceval-house-w-where-local/](https://southall.davidmarsden.info/2025/07/11/perceval-house-w-where-local/) — no HTTP response; streak 0
- **unreachable** — [https://southall.davidmarsden.info/2025/07/12/so-it-goes-ai-on/](https://southall.davidmarsden.info/2025/07/12/so-it-goes-ai-on/) — no HTTP response; streak 0
- **unreachable** — [https://t2m.io/z6shGyFn](https://t2m.io/z6shGyFn) — no HTTP response; streak 0
- **unreachable** — [https://theviewfromw5.substack.com/p/ealing-delivers-16-percent-of-its-affordable-homes-target](https://theviewfromw5.substack.com/p/ealing-delivers-16-percent-of-its-affordable-homes-target) — HTTP 403; streak 0
- **unreachable** — [https://theviewfromw5.substack.com/p/ealing-major-increase-homelessness](https://theviewfromw5.substack.com/p/ealing-major-increase-homelessness) — HTTP 403; streak 0
- **unreachable** — [https://www.timeanddate.com/weather/@2637490/historic?month=7&year=2018](https://www.timeanddate.com/weather/@2637490/historic?month=7&year=2018) — HTTP 403; streak 0
- **unreachable** — [https://www.unwomen.org/en/news-stories/news/2025/05/un-women-estimates-over-28000-women-and-girls-killed-in-gaza-since-october-2023](https://www.unwomen.org/en/news-stories/news/2025/05/un-women-estimates-over-28000-women-and-girls-killed-in-gaza-since-october-2023) — HTTP 403; streak 0
- **unreachable** — [https://web.archive.org/web/20040615012717/http://www.southallgasworks.com/Media/ConsultationReport.pdf](https://web.archive.org/web/20040615012717/http://www.southallgasworks.com/Media/ConsultationReport.pdf) — no HTTP response; streak 0
- **unreachable** — [https://www.whatdotheyknow.com/request/845384/response/2020637/attach/html/5/FOI%20Response%2022%200363%20FINAL.pdf.html](https://www.whatdotheyknow.com/request/845384/response/2020637/attach/html/5/FOI%20Response%2022%200363%20FINAL.pdf.html) — HTTP 403; streak 0
- **unreachable** — [https://www.whatdotheyknow.com/request/how_many_homes_have_been_complet/response/2002978/attach/5/FOI%20Internal%20Review%2022%200065%20FINAL.pdf](https://www.whatdotheyknow.com/request/how_many_homes_have_been_complet/response/2002978/attach/5/FOI%20Internal%20Review%2022%200065%20FINAL.pdf) — HTTP 403; streak 0
- **unreachable** — [https://www.whatdotheyknow.com/request/how_much_section_106_money_has_e/response/2061857/attach/5/EIR%20Internal%20Review%2022%200404%20FINAL.pdf?cookie_passthrough=1](https://www.whatdotheyknow.com/request/how_much_section_106_money_has_e/response/2061857/attach/5/EIR%20Internal%20Review%2022%200404%20FINAL.pdf?cookie_passthrough=1) — HTTP 403; streak 0

## Ordinary redirects

- [Ealing Council Leader Narrowly Survives No Confidence Vote](http://neighbournet.com/server/common/ldrseacouncil014.htm?site=2) → https://neighbournet.com/server/common/ldrseacouncil014.htm?site=2
- [Benzene and you. Working with benzene - are you at risk? INDG329](http://www.hse.gov.uk/pubns/indg329.pdf) → https://www.hse.gov.uk/pubns/indg329.pdf
- [Sign the Petition](https://chn.ge/2NarH6k) → https://www.change.org/p/cleanair-for-southall-and-hayes-stop-berkeleygroupuk-s-southallwaterside-polluting-our-kids-southalllivesmatter?recruiter=22186757&utm_source=share_petition&utm_medium=twitter&utm_campaign=share_twitter_responsive
- [Ealing Council leader Peter Mason gets massive allowance rise by over 70% along with more increases for his cabinet and other councillors - EALING.NEWS - The Voice of Ealing's 7 towns - Acton, Ealing, Greenford, Hanwell, Northolt, Perivale, Southall.](https://ealing.news/ealing-council/ealing-council-leader-peter-mason-massive-allowance-rise-by-over-70-along-with-increases-for-his-cabinet/) → https://www.ealing.news/ealing-council/ealing-council-leader-peter-mason-massive-allowance-rise-by-over-70-along-with-increases-for-his-cabinet/
- [Ealing Council leader Peter Mason gets massive allowance rise by over 70% along with more increases for his cabinet and other councillors - EALING.NEWS - The Voice of Ealing's 7 towns - Acton, Ealing, Greenford, Hanwell, Northolt, Perivale, Southall.](https://ealing.news/news/ealing-council-leader-peter-mason-massive-allowance-rise-by-over-70/) → https://www.ealing.news/ealing-council/ealing-council-leader-peter-mason-massive-allowance-rise-by-over-70-along-with-increases-for-his-cabinet/
- [Ealing Labour finally tax developers after 15 years delay!](https://ealinglibdems.org.uk/news/article/ealing-labour-finally-tax-developers-after-15-years-delay) → https://www.ealinglibdems.org.uk/news/article/ealing-labour-finally-tax-developers-after-15-years-delay
- [New video · Thursday, Jan 20, 2022 🎬](https://photos.app.goo.gl/4dN7oLJizqrSCZeG6) → https://photos.google.com/share/AF1QipM3kaDZrYldmtoRrQPqFOBcPMMr1ZQ2FFN2bxqZ6h-PtSy-U0kS_0TYAbbqp71HDQ?key=NGhnV0lINVgwQW9uWjlZYWd6eFVWUG1iYzQ1NXR3
- [Ealing Council to switch to co-mingled collections](https://resource.co/article/ealing-council-switch-co-mingled-collections-10222) → https://resourcemedia.eco/article/ealing-council-switch-co-mingled-collections-10222
- [Southall Reset Programme at the SCA Community Forum - Southall News](https://visitsouthall.co.uk/News/NewsDetails.php?recordID=1247) → https://www.visitsouthall.co.uk/News/NewsDetails.php?recordID=1247
- [TikTok - Make Your Day](https://vm.tiktok.com/ZNRfJ3fLA/) → https://www.tiktok.com/?_r=1
- [Share on WhatsApp](https://wa.me/qr/4MUTFBX64DCIB1) → https://api.whatsapp.com/qr/4MUTFBX64DCIB1?autoload=1&app_absent=0
- [A Baron’s Vision](https://wp.me/pfDRL-2l) → https://thesocialenterprise.wordpress.com/2012/10/04/baron-glasman/
- [Celebrating living wage employers - Around Ealing](https://www.aroundealing.com/fighting-inequality/london-living-wage-celebration-event/) → https://www.aroundealing.com/children/london-living-wage-celebration-event/
- [Labour council leader admits plan to 'take advantage' of Covid](https://www.dailymail.co.uk/news/article-8780309/Labour-council-leader-admits-plan-advantage-Covid.html) → https://www.dailymail.com/news/article-8780309/Labour-council-leader-admits-plan-advantage-Covid.html
- [Introduction | Council elections results 7 May 2026 | Ealing Council](https://www.ealing.gov.uk/info/201065/elections/3595/council_elections_results_7_may_2026) → https://www.ealing.gov.uk/info/201276/council_elections/3595/council_elections_results_7_may_2026
- [Introduction | Council elections results 7 May 2026 | Ealing Council](https://www.ealing.gov.uk/info/201065/elections/3595/council_elections_results_7_may_2026/11) → https://www.ealing.gov.uk/info/201276/council_elections/3595/council_elections_results_7_may_2026
- [Introduction | Council elections results 7 May 2026 | Ealing Council](https://www.ealing.gov.uk/info/201065/elections/3595/council_elections_results_7_may_2026/13) → https://www.ealing.gov.uk/info/201276/council_elections/3595/council_elections_results_7_may_2026
- [Introduction | Council elections results 7 May 2026 | Ealing Council](https://www.ealing.gov.uk/info/201065/elections/3595/council_elections_results_7_may_2026/20) → https://www.ealing.gov.uk/info/201276/council_elections/3595/council_elections_results_7_may_2026
- [Introduction | Council elections results 7 May 2026 | Ealing Council](https://www.ealing.gov.uk/info/201065/elections/3595/council_elections_results_7_may_2026/21) → https://www.ealing.gov.uk/info/201276/council_elections/3595/council_elections_results_7_may_2026
- [Introduction | Council elections results 7 May 2026 | Ealing Council](https://www.ealing.gov.uk/info/201065/elections/3595/council_elections_results_7_may_2026/22) → https://www.ealing.gov.uk/info/201276/council_elections/3595/council_elections_results_7_may_2026
- [Introduction | Council elections results 7 May 2026 | Ealing Council](https://www.ealing.gov.uk/info/201065/elections/3595/council_elections_results_7_may_2026/9) → https://www.ealing.gov.uk/info/201276/council_elections/3595/council_elections_results_7_may_2026
- [BIGHOKI !! Akses Alternatif Terbaru Game Online Buat Mata Melolok Liat Jepe!](https://www.ealinglabour.com/manifesto2022/) → https://www.bighokiajaib.com/
- [Petition for better odour control at asphalt plant gains momentum](https://www.getwestlondon.co.uk/news/west-london-news/ealing-hillingdon-southall-fm-conway-14255951) → https://www.mylondon.news/news/west-london-news/ealing-hillingdon-southall-fm-conway-14255951
- [A shameful day for the JLM - Jewish Voice for Liberation](https://www.jewishvoiceforlabour.org.uk/statement/a-shameful-day-for-the-jlm/) → https://jewishvoiceforliberation.org.uk/statement/a-shameful-day-for-the-jlm/
- [Fly tipping more than trebles after Ealing bin collection change](https://www.mylondon.news/news/west-london-news/y-tipping-ealing-risen-216-11921289) → https://www.mylondon.news/news/west-london-news/fly-tipping-ealing-risen-216-11921289
- [Poisoning](https://www.nhs.uk/conditions/poisoning/symptoms/) → https://www.nhs.uk/conditions/poisoning/
- [Save Southall Town Hall campaign - victory! | PILC](https://www.pilc.org.uk/news/save-southall-town-hall-campaign-victory/) → https://www.pilc.org.uk/post/save-southall-town-hall-campaign-victory
