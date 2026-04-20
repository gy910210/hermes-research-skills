# Hermes Research Skills (中文首发版)

一套面向 Hermes Agent 的中文研究工作流 skills。

本仓库首发版本聚焦中文研究场景，覆盖：
- 方向编排
- 文献扩展检索
- 论文/官方页面精读
- 证据审校
- 综述/专题综合成稿
- 研究文稿维护
- 周期性监测与增量更新
- 概念边界与长期口径维护
- 方法/样本流深挖
- 图示编排

## 首发范围

当前版本包含以下 skills：

- `research-orchestrator-zh`
- `brief-ingester-zh`
- `literature-scout-zh`
- `paper-reader-zh`
- `paper-critic-zh`
- `research-synthesizer-zh`
- `report-maintainer-zh`
- `scheduled-research-monitor-zh`
- `knowledge-base-updater-zh`
- `concept-boundary-analyzer-zh`
- `concept-registry-maintainer-zh`
- `critical-iteration-lab-zh`
- `methodology-sample-flow-extractor-zh`
- `role-review-panel-zh`
- `doc-diagram-orchestrator-zh`
- `paper-summarizer-zh`
- `paper-explorer-zh`
- `paper-explorer-brief-zh`
- `paper-collab-coordinator-zh`
- `awesome-repo-maintainer-zh`
- `agentic-commerce-research-profile-zh`

## 推荐调用链

标准研究主链：

1. `research-orchestrator-zh`
2. `literature-scout-zh`
3. `paper-reader-zh`
4. `paper-critic-zh`
5. `research-synthesizer-zh`
6. `report-maintainer-zh` / `knowledge-base-updater-zh`
7. `scheduled-research-monitor-zh`（用于持续跟踪）

## 适用场景

- 中文综述写作
- 方向研究与路线图梳理
- 学术 vs 工业证据对照
- 概念边界辨析
- 周期性研究监测
- 方法、样本流、prompt/template 深挖

## 依赖的 Hermes 工具

建议启用这些 toolsets：
- `file`
- `web`
- `browser`
- `delegation`
- `session_search`
- `cronjob`
- `vision`
- `skills`

## 安装方式

方式 1：作为外部 tap 源

```bash
hermes skills tap add gy910210/hermes-research-skills
```

方式 2：手动安装/复制 skill 目录（适合本地测试）

将 `skills/` 下需要的技能目录复制到你的 Hermes skills 目录中。

## 仓库结构

```text
skills/
  research-orchestrator-zh/
  literature-scout-zh/
  paper-reader-zh/
  paper-critic-zh/
  research-synthesizer-zh/
  ...
```

## 发布建议

首版建议发布为：`v0.1.0-zh`

后续可继续拆分：
- Core Pack
- Monitoring Pack
- Diagram / Concept / Methodology 扩展包

## 许可证

当前仓库使用 MIT License。

## 说明

这些 skills 已做 Hermes 适配，优先使用 Hermes 原生工具链：
- `search_files`
- `read_file`
- `write_file`
- `patch`
- `session_search`
- `delegate_task`
- `cronjob`
- `browser`
- `web/search`
- `vision`
