#!/usr/bin/env python3
"""Suggest diagram-worthy sections from a Markdown document."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
BULLET_RE = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+")

KEYWORDS = {
    "architecture": [
        "架构",
        "结构",
        "系统",
        "模块",
        "分层",
        "层",
        "组件",
        "框架",
        "底座",
        "backbone",
        "stack",
        "orchestrator",
        "编排",
        "总图",
    ],
    "flowchart": [
        "流程",
        "步骤",
        "阶段",
        "pipeline",
        "工作流",
        "decision",
        "决策流",
        "闭环",
        "loop",
        "从",
        "到",
        "演进",
        "执行",
        "协议",
    ],
    "sequence": [
        "时序",
        "交互",
        "调用",
        "request",
        "response",
        "authorize",
        "verify",
        "checkout",
        "delegate",
        "授权",
        "验证",
        "回调",
        "往返",
        "轮次",
    ],
    "comparison": [
        "对比",
        "比较",
        "差异",
        "矛盾",
        "优劣",
        "trade-off",
        "vs",
        "versus",
        "学术界",
        "工业界",
        "路径 a",
        "路径 b",
        "双线",
    ],
    "timeline": [
        "演化",
        "timeline",
        "年份",
        "里程碑",
        "迭代",
        "阶段 a",
        "阶段 b",
        "阶段 c",
        "2024",
        "2025",
        "2026",
    ],
    "matrix": [
        "矩阵",
        "象限",
        "二维",
        "维度",
        "能力",
        "风险",
        "价值",
        "可控性",
    ],
}


@dataclass
class Section:
    title: str
    level: int
    line_start: int
    line_end: int
    content: list[str]


def split_sections(text: str) -> list[Section]:
    sections: list[Section] = []
    current_title = "Document"
    current_level = 1
    current_start = 1
    current_lines: list[str] = []

    lines = text.splitlines()
    for idx, line in enumerate(lines, start=1):
        match = HEADING_RE.match(line)
        if match:
            if current_lines:
                sections.append(
                    Section(
                        title=current_title,
                        level=current_level,
                        line_start=current_start,
                        line_end=idx - 1,
                        content=current_lines,
                    )
                )
            current_level = len(match.group(1))
            current_title = match.group(2).strip()
            current_start = idx
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        sections.append(
            Section(
                title=current_title,
                level=current_level,
                line_start=current_start,
                line_end=len(lines),
                content=current_lines,
            )
        )
    return [section for section in sections if "\n".join(section.content).strip()]


def count_hits(text: str, terms: Iterable[str]) -> int:
    lowered = text.lower()
    return sum(lowered.count(term.lower()) for term in terms)


def classify_section(section: Section) -> dict:
    body = "\n".join(section.content)
    lowered = body.lower()
    bullet_count = sum(1 for line in section.content if BULLET_RE.match(line))
    nonempty_lines = [line for line in section.content if line.strip()]
    table_line_count = sum(1 for line in nonempty_lines if line.lstrip().startswith("|"))
    arrow_count = body.count("->") + body.count("=>") + body.count("→")
    year_count = len(re.findall(r"\b20\d{2}\b", body))
    role_term_count = sum(
        lowered.count(term)
        for term in ("user", "agent", "tool", "platform", "merchant", "buyer", "seller")
    )
    title_lowered = section.title.lower()

    counts = {name: count_hits(lowered, terms) for name, terms in KEYWORDS.items()}
    title_counts = {name: count_hits(title_lowered, terms) for name, terms in KEYWORDS.items()}
    for name, value in title_counts.items():
        counts[name] += value * 2
    counts["flowchart"] += arrow_count
    counts["timeline"] += year_count
    counts["comparison"] += 2 if re.search(r"路径\s*[ab]", lowered) else 0
    counts["comparison"] += 1 if "vs" in lowered or "versus" in lowered else 0
    counts["architecture"] += 1 if "总图" in body else 0
    counts["flowchart"] += 1 if bullet_count >= 4 else 0
    counts["architecture"] += 2 if any(term in title_lowered for term in ("总图", "系统", "框架")) else 0
    counts["flowchart"] += 2 if any(term in title_lowered for term in ("流程", "路径", "主线")) else 0
    counts["timeline"] += 2 if any(term in title_lowered for term in ("演化", "时间线", "总览")) else 0
    counts["comparison"] += 2 if any(term in title_lowered for term in ("对比", "双线", "错位", "共振")) else 0
    counts["matrix"] += 2 if any(term in title_lowered for term in ("数据集", "benchmark", "图谱")) else 0

    reasons: list[str] = []
    if bullet_count >= 3:
        reasons.append(f"包含 {bullet_count} 条以上枚举，适合压缩成图")
    if arrow_count:
        reasons.append("出现箭头或显式流转信号")
    if year_count >= 2:
        reasons.append("出现多个年份，适合时间线")
    if table_line_count >= 4:
        reasons.append("包含明显表格结构")

    top_type = max(counts, key=counts.get)
    top_score = counts[top_type]

    if "总图" in title_lowered or ("system" in title_lowered and "decision" in title_lowered):
        top_type = "architecture"
        top_score = counts["architecture"] + 2
    elif "演化" in title_lowered or "时间线" in title_lowered:
        top_type = "timeline"
        top_score = counts["timeline"] + 2
    elif counts["comparison"] >= 3 and counts["comparison"] >= counts[top_type]:
        top_type = "comparison"
        top_score = counts["comparison"]
    elif counts["matrix"] >= 4 and table_line_count >= 4:
        top_type = "matrix"
        top_score = counts["matrix"]
    elif counts["sequence"] >= 3 and role_term_count >= 2:
        top_type = "sequence"
        top_score = counts["sequence"]
    elif counts["timeline"] >= 3:
        top_type = "timeline"
        top_score = counts["timeline"]
    elif counts["architecture"] >= 3 and counts["architecture"] >= counts["flowchart"]:
        top_type = "architecture"
        top_score = counts["architecture"]
    elif counts["flowchart"] >= 3:
        top_type = "flowchart"
        top_score = counts["flowchart"]

    ranked = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    alternates = [name for name, score in ranked if name != top_type and score > 0][:2]

    score = top_score + min(bullet_count, 4) * 0.5
    if section.level <= 2:
        score += 0.5
    if len(body) < 120:
        score -= 1.0
    if nonempty_lines and table_line_count / len(nonempty_lines) > 0.45:
        score -= 2.0
        if any(term in title_lowered for term in ("数据集", "benchmark", "清单")):
            score -= 5.0
    if any(term in title_lowered for term in ("总图", "总览", "主线", "演化", "路径", "结论")):
        score += 1.5

    if counts[top_type] > 0:
        reasons.append(f"关键词更接近 {top_type}")

    evidence = []
    for line in section.content:
        stripped = line.strip()
        if not stripped:
            continue
        if BULLET_RE.match(stripped) or any(term.lower() in stripped.lower() for term in KEYWORDS[top_type]):
            evidence.append(stripped)
        if len(evidence) >= 3:
            break

    if not evidence:
        evidence = [line.strip() for line in section.content if line.strip()][:2]

    priority = "high" if score >= 6 else "medium" if score >= 4 else "low"

    return {
        "section_title": section.title,
        "heading_level": section.level,
        "line_start": section.line_start,
        "line_end": section.line_end,
        "score": round(score, 2),
        "priority": priority,
        "recommended_diagram_type": top_type,
        "alternate_types": alternates,
        "signals": reasons,
        "placement_hint": "insert after heading",
        "evidence": evidence,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Find diagram-worthy sections in a Markdown document.",
    )
    parser.add_argument("path", help="Path to a Markdown or text document")
    parser.add_argument("--top", type=int, default=5, help="Maximum number of suggestions")
    parser.add_argument(
        "--min-score",
        type=float,
        default=3.5,
        help="Minimum score required to keep a suggestion",
    )
    args = parser.parse_args()

    path = Path(args.path).expanduser().resolve()
    if not path.exists():
        print(f"[ERROR] File not found: {path}", file=sys.stderr)
        return 1

    text = path.read_text(encoding="utf-8")
    sections = split_sections(text)
    suggestions = [classify_section(section) for section in sections]
    suggestions = [item for item in suggestions if item["score"] >= args.min_score]
    suggestions.sort(key=lambda item: item["score"], reverse=True)
    suggestions = suggestions[: args.top]

    payload = {
        "path": str(path),
        "candidate_count": len(suggestions),
        "candidates": suggestions,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
