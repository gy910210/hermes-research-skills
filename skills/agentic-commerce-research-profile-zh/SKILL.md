---
name: agentic-commerce-research-profile-zh
description: "电商研究领域插件：为 agentic e-commerce、shopping decision system、搜索推荐融合、购物研究代理等主题提供章节树、子方向 taxonomy、来源优先级、benchmark 检查项、工业信号清单与常见专题模板。主题属于电商搜推购物决策研究时调用。"
---

## Hermes 适配说明
- 本 skill 现面向 Hermes 使用，优先依赖 Hermes 原生工具：`search_files`、`read_file`、`write_file`、`patch`、`session_search`、`delegate_task`、`cronjob`、`browser`、`web/search`、`vision`。
- 若正文提到 `references/...` 或 `scripts/...`，优先读取当前 skill 目录下对应文件，不再依赖 Claude 专属目录结构。
- 原始 Claude `agents/openai.yaml` 不作为执行前提；需要并行研究、分工精读或角色评审时，改用 Hermes 的 `delegate_task`。
- 保留原有研究方法论与产物契约，但执行层统一按 Hermes 工具体系落地。

# Agentic Commerce Research Profile（中文）

这个 skill 不是主工作流，而是一个领域插件。只有当主题明确落在电商、购物代理、搜索推荐融合、shopping decision system 等方向时再加载。

## 用法
- 总编排 skill 判定属于电商购物决策主题时加载。
- 需要电商领域章节树、benchmark 检查项、工业落地视角时加载。

## 提供内容
- 规范化问题表述
- 常见一级章节树
- 子方向 taxonomy
- 证据优先级与高风险措辞
- benchmark / dataset / release 检查项
- 工业信号与校企结合视角
- 常见输出模板

## 资源
- 领域档案：`references/domain-profile-agentic-commerce.md`
