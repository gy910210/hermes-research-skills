---
name: brief-ingester-zh
description: "研究上下文摄取器：从本地 PDF、Markdown、笔记、已有报告与索引中抽取主题、术语、种子来源、已有结论、未解问题、文件角色和版本链，生成统一的中文 context_brief。已有研究资料或旧报告时调用。"
---

## Hermes 适配说明
- 本 skill 现面向 Hermes 使用，优先依赖 Hermes 原生工具：`search_files`、`read_file`、`write_file`、`patch`、`session_search`、`delegate_task`、`cronjob`、`browser`、`web/search`、`vision`。
- 若正文提到 `references/...` 或 `scripts/...`，优先读取当前 skill 目录下对应文件，不再依赖 Claude 专属目录结构。
- 原始 Claude `agents/openai.yaml` 不作为执行前提；需要并行研究、分工精读或角色评审时，改用 Hermes 的 `delegate_task`。
- 保留原有研究方法论与产物契约，但执行层统一按 Hermes 工具体系落地。

# Brief Ingester（中文）

## 输入
- `sources[]`: 本地 PDF、Markdown、txt、笔记、索引文件、旧版报告
- `extraction_focus`（可选，默认全选）
  - `概览`
  - `术语表`
  - `种子来源`
  - `已有结论`
  - `未解问题`
  - `文件角色`
  - `版本链`
  - `约束与偏好`
  - `数据与基准`
  - `引用提取`
- `language`: 固定中文

## 输出
- `context_brief`
  - 字段契约见 `../research-orchestrator-zh/references/artifact-contracts.md`

## 工作流
1. 先盘点输入材料的类型与角色：索引、主稿、增量稿、专题稿、附录、图示版或笔记。
2. 对 Markdown 优先抽取目录、标题层级、引文链接与“下一版建议”；对 PDF 优先抽取标题、摘要、目录、结论、参考文献。
3. 归纳当前项目已形成的主线、已有结论与仍未解决的问题。
4. 提取种子论文、关键 benchmark、官方来源与用户偏好的写作/输出习惯。
5. 识别版本链：哪些文件是旧版、哪些是成熟主稿、哪些是增量或专题。
6. 输出统一的 `context_brief`，并尽量为关键事实附文件路径、段落或页码线索。

## 守护
- 不用全文摘录替代摘要；只保留后续研究真正需要的结构化信息。
- 不确定的文件角色要标注 `待确认`，不要强行归类。
- 发现旧文件之间结论冲突时，先记录到 `open_questions`，交给后续审校环节处理。
