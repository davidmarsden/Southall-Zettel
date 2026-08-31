#!/usr/bin/env python3
"""Generate newsroom-style pre-publication reviews for Southall-Zettel drafts.

This is deliberately advisory. It flags mechanical problems and research prompts,
but it does not pretend to decide whether a claim is true or whether an article
is ready to publish.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

import yaml

REPO = Path.cwd()
DRAFTS = REPO / "posts" / "drafts"
REPORT_DIR = REPO / "generated" / "draft-review"
JSON_PATH = REPO / "generated" / "draft-review.json"
INDEX_PATH = REPO / "indexes" / "draft-review.md"
CITATION_CACHE = REPO / "generated" / "citation-metadata.json"

FRONT_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
MD_LINK_RE = re.compile(r"\[[^\]]*\]\((https?://[^)\s]+)")
HTML_LINK_RE = re.compile(r"href=[\"'](https?://[^\"']+)", re.I)
PLACEHOLDER_RE = re.compile(r"(?im)(?:\bTODO\b|\bTK\b|\bTBC\b|\bCHECK\b|\bSOURCE\?\b|\[citation needed\]|\[source needed\]|\?\?\?)")
NUMBER_RE = re.compile(r"(?:£\s?\d|\b\d+(?:\.\d+)?%|\b(?:19|20)\d{2}\b|\b\d{1,3}(?:,\d{3})+\b)")
QUOTE_RE = re.compile(r"[\"“”][^\"“”]{12,}[\"“”]")
MD_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
HTML_IMG_RE = re.compile(r"<img\b([^>]*)>", re.I)
ALT_RE = re.compile(r"\balt\s*=\s*[\"'][^\"']+[\"']", re.I)


def parse_md(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    m = FRONT_RE.match(text)
    if not m:
        return {}, text
    return yaml.safe_load(m.group(1)) or {}, text[m.end():]


def urls(body: str) -> list[str]:
    return sorted(set(MD_LINK_RE.findall(body)) | set(HTML_LINK_RE.findall(body)))


def load_cache() -> dict:
    if not CITATION_CACHE.exists():
        return {}
    try:
        return json.loads(CITATION_CACHE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def entity_catalog() -> list[dict]:
    entities = []
    for path in sorted((REPO / "entities").glob("**/*.md")):
        meta, _ = parse_md(path)
        name = str(meta.get("name") or "").strip()
        if not name:
            continue
        aliases = [str(a).strip() for a in (meta.get("aliases") or []) if str(a).strip()]
        entities.append({
            "id": str(meta.get("id") or path.stem),
            "name": name,
            "type": str(meta.get("type") or path.parent.name.rstrip("s")),
            "aliases": aliases,
            "path": str(path.relative_to(REPO)),
        })
    return entities


def mentioned_entities(body: str, entities: list[dict]) -> list[dict]:
    found = []
    lower = body.lower()
    for ent in entities:
        terms = [ent["name"], *ent["aliases"]]
        hits = []
        for term in terms:
            if len(term) < 4:
                continue
            pattern = r"(?<!\w)" + re.escape(term.lower()) + r"(?!\w)"
            count = len(re.findall(pattern, lower))
            if count:
                hits.append((term, count))
        if hits:
            found.append({**ent, "mentions": sum(c for _, c in hits), "matched_as": [t for t, _ in hits]})
    return sorted(found, key=lambda x: (-x["mentions"], x["name"].lower()))


def published_posts_with_entities(entities: list[dict], draft_path: Path) -> list[dict]:
    scores = []
    entity_ids = {e["id"] for e in entities}
    if not entity_ids:
        return []
    catalog = entity_catalog()
    for path in REPO.glob("posts/**/*.md"):
        if "drafts" in path.parts or path == draft_path:
            continue
        meta, body = parse_md(path)
        hits = mentioned_entities(body, catalog)
        shared = [e for e in hits if e["id"] in entity_ids]
        if not shared:
            continue
        score = len(shared)
        title = str(meta.get("title") or path.stem)
        url = str(meta.get("url") or "")
        if url.startswith("/"):
            url = "https://southallstories.uk" + url
        scores.append({"title": title, "url": url, "path": str(path.relative_to(REPO)), "score": score, "entities": [e["name"] for e in shared]})
    return sorted(scores, key=lambda x: (-x["score"], x["title"].lower()))[:8]


def uncited_evidence_lines(body: str) -> list[dict]:
    lines = body.splitlines()
    issues = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "<img", "![", "<!--")):
            continue
        evidence = []
        if NUMBER_RE.search(stripped):
            evidence.append("number/date")
        if QUOTE_RE.search(stripped) or stripped.startswith(">"):
            evidence.append("quotation")
        if not evidence:
            continue
        neighbourhood = " ".join(lines[max(0, i-1): min(len(lines), i+2)])
        has_link = bool(MD_LINK_RE.search(neighbourhood) or HTML_LINK_RE.search(neighbourhood))
        if not has_link:
            excerpt = re.sub(r"\s+", " ", stripped)
            issues.append({"line": i + 1, "kind": ", ".join(evidence), "text": excerpt[:240]})
    return issues[:30]


def image_alt_issues(body: str) -> list[str]:
    problems = []
    for alt, src in MD_IMAGE_RE.findall(body):
        if not alt.strip():
            problems.append(src)
    for attrs in HTML_IMG_RE.findall(body):
        if not ALT_RE.search(attrs):
            src = re.search(r"\bsrc\s*=\s*[\"']([^\"']+)", attrs, re.I)
            problems.append(src.group(1) if src else "HTML <img>")
    return problems


def review(path: Path, cache: dict, entities: list[dict]) -> dict:
    meta, body = parse_md(path)
    link_items = []
    for url in urls(body):
        item = cache.get(url) or {}
        health = item.get("health") or "unchecked"
        actionable = bool(item.get("actionable", health in {"gone", "suspicious-redirect"}))
        link_items.append({
            "url": url,
            "health": health,
            "actionable": actionable,
            "status": item.get("status"),
            "http_status": item.get("http_status"),
            "title": item.get("destination_title"),
        })

    placeholders = [{"text": m.group(0), "offset": m.start()} for m in PLACEHOLDER_RE.finditer(body)]
    mentioned = mentioned_entities(body, entities)
    uncited = uncited_evidence_lines(body)
    alt = image_alt_issues(body)
    related = published_posts_with_entities(mentioned, path)

    broken = [x for x in link_items if x["actionable"]]
    inconclusive = [x for x in link_items if x["health"] in {"blocked", "unreachable", "unchecked"} and not x["actionable"]]
    warnings = len(placeholders) + len(uncited) + len(alt) + len(inconclusive)
    blockers = len(broken) + len(placeholders)

    return {
        "path": str(path.relative_to(REPO)),
        "title": str(meta.get("title") or path.stem),
        "review_complete": bool(meta.get("review_complete", False)),
        "publish_new_to_microblog": bool(meta.get("publish_new_to_microblog", False)),
        "links": link_items,
        "broken_links": broken,
        "inconclusive_links": inconclusive,
        "placeholders": placeholders,
        "uncited_evidence": uncited,
        "missing_alt": alt,
        "entities": mentioned,
        "related_posts": related,
        "blockers": blockers,
        "warnings": warnings,
        "ready": blockers == 0,
    }


def md_report(item: dict) -> str:
    state = "PASS" if item["ready"] else "NEEDS ATTENTION"
    lines = [f"# Draft review: {item['title']}", "", f"**Publication readiness:** {state}", "", f"- Draft: `{item['path']}`", f"- Broken/actionable links: **{len(item['broken_links'])}**", f"- Inconclusive/unchecked links: **{len(item['inconclusive_links'])}**", f"- Placeholders: **{len(item['placeholders'])}**", f"- Evidence-heavy lines without a nearby citation: **{len(item['uncited_evidence'])}**", f"- Images missing alt text: **{len(item['missing_alt'])}**", f"- Recognised entities: **{len(item['entities'])}**", f"- Related published stories suggested: **{len(item['related_posts'])}**", ""]

    if item["broken_links"]:
        lines += ["## Links needing attention", ""]
        for x in item["broken_links"]:
            lines.append(f"- `{x['health']}` — {x['url']}")
        lines.append("")
    if item["inconclusive_links"]:
        lines += ["## Inconclusive automated link checks", "", "These are review prompts, not evidence that the link is broken.", ""]
        for x in item["inconclusive_links"]:
            lines.append(f"- `{x['health']}` — {x['url']}")
        lines.append("")
    if item["placeholders"]:
        lines += ["## Placeholders", ""]
        for x in item["placeholders"]:
            lines.append(f"- `{x['text']}`")
        lines.append("")
    if item["uncited_evidence"]:
        lines += ["## Claims worth checking for sourcing", "", "Heuristic only: dates, figures and quotations are flagged when no external citation appears on the same or neighbouring line.", ""]
        for x in item["uncited_evidence"]:
            lines.append(f"- Line {x['line']} ({x['kind']}): {x['text']}")
        lines.append("")
    if item["missing_alt"]:
        lines += ["## Images missing alt text", ""] + [f"- {x}" for x in item["missing_alt"]] + [""]
    if item["entities"]:
        lines += ["## Recognised entities", ""]
        for e in item["entities"]:
            aliases = ", ".join(e["matched_as"])
            lines.append(f"- **{e['name']}** ({e['type']}) — {e['mentions']} mention(s); matched as {aliases}. Entity: `{e['path']}`")
        lines.append("")
    if item["related_posts"]:
        lines += ["## Related Southall Stories coverage", ""]
        for p in item["related_posts"]:
            shared = ", ".join(p["entities"])
            if p["url"]:
                lines.append(f"- [{p['title']}]({p['url']}) — shared entities: {shared}")
            else:
                lines.append(f"- **{p['title']}** — shared entities: {shared}; `{p['path']}`")
        lines.append("")

    lines += ["## Editorial judgement", "", "This report is advisory. A PASS means the mechanical blockers found by this script are clear; it does **not** certify factual accuracy, fairness, legal safety or publication readiness.", ""]
    return "\n".join(lines)


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    cache = load_cache()
    entities = entity_catalog()
    drafts = sorted(DRAFTS.glob("**/*.md")) if DRAFTS.exists() else []
    reviews = [review(path, cache, entities) for path in drafts]

    wanted = set()
    for item in reviews:
        safe = re.sub(r"[^a-z0-9-]+", "-", Path(item["path"]).stem.lower()).strip("-") or "draft"
        report_path = REPORT_DIR / f"{safe}.md"
        report_path.write_text(md_report(item), encoding="utf-8")
        item["report"] = str(report_path.relative_to(REPO))
        wanted.add(report_path)
    for old in REPORT_DIR.glob("*.md"):
        if old not in wanted:
            old.unlink()

    JSON_PATH.write_text(json.dumps({"drafts": reviews}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = ["# Draft publication review", "", "Automated newsroom checks for Markdown drafts in `posts/drafts/**`. These are prompts for editorial review, not a truth score.", ""]
    if not reviews:
        lines.append("No drafts found.")
    for item in reviews:
        mark = "✅" if item["ready"] else "⚠️"
        lines.append(f"- {mark} **{item['title']}** — {item['blockers']} blocker(s), {item['warnings']} warning(s) — [{Path(item['report']).name}](../{item['report']})")
    lines.append("")
    INDEX_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Reviewed {len(reviews)} draft(s): {sum(r['ready'] for r in reviews)} mechanical pass, {sum(not r['ready'] for r in reviews)} need attention")


if __name__ == "__main__":
    main()
