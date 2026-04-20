# Hermes Research Skills

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Release](https://img.shields.io/badge/release-v0.1.0--zh-blue)
![Language](https://img.shields.io/badge/language-Chinese-red)
![Hermes](https://img.shields.io/badge/agent-Hermes-7C3AED)

中文研究工作流技能包，面向 Hermes Agent。

English summary: A Chinese-first research skill pack for Hermes Agent, designed to turn searching, paper reading, evidence auditing, synthesis writing, monitoring, and knowledge-base maintenance into a structured end-to-end workflow.

这个仓库提供一套可组合的中文 Research Skills，用来把“找资料、读论文、审证据、写综述、持续监测、维护知识库”串成一条完整工作流。

当前为中文首发版，优先服务这些场景：
- 中文综述与专题稿写作
- 方向研究与路线图梳理
- 学术 vs 工业证据对照
- 概念边界辨析与长期口径维护
- 方法、样本流、prompt/template 深挖
- 周期性研究监测与增量更新

## 为什么做这套 skills

通用 agent 很容易把研究任务做成：
- 搜一堆链接
- 摘几段话
- 拼成流水账

这套 skills 的目标不是“多搜一点”，而是“把研究过程结构化”：
- 先理解已有上下文
- 再扩展证据
- 再精读高价值来源
- 再区分直接证据、综合判断、待验证假设
- 最后生成可维护的文稿与知识库

换句话说，它更像一个中文研究工作流系统，而不是几个零散 prompt。

## 首发版本

首发 tag 建议：`v0.1.0-zh`

这一版以中文 research workflow 为主，不追求大而全，先把主链路做顺。

## 包含的 skills

### 1) 工作流主链
- `research-orchestrator-zh` — 研究总编排入口，负责判断任务类型与调用链
- `brief-ingester-zh` — 读取已有 brief、旧稿、笔记，抽取上下文
- `literature-scout-zh` — 扩展检索、聚类证据、生成 evidence map
- `paper-reader-zh` — 对高价值论文/官方页面做结构化精读
- `paper-critic-zh` — 证据审校，区分直接证据、邻近证据、综合判断
- `research-synthesizer-zh` — 把素材组织成综述/专题稿/方向比较稿
- `report-maintainer-zh` — 维护版本化文稿与索引
- `knowledge-base-updater-zh` — 将新证据稳妥并回既有知识库
- `scheduled-research-monitor-zh` — 周期性监测新证据、产出增量摘要

### 2) 分析与增强模块
- `concept-boundary-analyzer-zh` — 概念边界辨析
- `concept-registry-maintainer-zh` — 长期术语与概念口径维护
- `critical-iteration-lab-zh` — 多轮批判性迭代分析
- `methodology-sample-flow-extractor-zh` — 方法、样本流、训练阶段深挖
- `role-review-panel-zh` — 多职责评审面板
- `doc-diagram-orchestrator-zh` — 从文稿中识别适合补图的位置并生成绘图规格

### 3) 兼容与补充模块
- `paper-summarizer-zh`
- `paper-explorer-zh`
- `paper-explorer-brief-zh`
- `paper-collab-coordinator-zh`
- `awesome-repo-maintainer-zh`
- `agentic-commerce-research-profile-zh`

## 核心技能对照表

| Skill | 角色 | 典型输入 | 典型输出 | 是否建议安装 |
|---|---|---|---|---|
| `research-orchestrator-zh` | 总编排入口 | research goal、旧稿、笔记、brief | workflow 选择、research agenda、工件列表 | 强烈建议 |
| `brief-ingester-zh` | 上下文摄取 | 旧报告、Markdown、PDF、笔记 | `context_brief` | 强烈建议 |
| `literature-scout-zh` | 扩展检索与证据地图 | 主题问题、`context_brief`、时间窗口 | `evidence_map`、阅读队列、聚类结果 | 强烈建议 |
| `paper-reader-zh` | 结构化精读 | 论文、官方博客、benchmark page、PDF | `paper_notes` | 强烈建议 |
| `paper-critic-zh` | 证据审校 | `paper_notes`、来源包、候选结论 | `evidence_audit` | 强烈建议 |
| `research-synthesizer-zh` | 综合写作 | `context_brief`、`evidence_map`、`paper_notes`、`evidence_audit` | `synthesis_packet`、章节草稿、专题稿 | 强烈建议 |
| `report-maintainer-zh` | 文稿维护 | 既有主稿/专题稿、索引、新增内容 | 新版报告、索引更新、版本化结果 | 建议 |
| `knowledge-base-updater-zh` | 知识库更新 | 既有知识库文件、新支持材料 | `kb_update_packet`、版本快照、变更说明 | 建议 |
| `scheduled-research-monitor-zh` | 周期性监测 | 主题、现有文档、时间窗口 | `monitoring_digest`、增量候选 | 建议 |
| `concept-boundary-analyzer-zh` | 概念边界辨析 | 多个相近概念、旧稿、问题定义 | 边界矩阵、分层口径 | 可选 |
| `concept-registry-maintainer-zh` | 长期口径维护 | 多份文档、术语漂移问题 | registry 更新、统一口径建议 | 可选 |
| `critical-iteration-lab-zh` | 多轮批判性分析 | 一组论文或一个方向 | 多轮 critical findings、稳定结论 | 可选 |
| `methodology-sample-flow-extractor-zh` | 方法/样本流深挖 | 论文、附录、官方页面 | 方法卡、样本流对照表 | 可选 |
| `role-review-panel-zh` | 多职责评审 | 技术方案稿、路线图、研究判断 | 分歧点、取舍、修订建议 | 可选 |
| `doc-diagram-orchestrator-zh` | 图示编排 | Markdown 文稿、章节内容 | diagram specs、插图计划 | 可选 |

## 推荐调用链

标准研究主链：

1. `research-orchestrator-zh`
2. `literature-scout-zh`
3. `paper-reader-zh`
4. `paper-critic-zh`
5. `research-synthesizer-zh`
6. `report-maintainer-zh` 或 `knowledge-base-updater-zh`
7. `scheduled-research-monitor-zh`（如果需要持续跟踪）

可以把它理解为：

`已有材料 -> 扩展检索 -> 精读 -> 审校 -> 综合 -> 维护 -> 监测`

## 这套 skills 和普通搜索/总结有什么不同

它强调几件事：

1. 先读现有材料，不盲搜
2. 搜索结果必须聚类和去重，不是链接堆砌
3. 精读要输出结构化 `paper_notes`
4. 综合写作时要区分：
   - 直接证据支持的结论
   - 综合判断
   - open question / hypothesis
5. 文稿默认要可维护，而不是一次性聊天产物

## 安装

### 方式 1：作为外部 tap 源接入

```bash
hermes skills tap add gy910210/hermes-research-skills
```

说明：不同 Hermes 版本对外部 tap 的安装体验可能略有差异。若已加 tap，可继续通过 Hermes 的 skills 子命令浏览、检查和安装。

### 方式 2：手动复制（最稳）

把本仓库 `skills/` 下面需要的目录复制到你的 Hermes skills 目录。

例如：

```bash
cp -R skills/research-orchestrator-zh ~/.hermes/skills/
cp -R skills/literature-scout-zh ~/.hermes/skills/
cp -R skills/paper-reader-zh ~/.hermes/skills/
```

如果你希望整套一起使用，建议至少安装主链上的 8 个核心 skills。

## 推荐开启的 Hermes toolsets

建议启用：
- `file`
- `web`
- `browser`
- `delegation`
- `session_search`
- `cronjob`
- `vision`
- `skills`

这些 skill 已按 Hermes 原生工具链适配，优先使用：
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

## 快速上手

### 场景 1：从零启动一个新研究方向

建议入口：
- `research-orchestrator-zh`

它会把任务分流到：
- context ingest
- evidence scouting
- paper reading
- synthesis

### 场景 2：已经有旧稿，要做增量更新

建议入口：
- `research-orchestrator-zh`
- 或直接 `scheduled-research-monitor-zh`

### 场景 3：只想精读几篇关键论文

建议入口：
- `paper-reader-zh`
- 然后接 `paper-critic-zh`

### 场景 4：已有素材，想出一篇结构化综述

建议入口：
- `research-synthesizer-zh`

## 端到端使用示例

下面是一个典型的中文 research workflow 示例。

### 示例任务

问题：

> 我已经有一份关于 agentic commerce 的旧综述，现在想补最近三个月的新论文和工业动态，并输出一版增量稿。

### 推荐调用链

1. `research-orchestrator-zh`
2. `brief-ingester-zh`
3. `literature-scout-zh`
4. `paper-reader-zh`
5. `paper-critic-zh`
6. `research-synthesizer-zh`
7. `report-maintainer-zh`

### 过程拆解

#### Step 1. 读取已有材料

输入：
- 旧综述 Markdown
- 历史笔记
- 目标问题

预期产物：
- `context_brief.md`

#### Step 2. 扩展近三个月证据

由 `literature-scout-zh` 负责：
- 搜最近三个月的新论文
- 搜 benchmark / dataset page 更新
- 搜公司官方博客和权威技术来源
- 去重、聚类、标注 support / contradiction / gap

预期产物：
- `evidence_map.md`
- `priority_reading_queue.md`

#### Step 3. 精读高价值来源

由 `paper-reader-zh` 负责：
- 对 3-8 篇最关键来源生成结构化 `paper_notes`

预期产物：
- `paper_notes_001.md`
- `paper_notes_002.md`
- `paper_notes_003.md`

#### Step 4. 审核证据质量

由 `paper-critic-zh` 负责：
- 区分直接证据与综合判断
- 标出未披露项、风险点、过度推理风险

预期产物：
- `evidence_audit.md`

#### Step 5. 生成增量稿

由 `research-synthesizer-zh` 负责：
- 把新增证据组织成增量章节
- 写清哪些是直接结论，哪些是综合判断，哪些仍是 open question

预期产物：
- `synthesis_packet.md`
- `report_incremental_2026-xx.md`

#### Step 6. 并回既有文稿

由 `report-maintainer-zh` 负责：
- 创建新版本
- 更新索引
- 给旧版补版本提示

预期产物：
- 新版主稿 / 增量稿
- 更新后的索引页

### 最终你会得到什么

不是一段聊天总结，而是一组可维护的研究工件：

- `context_brief.md`
- `evidence_map.md`
- `paper_notes_*.md`
- `evidence_audit.md`
- `synthesis_packet.md`
- 新版报告或增量稿

这也是这套 skills 和“普通 agent 搜完就总结”最大的区别。

## 仓库结构

```text
skills/
  research-orchestrator-zh/
  brief-ingester-zh/
  literature-scout-zh/
  paper-reader-zh/
  paper-critic-zh/
  research-synthesizer-zh/
  report-maintainer-zh/
  scheduled-research-monitor-zh/
  knowledge-base-updater-zh/
  concept-boundary-analyzer-zh/
  concept-registry-maintainer-zh/
  critical-iteration-lab-zh/
  methodology-sample-flow-extractor-zh/
  role-review-panel-zh/
  doc-diagram-orchestrator-zh/
  ...
```

每个 skill 目录通常包含：
- `SKILL.md`
- `references/`（如有）
- `scripts/`（如有）

## 版本规划

首发后建议逐步拆分成更清晰的包：
- Core Pack
- Monitoring Pack
- Diagram / Concept / Methodology Extensions
- Domain Profiles

## 当前限制

这是一版中文首发版，所以你应该预期：
- 文稿风格优先中文研究写作，不以英文论文写作风格为主
- 某些 skill 仍保留了从早期工作流演化来的兼容接口
- 不同 Hermes 版本对 `skills tap` / `publish` 的体验可能略有差异

但主链已经可用，而且适合作为后续公开迭代的基础版本。

## 开发与发布

发布说明见：
- `PUBLISHING.md`

变更记录见：
- `CHANGELOG.md`

## License

MIT

## 适合谁

这套 skills 最适合：
- 习惯中文研究写作的人
- 想把 research workflow 长期沉淀下来的人
- 希望 agent 不只是“总结”，而是“帮你维护研究系统”的人

如果你正想把 Hermes 用成一个长期研究搭子，这套技能包就是为这个目标设计的。