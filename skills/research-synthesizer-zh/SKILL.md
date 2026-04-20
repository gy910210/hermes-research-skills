---
name: research-synthesizer-zh
description: "跨文献综合器：把 evidence_map、paper_notes 与 evidence_audit 组织成中文章节、专题稿、方向比较稿、双视角稿或成熟主稿小节，强调按方向写作而不是按论文堆摘要。需要把证据整理成可交付文稿时调用。"
---

## Hermes 适配说明
- 本 skill 现面向 Hermes 使用，优先依赖 Hermes 原生工具：`search_files`、`read_file`、`write_file`、`patch`、`session_search`、`delegate_task`、`cronjob`、`browser`、`web/search`、`vision`。
- 若正文提到 `references/...` 或 `scripts/...`，优先读取当前 skill 目录下对应文件，不再依赖 Claude 专属目录结构。
- 原始 Claude `agents/openai.yaml` 不作为执行前提；需要并行研究、分工精读或角色评审时，改用 Hermes 的 `delegate_task`。
- 保留原有研究方法论与产物契约，但执行层统一按 Hermes 工具体系落地。

# Research Synthesizer（中文）

这个 skill 负责把前面的素材变成“像综述或专题稿的成品结构”。

## 何时使用
- 需要写增量稿、专题稿、方向比较稿、双视角稿、成熟主稿章节。
- 需要把支持与矛盾、学术与工业、主线与潜力方向组织成一篇连贯文稿。

## 输入
- `context_brief`
- `evidence_map`
- `paper_notes`（可选但强烈推荐）
- `evidence_audit`
- `target_output_type`
  - `awesome_page`
  - `institution_roadmap`
  - `critical_iteration_report`
  - `route_family_comparison`

## 输出
- `synthesis_packet`
  - `section_outline`
  - `evidence_backed_claims`
  - `support_vs_contradiction`
  - `new_angles`
  - `merge_ready_sections`
  - `keep_as_exploratory`

## 工作流
1. 依据 [../research-orchestrator-zh/references/report-types.md](../research-orchestrator-zh/references/report-types.md) 选择适合的成文结构。
2. 先定章节主线，再把来源放进去；不要反过来按论文流水账写作。
3. 将结论拆成三层：
   - 来源直接支持的结论
   - 来自多个来源的综合判断
   - 下一版值得追的新角度或待验证假设
4. 在每个方向内都尝试回答：
   - 大家共同支持什么观点？
   - 关键矛盾点在哪里？
   - 哪些内容已经足够成熟，可以并回主稿？
   - 哪些内容更适合单独保留为专题或建议？
5. 需要领域模板时，加载 `../agentic-commerce-research-profile-zh/references/domain-profile-agentic-commerce.md`。
6. 如果 `target_output_type=awesome_page`，优先组织成：
   - 阅读地图
   - 问题地图
   - 方向地图
   - 高价值新增条目
7. 如果 `target_output_type=institution_roadmap` 或 `route_family_comparison`，优先组织成：
   - 机构线/平台线
   - 业务表面
   - 技术重心
   - 最强证据
   - 当前短板
8. 如果 `target_output_type=critical_iteration_report`，优先保留轮次递进，而不是压平写成普通综述。

## 守护
- 章节之间要有过渡，不要把增量稿直接拼起来。
- 不因为结构完整就掩盖证据不足；证据不足时明确标成 `open question` 或 `hypothesis`。
- 对 benchmark、数据集、release 状态等硬事实，优先保守表述。
- 不把 repo 页面和深度分析稿写成同一风格：前者偏 catalog，后者偏判断。

## Hermes 强执行协议

调用这个 skill 时，目标是产出“可交付文稿骨架或正文”，不是只给提纲建议：

1. 先读取已有 `context_brief`、`evidence_map`、`paper_notes`、`evidence_audit`。
2. 明确本轮目标文稿类型：
   - 增量稿
   - 专题稿
   - 方向比较稿
   - 双视角稿
   - 成熟主稿章节
   - `awesome_page`
   - `institution_roadmap`
   - `critical_iteration_report`
   - `route_family_comparison`
3. 先定章节主线，再写每节的核心判断与证据支撑。
4. 对每个章节，至少区分三类内容：
   - 直接证据支持的结论
   - 综合判断
   - open question / hypothesis
5. 若素材很多，可用 `delegate_task` 让子代理分别起草不同章节，但主线程必须统一口径、去重和过渡。
6. 完成后优先写成 `synthesis_packet.md` 或具体文稿文件，而不是只保留在聊天回复里。

## 推荐输出骨架

建议输出中至少有：

- `section_outline`
- `evidence_backed_claims`
- `support_vs_contradiction`
- `new_angles`
- `merge_ready_sections`
- `keep_as_exploratory`

如果用户直接要成稿，建议按 Markdown 生成：

- 标题
- 摘要 / 本轮增量说明
- 章节正文
- 支持与矛盾
- 未决问题
- 下一步建议

## 质量门槛

- 不按论文顺序流水账写作
- 至少有一处明确处理“支持 vs 矛盾”
- 至少标出一处 `open question` 或 `hypothesis`（如果证据不足）
- 章节之间有过渡句，而不是素材拼接
