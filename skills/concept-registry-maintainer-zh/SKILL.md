---
name: concept-registry-maintainer-zh
description: "概念口径维护器：为长期研究项目维护统一术语、概念边界、成熟度标签和跨文档一致性，识别哪些旧定义需要降级、哪些新定义需要并回专题/主稿/资源页。适合在概念不断演化、文档很多、需要统一口径时调用。"
---

## Hermes 适配说明
- 本 skill 现面向 Hermes 使用，优先依赖 Hermes 原生工具：`search_files`、`read_file`、`write_file`、`patch`、`session_search`、`delegate_task`、`cronjob`、`browser`、`web/search`、`vision`。
- 若正文提到 `references/...` 或 `scripts/...`，优先读取当前 skill 目录下对应文件，不再依赖 Claude 专属目录结构。
- 原始 Claude `agents/openai.yaml` 不作为执行前提；需要并行研究、分工精读或角色评审时，改用 Hermes 的 `delegate_task`。
- 保留原有研究方法论与产物契约，但执行层统一按 Hermes 工具体系落地。

# Concept Registry Maintainer（中文）

这个 skill 负责维护“概念注册表”，不是普通的边界辨析。

如果 `concept-boundary-analyzer-zh` 回答的是：
- A 和 B 的边界是什么；
- 这是产品概念、系统概念还是能力概念；

那么本 skill 负责回答：
- 这套定义现在应该怎样固化成长期口径；
- 哪些文档还在使用旧定义；
- 哪些结论应该降级成 hypothesis；
- 哪些概念需要建立 `preferred / deprecated / adjacent` 关系。

## 何时使用
- 你已经完成了一轮概念辨析，想把新定义稳定写进主稿、专题稿、资源页。
- 最近多轮调研后，同一概念在不同文档里出现了不同说法。
- 你担心“主稿、专题稿、awesome 页面、技术方案”之间开始概念漂移。
- 你想给一个方向建立长期可维护的 glossary / concept registry。

## 输入
- `registry_scope`
  - `single_topic`
  - `cross_topic`
- `canonical_docs[]`
  - 当前最想作为“定义基准”的文档
- `related_docs[]`
  - 需要扫描和同步的文档
- `concept_targets[]`
  - 例如：
    - `AI 搜`
    - `Agentic Search`
    - `生成式能力`
    - `生成式搜推路线`
    - `sparse/control token`
    - `sample-level token`
- `maturity_policy`
  - 是否要求给每个概念打 `成熟 / 方向中 / hypothesis / 不建议写满`

## 输出
- `concept_registry`
  - `canonical_definition`
  - `preferred_term`
  - `deprecated_terms[]`
  - `adjacent_terms[]`
  - `maturity_tag`
  - `source_basis`
- `concept_drift_report`
  - 哪些文档仍在使用旧口径
  - 哪些地方把 hypothesis 写成了结论
  - 哪些地方术语未统一
- `sync_recommendations`
  - 该并回哪些文档
  - 该只更新 glossary 还是应该改正文

## 工作流
1. 先读取 `canonical_docs[]`，抽出当前最稳的定义和证据基础。
2. 为每个目标概念建立最小注册条目：
   - `preferred_term`
   - `one-line definition`
   - `layer`
     - 产品层 / 能力层 / 建模层 / 系统层 / 控制层
   - `maturity_tag`
3. 再扫描 `related_docs[]`，识别：
   - 仍在用旧术语的地方
   - 定义冲突
   - 成熟度冲突
   - 结论写满的问题
4. 对每个冲突给出处理建议：
   - `replace`
   - `clarify`
   - `downgrade`
   - `leave_as_historical`
5. 如果主题属于长期主线，建议把注册表同步到：
   - 主稿
   - 相关专题稿
   - 增强版资源页 / awesome 页
   - 技术方案稿

## 守护
- 不把“概念口径统一”误做成“大面积重写文风”。
- 如果新定义证据仍弱，只能注册为 `hypothesis` 或 `working definition`。
- 优先维护 `preferred_term`，不要强行删除历史术语；可保留“旧称/旧用法”。
- 概念注册表不等于结论注册表：定义稳定，不代表方向已经成熟。

## 推荐产出形式
- 一份 `概念注册表`
- 一份 `drift report`
- 一组“哪些文档该同步、同步到什么程度”的建议
