#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse

import yaml

SCHEMA_VERSION = 1
BASE_URL = "https://southallstories.uk"
FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^\s)]+)\)")
HTML_LINK_RE = re.compile(r'<a\s+[^>]*href=["\'](https?://[^"\']+)["\'][^>]*>(.*?)</a>', re.IGNORECASE | re.DOTALL)
HTML_TAG_RE = re.compile(r"<[^>]+>")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_note(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(text)
    if not match:
        raise ValueError(f"Missing YAML front matter: {path}")
    return yaml.safe_load(match.group(1)) or {}


def absolute_post_url(url: str) -> str:
    if not url:
        return ""
    if url.startswith("http://") or url.startswith("https://"):
        return url
    return BASE_URL + (url if url.startswith("/") else "/" + url)


def typed(kind: str, value) -> str:
    return f"{kind}:{value}"


def ensure_unique(items: list[dict], label: str) -> set[str]:
    ids = [item["id"] for item in items]
    if len(ids) != len(set(ids)):
        raise ValueError(f"Duplicate {label} IDs in Commons export")
    return set(ids)


def clean_link_label(value: str) -> str:
    value = HTML_TAG_RE.sub("", value)
    value = re.sub(r"[*_`]+", "", value)
    return re.sub(r"\s+", " ", value).strip()


def article_citations(repo: Path, post_id_by_path: dict[str, str]) -> list[dict]:
    citations: list[dict] = []
    for path, post_id in sorted(post_id_by_path.items()):
        text = (repo / path).read_text(encoding="utf-8")
        body_match = FRONT_MATTER_RE.match(text)
        body = text[body_match.end():] if body_match else text
        found: list[tuple[str, str]] = []
        found.extend((clean_link_label(label), url) for label, url in MARKDOWN_LINK_RE.findall(body))
        found.extend((clean_link_label(label), url) for url, label in HTML_LINK_RE.findall(body))
        seen: set[str] = set()
        for label, url in found:
            url = url.rstrip(".,;:")
            parsed = urlparse(url)
            domain = (parsed.hostname or "").lower().removeprefix("www.")
            if not domain or domain == "southallstories.uk" or url in seen:
                continue
            seen.add(url)
            citations.append({
                "post": post_id,
                "label": label or domain,
                "url": url,
                "domain": domain,
                "provenance": "source-post-link",
            })
    return citations


def validate_export(data: dict) -> None:
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("Unexpected Commons schema version")

    entity_ids = ensure_unique(data["entities"], "entity")
    topic_ids = ensure_unique(data["topics"], "topic")
    post_ids = ensure_unique(data["posts"], "post")
    source_ids = ensure_unique(data["sources"], "source")
    ensure_unique(data["relationships"], "relationship")
    evidence_ids = post_ids | source_ids

    for rel in data["relationships"]:
        if rel["from"] not in entity_ids or rel["to"] not in entity_ids:
            raise ValueError(f"Relationship {rel['id']} has an unknown endpoint")
        if rel.get("review_status") != "reviewed":
            raise ValueError(f"Relationship {rel['id']} is not reviewed")
        for evidence in rel.get("evidence", []):
            if evidence["id"] not in evidence_ids:
                raise ValueError(f"Relationship {rel['id']} has unknown evidence {evidence['id']}")

    for source in data["sources"]:
        if source.get("review_status") != "reviewed":
            raise ValueError(f"Source {source['id']} is not reviewed")
        for ref in source.get("cited_by", []):
            if ref not in post_ids:
                raise ValueError(f"Source {source['id']} cites unknown post {ref}")
        for ref in source.get("related_entities", []):
            if ref not in entity_ids:
                raise ValueError(f"Source {source['id']} references unknown entity {ref}")
        for ref in source.get("related_topics", []):
            if ref not in topic_ids:
                raise ValueError(f"Source {source['id']} references unknown topic {ref}")

    for citation in data.get("citations", []):
        if citation.get("post") not in post_ids:
            raise ValueError(f"Citation references unknown post: {citation}")
        if citation.get("provenance") != "source-post-link":
            raise ValueError(f"Citation has invalid provenance: {citation}")

    for edge in data["links"]:
        if edge["source"].startswith("entity:") and edge["source"] not in entity_ids:
            raise ValueError(f"Link has unknown entity source: {edge}")
        if edge["source"].startswith("topic:") and edge["source"] not in topic_ids:
            raise ValueError(f"Link has unknown topic source: {edge}")
        if edge["source"].startswith("post:") and edge["source"] not in post_ids:
            raise ValueError(f"Link has unknown post source: {edge}")
        if edge["target"].startswith("post:") and edge["target"] not in post_ids:
            raise ValueError(f"Link has unknown post target: {edge}")


def main() -> None:
    repo = Path.cwd()
    generated = repo / "generated"

    posts_raw = load_json(generated / "posts.json")
    mentions_entities = load_json(generated / "entity-mentions.json")
    mentions_topics = load_json(generated / "topic-mentions.json")
    backlinks = load_json(generated / "backlinks.json")
    relationships_raw = load_json(generated / "entity-relationships.json")

    entity_notes = [load_note(p) for p in sorted(repo.glob("entities/*/*.md"))]
    topic_notes = [load_note(p) for p in sorted(repo.glob("topics/*.md"))]
    source_note_paths = sorted(repo.glob("sources/**/*.md"))
    source_notes = [(p.relative_to(repo).as_posix(), load_note(p)) for p in source_note_paths]

    post_id_by_path: dict[str, str] = {}
    posts = []
    for post in posts_raw:
        stable = post.get("post_id") or post["path"]
        public_id = typed("post", stable)
        post_id_by_path[post["path"]] = public_id
        posts.append({
            "id": public_id,
            "title": post.get("title"),
            "summary": post.get("summary"),
            "date": post.get("date"),
            "lastmod": post.get("lastmod"),
            "url": absolute_post_url(post.get("url") or ""),
            "categories": post.get("categories") or [],
            "sha256": post.get("sha256"),
            "provenance": "southall-stories-corpus",
        })

    entities = []
    for note in entity_notes:
        entities.append({
            "id": typed("entity", note["id"]),
            "name": note.get("name"),
            "type": note.get("type"),
            "aliases": note.get("aliases") or [],
            "description": note.get("description"),
            "review_status": "reviewed",
            "provenance": "curated-entity",
        })

    topics = []
    for note in topic_notes:
        topics.append({
            "id": typed("topic", note["id"]),
            "name": note.get("name"),
            "aliases": note.get("aliases") or [],
            "review_status": "reviewed",
            "provenance": "curated-topic",
        })

    source_id_by_path = {path: typed("source", note["id"]) for path, note in source_notes}
    sources = []
    for _, source in source_notes:
        cited_by = []
        for post_path in source.get("cited_by") or []:
            if post_path not in post_id_by_path:
                raise ValueError(f"Curated source {source['id']} cites unknown corpus post {post_path}")
            cited_by.append(post_id_by_path[post_path])
        sources.append({
            "id": typed("source", source["id"]),
            "title": source.get("title"),
            "publisher": source.get("publisher"),
            "source_type": source.get("source_type"),
            "canonical_url": source.get("canonical_url"),
            "archive_urls": source.get("archive_urls") or [],
            "publication_date": source.get("publication_date"),
            "meeting_date": source.get("meeting_date"),
            "cited_by": cited_by,
            "related_entities": [typed("entity", e) for e in source.get("related_entities") or []],
            "related_topics": [typed("topic", t) for t in source.get("related_topics") or []],
            "review_status": source.get("review_status"),
            "temporal_status": source.get("temporal_status"),
            "provenance": "reviewed-source-record",
        })

    relationships = []
    for rel in relationships_raw:
        evidence = []
        for path in rel.get("evidence") or []:
            if path in post_id_by_path:
                evidence.append({"id": post_id_by_path[path]})
            elif path in source_id_by_path:
                evidence.append({"id": source_id_by_path[path]})
            else:
                raise ValueError(f"Commons relationship evidence is neither a corpus post nor curated source: {path}")
        relationships.append({
            "id": typed("relationship", rel["id"]),
            "from": typed("entity", rel["from"]),
            "to": typed("entity", rel["to"]),
            "type": rel["type"],
            "directional": bool(rel.get("directional", True)),
            "evidence": evidence,
            "confidence": rel.get("confidence"),
            "created_by": rel.get("created_by"),
            "review_status": rel.get("review_status"),
            "valid_from": rel.get("valid_from"),
            "valid_to": rel.get("valid_to"),
            "note": rel.get("note"),
            "provenance": "reviewed-relationship",
        })

    links = []
    for entity_id, mentions in sorted(mentions_entities.items()):
        for mention in mentions:
            links.append({"source": typed("entity", entity_id), "target": post_id_by_path[mention["path"]], "type": "mentioned-in", "provenance": "deterministic-alias-match"})
    for topic_id, mentions in sorted(mentions_topics.items()):
        for mention in mentions:
            links.append({"source": typed("topic", topic_id), "target": post_id_by_path[mention["path"]], "type": "mentioned-in", "provenance": "deterministic-alias-match"})
    for target_path, source_paths in sorted((backlinks.get("posts") or {}).items()):
        for source_path in source_paths:
            links.append({"source": post_id_by_path[source_path], "target": post_id_by_path[target_path], "type": "links-to", "provenance": "source-post-link"})

    citations = article_citations(repo, post_id_by_path)

    data = {
        "schema_version": SCHEMA_VERSION,
        "export_name": "Southall-Zettel Civic Commons Export",
        "publisher": "Southall-Zettel",
        "canonical_corpus": "https://southallstories.uk",
        "policy": {
            "candidates_exported": False,
            "raw_source_urls_exported": False,
            "article_citations_exported": True,
            "full_post_text_exported": False,
            "reviewed_relationships_only": True,
        },
        "counts": {
            "entities": len(entities),
            "topics": len(topics),
            "posts": len(posts),
            "relationships": len(relationships),
            "sources": len(sources),
            "citations": len(citations),
            "links": len(links),
        },
        "entities": sorted(entities, key=lambda x: x["id"]),
        "topics": sorted(topics, key=lambda x: x["id"]),
        "posts": sorted(posts, key=lambda x: x["id"]),
        "relationships": sorted(relationships, key=lambda x: x["id"]),
        "sources": sorted(sources, key=lambda x: x["id"]),
        "citations": sorted(citations, key=lambda x: (x["post"], x["url"])),
        "links": sorted(links, key=lambda x: (x["source"], x["target"], x["type"])),
    }

    validate_export(data)
    (generated / "commons.json").write_text(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")

    print(
        "Commons export v1: "
        f"{len(entities)} entities, {len(topics)} topics, {len(posts)} posts, "
        f"{len(relationships)} relationships, {len(sources)} sources, "
        f"{len(citations)} article citations, {len(links)} links"
    )


if __name__ == "__main__":
    main()
