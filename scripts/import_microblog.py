#!/usr/bin/env python3
"""Import a Micro.blog theme/content export into the Southall Zettel corpus.

This script deliberately preserves each source post byte-for-byte while deriving
an inventory and simple indexes alongside it. Generated files can be rebuilt at
any time; the copied post files remain the source of truth for the corpus.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
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
    metadata = yaml.safe_load(match.group(1)) or {}
    body = text[match.end():]
    return metadata, body


def outbound_links(body: str) -> list[str]:
    links = set(MARKDOWN_LINK_RE.findall(body)) | set(HTML_LINK_RE.findall(body))
    return sorted(link.rstrip(".,;:") for link in links)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("export", type=Path, help="Extracted Micro.blog export directory")
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help="Repository root")
    args = parser.parse_args()

    export_root = args.export.resolve()
    repo_root = args.repo.resolve()
    content_root = export_root / "content"
    if not content_root.exists():
        raise SystemExit(f"Expected {content_root}")

    source_posts = sorted(content_root.glob("[0-9][0-9][0-9][0-9]/*/*/*.md"))
    if not source_posts:
        raise SystemExit("No dated Micro.blog posts found")

    records: list[dict] = []
    category_counts: Counter[str] = Counter()
    domain_counts: Counter[str] = Counter()
    year_posts: dict[str, list[dict]] = defaultdict(list)

    for source in source_posts:
        metadata, body = parse_post(source)
        relative = source.relative_to(content_root)
        destination = repo_root / "posts" / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

        links = outbound_links(body)
        domains = sorted({urlparse(link).netloc.lower().removeprefix("www.") for link in links})
        categories = [str(c).strip() for c in (metadata.get("categories") or []) if str(c).strip()]
        category_counts.update(categories)
        domain_counts.update(domains)

        record = {
            "path": str(Path("posts") / relative),
            "sha256": sha256(destination),
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
        year_posts[relative.parts[0]].append(record)

    generated = repo_root / "generated"
    indexes = repo_root / "indexes"
    generated.mkdir(parents=True, exist_ok=True)
    indexes.mkdir(parents=True, exist_ok=True)

    (generated / "posts.json").write_text(
        json.dumps(records, indent=2, ensure_ascii=False, default=str) + "\n",
        encoding="utf-8",
    )

    years_lines = ["# Posts by year", ""]
    for year in sorted(year_posts, reverse=True):
        years_lines += [f"## {year}", ""]
        for item in sorted(year_posts[year], key=lambda r: r["date"] or "", reverse=True):
            years_lines.append(f"- [{item['title']}](/../{item['path']}) — {item['date']}")
        years_lines.append("")
    (indexes / "years.md").write_text("\n".join(years_lines), encoding="utf-8")

    category_lines = ["# Categories", ""]
    for category, count in category_counts.most_common():
        category_lines.append(f"- **{category}** — {count}")
    category_lines.append("")
    (indexes / "categories.md").write_text("\n".join(category_lines), encoding="utf-8")

    domain_lines = ["# Outbound source domains", ""]
    for domain, count in domain_counts.most_common():
        domain_lines.append(f"- **{domain}** — {count} post{'s' if count != 1 else ''}")
    domain_lines.append("")
    (indexes / "sources.md").write_text("\n".join(domain_lines), encoding="utf-8")

    print(f"Imported {len(records)} posts")
    print(f"Categories: {len(category_counts)}")
    print(f"Outbound domains: {len(domain_counts)}")


if __name__ == "__main__":
    main()
