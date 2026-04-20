---
name: paper-explorer-zh
description: "【兼容旧入口】旧的文献扩展 skill。默认改用 literature-scout-zh：基于 context_brief 或主题问题扩展论文、benchmark、dataset page 与官方来源，并生成 evidence_map、方向聚类和支持/矛盾线索。只有兼容历史调用时才直接使用本 skill。"
---

## Hermes 适配说明
- 本 skill 现面向 Hermes 使用，优先依赖 Hermes 原生工具：`search_files`、`read_file`、`write_file`、`patch`、`session_search`、`delegate_task`、`cronjob`、`browser`、`web/search`、`vision`。
- 若正文提到 `references/...` 或 `scripts/...`，优先读取当前 skill 目录下对应文件，不再依赖 Claude 专属目录结构。
- 原始 Claude `agents/openai.yaml` 不作为执行前提；需要并行研究、分工精读或角色评审时，改用 Hermes 的 `delegate_task`。
- 保留原有研究方法论与产物契约，但执行层统一按 Hermes 工具体系落地。

# Paper Explorer（中文，兼容入口）

这个 skill 已被 `literature-scout-zh` 取代。若被触发，直接按新 skill 的方式执行，不再维护旧的输入输出约定。

## 迁移规则
- 旧输入 `seed_papers / keywords / year_range` -> 新输入 `context_brief 或主题问题 + time_window`
- 旧输出 `papers / clusters / overview` -> 新输出 `evidence_map / candidate_clusters / priority_reading_queue`

## 实际执行
1. 读取 `../literature-scout-zh/SKILL.md`。
2. 按新 skill 生成 evidence map，而不是只生成论文清单。
3. 明确标注 `direct / adjacent / background` 与 `support / contradiction / open gap`。
