---
name: doc-diagram-orchestrator-zh
description: "从中文或英文 Markdown/文字稿中识别适合插图的段落，判断应使用结构图、流程图、时序图、对比图、时间线或矩阵图，生成插图计划、绘图规格与正文落位建议。用于长文综述、技术方案、研究笔记、产品文档等需要把纯文字转成可视化内容的场景；当用户要求“给这篇文档补图”“找出哪些地方该画图”“基于当前文稿生成结构图/流程图”时调用。"
---

## Hermes 适配说明
- 本 skill 现面向 Hermes 使用，优先依赖 Hermes 原生工具：`search_files`、`read_file`、`write_file`、`patch`、`session_search`、`delegate_task`、`cronjob`、`browser`、`web/search`、`vision`。
- 若正文提到 `references/...` 或 `scripts/...`，优先读取当前 skill 目录下对应文件，不再依赖 Claude 专属目录结构。
- 原始 Claude `agents/openai.yaml` 不作为执行前提；需要并行研究、分工精读或角色评审时，改用 Hermes 的 `delegate_task`。
- 保留原有研究方法论与产物契约，但执行层统一按 Hermes 工具体系落地。

# Document Diagram Orchestrator（中文）

目标：把纯文字文稿转成“可委派绘图”的结构化任务，而不是直接让绘图器猜全文。

## 输入
- `doc_path` 或原始文稿内容（优先 Markdown）
- `audience`: `"internal"|"external"|"academic"|"exec"`（默认 `academic`）
- `density`: `"light"|"balanced"|"rich"`（默认 `balanced`）
- `preferred_renderer`: drawing skill 名称（可选）
- `max_diagrams`（默认 `3`）

## 输出
- `diagram_slots`: 适合出图的位置列表，含小节、原因、图型、优先级、落位建议
- `diagram_specs`: 可直接委派给 drawing skill 的最小绘图规格
- `edit_plan`: 说明每张图插在何处、如何和上下文衔接

## 工作流
1. 读取文稿并先理解主线，不要一上来就画图。
2. 对 Markdown 文件优先运行 `python3 scripts/find_diagram_slots.py <doc_path> --top <N>` 获取候选出图点。
3. 只保留能显著降低理解成本的位置，默认控制在 `2-4` 张图，不要把每个小节都机械地画出来。
4. 依据 [diagram-selection.md](references/diagram-selection.md) 选择图型。
5. 先冻结事实边界，产出 `diagram_specs`，再进入绘图阶段。
6. 若存在明确的 drawing skill，只把 `diagram_specs` 的最小必要信息委派给它，不要把整篇文稿原样转交。
7. 若不存在 drawing skill，直接输出 Mermaid 作为回退方案。
8. 依据 [output-contract.md](references/output-contract.md) 生成图注、插图位置和正文过渡语。

## 选择图型
- 使用结构图：表达系统组成、分层、模块关系、backbone 与 capability stack。
- 使用流程图：表达阶段、步骤、pipeline、decision flow、从 A 到 B 的演进。
- 使用时序图：表达 user/agent/tool/platform/merchant 之间的交互与往返调用。
- 使用对比图：表达路径 A vs B、学术 vs 工业、优劣与 trade-off。
- 使用时间线：表达年份推进、阶段演化、里程碑变化。
- 使用矩阵图：表达两个维度的交叉，例如能力 x 风险、价值 x 可控性。

## 调用外部 Drawing Skill
- 先完成“分析与编排”，再调用绘图 skill。
- 交给绘图 skill 的内容至少包含：
  - `diagram_type`
  - `goal`
  - `source_evidence`
  - `nodes`
  - `edges` 或 `lanes`
  - `caption`
  - `style_constraints`
- 明确要求绘图 skill 不要补充文中没有的实体、关系或因果。
- 若绘图结果与原文冲突，以原文为准，必要时回退 Mermaid。

## 质量门槛
- 让图减少认知负担，而不是把段落换一种方式重复一遍。
- 让图中每个节点都能在原文找到依据。
- 让单图默认控制在 `5-9` 个核心节点；超过 `12` 个节点时优先拆图。
- 让一张图只表达一个主问题，不要混入结构、流程、对比三种逻辑。
- 在关系不清晰时不要强行出图。

## 常见触发语
- 帮我给这篇综述补几张结构图/流程图
- 看这篇 Markdown 哪些地方适合画图
- 把这一节改成一张系统结构图
- 给这段“学术 vs 工业”的内容做一张对比图

## 资源
- 候选扫描脚本：`scripts/find_diagram_slots.py`
- 图型启发式：`references/diagram-selection.md`
- 输出契约：`references/output-contract.md`
