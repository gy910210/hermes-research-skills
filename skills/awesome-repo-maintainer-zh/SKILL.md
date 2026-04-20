---
name: awesome-repo-maintainer-zh
description: "Awesome/README 维护器：专门维护 awesome-*.md、repo README 与长列表资源页，负责识别遗漏条目、做差分同步、补 source/publish date/一句话说明，并输出可回写的 catalog_update_packet。需要把支持文档里的论文稳妥同步到 curated repo 页面时调用。"
---

## Hermes 适配说明
- 本 skill 现面向 Hermes 使用，优先依赖 Hermes 原生工具：`search_files`、`read_file`、`write_file`、`patch`、`session_search`、`delegate_task`、`cronjob`、`browser`、`web/search`、`vision`。
- 若正文提到 `references/...` 或 `scripts/...`，优先读取当前 skill 目录下对应文件，不再依赖 Claude 专属目录结构。
- 原始 Claude `agents/openai.yaml` 不作为执行前提；需要并行研究、分工精读或角色评审时，改用 Hermes 的 `delegate_task`。
- 保留原有研究方法论与产物契约，但执行层统一按 Hermes 工具体系落地。

# Awesome Repo Maintainer（中文）

这个 skill 负责维护 `awesome-*.md`、repo README 和长列表资源页。  
它不是知识库主稿维护器，而是 `curated catalog / repo page` 维护器。

## 何时使用
- 已有一个 `awesome-*.md` 或 README 形式的论文资源页。
- 中文增强版资源页、专题稿、周度增量稿里出现了新论文，想同步回 repo 页面。
- 想统一补齐标题、来源、发布日期、一句话说明、章节归类。
- 想检查“支持文档里有、repo 页面里没有”的遗漏条目。

## 输入
- `catalog_file`
- `support_docs[]`
- `normalization_policy`
  - `title_style`
  - `source_and_date_required`
  - `one_line_note_required`
- `sync_goal`
  - `diff_only`
  - `append_missing`
  - `normalize_all`
  - `restructure_sections`

## 输出
- `catalog_update_packet`
  - `missing_entries[]`
  - `duplicate_entries[]`
  - `normalization_fixes[]`
  - `section_moves[]`
  - `ready_to_apply_entries[]`
  - `unverifiable_candidates[]`
- `normalized_repo_page`

## 工作流
1. 先读取现有 repo 页面，识别现有章节树、条目格式和元数据规范。
2. 读取支持文档，提取其中已经稳定出现的论文、benchmark、dataset、challenge 条目。
3. 做差分检查：
   - 支持文档里有、repo 页面里没有
   - repo 页面里有，但 source/date/一句话说明不完整
   - 同一论文在多个章节重复出现
4. 对每个候选条目执行规范化：
   - 标题
   - 链接
   - `Source`
   - `Published`
   - 一句话说明
   - 推荐章节
5. 对无法稳定核实的条目，放入 `unverifiable_candidates`，不要硬写入正式 repo 页面。
6. 如果主题属于电商搜推/生成式搜推，优先和中文增强版资源页、深度分析稿做 paired sync，而不是只对单一文件更新。

## 守护
- repo 页面优先短、准、可维护，不把长分析直接灌进去。
- 不把中文分析稿的综合判断直接写成 repo 页面里的论文结论。
- 如果 publication/source 还不能核实，宁可不加，也不要伪精确。
- 标题风格统一，但不擅自改论文原始标题含义。

## 推荐产出形式
- 一个 `missing_entries + normalization_fixes` 差分表
- 一份更新后的 repo 页面草稿
- 一个“哪些条目仍待验证”的小结
