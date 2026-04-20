# Workflow State Machine

## 状态
- `bootstrap`
  - 目标：理解已有项目、文件角色、版本链与未解问题。
  - 进入条件：给定任何本地资料或旧报告。
  - 退出条件：产出 `context_brief`。
- `scout`
  - 目标：扩展近一年或指定时间窗口的新证据，形成文献与来源地图。
  - 退出条件：产出 `evidence_map`，并标出优先精读项与关键空白。
- `read`
  - 目标：对高价值来源做结构化精读。
  - 退出条件：产出 `paper_notes`。
- `audit`
  - 目标：检查过度推理、证据层级、数据/benchmark/release 风险。
  - 退出条件：产出 `evidence_audit`。
- `synthesize`
  - 目标：按方向、章节或视角重组内容。
  - 退出条件：产出 `synthesis_packet`。
- `maintain`
  - 目标：创建新稿、更新索引、补旧版提示、执行跨文档一致性扫描。
  - 退出条件：产出 `maintenance_packet`。
- `diagram`
  - 目标：在结构稳定后补图，不改变原始证据结论。
  - 退出条件：图示增强稿或图示插入计划。

## 场景映射
- 新方向启动：`bootstrap -> scout -> read -> audit -> synthesize -> maintain`
- 已有项目增量扩展：`bootstrap -> scout -> audit -> synthesize -> maintain`
- 专题深挖：`bootstrap -> scout -> read -> audit -> synthesize`
- 主稿成熟化合并：`synthesize -> maintain`
- 图示增强：`diagram`

## 默认出口条件
- 没有 `context_brief`，不要跳过 `bootstrap`。
- 没有证据地图，不进入主稿级综合。
- 没有审校，不把 exploratory 观点写成成熟结论。
- 没有维护步骤，不视为完整交付。

## 阻塞处理
- 如果新证据不足：转为 `open gap` 列表，而不是填充想象性内容。
- 如果来源之间冲突：并列展示，并说明谁是原始来源、谁是综合判断。
- 如果只需局部补充：允许停在专题稿，不强行并回主稿。
