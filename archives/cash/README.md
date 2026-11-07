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
