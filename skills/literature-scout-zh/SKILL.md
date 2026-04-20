---
name: literature-scout-zh
description: "文献与证据扩展器：基于 context_brief 或主题问题检索近一年或指定时间窗口的新论文、benchmark、dataset page、官方博客与权威技术来源，生成中文 evidence_map、方向聚类、支持与矛盾线索。需要扩展资料、补证据、找边界或更新文献库时调用。"
---

## Hermes 适配说明
- 本 skill 现面向 Hermes 使用，优先依赖 Hermes 原生工具：`search_files`、`read_file`、`write_file`、`patch`、`session_search`、`delegate_task`、`cronjob`、`browser`、`web/search`、`vision`。
- 若正文提到 `references/...` 或 `scripts/...`，优先读取当前 skill 目录下对应文件，不再依赖 Claude 专属目录结构。
- 原始 Claude `agents/openai.yaml` 不作为执行前提；需要并行研究、分工精读或角色评审时，改用 Hermes 的 `delegate_task`。
- 保留原有研究方法论与产物契约，但执行层统一按 Hermes 工具体系落地。

# Literature Scout（中文）

这个 skill 负责“扩展检索 + 证据地图”，不是单篇精读器。

## 何时使用
- 已有 brief 或旧报告，需要继续找新论文和新证据。
- 要围绕一个子方向做近一年检索。
- 要找支持证据、反例、benchmark、数据集 release 状态或产业官方信号。

## 输入
- `context_brief` 或主题问题
- `time_window`：优先最近一年；若用户指定则按指定范围
- `result_budget`：默认只保留高价值结果
- `source_mix`：`academic / industrial / official` 的偏好
- `search_mode`
  - `fresh_scan`
  - `institution_line`
  - `citation_neighborhood`
  - `diff_against_catalog`
  - `bridge_line`
  - `artifact_hunt`

## 输出
- `evidence_map`
- `candidate_clusters`
- `support_vs_contradiction_seeds`
- `priority_reading_queue`
- `missing_from_catalog`
- `institution_clusters`
- `citation_frontier`
- `route_family_candidates`

## 工作流
1. 先从 `context_brief` 提取方向、术语、已有结论与未解问题。
2. 按 [../research-orchestrator-zh/references/source-tiering.md](../research-orchestrator-zh/references/source-tiering.md) 选择来源优先级。
3. 每条结果都要标注：
   - `direct / adjacent / background`
   - `academic / industrial / official`
   - `public benchmark / private data / unknown release`
   - `support / contradiction / open gap`
4. 去重后按方向聚类，而不是只给一长串论文。
5. 优先输出“为什么值得继续读”的队列：哪些能直接改主稿，哪些更适合作为旁证或潜力方向。
6. 若主题属于电商搜推购物决策类，加载 `../agentic-commerce-research-profile-zh/references/domain-profile-agentic-commerce.md` 对齐领域 taxonomy 与 benchmark 检查项。
7. 如果 `search_mode=diff_against_catalog`，额外读取现有 `awesome-*.md` 或 curated repo 页面，识别：
   - 支持文档里有但 catalog 里没有
   - 同一论文是否已被重复收录
   - 哪些新条目只够做 watchlist
8. 如果 `search_mode=institution_line`，优先按机构/平台/团队聚类输出，而不是只按技术树输出。
9. 如果 `search_mode=citation_neighborhood`，优先围绕核心种子论文的引用邻域和同机构家族继续扩展。
10. 如果 `search_mode=bridge_line`，优先找“概念桥接”论文：它们不一定是主线核心论文，但能解释两个研究家族之间的结构关系。
11. 如果 `search_mode=artifact_hunt`，优先寻找附录、prompt template、训练表格、数据构造细节、ratio 披露和公开示例，而不只找新论文标题。

## 守护
- 不把搜索结果列表冒充成综合结论。
- 不因为“新”就高优先；优先级看与主题的直接性、来源可靠性与复用价值。
- 数据集、benchmark、release 状态没有明确来源时标 `unknown`。

## 推荐产出形式
- 一个按方向聚类的证据表
- 一个 `support / contradiction / gap` 视角的小结
- 一个“下一步优先精读清单”
- 一个 `catalog diff` 或 `institution roadmap seed`（按场景可选）

## Hermes 强执行协议

调用这个 skill 时，默认执行而不是只解释方法：

1. 如果用户给了本地 brief / 旧稿 / 笔记，先用 `read_file` 读取；如果是目录，用 `search_files` 找候选文档。
2. 如果用户只给了主题问题，没有材料，先把主题拆成：核心术语、机构词、benchmark 词、数据集词、应用词。
3. 联网检索优先使用 Hermes 的 `web/search` 能力；需要打开动态页面或截图时再用 `browser`。
4. 搜到来源后，不要停在链接列表，必须整理成去重后的 `evidence_map`。
5. 输出里至少包含这些字段：
   - 标题 / 来源
   - 时间
   - 类型（academic / industrial / official）
   - 证据距离（direct / adjacent / background）
   - 作用（support / contradiction / open gap）
   - 为什么值得继续读
6. 若结果很多，优先保留高价值前 N 条，并把其余来源归入 watchlist。
7. 若用户要深入，挑 3-8 个高价值来源交给 `paper-reader-zh`，必要时用 `delegate_task` 并行精读。

## Hermes 输出落地建议

优先把结果写成 Markdown，而不是散落在对话里。推荐文件结构：

- `evidence_map.md`
- `priority_reading_queue.md`
- `catalog_diff.md`（仅在 `diff_against_catalog` 时）
- `institution_clusters.md`（仅在 `institution_line` 时）

## 质量门槛

- 至少完成一次去重和聚类
- 至少区分支持证据与矛盾证据
- 至少给出一个“下一步优先精读清单”
- 没有可靠日期、release 状态或 benchmark 来源时，明确标记 `unknown`
