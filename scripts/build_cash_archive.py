#!/usr/bin/env python3
"""Build the static preserved copy of the Clean Air for Southall and Hayes website.

Source:  archives/cash/content/**/*.md  (Markdown with YAML front matter)
Output:  archives/cash/site/            (self-contained static HTML)
         archives/cash/manifest.json    (provenance manifest)

Content shortcuts understood in the Markdown:
  ![alt](wayback:2020/01/file.jpg)        image from the archived wp-content/uploads
  [text](wayback-file:2020/01/x.pdf|TS)   link to an archived upload at Wayback timestamp TS
"""

from __future__ import annotations

import html
import json
import re
import shutil
from pathlib import Path

import markdown
import yaml

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "archives" / "cash"
CONTENT = ROOT / "content"
SITE = ROOT / "site"
ASSETS = ROOT / "assets"

ORIGIN = "https://southallandhayescleanair.org.uk"
UPLOADS = f"{ORIGIN}/wp-content/uploads/"
SITE_TITLE = "Clean Air for Southall and Hayes"
TAGLINE = "Campaign for justice for the Gasworks residents."


IMAGES = ROOT / "images"


def wayback_image(path: str, slug: str = "index") -> str:
    """Prefer the locally preserved copy; fall back to the Wayback Machine."""
    name = path.rsplit("/", 1)[-1]
    if (IMAGES / name).exists():
        return rel(slug, f"images/{name}")
    # im_ returns the raw archived image without the Wayback toolbar.
    return f"https://web.archive.org/web/2021im_/{UPLOADS}{path}"


def wayback_file(spec: str) -> str:
    path, _, ts = spec.partition("|")
    return f"https://web.archive.org/web/{ts or '2021'}/{UPLOADS}{path}"


def load(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise SystemExit(f"{path}: missing front matter")
    meta = yaml.safe_load(m.group(1))
    meta["body_md"] = m.group(2)
    meta["source"] = str(path.relative_to(REPO))
    return meta


def youtube_block(m: re.Match) -> str:
    vid, title, channel, *note = [x.strip() for x in m.group(1).split("|")]
    watch = f"https://www.youtube.com/watch?v={vid}"
    caption = f"{html.escape(title)} <span>· {html.escape(channel)} on YouTube</span>"
    if note:
        caption += f' <span class="vnote">{html.escape(note[0])}</span>'
    return (
        f'<figure class="video" data-yt="{vid}">'
        f'<a class="video-frame" href="{watch}" rel="noopener external" aria-label="Play video: {html.escape(title)}">'
        f'<img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" loading="lazy" decoding="async">'
        f'<span class="play" aria-hidden="true"></span></a>'
        f"<figcaption>{caption}</figcaption></figure>"
    )


VIDEO_JS = """<script>
document.addEventListener('click', function (e) {
  var a = e.target.closest('.video-frame'); if (!a) return;
  var fig = a.closest('.video'); var id = fig && fig.dataset.yt; if (!id) return;
  e.preventDefault();
  var f = document.createElement('iframe');
  f.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0';
  f.title = a.getAttribute('aria-label').replace('Play video: ', '');
  f.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
  f.allowFullscreen = true; f.className = 'video-frame';
  a.replaceWith(f); f.focus();
});
</script>"""


TYPE_GROUPS = [
    ("CASH’s own words", {"cash-authored", "petition"}),
    ("Official records", {"council-record", "gla-record", "parliament"}),
    ("Reports", {"report"}),
    ("Video", {"video"}),
    ("Press coverage", {"news"}),
    ("Social media and other", {"social", "other"}),
]


def catalogue_html(slug: str) -> str:
    """Render archives/cash/elsewhere.json as grouped, annotated lists."""
    items = json.loads((ROOT / "elsewhere.json").read_text(encoding="utf-8"))
    out = []
    for heading, types in TYPE_GROUPS:
        group = sorted((i for i in items if i["type"] in types), key=lambda i: i.get("date") or "0000")
        if not group:
            continue
        out.append(f'<h2>{html.escape(heading)} <span class="count">{len(group)}</span></h2><ul class="catalogue">')
        for i in group:
            date = fmt_date(i["date"]) if i.get("date") else "Undated"
            links = []
            if i.get("page"):
                links.append(f'<a class="chip chip-primary" href="{rel(slug, i["page"])}">Read preserved text</a>')
            if i.get("live_status") != "dead":
                links.append(f'<a class="chip" href="{html.escape(i["url"])}" rel="noopener external">Original</a>')
            if i.get("wayback_url"):
                links.append(f'<a class="chip" href="{html.escape(i["wayback_url"])}" rel="noopener external">Wayback</a>')
            quote = f'<blockquote>{html.escape(i["quote"])}</blockquote>' if i.get("quote") else ""
            out.append(
                f'<li><p class="meta">{html.escape(i["publisher"])} · <time>{html.escape(date)}</time></p>'
                f'<h3>{html.escape(i["title"])}</h3><p>{html.escape(i["summary"])}</p>{quote}'
                f'<p class="chips">{"".join(links)}</p></li>'
            )
        out.append("</ul>")
    return "\n".join(out)


def render_md(src: str, slug: str) -> str:
    src = re.sub(r"^\{\{youtube (.+?)\}\}$", youtube_block, src, flags=re.M)
    src = src.replace("{{catalogue}}", catalogue_html(slug))
    src = re.sub(r"\]\(wayback:([^)\s]+)\)", lambda m: f"]({wayback_image(m.group(1), slug)})", src)
    src = re.sub(r"\]\(wayback-file:([^)\s]+)\)", lambda m: f"]({wayback_file(m.group(1))})", src)
    # Let Markdown inside every raw HTML block container be parsed.
    src = re.sub(r"^<(div|figure|article|ul|li)\b(?![^>]*markdown=)", r'<\1 markdown="1"', src, flags=re.M)
    out = markdown.markdown(
        src,
        extensions=["extra", "attr_list", "md_in_html", "sane_lists", "smarty"],
        output_format="html",
    )
    out = out.replace("<img ", '<img loading="lazy" decoding="async" ')
    out = out.replace("<table>", '<table class="data">')
    # External links open normally but are marked for styling / rel hygiene.
    out = re.sub(
        r'<a href="(https?://[^"]+)"',
        lambda m: f'<a href="{m.group(1)}" rel="noopener external"',
        out,
    )
    return out


def fmt_date(iso: str) -> str:
    import datetime as dt

    d = dt.date.fromisoformat(str(iso))
    return d.strftime("%-d %B %Y")


def rel(from_slug: str, to: str) -> str:
    depth = from_slug.count("/")
    return "../" * depth + to


def nav_html(pages: list[dict], current: dict) -> str:
    items = []
    for p in pages:
        if not p.get("nav"):
            continue
        href = rel(current["slug"], f"{p['slug']}.html")
        cur = ' aria-current="page"' if p["slug"] == current["slug"] else ""
        cls = ' class="nav-meta"' if p["slug"] == "about-this-archive" else ""
        items.append(f'<li{cls}><a href="{href}"{cur}>{html.escape(p["nav"])}</a></li>')
    return "\n".join(items)


def provenance_html(p: dict) -> str:
    if p.get("source_url"):  # material gathered from elsewhere on the web
        rows = [
            ("Published by", html.escape(p.get("publisher", ""))),
            ("Source", f'<a class="mono" href="{html.escape(p["source_url"])}" rel="noopener external">{html.escape(p["source_url"])}</a>'),
            ("Retrieved", html.escape(fmt_date(p["retrieved"]))),
        ]
        if p.get("date"):
            rows.insert(1, ("Dated", html.escape(fmt_date(p["date"]))))
        if p.get("wayback_url"):
            rows.append(("Archived copy", f'<a href="{html.escape(p["wayback_url"])}" rel="noopener external">View on the Wayback Machine</a>'))
        dl = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in rows)
        return f'<aside class="provenance" aria-label="Source of this page"><dl>{dl}</dl></aside>'
    if not p.get("original_url"):
        return ""
    rows = [
        ("Originally at", f'<span class="mono">{html.escape(p["original_url"])}</span>'),
        ("Captured", html.escape(fmt_date(p["captured"]))),
        ("Archived copy", f'<a href="{html.escape(p["wayback_url"])}" rel="noopener external">View on the Wayback Machine</a>'),
    ]
    if p.get("document_type"):
        rows.insert(0, ("Document", html.escape(p["document_type"])))
    if p.get("licence"):
        rows.append(("Licence", html.escape(p["licence"])))
    dl = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in rows)
    return f'<aside class="provenance" aria-label="Source of this page"><dl>{dl}</dl></aside>'


HERO = """
<section class="hero" aria-labelledby="hero-title">
  <div class="hero-inner">
    <p class="eyebrow">Southall · Hayes · West London · 2018–2022</p>
    <h1 id="hero-title">Clean Air for<br>Southall and Hayes</h1>
    <p class="lede">{tagline} A community campaign over toxic odours and health fears linked to the
      redevelopment of the former Southall Gasworks.</p>
    <ol class="demands-strip" aria-label="CASH's demands">
      <li><span>01</span>Stop the works at Southall Waterside</li>
      <li><span>02</span>Set up independent monitoring of air quality and soil</li>
      <li><span>03</span>Investigate health impact on the community</li>
    </ol>
    <p class="hero-actions">
      <a class="btn btn-primary" href="about.html">Who are CASH?</a>
      <a class="btn" href="case-studies.html">Residents’ stories</a>
      <a class="btn" href="resources.html">Documents</a>
    </p>
  </div>
</section>
"""


def page_html(p: dict, pages: list[dict]) -> str:
    css = rel(p["slug"], "assets/style.css")
    home = rel(p["slug"], "index.html")
    about_archive = rel(p["slug"], "about-this-archive.html")
    is_home = p["slug"] == "index"
    title = SITE_TITLE if is_home else f"{p['title']} · {SITE_TITLE} (archive)"
    header_block = (
        HERO.format(tagline=html.escape(TAGLINE))
        if is_home
        else f'<header class="page-head"><p class="eyebrow">{html.escape(p.get("document_type") or "CASH website · archived page")}</p>'
        f'<h1>{html.escape(p["title"])}</h1>'
        + (f'<p class="lede">{html.escape(p["summary"])}</p>' if p.get("summary") else "")
        + "</header>"
    )
    section_title = '<h2 class="section-title">News</h2>' if is_home else ""
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(p.get('summary', ''))}">
<meta name="robots" content="index,follow">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(p.get('summary', ''))}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#0e4a40">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%230e4a40'/%3E%3Cpath d='M7 19c4-6 8 2 12-4s5-3 6-3' stroke='%23e9f3ea' stroke-width='2.6' fill='none' stroke-linecap='round'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{css}">
</head>
<body class="{'home' if is_home else 'inner'}">
<a class="skip" href="#main">Skip to content</a>
<div class="archive-bar" role="note">
  <div class="wrap">
    <strong>Preserved archive.</strong> CASH’s original domain was lost and now hosts spam. This is an unofficial copy rebuilt from the Internet Archive and is not run by CASH.
    <a href="{about_archive}">About this archive</a>
  </div>
</div>
<header class="site-head">
  <div class="wrap head-inner">
    <a class="brand" href="{home}" aria-label="{SITE_TITLE}: archive home">
      <svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="7"/><path d="M7 19c4-6 8 2 12-4s5-3 6-3"/></svg>
      <span><b>CASH</b><small>Clean Air for Southall and Hayes</small></span>
    </a>
    <nav aria-label="Main">
      <ul>{nav_html(pages, p)}</ul>
    </nav>
  </div>
</header>
<main id="main">
{header_block}
<div class="wrap content-grid">
  <article class="prose">
    {section_title}
    {p['body_html']}
  </article>
  {provenance_html(p)}
</div>
</main>
<footer class="site-foot">
  <div class="wrap">
    <p><b>Clean Air for Southall and Hayes (CASH)</b>: preserved copy of the campaign website, 2020–2022.
      Original content © CASH and contributors. Public Health England material is Crown copyright under the Open Government Licence.</p>
    <p>Preserved for public-interest research by <a href="https://southallstories.uk">Southall Stories</a>.
      Not affiliated with CASH. <a href="{about_archive}">Provenance, corrections and takedown</a>.</p>
  </div>
</footer>
{VIDEO_JS if 'class="video"' in p['body_html'] else ''}
</body>
</html>
"""


NETLIFY_TOML = """# Generated by scripts/build_cash_archive.py
[build]
  publish = "."
  command = "echo 'static site, no build'"

[[headers]]
  for = "/*"
  [headers.values]
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    X-Frame-Options = "SAMEORIGIN"

[[headers]]
  for = "/images/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 404
"""


def main() -> None:
    pages = [load(p) for p in sorted(CONTENT.rglob("*.md"))]
    pages.sort(key=lambda p: p.get("order", 99))
    if SITE.exists():
        shutil.rmtree(SITE)
    (SITE / "assets").mkdir(parents=True)
    shutil.copy(ASSETS / "style.css", SITE / "assets" / "style.css")
    shutil.copytree(IMAGES, SITE / "images")
    # Netlify config: plain static publish of this folder, no build step.
    (SITE / "netlify.toml").write_text(NETLIFY_TOML, encoding="utf-8")

    for p in pages:
        p["body_html"] = render_md(p["body_md"], p["slug"])
        out = SITE / f"{p['slug']}.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page_html(p, pages), encoding="utf-8")

    manifest = {
        "title": f"{SITE_TITLE}: preserved website",
        "original_domain": ORIGIN,
        "status_of_original_domain": "Lost by the campaign; now serves unrelated spam. Do not cite.",
        "source": "Internet Archive Wayback Machine",
        "pages": [
            {
                k: p.get(k)
                for k in ("title", "slug", "original_url", "wayback_url", "captured", "document_type", "source")
                if p.get(k)
            }
            for p in pages
        ],
        "videos": [
            dict(zip(("youtube_id", "title", "channel", "context"), [x.strip() for x in v.split("|")]))
            for v in re.findall(r"\{\{youtube (.+?)\}\}", "".join(p["body_md"] for p in pages))
        ],
        "images": sorted(set(re.findall(r"wayback:([^)\s]+)", "".join(p["body_md"] for p in pages)))),
        "omitted": [
            {"url": f"{ORIGIN}/contact/", "reason": "Archived capture could not be retrieved."},
            {"url": f"{ORIGIN}/hello-world/", "reason": "Default WordPress placeholder post."},
        ],
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Built {len(pages)} pages into {SITE.relative_to(REPO)}")


if __name__ == "__main__":
    main()
