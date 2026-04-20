#!/usr/bin/env python3
import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Append a markdown link entry to an index file if missing.")
    parser.add_argument("index_file", help="Markdown index file")
    parser.add_argument("label", help="Link label")
    parser.add_argument("target", help="Target path or URL")
    parser.add_argument("--section-header", default="", help="Optional section header to insert under")
    args = parser.parse_args()

    index_path = Path(args.index_file)
    text = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    entry = f"- [{args.label}]({args.target})"

    if entry in text:
        print("entry already exists")
        return 0

    if args.section_header and args.section_header in text:
        anchor = text.index(args.section_header) + len(args.section_header)
        new_text = text[:anchor] + "\n" + entry + text[anchor:]
    else:
        if text and not text.endswith("\n"):
            text += "\n"
        new_text = text + entry + "\n"

    index_path.write_text(new_text, encoding="utf-8")
    print(entry)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
