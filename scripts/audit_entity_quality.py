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
SOURCE_REVIEW_EXEMPTIONS = {"no-suitable-external-source", "not-applicable"}


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
        source_review = meta.get("source_review")
        source_exempt = source_review in SOURCE_REVIEW_EXEMPTIONS
        has_source_or_website = bool(website or reviewed_sources)
        source_complete = has_source_or_website or source_exempt
        row = {
            "id": entity_id,
            "name": meta.get("name"),
            "type": meta.get("type"),
            "path": note["path"],
            "description": description,
            "website": website,
            "reviewed_sources": reviewed_sources,
            "source_review": source_review,
            "source_review_note": meta.get("source_review_note"),
            "has_source_or_website": has_source_or_website,
            "source_complete": source_complete,
            "reasons": reasons(description),
        }
        if note.get("error"):
            row["reasons"].append(note["error"])
        rows.append(row)

    flagged = [row for row in rows if row["reasons"]]
    missing = [row for row in rows if "missing-description" in row["reasons"]]
    weak = [row for row in rows if row["reasons"] and "missing-description" not in row["reasons"]]
    without_website = [row for row in rows if not row.get("website")]
    source_review_queue = [row for row in rows if not row["source_complete"]]
    source_exemptions = [row for row in rows if row["source_review"] in SOURCE_REVIEW_EXEMPTIONS]
    complete = [row for row in rows if not row["reasons"] and row["source_complete"]]

    report = {
        "schema_version": 3,
        "rule": "An entity is complete when it has identity, a useful reader-facing description, provenance, and a first-party or authoritative source/website where one exists; reviewed exceptions are recorded explicitly rather than filled with artificial links.",
        "counts": {
            "entities": len(rows),
            "flagged": len(flagged),
            "missing_descriptions": len(missing),
            "weak_descriptions": len(weak),
            "without_explicit_website": len(without_website),
            "source_review_queue": len(source_review_queue),
            "reviewed_source_exemptions": len(source_exemptions),
            "complete": len(complete),
        },
        "flagged": flagged,
        "source_review_queue": [
            {"id": row["id"], "name": row["name"], "type": row["type"], "path": row["path"]}
            for row in source_review_queue
        ],
        "reviewed_source_exemptions": [
            {
                "id": row["id"],
                "name": row["name"],
                "type": row["type"],
                "path": row["path"],
                "source_review": row["source_review"],
                "source_review_note": row["source_review_note"],
            }
            for row in source_exemptions
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
        f"- Source/website review queue: **{len(source_review_queue)}**",
        f"- Reviewed source exemptions: **{len(source_exemptions)}**",
        f"- Fully reviewed complete entities: **{len(complete)}**",
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
        "These entities still need an editorial decision: attach a suitable first-party or authoritative source/website where one exists, or explicitly record `source_review: no-suitable-external-source` / `not-applicable` when no meaningful external link should be manufactured.",
        "",
    ])
    if source_review_queue:
        for row in source_review_queue:
            lines.append(f"- **{row['name'] or row['id']}** (`{row['path']}`)")
    else:
        lines.append("None.")

    lines.extend(["", "## Reviewed source exemptions", ""])
    if source_exemptions:
        for row in source_exemptions:
            suffix = f" — {row['source_review_note']}" if row.get("source_review_note") else ""
            lines.append(f"- **{row['name'] or row['id']}** — `{row['source_review']}`{suffix}")
    else:
        lines.append("None.")

    Path("indexes/entity-quality.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"Entity quality: {len(rows)} checked, {len(flagged)} description flags, "
        f"{len(source_review_queue)} source decisions outstanding, {len(source_exemptions)} reviewed exemptions"
    )


if __name__ == "__main__":
    main()
