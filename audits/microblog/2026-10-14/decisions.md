# Micro.blog audit — 14 October 2026

Source: user-provided Micro.blog audit for southallstories.uk. This is a **curated initial baseline**, not a complete machine export of every finding. HTTP outcomes are those reported by Micro.blog, not independently rechecked.

1. `/cllr-dhindsas-achievements-since-1998`: deliberately humorous 404. Preserve, do not redirect.
2. `/2026/01/22/its-never-enough-until-its/`: likely predecessor of `/2026/01/22/how-to-report-nuisance-and/`. Compare archived original and live replacement before a 301.
3. Micro.blog saved HTML for the 2019 Ealing health profile and Ealing Air reports: preserve both original URLs and snapshots; inspect saved page canonical/source metadata before repair.
4. `/feed.json`: audit says HTTP 404 while homepage advertises both feeds; `/feed.xml` valid. Verify output and fix in theme if reproducible.
5. Relative-looking external links (bard.google.com, gemini.google.com, council PDF in Feeling the Heat) appear malformed. Check source markup and fix the link target, not via redirects.
6. Moderngov, WhatDoTheyKnow and other 403 results may be bot blocking. Verify manually before declaring lost.
7. `/credentials`, `/private-key`, `/www.git/HEAD`, `/_ignition/execute-solution` and similar paths are likely scanning traffic. No redirects.

Next: import the full audit into a reproducible structured dataset, de-duplicate URLs and attach article references; verify candidates before publishing changes.
