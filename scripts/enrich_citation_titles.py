#!/usr/bin/env python3
from __future__ import annotations

import html
import io
import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from pypdf import PdfReader

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^\s)]+)\)")
HTML_LINK_RE = re.compile(r'<a\s+[^>]*href=["\'](https?://[^"\']+)["\'][^>]*>(.*?)</a>', re.IGNORECASE | re.DOTALL)
HTML_TAG_RE = re.compile(r"<[^>]+>")
CACHE_PATH = Path("generated/citation-metadata.json")
MAX_FETCH_BYTES = 5 * 1024 * 1024
MAX_NEW_FETCHES = 120
FETCH_WORKERS = 12
FETCH_TIMEOUT = 7
FULL_LINK_CHECK = os.environ.get("LINK_HEALTH_FULL", "").lower() in {"1", "true", "yes"}

EXCLUDED_DOMAINS = {
    "x.com", "twitter.com", "facebook.com", "instagram.com", "youtube.com", "youtu.be",
    "communitypoweredreporting.co.uk", "southallstories.uk",
}


class TitleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_title = False
        self.title_parts: list[str] = []
        self.og_title: str | None = None

    def handle_starttag(self, tag: str, attrs) -> None:
        attrs_dict = {str(k).lower(): v for k, v in attrs}
        if tag.lower() == "title":
            self.in_title = True
        if tag.lower() == "meta":
            prop = str(attrs_dict.get("property") or attrs_dict.get("name") or "").lower()
            content = attrs_dict.get("content")
            if prop == "og:title" and content and not self.og_title:
                self.og_title = str(content)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)

    @property
    def title(self) -> str | None:
        value = " ".join(self.title_parts).strip()
        return value or None


def clean_text(value: str | None) -> str | None:
    if not value:
        return None
    value = html.unescape(value)
    value = HTML_TAG_RE.sub("", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value[:300] if value else None


def normalise_domain(url: str) -> str:
    return (urlparse(url).hostname or "").lower().removeprefix("www.")


def should_fetch(url: str) -> bool:
    domain = normalise_domain(url)
    if not domain:
        return False
    return not any(domain == blocked or domain.endswith("." + blocked) for blocked in EXCLUDED_DOMAINS)


def discover_urls(repo: Path) -> list[str]:
    urls: list[str] = []
    seen: set[str] = set()
    for path in sorted(repo.glob("posts/**/*.md"), reverse=True):
        text = path.read_text(encoding="utf-8")
        body_match = FRONT_MATTER_RE.match(text)
        body = text[body_match.end():] if body_match else text
        found = [url for _, url in MARKDOWN_LINK_RE.findall(body)]
        found.extend(url for url, _ in HTML_LINK_RE.findall(body))
        for url in found:
            url = url.rstrip(".,;:")
            if url in seen or not should_fetch(url):
                continue
            seen.add(url)
            urls.append(url)
    return urls


def read_limited(response) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while total < MAX_FETCH_BYTES:
        chunk = response.read(min(65536, MAX_FETCH_BYTES - total))
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
    return b"".join(chunks)


def pdf_title(data: bytes) -> str | None:
    try:
        reader = PdfReader(io.BytesIO(data), strict=False)
        return clean_text(getattr(reader.metadata, "title", None))
    except Exception:
        return None


def html_title(data: bytes, charset: str | None) -> tuple[str | None, str | None]:
    try:
        text = data.decode(charset or "utf-8", errors="replace")
        parser = TitleParser()
        parser.feed(text)
        og = clean_text(parser.og_title)
        if og:
            return og, "og:title"
        title = clean_text(parser.title)
        if title:
            return title, "html-title"
    except Exception:
        pass
    return None, None


def classify_health(url: str, result: dict) -> str:
    status = result.get("http_status")
    if status in {404, 410}:
        return "gone"
    if status is None and result.get("status") in {"fetch-failed", "parse-failed"}:
        return "unreachable"
    if status and status >= 400:
        return "unreachable"
    resolved = result.get("resolved_url")
    if resolved and resolved.rstrip("/") != url.rstrip("/"):
        return "redirected"
    if status and 200 <= status < 400:
        return "healthy"
    return "unreachable"


def fetch_metadata(url: str) -> tuple[str, dict]:
    result = {
        "destination_title": None,
        "title_source": None,
        "resolved_url": None,
        "content_type": None,
        "http_status": None,
        "status": "unresolved",
        "health": "unreachable",
    }
    try:
        request = Request(
            url,
            headers={
                "User-Agent": "Southall-Zettel/1.0 (+https://southallstories.uk)",
                "Accept": "text/html,application/xhtml+xml,application/pdf;q=0.9,*/*;q=0.5",
            },
        )
        with urlopen(request, timeout=FETCH_TIMEOUT) as response:
            result["http_status"] = response.getcode()
            result["resolved_url"] = response.geturl()
            content_type = (response.headers.get_content_type() or "").lower()
            result["content_type"] = content_type
            result["status"] = "fetched"
            data = read_limited(response)
            if content_type == "application/pdf" or data.startswith(b"%PDF-"):
                title = pdf_title(data)
                if title:
                    result["destination_title"] = title
                    result["title_source"] = "pdf-title"
                    result["status"] = "resolved"
            elif content_type.startswith("text/html") or b"<html" in data[:4096].lower():
                charset = response.headers.get_content_charset()
                title, source = html_title(data, charset)
                if title:
                    result["destination_title"] = title
                    result["title_source"] = source
                    result["status"] = "resolved"
    except HTTPError as exc:
        result["http_status"] = exc.code
        result["resolved_url"] = exc.geturl()
        result["status"] = f"http-{exc.code}"
    except (URLError, TimeoutError, OSError):
        result["status"] = "fetch-failed"
    except Exception:
        result["status"] = "parse-failed"
    result["health"] = classify_health(url, result)
    return url, result


def main() -> None:
    repo = Path.cwd()
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    cache = json.loads(CACHE_PATH.read_text(encoding="utf-8")) if CACHE_PATH.exists() else {}
    urls = discover_urls(repo)

    if FULL_LINK_CHECK:
        pending = urls
        print(f"Weekly link-health check: refreshing all {len(pending)} checkable URLs")
    else:
        pending = [url for url in urls if url not in cache][:MAX_NEW_FETCHES]
        print(f"Citation metadata cache: {len(cache)} entries; resolving {len(pending)} new URLs")

    if pending:
        with ThreadPoolExecutor(max_workers=FETCH_WORKERS) as pool:
            futures = {pool.submit(fetch_metadata, url): url for url in pending}
            for future in as_completed(futures):
                url, metadata = future.result()
                metadata["checked_at"] = int(time.time())
                cache[url] = metadata
                if metadata.get("destination_title") and not FULL_LINK_CHECK:
                    print(f"  resolved: {metadata['destination_title'][:90]}")

    active = {url: cache[url] for url in urls if url in cache}
    CACHE_PATH.write_text(json.dumps(active, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    resolved = sum(1 for item in active.values() if item.get("destination_title"))
    health_counts: dict[str, int] = {}
    for item in active.values():
        health = item.get("health") or "unknown"
        health_counts[health] = health_counts.get(health, 0) + 1
    print(f"Citation metadata cache now contains {len(active)} active URLs ({resolved} titled); health={health_counts}")


if __name__ == "__main__":
    main()
