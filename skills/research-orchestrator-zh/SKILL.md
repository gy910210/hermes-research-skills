---
name: research-orchestrator-zh
description: "研究总编排入口：为新方向启动、已有报告增量扩展、专题深挖、概念边界辨析、概念注册表同步、survey 到技术方案转换、repo 页面维护、机构路线图拆解、critical thinking 报告、methodology/样本流深挖与主稿成熟化合并选择合适的中文研究工作流，并串联 brief-ingester、literature-scout、paper-reader、paper-critic、concept-boundary-analyzer、concept-registry-maintainer-zh、awesome-repo-maintainer-zh、critical-iteration-lab-zh、methodology-sample-flow-extractor-zh、research-synthesizer、role-review-panel、report-maintainer 与可选图示技能。需要把多轮调研工作流做成可复用链路时调用。"
---

## Hermes 适配说明
- 本 skill 现面向 Hermes 使用，优先依赖 Hermes 原生工具：`search_files`、`read_file`、`write_file`、`patch`、`session_search`、`delegate_task`、`cronjob`、`browser`、`web/search`、`vision`。
- 若正文提到 `references/...` 或 `scripts/...`，优先读取当前 skill 目录下对应文件，不再依赖 Claude 专属目录结构。
- 原始 Claude `agents/openai.yaml` 不作为执行前提；需要并行研究、分工精读或角色评审时，改用 Hermes 的 `delegate_task`。
- 保留原有研究方法论与产物契约，但执行层统一按 Hermes 工具体系落地。

# Research Orchestrator（中文）

这是研究项目的推荐入口 skill。它不替代子技能，而是负责判断当前任务属于哪种研究场景、加载哪些约束、以及每一步应该产出什么中间件。

## 何时使用
- 用户要从 `brief / notes / 现有报告` 启动一个新研究方向。
- 用户要在已有项目上继续扩展证据、补充空白、探索边界。
- 用户要把多个专题稿合并回成熟主稿，并控制版本与一致性。
- 用户要围绕一个子方向做深挖，但希望结果能回接主稿。
- 用户要把一次性调研扩展成周期性监测与知识库维护闭环。
- 用户要维护 `awesome-*.md`、repo README 或长列表资源页。
- 用户要按机构路线而不是技术树梳理一个方向。
- 用户要对一个方向做三轮以上批判性迭代。
- 用户要把新概念并回多份文档，统一长期口径。
- 用户要专门抽取 methodology、样本流、prompt/template 和 loss 设计。

## 默认原则
- 默认中文输出。
- 默认把结果落盘成 Markdown 文件，而不是只停留在对话里。
- 学术问题优先论文、benchmark、dataset page；产业问题优先官方页面与权威技术博客。
- 明确区分 `直接证据`、`邻近证据`、`综合判断`。
- 默认维护项目索引与版本链；非用户要求时不覆盖旧稿。

## 输入
- `research_goal`: 当前轮研究目标
- `existing_files[]`: 已有报告、笔记、PDF、Markdown、表格或索引（可为空）
- `time_window`: 年份或时间范围（可选）
- `deliverable_type`: `"增量稿"|"专题稿"|"方向比较稿"|"双视角稿"|"成熟主稿"|"图示增强"|"awesome_page"|"institution_roadmap"|"critical_iteration_report"|"route_family_comparison"`
- `domain_profile`: 默认为自动判断；电商搜推购物决策类优先加载 `agentic-commerce-research-profile-zh`

## 输出
- `research_agenda`
- `selected_workflow`
- `required_artifacts`
- `handoff_notes`

## 快速分流
1. `新方向启动`
   - 调用链：`brief-ingester-zh -> literature-scout-zh -> paper-reader-zh -> paper-critic-zh -> research-synthesizer-zh -> report-maintainer-zh`
2. `已有报告增量扩展`
   - 调用链：`brief-ingester-zh -> literature-scout-zh -> paper-critic-zh -> research-synthesizer-zh -> report-maintainer-zh`
3. `专题深挖`
   - 调用链：`brief-ingester-zh -> literature-scout-zh -> paper-reader-zh -> paper-critic-zh -> research-synthesizer-zh`
4. `主稿成熟化合并`
   - 调用链：`research-synthesizer-zh -> report-maintainer-zh`
5. `图示增强`
   - 只在主稿结构稳定后调用 `doc-diagram-orchestrator-zh`
6. `持续监测与落库`
   - 调用链：`scheduled-research-monitor-zh -> knowledge-base-updater-zh`
7. `概念边界辨析`
   - 调用链：`brief-ingester-zh -> concept-boundary-analyzer-zh -> research-synthesizer-zh -> report-maintainer-zh`
8. `survey -> 技术方案`
   - 调用链：`brief-ingester-zh -> literature-scout-zh -> paper-reader-zh -> paper-critic-zh -> research-synthesizer-zh -> role-review-panel-zh -> report-maintainer-zh`
9. `repo-curation-sync`
   - 调用链：`brief-ingester-zh -> literature-scout-zh -> awesome-repo-maintainer-zh -> research-synthesizer-zh -> report-maintainer-zh`
10. `institution-roadmap`
   - 调用链：`brief-ingester-zh -> literature-scout-zh -> paper-reader-zh -> paper-critic-zh -> critical-iteration-lab-zh -> research-synthesizer-zh -> report-maintainer-zh`
11. `critical-iteration-report`
   - 调用链：`brief-ingester-zh -> literature-scout-zh -> paper-reader-zh -> paper-critic-zh -> critical-iteration-lab-zh -> research-synthesizer-zh`

## 工作流
1. 先读取已有材料，明确项目现状，而不是直接搜索。
2. 基于目标与已有材料产出 `research_agenda`。
3. 依据 [workflow-state-machine.md](references/workflow-state-machine.md) 选择阶段与出口条件。
4. 依据 [artifact-contracts.md](references/artifact-contracts.md) 约束每个子技能的输入输出。
5. 依据 [evidence-discipline.md](references/evidence-discipline.md) 审核措辞与证据等级。
6. 依据 [source-tiering.md](references/source-tiering.md) 决定优先搜索哪些来源。
7. 若是电商购物决策相关主题，再加载 `../agentic-commerce-research-profile-zh/references/domain-profile-agentic-commerce.md` 获取领域结构、benchmark 检查项与常见专题模板。
8. 如果任务是 recurring research，优先把“监测”和“落库”拆成两个阶段，不直接让定时任务改主稿。
9. 只有在章节与结论稳定后，才进入图示阶段。
10. 若任务本质上是在分辨概念、框定边界或固定统一口径，优先走 `concept-boundary-analyzer-zh`，不要直接跳进长篇文献堆叠。
11. 若任务本质上是把研究判断落成技术蓝图或路线图，优先在成稿后走 `role-review-panel-zh` 做多职责交叉收敛。
12. 若任务本质上是维护 curated repo 页面，优先走 `awesome-repo-maintainer-zh`，不要把 repo README 当成熟主稿来更新。
13. 若任务本质上是多轮 critical thinking，优先走 `critical-iteration-lab-zh`，不要只靠 `paper-critic-zh` 做单轮结论审校。
14. 若任务本质上是统一长期定义、清理概念漂移、把 hypothesis 和成熟结论分开，优先走 `concept-registry-maintainer-zh`。
15. 若任务本质上是深挖训练方式、样本流、prompt/template、stagewise training，优先走 `methodology-sample-flow-extractor-zh`，不要只用通用 paper notes 兜底。

## 调度守则
- 能通过已有上下文判断的，不先问用户。
- 不把单篇摘要堆成综述；综合稿按方向与章节组织。
- 如果证据不足，保留为 `待验证假设` 或 `下一版建议`，不要写成成熟结论。
- 发现旧文档和新证据冲突时，以最新可核的原始来源为准，并把冲突记录到维护环节。

## 资源
- 状态机：`references/workflow-state-machine.md`
- 中间产物契约：`references/artifact-contracts.md`
- 证据纪律：`references/evidence-discipline.md`
- 来源分层：`references/source-tiering.md`
- 报告类型：`references/report-types.md`

## Hermes 强执行协议

当这个 skill 被调用时，不要只做“路线建议”。要按下面的执行顺序真正落地：

1. 先用 `read_file` / `search_files` 读取用户已有材料，而不是先联网。
2. 如用户提到“以前做过”“之前有稿子”，先用 `session_search` 回忆历史会话。
3. 产出一个明确的 `selected_workflow`，只能从本文“快速分流”里选一个主流程；若是复合任务，写出主流程 + 次流程。
4. 明确列出本轮必须生成的工件文件名，优先用 Markdown：
   - `context_brief.md`
   - `evidence_map.md`
   - `paper_notes_*.md`
   - `evidence_audit.md`
   - `synthesis_packet.md`
   - `report_*.md`
5. 需要并行精读、分工检索或多角色评审时，使用 `delegate_task`，不要依赖 Claude agent 配置文件。
6. 真正需要持续监测时，使用 `cronjob` 创建自包含任务；cron prompt 必须写清输入文档路径、时间窗口、输出路径，不能依赖当前对话上下文。
7. 需要写入文件时，用 `write_file` 或 `patch`；先写新稿，再决定是否合并进旧稿，默认不覆盖旧稿。

## Hermes 推荐编排模板

建议按下面的最小编排推进：

- 第 1 步：读取现有材料，生成 `research_agenda`
- 第 2 步：调用 `literature-scout-zh` 生成 `evidence_map`
- 第 3 步：挑选高价值来源，调用 `paper-reader-zh` 精读
- 第 4 步：必要时调用 `paper-critic-zh` 做证据审校
- 第 5 步：调用 `research-synthesizer-zh` 产出结构化文稿
- 第 6 步：若用户要落库/并回主稿，再调用 `report-maintainer-zh` 或 `knowledge-base-updater-zh`

## 停止条件

满足以下条件之一才能结束当前轮：

- 已明确 `selected_workflow`
- 已生成或更新至少一个可交付 Markdown 工件
- 已说明下一步该调用哪个子 skill，以及为什么
- 若证据不足，已明确记录为 `待验证假设` / `open question`
