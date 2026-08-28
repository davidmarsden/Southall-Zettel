#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

COMMONS_PATH = Path("generated/commons.json")
CACHE_PATH = Path("generated/citation-metadata.json")


def main() -> None:
    if not COMMONS_PATH.exists():
        raise SystemExit("generated/commons.json does not exist")

    data = json.loads(COMMONS_PATH.read_text(encoding="utf-8"))
    cache = json.loads(CACHE_PATH.read_text(encoding="utf-8")) if CACHE_PATH.exists() else {}

    enriched = 0
    for citation in data.get("citations", []):
        metadata = cache.get(citation.get("url")) or {}
        title = metadata.get("destination_title")
        if not title:
            continue
        citation["destination_title"] = title
        citation["title_source"] = metadata.get("title_source")
        citation["resolved_url"] = metadata.get("resolved_url")
        enriched += 1

    data.setdefault("policy", {})["citation_destination_titles_enriched"] = True
    data.setdefault("counts", {})["citations_with_destination_titles"] = enriched
    COMMONS_PATH.write_text(
        json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Applied destination titles to {enriched} Commons citations")


if __name__ == "__main__":
    main()
