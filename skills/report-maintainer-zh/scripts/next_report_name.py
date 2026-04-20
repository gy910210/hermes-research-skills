#!/usr/bin/env python3
import argparse
import json
from datetime import date
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Suggest a versioned markdown report filename.")
    parser.add_argument("base_report", help="Existing report path or report title")
    parser.add_argument("--suffix", default="", help="Optional suffix to append before the date")
    parser.add_argument("--date", dest="date_value", default=date.today().isoformat(), help="Date in YYYY-MM-DD")
    args = parser.parse_args()

    base = Path(args.base_report)
    parent = base.parent if base.suffix else Path(".")
    stem = base.stem if base.suffix else args.base_report
    suffix = f"_{args.suffix}" if args.suffix else ""
    target = parent / f"{stem}{suffix}_{args.date_value}.md"

    print(
        json.dumps(
            {
                "base_report": str(base),
                "suggested_path": str(target),
                "date": args.date_value,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
