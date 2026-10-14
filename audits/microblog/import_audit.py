#!/usr/bin/env python3
"""Import a verbatim Micro.blog audit CSV without losing per-article occurrences.

Input columns: original_url,affected_post,audit_result
Optional columns: section,notes. Do not infer missing URLs or statuses.
Usage: python3 audits/microblog/import_audit.py input.csv output.csv
"""
import argparse
import csv
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

REQUIRED = {"original_url", "affected_post", "audit_result"}
FIELDS = ["occurrence_id", "original_url", "normalized_url", "affected_post",
          "audit_result", "section", "notes"]

def normalized(url):
    # Lowercase only the host/scheme; keep path/query case and encoding intact.
    p = urlsplit(url.strip())
    if not p.scheme or not p.netloc:
        return url.strip()
    return urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path, p.query, p.fragment))

def import_rows(source):
    with source.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames or not REQUIRED.issubset(reader.fieldnames):
            raise ValueError("Required columns: " + ", ".join(sorted(REQUIRED)))
        rows = []
        for line, row in enumerate(reader, start=2):
            url = (row["original_url"] or "").strip()
            if not url:
                raise ValueError(f"Missing original_url on CSV line {line}")
            rows.append({
                "occurrence_id": f"MB-20261014-{len(rows)+1:05d}",
                "original_url": url,
                "normalized_url": normalized(url),
                "affected_post": (row["affected_post"] or "").strip(),
                "audit_result": (row["audit_result"] or "").strip(),
                "section": (row.get("section") or "").strip(),
                "notes": (row.get("notes") or "").strip(),
            })
    return rows

def write_rows(rows, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    rows = import_rows(args.source)
    write_rows(rows, args.output)
    by_url = defaultdict(list)
    for row in rows:
        by_url[row["normalized_url"]].append(row["occurrence_id"])
    print(f"{len(rows)} occurrences; {len(by_url)} distinct normalized URLs")
    print(f"{sum(len(v)>1 for v in by_url.values())} URLs occur more than once")

if __name__ == "__main__":
    main()
