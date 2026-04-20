---
name: critical-iteration-lab-zh
description: "批判性迭代实验室：把一组论文或一个方向拉入多轮 idea 碰撞、支持与矛盾拆解、关键假设反推、失败模式审查与 family-level 综合，输出 critical_rounds、stable_findings 与 new_questions。需要做三轮以上 critical thinking 或路线级反思时调用。"
---

## Hermes 适配说明
- 本 skill 现面向 Hermes 使用，优先依赖 Hermes 原生工具：`search_files`、`read_file`、`write_file`、`patch`、`session_search`、`delegate_task`、`cronjob`、`browser`、`web/search`、`vision`。
- 若正文提到 `references/...` 或 `scripts/...`，优先读取当前 skill 目录下对应文件，不再依赖 Claude 专属目录结构。
- 原始 Claude `agents/openai.yaml` 不作为执行前提；需要并行研究、分工精读或角色评审时，改用 Hermes 的 `delegate_task`。
- 保留原有研究方法论与产物契约，但执行层统一按 Hermes 工具体系落地。

# Critical Iteration Lab（中文）

这个 skill 负责做“多轮批判性迭代”，不是普通审稿，也不是简单综述。

## 何时使用
- 用户明确要求“至少三轮以上 critical thinking”。
- 想让不同论文的核心 idea 互相碰撞。
- 想把一个方向从“摘要堆叠”升级成“稳定 finding + 潜在问题 + 下一轮问题”。
- 想从单篇论文比较，提升到 family-level / institution-level synthesis。

## 输入
- `evidence_map`
- `paper_notes`
- `evidence_audit`
- `iteration_depth`
  - 默认 `6`
- `focus`
  - `idea_collision`
  - `assumption_stress_test`
  - `benefit_source_analysis`
  - `family_route_synthesis`

## 输出
- `critical_rounds`
  - `round_name`
  - `question`
  - `supporting_papers[]`
  - `conflicting_papers[]`
  - `interim_judgment`
- `collision_matrix`
- `stable_findings[]`
- `unstable_claims[]`
- `new_questions[]`

## 标准六轮
1. `按作者叙事整理`
   - 先接受论文自己的 framing，避免一上来过度反驳。
2. `支持与矛盾碰撞`
   - 让论文之间直接对照：谁支持谁，谁在挑战谁。
3. `关键假设拆解`
   - 找出每条路线的核心前提，检查它是否被数据/场景/系统条件限制。
4. `收益来源反推`
   - 判断收益到底来自 tokenizer、样本、loss、serving、reward 还是业务控制。
5. `失败模式与不可扩展点`
   - 梳理 latency、bias、benchmark gap、组织依赖、场景迁移风险。
6. `family-level / institution-level synthesis`
   - 从单论文上升到路线族、机构族或业务族的综合判断。

## 工作流
1. 先从 `paper_notes` 里抽核心假设，而不是只抽结果。
2. 每一轮都必须区分：
   - 来源直接支持的内容
   - 本轮综合判断
   - 仍待验证的问题
3. 如果某个判断依赖机构公开路线或业务场景差异，明确写出“这属于 family-level synthesis”。
4. 输出时优先保留：
   - 稳定 finding
   - 最强反证
   - 最值得继续追的新问题

## 守护
- 不把“更多轮数”误写成“更深的结论”。
- 轮次之间要递进，不要六轮都只是换说法复述。
- 证据不够时，把结论降级成 `hypothesis` 或 `route-level observation`。
- 如果机构公开证据稀疏，明确标“公开线索较薄”，不要强写完整路线。

## 推荐产出形式
- 多轮批判性报告
- idea collision 矩阵
- 最稳 finding 与最不稳 claim 列表
