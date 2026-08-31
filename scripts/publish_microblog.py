#!/usr/bin/env python3
"""Publish explicitly flagged Southall-Zettel post bodies back to Micro.blog.

Safety model:
- Never runs automatically; intended for workflow_dispatch only.
- A post must have `publish_to_microblog: true` in its YAML front matter.
- Only existing Southall Stories URLs are updated; this script never creates or deletes posts.
- Version 1 replaces only Micropub `content`; title/categories/front matter remain untouched.
- After Micro.blog confirms the update and q=source verifies the live body, the publish flag is removed.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
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


def normalise_body(value: str) -> str:
    return str(value or "").replace("\r\n", "\n").rstrip() + "\n"


def read_post(path: Path) -> tuple[dict, str, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(text)
    if not match:
        raise RuntimeError(f"No YAML front matter: {path}")
    metadata = yaml.safe_load(match.group(1)) or {}
    return metadata, normalise_body(text[match.end():]), text


def canonical_url(metadata: dict) -> str:
    value = str(metadata.get("url") or "").strip()
    if not value:
        raise RuntimeError("Post has no url in front matter")
    if value.startswith("http://") or value.startswith("https://"):
        return value
    return "https://southallstories.uk" + (value if value.startswith("/") else "/" + value)


def assert_allowed_url(url: str, allowed_hosts: set[str]) -> None:
    host = (urlparse(url).hostname or "").lower()
    if host not in allowed_hosts:
        raise RuntimeError(f"Refusing to publish outside Southall Stories: {url}")


def publish_content(token: str, url: str, body: str) -> None:
    payload = json.dumps({
        "action": "update",
        "url": url,
        "replace": {"content": [body.rstrip("\n")]},
    }).encode("utf-8")
    request = Request(
        ENDPOINT,
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json,*/*",
            "User-Agent": "Southall-Zettel/1.0 (+https://southallstories.uk)",
        },
    )
    with urlopen(request, timeout=30) as response:
        if not 200 <= response.getcode() < 300:
            raise RuntimeError(f"Micropub update returned HTTP {response.getcode()}")


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
        raise RuntimeError("Unexpected Micropub q=source response")
    return items


def live_body_for_url(token: str, url: str) -> str | None:
    target = url.rstrip("/")
    offset = 0
    while True:
        page = fetch_page(token, offset)
        if not page:
            return None
        for item in page:
            props = item.get("properties") or {}
            live_url = str(first(props, "url", "") or "").rstrip("/")
            if live_url != target:
                continue
            content = first(props, "content", "")
            if isinstance(content, dict):
                content = content.get("markdown") or content.get("html") or content.get("value") or ""
            return normalise_body(str(content or ""))
        if len(page) < PAGE_SIZE:
            return None
        offset += PAGE_SIZE


def clear_publish_flag(path: Path, metadata: dict, body: str) -> None:
    metadata = dict(metadata)
    metadata.pop("publish_to_microblog", None)
    front = yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True).rstrip()
    path.write_text(f"---\n{front}\n---\n{body}", encoding="utf-8")


def candidates(repo: Path, requested: str | None) -> list[Path]:
    if requested:
        path = (repo / requested).resolve()
        try:
            path.relative_to((repo / "posts").resolve())
        except ValueError as exc:
            raise RuntimeError("Requested path must be under posts/") from exc
        if not path.exists() or path.suffix != ".md":
            raise RuntimeError(f"Post not found: {requested}")
        return [path]

    flagged: list[Path] = []
    for path in sorted(repo.glob("posts/**/*.md")):
        metadata, _, _ = read_post(path)
        if metadata.get("publish_to_microblog") is True:
            flagged.append(path)
    return flagged


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--post", help="Optional repository-relative posts/...md path; still requires publish_to_microblog: true")
    args = parser.parse_args()

    token = os.environ.get("MICROBLOG_TOKEN", "").strip()
    if not token:
        raise SystemExit("MICROBLOG_TOKEN is required")

    configured = os.environ.get("MICROBLOG_HOSTS", "")
    allowed_hosts = {h.strip().lower() for h in configured.split(",") if h.strip()} or DEFAULT_HOSTS
    repo = Path.cwd().resolve()
    paths = candidates(repo, args.post)
    if not paths:
        raise SystemExit("No posts are marked publish_to_microblog: true")
    if len(paths) > 1:
        raise SystemExit("More than one post is flagged. Publish one article at a time for safety.")

    path = paths[0]
    metadata, body, _ = read_post(path)
    if metadata.get("publish_to_microblog") is not True:
        raise SystemExit(f"Refusing to publish {path.relative_to(repo)}: publish_to_microblog is not true")

    url = canonical_url(metadata)
    assert_allowed_url(url, allowed_hosts)
    before = live_body_for_url(token, url)
    if before is None:
        raise SystemExit(f"Live post not found in Micropub source; refusing to create anything: {url}")
    if before == body:
        print(f"Live content already matches {path.relative_to(repo)}; clearing publish flag without posting")
        clear_publish_flag(path, metadata, body)
        return

    print(f"Publishing body update: {path.relative_to(repo)} -> {url}")
    publish_content(token, url, body)
    after = live_body_for_url(token, url)
    if after != body:
        raise RuntimeError("Micropub accepted the update but live q=source verification does not match; publish flag retained")

    clear_publish_flag(path, metadata, body)
    print("Verified live Micro.blog content matches Zettel; publish flag cleared")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Micro.blog publish failed: {exc}", file=sys.stderr)
        raise
