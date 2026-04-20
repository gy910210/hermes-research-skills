---
name: paper-reader-zh
description: "结构化精读取证器：对论文、官方博客、benchmark 页面、数据集页面或 PDF 执行精读，抽取问题、方法/系统、数据与实验、显式结论、来源、时间和复用价值，生成可直接支撑主稿写作的中文 paper_notes。需要高价值来源精读时调用。"
---

## Hermes 适配说明
- 本 skill 现面向 Hermes 使用，优先依赖 Hermes 原生工具：`search_files`、`read_file`、`write_file`、`patch`、`session_search`、`delegate_task`、`cronjob`、`browser`、`web/search`、`vision`。
- 若正文提到 `references/...` 或 `scripts/...`，优先读取当前 skill 目录下对应文件，不再依赖 Claude 专属目录结构。
- 原始 Claude `agents/openai.yaml` 不作为执行前提；需要并行研究、分工精读或角色评审时，改用 Hermes 的 `delegate_task`。
- 保留原有研究方法论与产物契约，但执行层统一按 Hermes 工具体系落地。

# Paper Reader（中文）

## 输入
- `sources[]`: 论文、官方博客、benchmark 页面、dataset page、PDF
- `depth`: `"concise"|"full"`（默认 `concise`）

## 输出
- `paper_notes`
  - 字段契约见 `../research-orchestrator-zh/references/artifact-contracts.md`

## 步骤
1. 明确来源类型：论文、官方博客、benchmark 页面、dataset page 或其他。
2. 记录 `publication_time`、`venue_or_source`、`institution_or_company`；无法确认时标明未披露。
3. 抽取问题设定、任务类型、方法/系统结构、关键数据集与 benchmark。
4. 只记录来源明确写出的结论与结果，整理为 `explicit_claims[]` 与 `results[]`。
5. 对论文记录训练设置、评测协议、消融与失败案例；对官方页面记录产品能力边界与未披露项。
6. 补充 `reusable_for_sections[]`，说明这些内容最适合回写到哪些综述章节。
7. 如果论文明显属于“方法/训练样本流密集型”论文，额外抽取：
   - `raw_data_objects`
   - `token_objects`
   - `stagewise_training`
   - `public_prompt_or_template_evidence`
   - `disclosed_vs_undisclosed_ratios`

## 守护
- 明确区分“来源显式陈述”和“阅读者推断”。
- 引用要带页码、章节、段落或 URL 线索。
- 对 benchmark、release 状态、数据规模、是否开源等硬事实，优先保守。
- 对 prompt/template、样本比例、过滤阈值、sampling 规则尤其保守；没看到正文/附录原文就不要写满。

## Hermes 强执行协议

调用这个 skill 时要真正完成“精读记录”：

1. 先判断来源类型：本地 PDF、本地 Markdown、网页、官方博客、benchmark 页面、dataset page。
2. 本地文件优先：
   - Markdown / txt 用 `read_file`
   - PDF 优先走 OCR/文档提取相关能力，再进入精读
3. 网页优先使用 `web/search` + 抽取；页面结构复杂时再用 `browser`。
4. 输出不能只是一段摘要，必须整理成结构化 `paper_notes`。
5. 每条核心结论都尽量带出处线索：页码、章节名、表格号、URL、小节标题。
6. 若用户给了多篇来源且内容较长，使用 `delegate_task` 分篇精读，再在主线程合并结果。

## 推荐的 paper_notes 结构

建议至少包含：

- `source_type`
- `title`
- `publication_time`
- `venue_or_source`
- `institution_or_company`
- `problem_statement`
- `task_type`
- `method_or_system`
- `datasets_and_benchmarks`
- `explicit_claims`
- `results`
- `limitations_or_undisclosed_items`
- `reusable_for_sections`

若是方法/训练样本流密集型论文，再补：

- `raw_data_objects`
- `token_objects`
- `stagewise_training`
- `public_prompt_or_template_evidence`
- `disclosed_vs_undisclosed_ratios`

## 停止条件

满足以下条件之一才算完成：

- 已为至少一个高价值来源生成可复用的 `paper_notes`
- 已给出明确可引用的结论与出处线索
- 已明确指出哪些事实仍未披露或只能保守表述
