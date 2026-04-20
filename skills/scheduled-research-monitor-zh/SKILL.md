---
name: scheduled-research-monitor-zh
description: "定时研究监测器：围绕已有文档或给定 topic 理解当前研究方向，按最近一段时间持续检索 arXiv、官方 benchmark 页面、数据集页面、公司官方博客和权威技术来源，生成中文增量证据摘要与待更新候选项。适合 recurring research、自动化巡检和新证据跟踪时调用。"
---

## Hermes 适配说明
- 本 skill 现面向 Hermes 使用，优先依赖 Hermes 原生工具：`search_files`、`read_file`、`write_file`、`patch`、`session_search`、`delegate_task`、`cronjob`、`browser`、`web/search`、`vision`。
- 若正文提到 `references/...` 或 `scripts/...`，优先读取当前 skill 目录下对应文件，不再依赖 Claude 专属目录结构。
- 原始 Claude `agents/openai.yaml` 不作为执行前提；需要并行研究、分工精读或角色评审时，改用 Hermes 的 `delegate_task`。
- 保留原有研究方法论与产物契约，但执行层统一按 Hermes 工具体系落地。

# Scheduled Research Monitor（中文）

这个 skill 适合“持续跟踪一个方向”，尤其适合被 automation 周期性触发。

## 何时使用
- 你已经有一套研究文档，希望每周或每天自动看有没有新论文、新 benchmark、新官方信号。
- 你只有一个 topic，也希望持续搜集近一段时间的新资料。
- 你想先得到增量证据摘要，再决定是否更新主知识库。

## 输入
- `topic` 或 `existing_docs[]`
- `recency_window`: 默认最近 `7-14` 天；也可按周、双周或月度
- `source_policy`: 默认 `arXiv + 官方页面 + 权威技术博客`
- `update_mode`
  - `digest_only`
  - `draft_update_candidates`
  - `handoff_to_kb_updater`

## 输出
- `monitoring_digest`
- `delta_evidence_map`
- `update_candidates`
- `no_update_reasons`（如果没有足够强的新证据）

## 工作流
1. 先用 `brief-ingester-zh` 读取已有文档或笔记，形成当前方向的 `context_brief`。
2. 从已有结论、开放问题、种子来源里抽出监测关键词、子方向和高优先来源。
3. 用 `literature-scout-zh` 对最近窗口内的新论文、benchmark、dataset page、官方博客做增量检索。
4. 去重并与已有知识库比对，避免重复收录旧来源。
5. 对新来源标注：
   - `direct / adjacent / background`
   - `support / contradiction / open gap`
   - `academic / industrial / official`
6. 生成一个“这轮有什么值得更新”的增量摘要，而不是直接改主稿。
7. 只有当新证据达到 [monitoring-runbook.md](references/monitoring-runbook.md) 中定义的更新门槛时，才把结果交给 `knowledge-base-updater-zh`。

## 守护
- 明确写出具体日期，不要用模糊的“最近”替代。
- 没有足够强的新证据时，输出 `no_update_reasons`，不要为了更新而更新。
- 这个 skill 默认产出“增量观察结果”，不直接改知识库正稿。

## 与现有技能的关系
- 方向理解：`brief-ingester-zh`
- 新证据扩展：`literature-scout-zh`
- 深读高价值来源：`paper-reader-zh`
- 审核是否足够强：`paper-critic-zh`
- 真正落库：`knowledge-base-updater-zh`

## 资源
- 监测运行手册：`references/monitoring-runbook.md`
