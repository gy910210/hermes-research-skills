#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

TABLE_HEADER_RE = re.compile(r"^\|(.+)\|\s*$")


def inspect_file(path: Path) -> list[dict]:
    findings = []
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    for i, line in enumerate(lines):
        match = TABLE_HEADER_RE.match(line)
        if not match:
            continue
        headers = [part.strip().lower() for part in match.group(1).split("|")]
        if not any(token in " ".join(headers) for token in ("benchmark", "数据集", "dataset")):
            continue
        normalized = " ".join(headers)
        missing = []
        if "release" not in normalized and "发布时间" not in normalized and "release time" not in normalized:
            missing.append("release_time")
        if "source" not in normalized and "来源" not in normalized and "builder" not in normalized:
            missing.append("source_or_builder")
        if "open" not in normalized and "private" not in normalized and "开源" not in normalized and "私有" not in normalized:
            missing.append("open_private_status")
        if missing:
            findings.append({"line": i + 1, "missing_columns": missing, "headers": headers})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Find markdown benchmark tables missing key metadata columns.")
    parser.add_argument("paths", nargs="+", help="Markdown files")
    args = parser.parse_args()

    output = []
    for raw in args.paths:
        path = Path(raw)
        if not path.exists():
            continue
        output.append({"file": str(path), "findings": inspect_file(path)})
    print(json.dumps({"results": output}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
