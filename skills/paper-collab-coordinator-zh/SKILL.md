---
name: paper-collab-coordinator-zh
description: "【兼容旧入口】旧的多人协作分派器。默认改用 research-orchestrator-zh 做单 agent 研究编排；只有当用户明确要求把论文分给多人协作时，才保留这里的角色分派逻辑。"
---

## Hermes 适配说明
- 本 skill 现面向 Hermes 使用，优先依赖 Hermes 原生工具：`search_files`、`read_file`、`write_file`、`patch`、`session_search`、`delegate_task`、`cronjob`、`browser`、`web/search`、`vision`。
- 若正文提到 `references/...` 或 `scripts/...`，优先读取当前 skill 目录下对应文件，不再依赖 Claude 专属目录结构。
- 原始 Claude `agents/openai.yaml` 不作为执行前提；需要并行研究、分工精读或角色评审时，改用 Hermes 的 `delegate_task`。
- 保留原有研究方法论与产物契约，但执行层统一按 Hermes 工具体系落地。

# Paper Collaboration Coordinator（中文，兼容入口）

这个 skill 不再是研究项目的推荐入口。当前默认入口是 `research-orchestrator-zh`。

## 默认迁移规则
- 没有明确的人类协作者名单时：直接切换到 `../research-orchestrator-zh/SKILL.md`
- 只有当输入里真的出现 `assignees / deadlines / role allocation` 时，才继续使用本 skill 的多人任务卡逻辑

## 若保留多人协作模式
1. 先让 `research-orchestrator-zh` 决定研究阶段与所需产物。
2. 再把 `paper-reader-zh / paper-summarizer-zh / paper-critic-zh` 分发给不同协作者。
3. 最终仍由 `research-synthesizer-zh` 与 `report-maintainer-zh` 收束成统一文稿。
