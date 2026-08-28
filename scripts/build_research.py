#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse

import yaml

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
HTTP_RE = re.compile(r"https?://[^\s)\]>'\"]+")


def read_note(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(text)
    if not match:
        raise ValueError(f"Missing YAML front matter: {path}")
    meta = yaml.safe_load(match.group(1)) or {}
    meta["path"] = path.as_posix()
    meta["body"] = text[match.end():].strip()
    return meta


def read_post(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(text)
    if not match:
        raise ValueError(f"Missing YAML front matter: {path}")
    return yaml.safe_load(match.group(1)) or {}, text[match.end():]


def phrase_re(phrase: str) -> re.Pattern[str]:
    return re.compile(rf"(?<![\w]){re.escape(phrase.strip())}(?![\w])", re.IGNORECASE)


def matches(text: str, aliases: list[str]) -> list[str]:
    return [alias for alias in aliases if alias and phrase_re(alias).search(text)]


def slug_from_url(url: str) -> str:
    return urlparse(url).netloc.lower().removeprefix("www.") or "unknown"


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def md_link(path: str, label: str) -> str:
    return f"[{label}](../{path})"


def main() -> None:
    repo = Path.cwd()
    post_paths = sorted(repo.glob("posts/[0-9][0-9][0-9][0-9]/*/*/*.md"))
    entity_paths = sorted(repo.glob("entities/*/*.md"))
    topic_paths = sorted(repo.glob("topics/*.md"))
    source_paths = sorted(repo.glob("sources/**/*.md"))

    entities = [read_note(p.relative_to(repo)) for p in entity_paths]
    topics = [read_note(p.relative_to(repo)) for p in topic_paths]
    curated_sources = [read_note(p.relative_to(repo)) for p in source_paths]
    entity_by_id = {e["id"]: e for e in entities}
    topic_by_id = {t["id"]: t for t in topics}

    rel_path = repo / "relationships/reviewed.yml"
    rel_doc = yaml.safe_load(rel_path.read_text(encoding="utf-8")) if rel_path.exists() else {"relationships": []}
    relationships = rel_doc.get("relationships") or []
    for rel in relationships:
        if rel.get("from") not in entity_by_id or rel.get("to") not in entity_by_id:
            raise ValueError(f"Relationship {rel.get('id')} references unknown entity")
        for evidence in rel.get("evidence") or []:
            if evidence.startswith("posts/") and not (repo / evidence).exists():
                raise ValueError(f"Relationship {rel.get('id')} has missing evidence: {evidence}")

    posts = []
    canonical_lookup: dict[str, str] = {}
    for path in post_paths:
        rel = path.relative_to(repo).as_posix()
        meta, body = read_post(path)
        title = meta.get("title") or path.stem
        date = str(meta.get("date") or "")
        url = str(meta.get("url") or "")
        text = f"{title}\n{meta.get('summary') or ''}\n{body}"
        urls = sorted({u.rstrip(".,;:") for u in HTTP_RE.findall(body)})
        posts.append({"path": rel, "title": title, "date": date, "url": url, "body": body, "text": text, "outbound_links": urls})
        if url:
            canonical_lookup[url.rstrip("/")] = rel
            canonical_lookup[("https://southallstories.uk" + url).rstrip("/")] = rel
            canonical_lookup[("http://southallstories.uk" + url).rstrip("/")] = rel

    entity_mentions: dict[str, list[dict]] = defaultdict(list)
    topic_mentions: dict[str, list[dict]] = defaultdict(list)
    post_entities: dict[str, list[str]] = defaultdict(list)
    post_topics: dict[str, list[str]] = defaultdict(list)
    post_links: dict[str, list[str]] = defaultdict(list)
    post_backlinks: dict[str, list[str]] = defaultdict(list)
    source_urls: dict[str, dict] = {}
    domain_posts: dict[str, set[str]] = defaultdict(set)

    for post in posts:
        rel = post["path"]
        text = post["text"]
        for entity in entities:
            hit = matches(text, [entity.get("name", "")] + list(entity.get("aliases") or []))
            if hit:
                entity_mentions[entity["id"]].append({"path": rel, "title": post["title"], "date": post["date"], "matched_aliases": hit})
                post_entities[rel].append(entity["id"])
        for topic in topics:
            hit = matches(text, [topic.get("name", "")] + list(topic.get("aliases") or []))
            if hit:
                topic_mentions[topic["id"]].append({"path": rel, "title": post["title"], "date": post["date"], "matched_aliases": hit})
                post_topics[rel].append(topic["id"])

        for url in post["outbound_links"]:
            normalized = url.rstrip("/")
            target = canonical_lookup.get(normalized)
            if not target and "southallstories.uk" in normalized:
                target = canonical_lookup.get(urlparse(normalized).path.rstrip("/"))
            if target and target != rel:
                post_links[rel].append(target)
                post_backlinks[target].append(rel)
                continue
            domain = slug_from_url(url)
            domain_posts[domain].add(rel)
            source_urls.setdefault(url, {"url": url, "domain": domain, "posts": []})["posts"].append(rel)

    for mapping in (post_entities, post_topics, post_links, post_backlinks):
        for key in list(mapping):
            mapping[key] = sorted(set(mapping[key]))
    for item in source_urls.values():
        item["posts"] = sorted(set(item["posts"]))

    generated = repo / "generated"
    indexes = repo / "indexes"
    generated.mkdir(exist_ok=True)
    indexes.mkdir(exist_ok=True)

    write_json(generated / "entity-mentions.json", {k: entity_mentions.get(k, []) for k in sorted(entity_by_id)})
    write_json(generated / "topic-mentions.json", {k: topic_mentions.get(k, []) for k in sorted(topic_by_id)})
    write_json(generated / "backlinks.json", {
        "entities": {k: [m["path"] for m in entity_mentions.get(k, [])] for k in sorted(entity_by_id)},
        "topics": {k: [m["path"] for m in topic_mentions.get(k, [])] for k in sorted(topic_by_id)},
        "posts": {p["path"]: post_backlinks.get(p["path"], []) for p in posts},
    })
    write_json(generated / "sources.json", sorted(source_urls.values(), key=lambda x: (x["domain"], x["url"])))
    write_json(generated / "entity-relationships.json", relationships)
    write_json(generated / "curated-sources.json", curated_sources)

    nodes = []
    edges = []
    for post in posts:
        pid = "post:" + post["path"]
        nodes.append({"id": pid, "type": "post", "label": post["title"], "path": post["path"], "date": post["date"]})
        for eid in post_entities.get(post["path"], []):
            edges.append({"source": "entity:" + eid, "target": pid, "type": "mentioned-in", "provenance": "deterministic-alias-match"})
        for tid in post_topics.get(post["path"], []):
            edges.append({"source": "topic:" + tid, "target": pid, "type": "mentioned-in", "provenance": "deterministic-alias-match"})
        for target in post_links.get(post["path"], []):
            edges.append({"source": pid, "target": "post:" + target, "type": "links-to", "provenance": "source-post-link"})
    for entity in entities:
        nodes.append({"id": "entity:" + entity["id"], "type": "entity", "subtype": entity.get("type"), "label": entity.get("name"), "path": entity["path"]})
    for topic in topics:
        nodes.append({"id": "topic:" + topic["id"], "type": "topic", "label": topic.get("name"), "path": topic["path"]})
    for domain, paths in sorted(domain_posts.items()):
        nodes.append({"id": "domain:" + domain, "type": "source-domain", "label": domain, "post_count": len(paths)})
        for rel in sorted(paths):
            edges.append({"source": "post:" + rel, "target": "domain:" + domain, "type": "cites-domain", "provenance": "source-post-link"})

    for rel in relationships:
        edges.append({
            "source": "entity:" + rel["from"], "target": "entity:" + rel["to"], "type": rel["type"],
            "directional": bool(rel.get("directional", True)), "evidence": rel.get("evidence") or [],
            "confidence": rel.get("confidence"), "created_by": rel.get("created_by"), "review_status": rel.get("review_status"),
            "provenance": "reviewed-relationship",
        })

    for source in curated_sources:
        sid = "source:" + source["id"]
        nodes.append({"id": sid, "type": "source-record", "label": source.get("title"), "path": source["path"], "publisher": source.get("publisher"), "source_type": source.get("source_type")})
        for post in source.get("cited_by") or []:
            edges.append({"source": "post:" + post, "target": sid, "type": "cites-source", "provenance": "reviewed-source-record"})
        for eid in source.get("related_entities") or []:
            if eid not in entity_by_id:
                raise ValueError(f"Source {source['id']} references unknown entity {eid}")
            edges.append({"source": sid, "target": "entity:" + eid, "type": "relates-to", "provenance": "reviewed-source-record"})
        for tid in source.get("related_topics") or []:
            if tid not in topic_by_id:
                raise ValueError(f"Source {source['id']} references unknown topic {tid}")
            edges.append({"source": sid, "target": "topic:" + tid, "type": "relates-to", "provenance": "reviewed-source-record"})

    write_json(generated / "graph.json", {"nodes": nodes, "edges": edges})

    entity_lines = ["# Entity index", "", "Curated entities with generated mention counts.", ""]
    by_type: dict[str, list[dict]] = defaultdict(list)
    for entity in entities:
        by_type[entity.get("type", "other")].append(entity)
    for kind in sorted(by_type):
        entity_lines += [f"## {kind.title()}", ""]
        for entity in sorted(by_type[kind], key=lambda x: x.get("name", "")):
            count = len(entity_mentions.get(entity["id"], []))
            entity_lines.append(f"- {md_link(entity['path'], entity['name'])} — {count} post{'s' if count != 1 else ''}")
        entity_lines.append("")
    (indexes / "entities.md").write_text("\n".join(entity_lines), encoding="utf-8")

    topic_lines = ["# Topic index", "", "Curated topics with generated mention counts.", ""]
    for topic in sorted(topics, key=lambda x: x.get("name", "")):
        count = len(topic_mentions.get(topic["id"], []))
        topic_lines.append(f"- {md_link(topic['path'], topic['name'])} — {count} post{'s' if count != 1 else ''}")
    topic_lines.append("")
    (indexes / "topics.md").write_text("\n".join(topic_lines), encoding="utf-8")

    domain_lines = ["# Source graph", "", "Outbound source domains ranked by the number of Southall Stories posts citing them.", ""]
    for domain, paths in sorted(domain_posts.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        domain_lines.append(f"- **{domain}** — {len(paths)} post{'s' if len(paths) != 1 else ''}")
    domain_lines.append("")
    (indexes / "source-graph.md").write_text("\n".join(domain_lines), encoding="utf-8")

    relationship_lines = ["# Reviewed entity relationships", "", "Curated edges with explicit evidence. These are assertions, not co-occurrence.", ""]
    for rel in relationships:
        relationship_lines += [f"## {entity_by_id[rel['from']]['name']} → {entity_by_id[rel['to']]['name']}", "", f"- **Type:** `{rel['type']}`", f"- **Confidence:** {rel.get('confidence')}", f"- **Review:** {rel.get('review_status')}", "- **Evidence:**"]
        relationship_lines += [f"  - `{e}`" for e in rel.get("evidence") or []]
        if rel.get("note"):
            relationship_lines.append(f"- **Note:** {rel['note']}")
        relationship_lines.append("")
    (indexes / "relationships.md").write_text("\n".join(relationship_lines), encoding="utf-8")

    source_lines = ["# Curated source records", "", "High-value primary or authoritative evidence promoted from raw outbound links.", ""]
    for source in sorted(curated_sources, key=lambda s: (s.get("publisher", ""), s.get("title", ""))):
        source_lines += [f"## {source['title']}", "", f"- **ID:** `{source['id']}`", f"- **Publisher:** {source.get('publisher')}", f"- **Type:** `{source.get('source_type')}`", f"- **URL:** {source.get('canonical_url')}", f"- **Cited by:** {len(source.get('cited_by') or [])} post(s)", ""]
    (indexes / "source-records.md").write_text("\n".join(source_lines), encoding="utf-8")

    backlink_lines = ["# Backlinks", "", "Generated reverse links between posts plus entity/topic mention counts.", "", "## Posts with the most internal backlinks", ""]
    ranked = sorted(((p, len(post_backlinks.get(p, []))) for p in (x["path"] for x in posts)), key=lambda x: (-x[1], x[0]))
    title_by_path = {p["path"]: p["title"] for p in posts}
    for path, count in ranked:
        if count:
            backlink_lines.append(f"- [{title_by_path[path]}](../{path}) — {count}")
    backlink_lines += ["", "## Most-mentioned entities", ""]
    for eid, mentions in sorted(entity_mentions.items(), key=lambda kv: (-len(kv[1]), entity_by_id[kv[0]]["name"])):
        backlink_lines.append(f"- **{entity_by_id[eid]['name']}** — {len(mentions)}")
    backlink_lines += ["", "## Most-mentioned topics", ""]
    for tid, mentions in sorted(topic_mentions.items(), key=lambda kv: (-len(kv[1]), topic_by_id[kv[0]]["name"])):
        backlink_lines.append(f"- **{topic_by_id[tid]['name']}** — {len(mentions)}")
    backlink_lines.append("")
    (indexes / "backlinks.md").write_text("\n".join(backlink_lines), encoding="utf-8")

    summary = {
        "posts": len(posts), "entities": len(entities), "topics": len(topics), "curated_sources": len(curated_sources),
        "reviewed_relationships": len(relationships), "entity_mentions": sum(len(v) for v in entity_mentions.values()),
        "topic_mentions": sum(len(v) for v in topic_mentions.values()), "internal_post_links": sum(len(v) for v in post_links.values()),
        "source_urls": len(source_urls), "source_domains": len(domain_posts), "graph_nodes": len(nodes), "graph_edges": len(edges),
    }
    write_json(generated / "research-summary.json", summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
