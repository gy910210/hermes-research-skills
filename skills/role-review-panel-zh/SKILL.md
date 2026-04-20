---
name: role-review-panel-zh
description: "多职责评审面板：围绕同一份方案或文稿，模拟架构、产品、算法、工程等不同职责视角进行中文审查、互相提问、多轮讨论与收敛，输出分歧点、取舍与修订动作。适合技术方案评审、路线图收敛与复杂研究判断。"
---

## Hermes 适配说明
- 本 skill 现面向 Hermes 使用，优先依赖 Hermes 原生工具：`search_files`、`read_file`、`write_file`、`patch`、`session_search`、`delegate_task`、`cronjob`、`browser`、`web/search`、`vision`。
- 若正文提到 `references/...` 或 `scripts/...`，优先读取当前 skill 目录下对应文件，不再依赖 Claude 专属目录结构。
- 原始 Claude `agents/openai.yaml` 不作为执行前提；需要并行研究、分工精读或角色评审时，改用 Hermes 的 `delegate_task`。
- 保留原有研究方法论与产物契约，但执行层统一按 Hermes 工具体系落地。

# Role Review Panel（中文）

这个 skill 适合把“一个人的单线分析”升级成“多职责交叉审查后的方案”。

## 何时使用
- 用户要从架构、产品、算法、工程等多个角色同时审查一个方案。
- 用户明确要求“让不同 agent 互相提问、互相讨论、再收敛”。
- 需要把 survey 继续推进成技术方案、阶段路线图或模块设计。

## 输入
- `target_doc` 或 `plan_summary`
- `roles[]`
  - 默认：`架构 / 产品 / 算法 / 工程`
- `review_focus`
  - `完整性`
  - `可落地性`
  - `阶段优先级`
  - `延迟与成本`
  - `数据与评测`
  - `风险与边界`
- `rounds`: 默认 `2-3`

## 输出
- `role_review_packet`
  - `role_findings`
  - `cross_questions`
  - `consensus_points`
  - `core_disagreements`
  - `decision_log`
  - `revision_actions`

## 工作流
1. 先让每个角色独立审查目标文稿，避免一开始就互相污染判断。
2. 每个角色至少回答：
   - 这份方案最强的部分是什么？
   - 最大风险是什么？
   - 最希望别的角色回答什么问题？
3. 组织 `2-3` 轮交叉提问：
   - 架构问产品：目标是否过宽、阶段是否过重
   - 产品问算法：哪些能力现在并不成熟
   - 算法问工程：哪些链路没有观测与评测基础
   - 工程问架构：模块边界、SLA、降级策略是否清楚
4. 收敛为三类结果：
   - 一致意见
   - 关键分歧
   - 最终取舍
5. 输出可以直接回写文稿的 `revision_actions`，而不是只给会议纪要。

## 守护
- 角色讨论要服务于方案收敛，不是表演式辩论。
- 不同角色的批评要落到可修改项，而不是抽象反对。
- 若角色之间分歧无法消除，必须给出默认取舍原则。
- 讨论结果最终要反映到文稿结构、阶段优先级或模块边界上。

## 推荐配合
- survey 转技术方案：`../research-synthesizer-zh/SKILL.md`
- 主稿或方案维护：`../report-maintainer-zh/SKILL.md`
- 证据与措辞审校：`../paper-critic-zh/SKILL.md`
