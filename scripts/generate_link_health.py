#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlparse

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^\s)]+)\)")
HTML_LINK_RE = re.compile(r'<a\s+[^>]*href=["\'](https?://[^"\']+)["\'][^>]*>(.*?)</a>', re.IGNORECASE | re.DOTALL)
CACHE_PATH = Path("generated/citation-metadata.json")
REPORT_PATH = Path("generated/link-health.json")
INDEX_PATH = Path("indexes/link-health.md")
ALERT_PATH = Path("generated/link-health-alert.md")
BASE_URL = "https://southallstories.uk"
PROBLEM_STATES = {"gone", "unreachable", "suspicious-redirect"}
STOPWORDS = {
    "www", "http", "https", "html", "htm", "pdf", "download", "downloads", "info",
    "page", "pages", "document", "documents", "default", "index", "public", "report",
    "ealing", "council", "southall", "london", "news", "uk", "org", "com", "co",
}


def words(value: str) -> set[str]:
    return {
        token for token in re.findall(r"[a-z0-9]+", unquote(value or "").lower())
        if len(token) >= 4 and token not in STOPWORDS and not token.isdigit()
    }


def suspicious_redirect(original_url: str, resolved_url: str | None, title: str | None) -> bool:
    if not resolved_url or not title or resolved_url.rstrip("/") == original_url.rstrip("/"):
        return False
    try:
        original = urlparse(original_url)
        resolved = urlparse(resolved_url)
    except Exception:
        return False
    if original.hostname != resolved.hostname:
        return False
    # A simple http→https upgrade (or equivalent scheme-only canonicalisation) is benign.
    if original.path.rstrip("/") == resolved.path.rstrip("/") and original.query == resolved.query:
        return False
    original_terms = words(original.path)
    if len(original_terms) < 2:
        return False
    return not bool(original_terms & words(title))


def absolute_post_url(value: str) -> str:
    if not value:
        return ""
    if value.startswith("http://") or value.startswith("https://"):
        return value
    return BASE_URL + (value if value.startswith("/") else "/" + value)


def source_posts(repo: Path) -> tuple[dict[str, list[dict]], dict[str, dict]]:
    posts = json.loads((repo / "generated/posts.json").read_text(encoding="utf-8"))
    post_by_path = {post["path"]: post for post in posts}
    refs: dict[str, list[dict]] = defaultdict(list)
    for path in sorted(repo.glob("posts/**/*.md")):
        rel = path.relative_to(repo).as_posix()
        post = post_by_path.get(rel, {})
        text = path.read_text(encoding="utf-8")
        match = FRONT_MATTER_RE.match(text)
        body = text[match.end():] if match else text
        found = [(label, url) for label, url in MARKDOWN_LINK_RE.findall(body)]
        found.extend((label, url) for url, label in HTML_LINK_RE.findall(body))
        seen: set[str] = set()
        for label, url in found:
            url = url.rstrip(".,;:")
            if url in seen:
                continue
            seen.add(url)
            refs[url].append({
                "path": rel,
                "title": post.get("title") or rel,
                "url": absolute_post_url(post.get("url") or ""),
                "article_label": re.sub(r"<[^>]+>", "", label).strip(),
            })
    return refs, post_by_path


def recommendation(health: str) -> str:
    if health == "gone":
        return "Use Micro.blog’s archived version or replace the source URL."
    if health == "suspicious-redirect":
        return "Check the Micro.blog archived version; the live URL now appears to point at unrelated content."
    if health == "unreachable":
        return "Retry before editing; the site may be blocking automated checks or temporarily unavailable."
    if health == "redirected":
        return "No urgent action unless the redirect becomes unstable; consider updating to the canonical destination."
    return "No action needed."


def md_link(label: str, url: str) -> str:
    if not url:
        return label
    safe_label = label.replace("[", "\\[").replace("]", "\\]")
    return f"[{safe_label}]({url})"


def main() -> None:
    repo = Path.cwd()
    cache = json.loads(CACHE_PATH.read_text(encoding="utf-8")) if CACHE_PATH.exists() else {}
    old_report = json.loads(REPORT_PATH.read_text(encoding="utf-8")) if REPORT_PATH.exists() else {"links": []}
    old_health = {item["url"]: item.get("health") for item in old_report.get("links", [])}
    refs, _ = source_posts(repo)

    entries = []
    for url, metadata in sorted(cache.items()):
        health = metadata.get("health") or "unknown"
        if suspicious_redirect(url, metadata.get("resolved_url"), metadata.get("destination_title")):
            health = "suspicious-redirect"
        affected = refs.get(url, [])
        entry = {
            "url": url,
            "domain": (urlparse(url).hostname or "").lower().removeprefix("www."),
            "health": health,
            "http_status": metadata.get("http_status"),
            "resolved_url": metadata.get("resolved_url"),
            "destination_title": metadata.get("destination_title"),
            "checked_at": metadata.get("checked_at"),
            "affected_posts": affected,
            "recommendation": recommendation(health),
        }
        entry["new_problem"] = health in PROBLEM_STATES and old_health.get(url) not in PROBLEM_STATES
        entries.append(entry)

    counts: dict[str, int] = defaultdict(int)
    for entry in entries:
        counts[entry["health"]] += 1
    problems = [entry for entry in entries if entry["health"] in PROBLEM_STATES]
    redirects = [entry for entry in entries if entry["health"] == "redirected"]
    new_problems = [entry for entry in problems if entry["new_problem"]]

    report = {
        "counts": dict(sorted(counts.items())),
        "problem_count": len(problems),
        "new_problem_count": len(new_problems),
        "links": entries,
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Link health",
        "",
        "Automated health checks for external links cited by the Southall Stories research corpus.",
        "",
        f"- Checked/cached links: **{len(entries)}**",
        f"- Actionable problems: **{len(problems)}**",
        f"- Newly degraded since the previous report: **{len(new_problems)}**",
        f"- Ordinary redirects: **{len(redirects)}**",
        "",
        "`gone` means HTTP 404/410. `unreachable` can include temporary failures or automation blocking. `suspicious-redirect` means a URL resolves successfully but appears to have been repointed to unrelated content.",
        "",
        "For genuine link rot, Southall Stories can use Micro.blog’s archived-link feature to recover or replace the destination while preserving the original reporting context.",
        "",
    ]

    if problems:
        lines += ["## Needs attention", ""]
        order = {"gone": 0, "suspicious-redirect": 1, "unreachable": 2}
        for entry in sorted(problems, key=lambda x: (order.get(x["health"], 9), x["domain"], x["url"])):
            title = entry.get("destination_title") or entry["url"]
            lines.append(f"### {entry['health']}: {title}")
            lines.append("")
            lines.append(f"- Original: {md_link(entry['url'], entry['url'])}")
            if entry.get("resolved_url") and entry["resolved_url"] != entry["url"]:
                lines.append(f"- Current destination: {md_link(entry['resolved_url'], entry['resolved_url'])}")
            if entry.get("http_status"):
                lines.append(f"- HTTP: `{entry['http_status']}`")
            lines.append(f"- Action: {entry['recommendation']}")
            if entry["affected_posts"]:
                lines.append("- Appears in:")
                for post in entry["affected_posts"]:
                    lines.append(f"  - {md_link(post['title'], post['url'])} — anchor text: `{post['article_label']}`")
            lines.append("")
    else:
        lines += ["## Needs attention", "", "No actionable link-health problems currently recorded.", ""]

    if redirects:
        lines += ["## Ordinary redirects", ""]
        for entry in redirects:
            label = entry.get("destination_title") or entry["url"]
            lines.append(f"- {md_link(label, entry['url'])} → {entry.get('resolved_url') or 'unknown destination'}")
        lines.append("")

    INDEX_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    if new_problems:
        alert = [
            "## New Southall Stories link-health problems",
            "",
            f"The weekly link-health check found **{len(new_problems)}** newly degraded external link(s).",
            "",
        ]
        for entry in new_problems:
            affected = ", ".join(post["title"] for post in entry["affected_posts"]) or "affected post unknown"
            alert.append(f"- **{entry['health']}** — {entry['url']} — {affected}")
        alert += ["", "See `indexes/link-health.md` for details and suggested Micro.blog archive/replacement actions.", ""]
        ALERT_PATH.write_text("\n".join(alert), encoding="utf-8")
    elif ALERT_PATH.exists():
        ALERT_PATH.unlink()

    print(f"Link health: {len(entries)} cached/checkable links; {len(problems)} problems; {len(new_problems)} new")


if __name__ == "__main__":
    main()
