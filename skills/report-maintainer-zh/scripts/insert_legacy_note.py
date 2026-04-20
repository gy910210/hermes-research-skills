#!/usr/bin/env python3
import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Insert a legacy-version note near the top of a markdown file.")
    parser.add_argument("markdown_file", help="Markdown file to update")
    parser.add_argument("note", help="Note text to insert")
    args = parser.parse_args()

    path = Path(args.markdown_file)
    text = path.read_text(encoding="utf-8")
    note = f"> {args.note}"

    if note in text:
        print("note already exists")
        return 0

    lines = text.splitlines()
    insert_at = 0
    if lines and lines[0].startswith("---"):
        for idx in range(1, len(lines)):
            if lines[idx].startswith("---"):
                insert_at = idx + 1
                break
    elif lines and lines[0].startswith("#"):
        insert_at = 1

    lines.insert(insert_at, note)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(note)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
