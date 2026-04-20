---
name: paper-explorer-brief-zh
description: "【兼容旧入口】旧的简版文献扩展说明。默认改用 literature-scout-zh，并以 evidence_map 作为正式输出。只有兼容历史调用时才直接使用本 skill。"
---

## Hermes 适配说明
- 本 skill 现面向 Hermes 使用，优先依赖 Hermes 原生工具：`search_files`、`read_file`、`write_file`、`patch`、`session_search`、`delegate_task`、`cronjob`、`browser`、`web/search`、`vision`。
- 若正文提到 `references/...` 或 `scripts/...`，优先读取当前 skill 目录下对应文件，不再依赖 Claude 专属目录结构。
- 原始 Claude `agents/openai.yaml` 不作为执行前提；需要并行研究、分工精读或角色评审时，改用 Hermes 的 `delegate_task`。
- 保留原有研究方法论与产物契约，但执行层统一按 Hermes 工具体系落地。

# Paper Explorer Brief（中文，兼容入口）

这个 skill 仅用于兼容旧提示。新的正式入口是 `literature-scout-zh`。

## 迁移说明
- 旧的“从种子论文扩展”逻辑仍可保留，但必须升级为：
  - 以 `context_brief` 或主题问题为起点
  - 输出 `evidence_map`
  - 标注 `source_type / directness / support-or-contradiction / data status`

## 实际执行
1. 读取 `../literature-scout-zh/SKILL.md`。
2. 如有已有项目资料，先读取 `../brief-ingester-zh/SKILL.md`。
3. 只在需要快速兼容旧调用时保留本 skill 名称。
