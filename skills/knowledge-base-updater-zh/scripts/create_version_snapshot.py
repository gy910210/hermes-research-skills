#!/usr/bin/env python3
import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a versioned snapshot copy of a knowledge-base markdown file.")
    parser.add_argument("source_file", help="Source markdown file")
    parser.add_argument("--tag", default="snapshot", help="Tag to append to the new version")
    parser.add_argument("--timestamp", default="", help="Timestamp override, default UTC YYYYMMDD-HHMMSS")
    args = parser.parse_args()

    src = Path(args.source_file)
    stamp = args.timestamp or datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    target = src.with_name(f"{src.stem}_{args.tag}_{stamp}{src.suffix}")
    shutil.copy2(src, target)

    print(
        json.dumps(
            {
                "source_file": str(src),
                "snapshot_file": str(target),
                "tag": args.tag,
                "timestamp": stamp,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
