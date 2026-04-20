---
name: report-maintainer-zh
description: "研究文稿维护器：为版本化 Markdown 报告创建新文件、更新索引、给旧版加更新提示、合并专题稿进入成熟主稿，并检查跨文档链接、一致性和 benchmark 元数据缺口。需要把研究结果真正维护成项目文档时调用。"
---

## Hermes 适配说明
- 本 skill 现面向 Hermes 使用，优先依赖 Hermes 原生工具：`search_files`、`read_file`、`write_file`、`patch`、`session_search`、`delegate_task`、`cronjob`、`browser`、`web/search`、`vision`。
- 若正文提到 `references/...` 或 `scripts/...`，优先读取当前 skill 目录下对应文件，不再依赖 Claude 专属目录结构。
- 原始 Claude `agents/openai.yaml` 不作为执行前提；需要并行研究、分工精读或角色评审时，改用 Hermes 的 `delegate_task`。
- 保留原有研究方法论与产物契约，但执行层统一按 Hermes 工具体系落地。

# Report Maintainer（中文）

这个 skill 负责把“研究结果”变成“维护良好的文档项目”。

## 何时使用
- 要生成带日期的新报告文件。
- 要把专题稿或增量稿并回成熟主稿。
- 要更新项目索引、旧版提示或图示版入口。
- 要检查链接、章节编号、版本口径、benchmark 元数据缺口。
- 要扫描 curated repo 页面与支持文档之间的条目遗漏。
- 要统一标题、source、publish date、链接样式。
- 要检查增强版资源页、深度分析稿、机构路线图这类成对文档的一致性。

## 输入
- `index_file`
- `base_report`
- `new_content` 或 `synthesis_packet`
- `version_strategy`：默认新建文件，不覆盖旧稿
- `related_docs[]`

## 输出
- `maintenance_packet`
- 新文件路径建议
- 一致性检查结果

## 工作流
1. 优先运行 `scripts/next_report_name.py` 生成新文件名。
2. 默认创建新文件；只有用户明确要求时才覆盖已有文档。
3. 需要更新索引时，优先运行 `scripts/append_index_entry.py` 生成或插入新入口。
4. 需要给旧版加提示时，优先运行 `scripts/insert_legacy_note.py`。
5. 运行 `scripts/scan_cross_doc_consistency.py` 检查：
   - 断链
   - 旧版口径冲突
   - 章节编号错位
   - 主稿与专题稿结论冲突线索
6. 若文档含 benchmark / dataset 章节，再运行 `scripts/find_benchmark_metadata_gaps.py` 扫描是否缺失 `release time / source / open-private status` 等列或字段。
7. 如果是 curated repo 或阅读地图类文档，额外执行三类维护动作：
   - `catalog_diff_scan`
   - `link_and_title_normalization`
   - `paired_doc_consistency_check`
8. 如果这轮更新涉及概念口径变化，额外执行：
   - `concept_consistency_scan`
   - 检查 preferred term / deprecated term / maturity tag 是否在主稿、专题稿、资源页间一致。

## 守护
- 文档维护默认是保守变更；不大面积重写用户未要求改动的老稿。
- 旧版文件不删除，只加更新提示。
- 扫描脚本的结果是“线索”，人工复核后再写回主稿。
- 对 repo 页面和资源页，优先做差分同步，不做大段风格重写。

## 资源
- 新文件名建议：`scripts/next_report_name.py`
- 索引入口追加：`scripts/append_index_entry.py`
- 旧版更新提示：`scripts/insert_legacy_note.py`
- 跨文档一致性扫描：`scripts/scan_cross_doc_consistency.py`
- benchmark 元数据缺口扫描：`scripts/find_benchmark_metadata_gaps.py`
