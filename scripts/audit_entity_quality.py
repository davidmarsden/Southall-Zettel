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


def main() -> None:
    rows = []
    for path in sorted(Path("entities").glob("*/*.md")):
        note = load_note(path)
        meta = note.get("meta") or {}
        description = note.get("description") or ""
        row = {
            "id": meta.get("id"),
            "name": meta.get("name"),
            "type": meta.get("type"),
            "path": note["path"],
            "description": description,
            "website": meta.get("website"),
            "reasons": reasons(description),
        }
        if note.get("error"):
            row["reasons"].append(note["error"])
        rows.append(row)

    flagged = [row for row in rows if row["reasons"]]
    missing = [row for row in rows if "missing-description" in row["reasons"]]
    weak = [row for row in rows if row["reasons"] and "missing-description" not in row["reasons"]]
    without_website = [row for row in rows if not row.get("website")]

    report = {
        "schema_version": 1,
        "rule": "An entity is complete when it has identity, a useful reader-facing description, provenance, and a first-party or authoritative source/website where one exists.",
        "counts": {
            "entities": len(rows),
            "flagged": len(flagged),
            "missing_descriptions": len(missing),
            "weak_descriptions": len(weak),
            "without_explicit_website": len(without_website),
        },
        "flagged": flagged,
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
        f"- No explicit website field: **{len(without_website)}** (review required; not automatically an error)",
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
        "## Website/source review",
        "",
        "Absence of an explicit website is a review prompt, not a failure: some historical people, places and defunct organisations legitimately have no current first-party site. Prefer a first-party site when available; otherwise use an authoritative or archived source.",
        "",
    ])
    Path("indexes/entity-quality.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Entity quality: {len(rows)} checked, {len(flagged)} description flags, {len(without_website)} without explicit website")


if __name__ == "__main__":
    main()
