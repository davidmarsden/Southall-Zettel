#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def load_note(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(text)
    if not match:
        raise ValueError(f"Missing YAML front matter: {path}")
    return yaml.safe_load(match.group(1)) or {}, text[match.end():]


def phrase_pattern(phrase: str) -> re.Pattern[str]:
    return re.compile(rf"(?<![\w]){re.escape(phrase.strip())}(?![\w])", re.IGNORECASE)


def has_valid_occurrence(text: str, phrase: str, excluded_suffixes: list[str]) -> bool:
    for match in phrase_pattern(phrase).finditer(text):
        tail = text[match.end():]
        blocked = False
        for suffix in excluded_suffixes:
            if re.match(rf"^\s+{re.escape(suffix.strip())}(?![\w])", tail, re.IGNORECASE):
                blocked = True
                break
        if not blocked:
            return True
    return False


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    repo = Path.cwd()
    generated = repo / "generated"

    mentions_path = generated / "entity-mentions.json"
    backlinks_path = generated / "backlinks.json"
    graph_path = generated / "graph.json"
    summary_path = generated / "research-summary.json"

    mentions = json.loads(mentions_path.read_text(encoding="utf-8"))
    backlinks = json.loads(backlinks_path.read_text(encoding="utf-8"))
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    summary = json.loads(summary_path.read_text(encoding="utf-8"))

    changed: dict[str, tuple[int, int]] = {}

    for entity_path in sorted(repo.glob("entities/*/*.md")):
        entity, _ = load_note(entity_path)
        suffixes = list(entity.get("exclude_suffixes") or [])
        if not suffixes:
            continue

        entity_id = entity["id"]
        phrases = [entity.get("name", ""), *list(entity.get("aliases") or [])]
        old_mentions = list(mentions.get(entity_id) or [])
        kept = []

        for mention in old_mentions:
            post_path = repo / mention["path"]
            meta, body = load_note(post_path)
            title = meta.get("title") or post_path.stem
            text = f"{title}\n{meta.get('summary') or ''}\n{body}"
            valid_aliases = [p for p in phrases if p and has_valid_occurrence(text, p, suffixes)]
            if valid_aliases:
                kept.append({**mention, "matched_aliases": valid_aliases})

        if len(kept) == len(old_mentions) and kept == old_mentions:
            continue

        mentions[entity_id] = kept
        backlinks.setdefault("entities", {})[entity_id] = [m["path"] for m in kept]
        changed[entity_id] = (len(old_mentions), len(kept))

        typed_id = f"entity:{entity_id}"
        graph["edges"] = [
            edge for edge in graph.get("edges", [])
            if not (edge.get("source") == typed_id and edge.get("type") == "mentioned-in")
        ]
        for mention in kept:
            graph["edges"].append({
                "source": typed_id,
                "target": "post:" + mention["path"],
                "type": "mentioned-in",
                "provenance": "deterministic-alias-match",
            })

    if not changed:
        print("No ambiguous entity mentions required disambiguation.")
        return

    summary["entity_mentions"] = sum(len(items) for items in mentions.values())
    summary["graph_edges"] = len(graph.get("edges", []))

    write_json(mentions_path, mentions)
    write_json(backlinks_path, backlinks)
    write_json(graph_path, graph)
    write_json(summary_path, summary)

    # Keep the human-readable entity index count aligned with the generated data.
    index_path = repo / "indexes/entities.md"
    index_text = index_path.read_text(encoding="utf-8")
    for entity_id, (_, new_count) in changed.items():
        note = next(load_note(p)[0] for p in repo.glob("entities/*/*.md") if load_note(p)[0].get("id") == entity_id)
        name = re.escape(note["name"])
        index_text = re.sub(
            rf"(- \[[^\]]*{name}[^\]]*\]\([^\)]*\) — )\d+( post(?:s)?)",
            lambda m: f"{m.group(1)}{new_count}{m.group(2)}",
            index_text,
        )
    index_path.write_text(index_text, encoding="utf-8")

    for entity_id, (old_count, new_count) in changed.items():
        print(f"Disambiguated {entity_id}: {old_count} → {new_count} mentions")


if __name__ == "__main__":
    main()
