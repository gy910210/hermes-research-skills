---
name: concept-boundary-analyzer-zh
description: "概念边界辨析器：用于比较多个相近但不同层级的概念，区分它们在产品形态、系统技术、能力基座、任务边界、替代关系与互补关系上的差异，并生成中文边界矩阵、分层定义与统一口径。适合“AI 搜 vs Agentic Search vs 生成式 vs 传统搜推”这类容易混淆的分析场景。"
---

## Hermes 适配说明
- 本 skill 现面向 Hermes 使用，优先依赖 Hermes 原生工具：`search_files`、`read_file`、`write_file`、`patch`、`session_search`、`delegate_task`、`cronjob`、`browser`、`web/search`、`vision`。
- 若正文提到 `references/...` 或 `scripts/...`，优先读取当前 skill 目录下对应文件，不再依赖 Claude 专属目录结构。
- 原始 Claude `agents/openai.yaml` 不作为执行前提；需要并行研究、分工精读或角色评审时，改用 Hermes 的 `delegate_task`。
- 保留原有研究方法论与产物契约，但执行层统一按 Hermes 工具体系落地。

# Concept Boundary Analyzer（中文）

这个 skill 适合处理“概念很像，但其实不在一个层级上”的问题。

## 何时使用
- 用户要求辨析两个或多个概念的边界、界限、关系、定位。
- 用户反复在“产品入口 / 技术方案 / 模型能力 / 业务形态”之间跳转，容易混写。
- 需要判断概念之间是 `替代`、`互补`、`上下位` 还是 `并行分工`。

## 输入
- `concepts[]`: 需要比较的概念列表
- `context_files[]`（可选）：已有主稿、专题稿、技术方案、行业观察稿
- `comparison_focus`
  - `产品形态`
  - `技术架构`
  - `任务边界`
  - `用户心智`
  - `工业落地`
  - `替代与互补`

## 输出
- `boundary_packet`
  - `layered_definitions`
  - `boundary_matrix`
  - `substitution_vs_complementarity`
  - `common_confusions`
  - `recommended_canonical_wording`
  - `merge_back_suggestions`

## 工作流
1. 先判断每个概念属于哪一层：
   - 产品/界面层
   - 系统/架构层
   - 能力/模型层
   - 任务/场景层
2. 对每个概念固定工作定义，并标出“它不是什么”。
3. 生成边界矩阵，至少覆盖：
   - 默认输出
   - 默认交互
   - 典型任务
   - 技术中枢
   - 主要 KPI
   - 适用品类/场景
4. 强制回答：
   - 哪些是替代关系？
   - 哪些是互补关系？
   - 哪些只是在不同层级上相交？
5. 标出常见混淆来源，例如：
   - 把产品入口当成技术路线
   - 把生成能力当成完整系统
   - 把复杂任务模式误写成主流默认 UI
6. 输出一版“以后知识库里应该固定怎么写”的统一口径。

## 守护
- 不把“都用了 LLM”当成同一概念。
- 不把“看起来像 chat”误写成“底层已经 agentic”。
- 优先用任务边界和系统职责来分，而不是用营销名称来分。
- 若存在行业报道和内部传闻，只能作为较低证据等级的旁证。

## 推荐配合
- 已有材料摄取：`../brief-ingester-zh/SKILL.md`
- 扩展新证据：`../literature-scout-zh/SKILL.md`
- 稳定写成专题稿：`../research-synthesizer-zh/SKILL.md`
