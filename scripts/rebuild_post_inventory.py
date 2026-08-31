#!/usr/bin/env python3
"""Rebuild the basic post inventory and indexes from posts/**."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

import yaml

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\((https?://[^)\s]+)")
HTML_LINK_RE = re.compile(r"href=[\"'](https?://[^\"']+)", re.IGNORECASE)


def parse_post(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(text)
    if not match:
        raise ValueError(f"No YAML front matter: {path}")
    return yaml.safe_load(match.group(1)) or {}, text[match.end():]


def outbound_links(body: str) -> list[str]:
    links = set(MARKDOWN_LINK_RE.findall(body)) | set(HTML_LINK_RE.findall(body))
    return sorted(link.rstrip(".,;:") for link in links)


def sha256(path: Path) -> str:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest


def main() -> None:
    repo = Path.cwd()
    paths = sorted(repo.glob("posts/[0-9][0-9][0-9][0-9]/*/*/*.md"))
    records: list[dict] = []
    category_counts: Counter[str] = Counter()
    domain_counts: Counter[str] = Counter()
    year_posts: dict[str, list[dict]] = defaultdict(list)

    for path in paths:
        metadata, body = parse_post(path)
        rel = path.relative_to(repo)
        links = outbound_links(body)
        domains = sorted({urlparse(link).netloc.lower().removeprefix("www.") for link in links})
        categories = [str(c).strip() for c in (metadata.get("categories") or []) if str(c).strip()]
        category_counts.update(categories)
        domain_counts.update(domains)
        record = {
            "path": rel.as_posix(),
            "sha256": sha256(path),
            "post_id": metadata.get("post_id"),
            "title": metadata.get("title"),
            "summary": metadata.get("summary"),
            "date": str(metadata.get("date")) if metadata.get("date") is not None else None,
            "lastmod": str(metadata.get("lastmod")) if metadata.get("lastmod") is not None else None,
            "url": metadata.get("url"),
            "guid": metadata.get("guid"),
            "categories": categories,
            "outbound_links": links,
            "outbound_domains": domains,
            "images": metadata.get("images") or [],
            "videos": metadata.get("videos") or [],
        }
        records.append(record)
        year_posts[rel.parts[1]].append(record)

    generated = repo / "generated"
    indexes = repo / "indexes"
    generated.mkdir(exist_ok=True)
    indexes.mkdir(exist_ok=True)
    (generated / "posts.json").write_text(json.dumps(records, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")

    lines = ["# Posts by year", ""]
    for year in sorted(year_posts, reverse=True):
        lines += [f"## {year}", ""]
        for item in sorted(year_posts[year], key=lambda r: r["date"] or "", reverse=True):
            lines.append(f"- [{item['title']}](/../{item['path']}) — {item['date']}")
        lines.append("")
    (indexes / "years.md").write_text("\n".join(lines), encoding="utf-8")

    lines = ["# Categories", ""]
    for category, count in category_counts.most_common():
        lines.append(f"- **{category}** — {count}")
    lines.append("")
    (indexes / "categories.md").write_text("\n".join(lines), encoding="utf-8")

    lines = ["# Outbound source domains", ""]
    for domain, count in domain_counts.most_common():
        lines.append(f"- **{domain}** — {count} post{'s' if count != 1 else ''}")
    lines.append("")
    (indexes / "sources.md").write_text("\n".join(lines), encoding="utf-8")

    print(f"Rebuilt inventory for {len(records)} posts")


if __name__ == "__main__":
    main()
