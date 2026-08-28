#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

import yaml

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")
CANDIDATE_RE = re.compile(r"\b(?:[A-Z][A-Za-z'’&.-]+(?:\s+|$)){1,5}")

ORG_HINTS = {"Council", "Ltd", "Limited", "Group", "Agency", "Authority", "Committee", "Party", "Trust", "Association", "Company", "Construction", "Homes", "Labour"}
PLACE_HINTS = {"Road", "Street", "Lane", "Park", "Green", "Estate", "House", "Hall", "Centre", "Center", "Market", "Gasworks", "Southall", "Ealing"}
STOP = {
    "Southall Stories", "Read More", "Local Democracy", "United Kingdom", "New Year", "The Council", "The Labour Party",
    "Ealing Labour", "Ealing Council", "Peter Mason", "Julian Bell", "Berkeley Group", "Environment Agency", "Public Health England",
}


def front_matter_and_body(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}, text
    return yaml.safe_load(match.group(1)) or {}, text[match.end():]


def clean_text(text: str) -> str:
    text = MARKDOWN_LINK_RE.sub(r"\1", text)
    text = TAG_RE.sub(" ", text)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"[`*_>#|]", " ", text)
    return re.sub(r"\s+", " ", text)


def classify(name: str) -> str:
    words = set(name.replace("&", " ").split())
    if words & ORG_HINTS:
        return "organisation"
    if words & PLACE_HINTS:
        return "place_or_site"
    if len(name.split()) in (2, 3):
        return "person_or_body"
    return "unknown"


def context(text: str, name: str, radius: int = 120) -> str:
    match = re.search(re.escape(name), text, re.IGNORECASE)
    if not match:
        return ""
    start = max(0, match.start() - radius)
    end = min(len(text), match.end() + radius)
    return text[start:end].strip()


def main() -> None:
    repo = Path.cwd()
    ignore_path = repo / "config/entity-candidate-ignore.txt"
    ignored = {line.strip() for line in ignore_path.read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith("#")} if ignore_path.exists() else set()

    curated_aliases = set()
    for path in repo.glob("entities/*/*.md"):
        meta, _ = front_matter_and_body(path)
        curated_aliases.add(str(meta.get("name") or "").casefold())
        curated_aliases.update(str(a).casefold() for a in (meta.get("aliases") or []))

    occurrences: dict[str, dict] = defaultdict(lambda: {"posts": set(), "dates": [], "contexts": [], "forms": defaultdict(int)})

    for path in sorted(repo.glob("posts/[0-9][0-9][0-9][0-9]/*/*/*.md")):
        meta, body = front_matter_and_body(path)
        rel = path.relative_to(repo).as_posix()
        date = str(meta.get("date") or "")
        text = clean_text(f"{meta.get('title') or ''} {meta.get('summary') or ''} {body}")
        seen = set()
        for raw in CANDIDATE_RE.findall(text):
            name = re.sub(r"\s+", " ", raw).strip(" .,:;!?-\n\t")
            if len(name) < 4 or len(name) > 80 or name in STOP or name in ignored:
                continue
            if name.casefold() in curated_aliases:
                continue
            if name.lower().startswith(("the ", "this ", "that ", "these ", "those ")):
                name = name.split(" ", 1)[1]
            if not name or name.casefold() in curated_aliases or name in ignored:
                continue
            key = name.casefold()
            data = occurrences[key]
            data["posts"].add(rel)
            data["dates"].append(date)
            data["forms"][name] += 1
            if key not in seen and len(data["contexts"]) < 3:
                data["contexts"].append({"post": rel, "snippet": context(text, name)})
            seen.add(key)

    candidates = []
    for key, data in occurrences.items():
        post_count = len(data["posts"])
        if post_count < 2:
            continue
        canonical = sorted(data["forms"].items(), key=lambda kv: (-kv[1], -len(kv[0]), kv[0]))[0][0]
        dates = sorted(d for d in data["dates"] if d)
        score = post_count * 10 + min(sum(data["forms"].values()), 20)
        candidates.append({
            "name": canonical,
            "class_hint": classify(canonical),
            "score": score,
            "post_count": post_count,
            "mention_count": sum(data["forms"].values()),
            "first_mention": dates[0] if dates else None,
            "last_mention": dates[-1] if dates else None,
            "variant_forms": sorted(data["forms"], key=lambda x: (-data["forms"][x], x)),
            "representative_posts": sorted(data["posts"])[:5],
            "contexts": data["contexts"],
            "review_status": "candidate",
        })

    candidates.sort(key=lambda x: (-x["score"], x["name"]))
    out = repo / "generated/entity-candidates.json"
    out.write_text(json.dumps(candidates, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = ["# Entity candidates", "", "Machine-generated review queue. Nothing here is a curated assertion until promoted into `entities/`.", ""]
    for item in candidates[:100]:
        lines += [f"## {item['name']}", "", f"- **Class hint:** {item['class_hint']}", f"- **Posts:** {item['post_count']}", f"- **Mentions:** {item['mention_count']}", f"- **Score:** {item['score']}", f"- **First / last:** {item['first_mention']} / {item['last_mention']}", ""]
        for ctx in item["contexts"][:2]:
            lines.append(f"- `{ctx['post']}` — {ctx['snippet']}")
        lines.append("")
    (repo / "indexes/entity-candidates.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated {len(candidates)} entity candidates")


if __name__ == "__main__":
    main()
