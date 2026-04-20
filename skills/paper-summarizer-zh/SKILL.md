---
name: paper-summarizer-zh
description: "轻摘要器：把单篇来源或单组 reading_notes 转成精炼中文摘要、一句话结论和要点卡片，适合快速传播或做卡片库；不负责长综述综合与章节重构。需要快速单篇摘要时调用。"
---

## Hermes 适配说明
- 本 skill 现面向 Hermes 使用，优先依赖 Hermes 原生工具：`search_files`、`read_file`、`write_file`、`patch`、`session_search`、`delegate_task`、`cronjob`、`browser`、`web/search`、`vision`。
- 若正文提到 `references/...` 或 `scripts/...`，优先读取当前 skill 目录下对应文件，不再依赖 Claude 专属目录结构。
- 原始 Claude `agents/openai.yaml` 不作为执行前提；需要并行研究、分工精读或角色评审时，改用 Hermes 的 `delegate_task`。
- 保留原有研究方法论与产物契约，但执行层统一按 Hermes 工具体系落地。

# Paper Summarizer（中文）

## 输入
- `reading_notes` 或 `papers` 元信息
- `style`: `"简洁"|"详细"`（默认 `简洁`）
- `bullets`: 每篇要点数（默认 `5`）

## 输出（中文）
- `summaries`
  - `one_sentence_summary`
  - `key_points`
  - `contributions`
  - `limitations`
  - `tags`
  - `suggested_followups`

## 步骤
1. 将阅读笔记转为“一句话摘要+要点”。
2. 标注贡献、创新点与局限。
3. 给出后续阅读或实验建议。
4. 保持用词一致与中文表述。

## 边界
- 需要跨文献比较、方向重构、主稿合并时，改用 `research-synthesizer-zh`。
