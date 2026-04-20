---
name: methodology-sample-flow-extractor-zh
description: "方法与样本流抽取器：专门从论文、附录、官方页面中抽取训练方式、样本流、任务阶段、prompt/template、loss 栈、披露比例和工业结果，生成可比较的方法卡与样本流对照表。适合深挖生成式搜推、训练数据构造、methodology 例子集和实验设计模板时调用。"
---

## Hermes 适配说明
- 本 skill 现面向 Hermes 使用，优先依赖 Hermes 原生工具：`search_files`、`read_file`、`write_file`、`patch`、`session_search`、`delegate_task`、`cronjob`、`browser`、`web/search`、`vision`。
- 若正文提到 `references/...` 或 `scripts/...`，优先读取当前 skill 目录下对应文件，不再依赖 Claude 专属目录结构。
- 原始 Claude `agents/openai.yaml` 不作为执行前提；需要并行研究、分工精读或角色评审时，改用 Hermes 的 `delegate_task`。
- 保留原有研究方法论与产物契约，但执行层统一按 Hermes 工具体系落地。

# Methodology Sample Flow Extractor（中文）

这个 skill 负责抽取“方法怎么做”，尤其是：
- 训练样本怎么构造；
- 分几个阶段；
- 哪些是公开 prompt / template；
- 哪些比例和规则公开了，哪些没有。

它不是普通 `paper-reader-zh` 的替代，而是一个更偏“实验与实现结构”的专用抽取器。

## 何时使用
- 你要做“训练方式 / 样本流”专题。
- 你想把多篇论文的 methodology 放到统一模板里比较。
- 你想知道论文有没有公开 prompt、appendix template、task mixture、sample ratio。
- 你想产出方法例子集、实验设计模板、样本构造路线图。

## 输入
- `sources[]`
  - 论文、PDF、appendix、官方技术页
- `focus`
  - `sample_flow`
  - `public_prompt_evidence`
  - `loss_stack`
  - `stagewise_training`
  - `industrial_result_mapping`
- `granularity`
  - `paper_card`
  - `comparison_table`
  - `execution_template`

## 输出
- `methodology_packet`
  - `task_and_scene`
  - `raw_data_objects`
  - `token_objects`
  - `stagewise_sample_flow`
  - `training_targets`
  - `loss_stack`
  - `public_prompt_evidence`
  - `disclosed_ratios`
  - `undisclosed_gaps`
  - `industrial_results`
- `method_comparison_rows[]`
- `illustrative_examples[]`

## 工作流
1. 先判断论文属于哪一类：
   - tokenizer / SID
   - generative retrieval/search
   - recommendation backbone
   - reranking / control
   - training system / serving
2. 优先抽“对象定义”，再抽“怎么训练”：
   - raw tables / raw logs
   - sample object
   - token object
   - list object
3. 再按阶段抽取：
   - `Stage A` tokenizer / SID
   - `Stage B` backbone supervision
   - `Stage C` alignment / preference
   - `Stage D` online refresh / serving coupling
4. 识别是否存在公开 prompt / template：
   - 正文里的 instruction 示例
   - appendix 表格里的 prompt template
   - figure / pseudo-template
5. 把没有公开的地方显式记成：
   - `未披露`
   - `摘要级可知`
   - `appendix 可知`
6. 如果用户要求例子集，可在论文支持范围外补 `illustrative example`，但必须明确标注为示意，不得冒充论文原文。

## 守护
- 不把“方法直觉”写成“论文披露的实现细节”。
- 对 prompt/template 尤其保守：只有公开正文/附录稳定可见时，才记为公开证据。
- 对 ratio、filtering threshold、sampling policy，只要没看到原文，就写 `未披露`。
- 对工业收益，不做跨论文强行横比；只记录论文公开写出的结果。

## 推荐产出形式
- 单篇 methodology 卡
- 样本流对照表
- prompt 证据表
- 可执行实验设计模板
