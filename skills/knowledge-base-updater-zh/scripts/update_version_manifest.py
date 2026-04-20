#!/usr/bin/env python3
import argparse
from datetime import datetime
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Append a version entry to a markdown manifest.")
    parser.add_argument("manifest_file", help="Markdown manifest/changelog path")
    parser.add_argument("--version-note", required=True, help="Short reason for the update")
    parser.add_argument("--updated-file", action="append", default=[], help="Updated file path; may be repeated")
    parser.add_argument("--new-version", action="append", default=[], help="New version file path; may be repeated")
    parser.add_argument("--source-summary", default="", help="Short summary of the new evidence")
    parser.add_argument("--timestamp", default="", help="Timestamp override, default local ISO format")
    args = parser.parse_args()

    manifest = Path(args.manifest_file)
    timestamp = args.timestamp or datetime.now().isoformat(timespec="minutes")

    lines = []
    if manifest.exists():
        lines = manifest.read_text(encoding="utf-8").splitlines()
    elif not lines:
        lines = ["# Knowledge Base Version Manifest", ""]

    entry = [f"## {timestamp}", f"- 更新说明：{args.version_note}"]
    if args.source_summary:
        entry.append(f"- 新证据摘要：{args.source_summary}")
    for item in args.updated_file:
        entry.append(f"- 更新文件：{item}")
    for item in args.new_version:
        entry.append(f"- 新版本：{item}")
    entry.append("")

    if lines and lines[-1] != "":
        lines.append("")
    lines.extend(entry)
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(entry))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
