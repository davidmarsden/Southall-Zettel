#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

PROBLEM_STATES = {"gone", "unreachable", "suspicious-redirect"}
REPORT_PATH = Path("generated/link-health.json")
INDEX_PATH = Path("indexes/link-health.md")


def md_link(label: str, url: str) -> str:
    safe = (label or url).replace("[", "\\[").replace("]", "\\]")
    return f"[{safe}]({url})" if url else safe


def main() -> None:
    previous_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/link-health-previous.json")
    if not previous_path.exists() or not REPORT_PATH.exists():
        print("No previous link-health report available; resolved audit skipped")
        return

    previous = json.loads(previous_path.read_text(encoding="utf-8"))
    current = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    old = {item["url"]: item for item in previous.get("links", [])}
    now = {item["url"]: item for item in current.get("links", [])}

    resolved = []
    for url, old_item in old.items():
        if old_item.get("health") not in PROBLEM_STATES:
            continue
        new_item = now.get(url)
        if new_item is None:
            resolved.append({
                "url": url,
                "previous_health": old_item.get("health"),
                "current_health": "removed-or-replaced",
                "resolution": "removed-or-replaced-in-corpus",
                "destination_title": old_item.get("destination_title"),
                "affected_posts": old_item.get("affected_posts", []),
            })
        elif new_item.get("health") not in PROBLEM_STATES:
            resolved.append({
                "url": url,
                "previous_health": old_item.get("health"),
                "current_health": new_item.get("health"),
                "resolution": "link-recovered",
                "destination_title": new_item.get("destination_title") or old_item.get("destination_title"),
                "affected_posts": new_item.get("affected_posts", []) or old_item.get("affected_posts", []),
            })

    current["resolved_since_last_check_count"] = len(resolved)
    current["resolved_since_last_check"] = resolved
    REPORT_PATH.write_text(json.dumps(current, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")

    text = INDEX_PATH.read_text(encoding="utf-8")
    marker = "- Ordinary redirects:"
    summary = f"- Resolved since the previous report: **{len(resolved)}**\n"
    if marker in text:
        text = text.replace(marker, summary + marker, 1)

    if resolved:
        section = ["## Resolved since last check", ""]
        for item in sorted(resolved, key=lambda x: x["url"]):
            label = item.get("destination_title") or item["url"]
            if item["resolution"] == "removed-or-replaced-in-corpus":
                status = "removed or replaced in the Southall Stories article"
            else:
                status = f"now `{item['current_health']}`"
            section.append(f"- {md_link(label, item['url'])} — was `{item['previous_health']}`; {status}.")
            for post in item.get("affected_posts", []):
                if post.get("url"):
                    section.append(f"  - {md_link(post.get('title') or post['url'], post['url'])}")
        section.append("")
        insertion = "\n".join(section)
        anchor = "## Needs attention"
        text = text.replace(anchor, insertion + "\n" + anchor, 1)

    INDEX_PATH.write_text(text, encoding="utf-8")
    print(f"Resolved link-health problems since previous report: {len(resolved)}")


if __name__ == "__main__":
    main()
