---
name: knowledge-base-updater-zh
description: "知识库更新器：读取已有知识库文档与新加入的支持材料，判断哪些信息应该追加、修正、合并或暂缓，并在默认不覆盖旧稿的前提下执行版本化更新、记录变更和维护索引。需要把新证据稳妥并回知识库时调用。"
---

## Hermes 适配说明
- 本 skill 现面向 Hermes 使用，优先依赖 Hermes 原生工具：`search_files`、`read_file`、`write_file`、`patch`、`session_search`、`delegate_task`、`cronjob`、`browser`、`web/search`、`vision`。
- 若正文提到 `references/...` 或 `scripts/...`，优先读取当前 skill 目录下对应文件，不再依赖 Claude 专属目录结构。
- 原始 Claude `agents/openai.yaml` 不作为执行前提；需要并行研究、分工精读或角色评审时，改用 Hermes 的 `delegate_task`。
- 保留原有研究方法论与产物契约，但执行层统一按 Hermes 工具体系落地。

# Knowledge Base Updater（中文）

这个 skill 负责把“新的支持材料”稳妥并回“已有知识库”，并且默认带版本控制。

## 何时使用
- `scheduled-research-monitor-zh` 发现了值得吸收的新证据。
- 你手动收集了一批新论文、新 blog、新 benchmark，想把它们并回现有知识库。
- 你想统一更新主稿、专题稿、索引和版本记录。

## 输入
- `knowledge_base_files[]`: 主稿、专题稿、索引、附录、基准表、知识卡片库
- `support_materials[]`: 新的论文笔记、增量摘要、官方页面、benchmark 信息
- `update_scope`
  - `append`
  - `refine`
  - `merge`
  - `version_only`
- `version_note`: 这次为什么更新

## 输出
- `kb_update_packet`
  - `update_summary`
  - `changed_files`
  - `new_version_paths`
  - `manifest_updates`
  - `unresolved_conflicts`

## 工作流
1. 先用 `brief-ingester-zh` 理解现有知识库结构、文件角色与版本链。
2. 读取新的支持材料，必要时用 `paper-reader-zh` 和 `paper-critic-zh` 做精读与审校。
3. 判断这批新材料属于哪种更新：
   - 新增证据
   - 修正旧结论
   - 补 benchmark / dataset 元数据
   - 只值得进入“下一版建议”
4. 先判断目标文档的角色，再决定怎么更新：
   - `项目总索引 / 工作台`：只更新入口、状态、文件地图、待办和专题入口
   - `成熟主稿 / canonical report`：只吸收证据足够稳、会改变主结论或明显补强章节的内容
   - `专题稿`：允许吸收边界分析、潜力方向和局部细化
   - `技术方案稿`：优先吸收会改变阶段、模块边界、SLA、评测或数据准备的内容
   - `awesome_repo`：优先补齐遗漏条目、source/date/一句话说明与章节归类，不写长段分析
   - `reading_map / route_map`：允许保留阅读路径、问题地图、机构路线和潜力方向
   - `analysis_pair`：把资源页和深度分析稿视为成对文档，优先保持条目与核心口径同步
   - `concept_registry`：优先维护 preferred term、边界、成熟度和跨文档统一口径
   - `methodology_notebook`：优先维护训练方式、样本流、prompt/template 和披露缺口
5. 依据 `references/versioning-policy.md` 先创建版本快照，再更新知识库。
6. 默认调用 `report-maintainer-zh` 的维护动作：新建版本、更新索引、补旧版提示、检查一致性。
7. 更新版本清单与变更说明，确保以后能追溯“哪一轮引入了哪些证据”。

## 守护
- 默认不覆盖旧版知识库。
- 没有足够证据时，不把新材料硬并回主稿。
- 新证据和综合判断要分开写入。
- 如果新旧材料冲突，先记录到 `unresolved_conflicts`，再决定是否重写主结论。
- 不同角色的文档不要用同一标准更新：工作台负责管理过程，主稿负责沉淀结论，专题稿负责保留探索。
- 如果是同步组更新，优先按组处理，而不是只改其中一个文件。

## 版本控制
- 默认先创建版本快照，再做更新。
- 默认维护一个 manifest / changelog，用于记录：
  - 版本时间
  - 来源摘要
  - 更新范围
  - 相关文件

## 同步组
- `awesome repo + 中文增强版资源页`
- `深度分析稿 + 机构路线图`
- `总索引 + 版本提示`
- `概念注册表 + 相关专题稿`
- `样本流深度调研 + 方法例子集`

## 与现有技能的关系
- 版本化文稿维护：`report-maintainer-zh`
- 方向级综合：`research-synthesizer-zh`
- 周期性新证据入口：`scheduled-research-monitor-zh`

## 资源
- 版本策略：`references/versioning-policy.md`
- 创建版本快照：`scripts/create_version_snapshot.py`
- 更新版本清单：`scripts/update_version_manifest.py`
