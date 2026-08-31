#!/usr/bin/env python3
"""Synchronise the Southall-Zettel post corpus from live Micro.blog via Micropub.

Existing exported posts keep their original front matter byte-for-byte; only the
post body is replaced when the live Micropub source differs. New live posts get
minimal compatible front matter so the research corpus can ingest them without
waiting for a manual Micro.blog export.
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import yaml

ENDPOINT = "https://micro.blog/micropub"
PAGE_SIZE = 100
FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
DEFAULT_HOSTS = {"southallstories.uk", "www.southallstories.uk", "southall.micro.blog"}


def first(properties: dict, key: str, default=None):
    value = properties.get(key, default)
    if isinstance(value, list):
        return value[0] if value else default
    return value


def fetch_page(token: str, offset: int) -> list[dict]:
    query = urlencode({"q": "source", "limit": PAGE_SIZE, "offset": offset})
    request = Request(
        f"{ENDPOINT}?{query}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "User-Agent": "Southall-Zettel/1.0 (+https://southallstories.uk)",
        },
    )
    with urlopen(request, timeout=30) as response:
        payload = json.load(response)
    items = payload.get("items", [])
    if not isinstance(items, list):
        raise RuntimeError("Unexpected Micropub q=source response: items is not a list")
    return items


def live_posts(token: str, allowed_hosts: set[str]) -> list[dict]:
    result: list[dict] = []
    offset = 0
    while True:
        page = fetch_page(token, offset)
        if not page:
            break
        for item in page:
            props = item.get("properties") or {}
            url = str(first(props, "url", "") or "")
            host = (urlparse(url).hostname or "").lower()
            status = str(first(props, "post-status", "published") or "published")
            if host in allowed_hosts and status == "published":
                result.append(item)
        if len(page) < PAGE_SIZE:
            break
        offset += PAGE_SIZE
    return result


def existing_index(repo: Path) -> tuple[dict[str, Path], dict[str, Path]]:
    by_url: dict[str, Path] = {}
    by_uid: dict[str, Path] = {}
    for path in repo.glob("posts/**/*.md"):
        text = path.read_text(encoding="utf-8")
        match = FRONT_MATTER_RE.match(text)
        if not match:
            continue
        metadata = yaml.safe_load(match.group(1)) or {}
        url = str(metadata.get("url") or "")
        if url:
            by_url[url.rstrip("/")] = path
            if url.startswith("/"):
                by_url[("https://southallstories.uk" + url).rstrip("/")] = path
        guid = str(metadata.get("guid") or "")
        if guid:
            by_url[guid.rstrip("/")] = path
        post_id = metadata.get("post_id")
        if post_id is not None:
            by_uid[str(post_id)] = path
    return by_url, by_uid


def source_body(item: dict) -> str:
    props = item.get("properties") or {}
    content = first(props, "content", "")
    if isinstance(content, dict):
        content = content.get("markdown") or content.get("html") or content.get("value") or ""
    return str(content or "").replace("\r\n", "\n").rstrip() + "\n"


def path_for_new_post(repo: Path, item: dict) -> Path:
    props = item.get("properties") or {}
    published = str(first(props, "published", "") or "")
    url = str(first(props, "url", "") or "")
    if published:
        dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
        year, month, day = dt.strftime("%Y"), dt.strftime("%m"), dt.strftime("%d")
    else:
        parts = [p for p in urlparse(url).path.split("/") if p]
        if len(parts) < 4 or not all(part.isdigit() for part in parts[:3]):
            raise RuntimeError(f"Cannot derive date for new post {url}")
        year, month, day = parts[:3]
    slug = [p for p in urlparse(url).path.split("/") if p]
    slug = slug[-1] if slug else f"post-{first(props, 'uid', 'unknown')}"
    return repo / "posts" / year / month / day / f"{slug}.md"


def new_post_text(item: dict) -> str:
    props = item.get("properties") or {}
    uid = first(props, "uid")
    title = str(first(props, "name", "") or "")
    published = str(first(props, "published", "") or "")
    url = str(first(props, "url", "") or "")
    parsed = urlparse(url)
    relative_url = parsed.path or url
    categories = props.get("category") or []
    if not isinstance(categories, list):
        categories = [categories]
    metadata = {
        "layout": "post",
        "title": title,
        "microblog": not bool(title),
        "post_id": uid,
        "date": published,
        "type": "post",
        "categories": [str(c) for c in categories if str(c).strip()],
        "url": relative_url,
    }
    front = yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True).rstrip()
    return f"---\n{front}\n---\n{source_body(item)}"


def main() -> None:
    token = os.environ.get("MICROBLOG_TOKEN", "").strip()
    if not token:
        raise SystemExit("MICROBLOG_TOKEN is required")
    repo = Path.cwd()
    configured = os.environ.get("MICROBLOG_HOSTS", "")
    allowed_hosts = {h.strip().lower() for h in configured.split(",") if h.strip()} or DEFAULT_HOSTS

    posts = live_posts(token, allowed_hosts)
    if not posts:
        raise SystemExit(f"Micropub returned no published posts for {sorted(allowed_hosts)}; refusing to modify corpus")

    by_url, by_uid = existing_index(repo)
    updated = created = unchanged = 0
    seen_paths: set[Path] = set()

    for item in posts:
        props = item.get("properties") or {}
        uid = str(first(props, "uid", "") or "")
        url = str(first(props, "url", "") or "")
        path = by_uid.get(uid) if uid else None
        if path is None:
            path = by_url.get(url.rstrip("/"))
        if path is None:
            parsed = urlparse(url)
            path = by_url.get(parsed.path.rstrip("/"))

        if path is None:
            path = path_for_new_post(repo, item)
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.exists():
                raise RuntimeError(f"New-post path collision: {path}")
            path.write_text(new_post_text(item), encoding="utf-8")
            created += 1
            seen_paths.add(path)
            continue

        seen_paths.add(path)
        old = path.read_text(encoding="utf-8")
        match = FRONT_MATTER_RE.match(old)
        if not match:
            raise RuntimeError(f"Existing corpus post has no YAML front matter: {path}")
        prefix = old[:match.end()]
        live_body = source_body(item)
        current_body = old[match.end():].replace("\r\n", "\n").rstrip() + "\n"
        if current_body == live_body:
            unchanged += 1
            continue
        path.write_text(prefix + live_body, encoding="utf-8")
        updated += 1

    print(f"Micro.blog sync: {len(posts)} live posts; {updated} updated; {created} created; {unchanged} unchanged")
    print("Live deletions are intentionally not removed automatically; the corpus remains an archive.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Micro.blog sync failed: {exc}", file=sys.stderr)
        raise
