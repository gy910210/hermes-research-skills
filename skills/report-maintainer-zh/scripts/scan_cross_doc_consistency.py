#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^(#+)\s+(.*)$", re.MULTILINE)


def scan_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    links = []
    broken_links = []
    for match in LINK_RE.finditer(text):
        target = match.group(1)
        if target.startswith("http://") or target.startswith("https://") or target.startswith("#"):
            continue
        target_path = (path.parent / target).resolve()
        links.append(target)
        if not target_path.exists():
            broken_links.append(target)

    headings = []
    numbering_gaps = []
    for heading in HEADING_RE.finditer(text):
        headings.append(heading.group(2).strip())
    expected = 1
    for heading in headings:
        match = re.match(r"(\d+)\.", heading)
        if match:
            value = int(match.group(1))
            if value != expected:
                numbering_gaps.append({"expected": expected, "found": value, "heading": heading})
                expected = value
            expected += 1

    return {
        "file": str(path),
        "broken_links": broken_links,
        "heading_count": len(headings),
        "numbering_gaps": numbering_gaps,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan markdown files for broken links and heading numbering anomalies.")
    parser.add_argument("paths", nargs="+", help="Markdown files or directories")
    args = parser.parse_args()

    files = []
    for raw in args.paths:
        path = Path(raw)
        if path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
        elif path.exists():
            files.append(path)

    results = [scan_file(path) for path in files]
    print(json.dumps({"results": results}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
