#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote, urlparse

COMMONS_PATH = Path("generated/commons.json")
CACHE_PATH = Path("generated/citation-metadata.json")
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


def title_is_safe(original_url: str, resolved_url: str | None, title: str) -> bool:
    if not resolved_url or resolved_url == original_url:
        return True
    try:
        original = urlparse(original_url)
        resolved = urlparse(resolved_url)
    except Exception:
        return True
    if original.hostname != resolved.hostname:
        return True

    original_terms = words(original.path)
    if len(original_terms) < 2:
        return True

    title_terms = words(title)
    # Old civic-site routes can be recycled or redirected to an unrelated page. If a descriptive
    # original path and the destination title share no meaningful subject words, retain the
    # article's original anchor text rather than publish misleading current metadata.
    return bool(original_terms & title_terms)


def main() -> None:
    if not COMMONS_PATH.exists():
        raise SystemExit("generated/commons.json does not exist")

    data = json.loads(COMMONS_PATH.read_text(encoding="utf-8"))
    cache = json.loads(CACHE_PATH.read_text(encoding="utf-8")) if CACHE_PATH.exists() else {}

    enriched = 0
    rejected_redirects = 0
    for citation in data.get("citations", []):
        metadata = cache.get(citation.get("url")) or {}
        title = metadata.get("destination_title")
        if not title:
            continue
        if not title_is_safe(citation.get("url") or "", metadata.get("resolved_url"), title):
            rejected_redirects += 1
            continue
        citation["article_label"] = citation.get("label")
        citation["label"] = title
        citation["destination_title"] = title
        citation["title_source"] = metadata.get("title_source")
        citation["resolved_url"] = metadata.get("resolved_url")
        enriched += 1

    data.setdefault("policy", {})["citation_destination_titles_enriched"] = True
    data.setdefault("counts", {})["citations_with_destination_titles"] = enriched
    data.setdefault("counts", {})["citation_titles_rejected_as_stale_redirects"] = rejected_redirects
    COMMONS_PATH.write_text(
        json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Applied destination titles to {enriched} Commons citations; rejected {rejected_redirects} suspicious redirects")


if __name__ == "__main__":
    main()
