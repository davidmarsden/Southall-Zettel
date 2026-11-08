# Clean Air for Southall and Hayes: preserved website

An unofficial, research-grade preserved copy of the website of **Clean Air for Southall and Hayes (CASH)**, formerly at `southallandhayescleanair.org.uk`.

That domain is no longer controlled by the campaign and now serves unrelated spam. **Do not cite it.** Cite this archive or the Wayback Machine snapshots listed in `manifest.json` instead.

This archive is not run by, affiliated with or endorsed by CASH.

## Layout

| Path | What it is |
|---|---|
| `content/` | Page text as Markdown with provenance front matter (`original_url`, `wayback_url`, `captured`). This is the source of truth. |
| `content/documents/` | Full-text transcriptions of the three PDFs CASH hosted. |
| `images/` | Campaign photographs and graphics recovered byte-for-byte from the Wayback Machine. |
| `assets/style.css` | Site design. |
| `site/` | Generated static website. Do not edit by hand. |
| `manifest.json` | Generated provenance manifest. |

## Rebuild

```sh
pip install -r requirements.txt
python3 scripts/build_cash_archive.py
```

Open `archives/cash/site/index.html` or serve the `site/` folder from any static host.

## Provenance and editorial rules

- Source: the Internet Archive Wayback Machine, using the latest capture of each page made before the domain changed hands (August 2020 to May 2022).
- Text is reproduced as published, including original spelling. Only layout, navigation and design are new.
- Notes added by the archive are set apart as `.note` blocks.
- **Not preserved:** the Contact page (the archive would not return it) and the default WordPress "Hello world!" post. Personal phone numbers on the Save Our Southall leaflet are left out of the transcription.
- **PDFs** are linked at their Wayback Machine originals rather than copied here, because the retrieval tool cut off files of that size.
- **One image** (the open-letter screenshot, `2020/09/Screen-Shot-2020-09-25-at-20.09.30-1024x628.png`) also loads from the Wayback Machine for the same reason.

## Beyond the website

`elsewhere.json` lists CASH material and campaign records found elsewhere on the web (gathered 8 November 2026). `content/elsewhere/` holds full texts: CASH-authored material and public-sector records under the Open Government or Open Parliament Licence. Journalism is listed with a summary and links only.

### Still to capture in the Wayback Machine

These sources had no Wayback snapshot when gathered. Submit each at <https://web.archive.org/save> so every preserved text can be checked against an independent copy:

- https://www.change.org/p/cleanair-for-southall-and-hayes-stop-berkeleygroupuk-s-southallwaterside-polluting-our-kids-southalllivesmatter
- https://www.change.org/p/cleanair-for-southall-and-hayes-stop-berkeleygroupuk-s-southallwaterside-polluting-our-kids-southalllivesmatter/u/23075132
- https://www.ealing.gov.uk/download/downloads/id/18503/open_letter_to_cash_from_cllr_peter_mason_leader_of_ealing_council_november_2022.pdf
- https://www.ealing.gov.uk/download/downloads/id/16356/letter_to_cash_from_cllr_peter_mason.pdf
- https://www.ealing.gov.uk/downloads/download/6227/southall_gasworks_correspondence
- https://www.ealing.gov.uk/download/downloads/id/19134/to_cash_24_august_2023_from_cllr_peter_mason.pdf
- https://www.ealing.gov.uk/download/downloads/id/19206/cllr_mason_reply_to_zack_polanski_-_oct_23.pdf
- https://www.ealing.gov.uk/download/downloads/id/16850/legal_advice.pdf
- https://www.ealing.gov.uk/download/downloads/id/16684/counsel_opinion.pdf
- https://ealing.moderngov.co.uk/Data/Southall%20Broadway%20Ward%20Forum/201907291900/Agenda/Southall%20Broadway%20odour%20issue%20July%202019.pdf
- https://hansard.parliament.uk/commons/2021-01-21/debates/0476D713-A47A-4E95-96DD-AC57B4B64B76/AirPollutionBrownfieldRedevelopment
- https://www.london.gov.uk/who-we-are/what-london-assembly-does/questions-mayor/find-an-answer/funding-studies-chemicals-released-redevelopment
- https://committees.parliament.uk/writtenevidence/162732/pdf/
- https://www.thecentriclab.com/research-library/air-pollution-amp-health-in-southall-london
- https://nationalretrofithub.org.uk/case-studies/centric-lab-chia-scenario/
