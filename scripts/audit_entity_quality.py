#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
GENERIC_PATTERNS = [
    re.compile(r"\brecurring (?:in|subject of) .*reporting\b", re.I),
    re.compile(r"\brecurring figure\b", re.I),
    re.compile(r"\bassociated with\b", re.I),
    re.compile(r"\bappears? in .*reporting\b", re.I),
    re.compile(r"\bmentioned in .*reporting\b", re.I),
    re.compile(r"\bsubject of .*reporting\b", re.I),
    re.compile(r"^local (?:political|community|civic|public) (?:and \w+ )?figure\b", re.I),
]


def clean_body(value: str) -> str:
    value = re.sub(r"^#{1,6}\s+", "", value.strip(), flags=re.MULTILINE)
    value = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", value)
    value = re.sub(r"[*_`]+", "", value)
    value = re.sub(r"<[^>]+>", "", value)
    return re.sub(r"\s+", " ", value).strip()


def load_note(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {"path": path.as_posix(), "error": "missing-front-matter"}
    meta = yaml.safe_load(match.group(1)) or {}
    body = clean_body(text[match.end():])
    return {"path": path.as_posix(), "meta": meta, "description": meta.get("description") or body}


def reasons(description: str) -> list[str]:
    if not description:
        return ["missing-description"]
    found: list[str] = []
    if len(description) < 60:
        found.append("very-short-description")
    if any(pattern.search(description) for pattern in GENERIC_PATTERNS):
        found.append("reporting-defined-or-generic-description")
    if "southall stories" in description.lower() and len(description) < 150:
        found.append("identity-too-dependent-on-southall-stories")
    return found


def reviewed_sources_by_entity() -> dict[str, list[dict]]:
    lookup: dict[str, list[dict]] = {}
    for path in sorted(Path("sources").glob("**/*.md")):
        note = load_note(path)
        meta = note.get("meta") or {}
        if meta.get("review_status") != "reviewed" or not meta.get("canonical_url"):
            continue
        source = {
            "title": meta.get("title"),
            "publisher": meta.get("publisher"),
            "url": meta.get("canonical_url"),
            "path": path.as_posix(),
        }
        for entity_id in meta.get("related_entities") or []:
            lookup.setdefault(entity_id, []).append(source)
    return lookup


def main() -> None:
    source_lookup = reviewed_sources_by_entity()
    rows = []
    for path in sorted(Path("entities").glob("*/*.md")):
        note = load_note(path)
        meta = note.get("meta") or {}
        entity_id = meta.get("id")
        description = note.get("description") or ""
        reviewed_sources = source_lookup.get(entity_id, [])
        website = meta.get("website")
        row = {
            "id": entity_id,
            "name": meta.get("name"),
            "type": meta.get("type"),
            "path": note["path"],
            "description": description,
            "website": website,
            "reviewed_sources": reviewed_sources,
            "has_source_or_website": bool(website or reviewed_sources),
            "reasons": reasons(description),
        }
        if note.get("error"):
            row["reasons"].append(note["error"])
        rows.append(row)

    flagged = [row for row in rows if row["reasons"]]
    missing = [row for row in rows if "missing-description" in row["reasons"]]
    weak = [row for row in rows if row["reasons"] and "missing-description" not in row["reasons"]]
    without_website = [row for row in rows if not row.get("website")]
    without_source_or_website = [row for row in rows if not row["has_source_or_website"]]
    complete = [row for row in rows if not row["reasons"] and row["has_source_or_website"]]

    report = {
        "schema_version": 2,
        "rule": "An entity is complete when it has identity, a useful reader-facing description, provenance, and a first-party or authoritative source/website where one exists.",
        "counts": {
            "entities": len(rows),
            "flagged": len(flagged),
            "missing_descriptions": len(missing),
            "weak_descriptions": len(weak),
            "without_explicit_website": len(without_website),
            "without_source_or_website": len(without_source_or_website),
            "description_and_source_complete": len(complete),
        },
        "flagged": flagged,
        "without_source_or_website": [
            {"id": row["id"], "name": row["name"], "type": row["type"], "path": row["path"]}
            for row in without_source_or_website
        ],
        "without_explicit_website": [
            {"id": row["id"], "name": row["name"], "type": row["type"], "path": row["path"]}
            for row in without_website
        ],
    }
    Path("generated/entity-quality.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# Entity quality audit",
        "",
        report["rule"],
        "",
        f"- Entities checked: **{len(rows)}**",
        f"- Missing descriptions: **{len(missing)}**",
        f"- Weak/generic descriptions: **{len(weak)}**",
        f"- No source or website: **{len(without_source_or_website)}**",
        f"- Description + source/website complete: **{len(complete)}**",
        f"- No explicit website field: **{len(without_website)}** (informational only)",
        "",
        "## Description review queue",
        "",
    ]
    if not flagged:
        lines.append("No description-quality flags.")
    else:
        for row in flagged:
            lines.append(f"- **{row['name'] or row['id']}** (`{row['path']}`) — {', '.join(row['reasons'])}")
            if row["description"]:
                lines.append(f"  - Current: {row['description']}")
    lines.extend([
        "",
        "## Source / website review queue",
        "",
        "These entities currently have neither an explicit website nor a reviewed source record with a canonical URL. This is a review queue, not automatically an error: some historical people, streets and defunct organisations may legitimately have no suitable first-party site. Prefer first-party evidence where available, then authoritative or archived sources.",
        "",
    ])
    if without_source_or_website:
        for row in without_source_or_website:
            lines.append(f"- **{row['name'] or row['id']}** (`{row['path']}`)")
    else:
        lines.append("None.")
    Path("indexes/entity-quality.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Entity quality: {len(rows)} checked, {len(flagged)} description flags, {len(without_source_or_website)} without source/website")


if __name__ == "__main__":
    main()
