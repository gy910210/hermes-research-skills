# Domain Profile: Agentic Commerce

## 推荐总 framing
- 默认把主题写成 `Agentic Shopping Decision System`，而不只是并列的 `Agentic Search + Agentic Recommendation`。
- 只有当材料确实只覆盖搜索或只覆盖推荐时，才退回 narrower framing。

## 常见一级章节树
1. 问题定义与研究范围
2. 2025-2026 演化总览
3. 学术界主线
4. 工业界产品化路径
5. 学术界与工业界之间的连接与错位
6. 系统分层与核心能力
7. 关键子方向
8. 数据集与 benchmark
9. 协议、权限、交易与安全
10. 能做 / 不能做 / 风险边界
11. 下一版建议

## 常见子方向 taxonomy
- shopping deep research / decision support
- agentic search / query planning / tool use
- agentic recommendation / memory / preference elicitation
- governance-constrained recommendation
- simulation / benchmark / offline-to-online calibration
- protocol / permission / transaction infrastructure
- seller-side / merchant-side agent
- observability / optimization / production loop

## 来源优先级
- 学术：论文原文、benchmark 页面、dataset 页面、会议官网
- 工业：官方产品页、工程博客、开发者文档
- 结合视角：校企合作论文、公开 benchmark、工业 demo 与实际产品能力对照

## Benchmark / Dataset 检查项
- 任务定义是什么
- 数据集或环境的来源与构建方
- release 时间
- 样本规模、用户或商品规模、会话长度等公开字段
- 开源 / 私有 / 是否已 release
- 哪些论文复用
- 训练、评测、模拟、judge、对话、检索分别支持什么任务

## 文件命名与版本策略
- 主稿默认命名：`<主题>_正式综述主稿_YYYY-MM-DD.md`
- 图示增强稿默认命名：`<主题>_正式综述主稿_YYYY-MM-DD_with_diagrams.md`
- 专题稿默认命名：`<主题>_专题_<子方向>_YYYY-MM-DD.md`
- 增量稿默认命名：`<主题>_增补分析_<日期>.md` 或 `<主题>_优化点整合与进一步探索_<日期>.md`
- 默认新建新文件，不覆盖旧版；旧版只补“已被新版替代”的提示。

## 工业信号检查项
- 是否来自官方页面
- 是否是真实产品能力，还是研究 demo
- 是否包含支付、权限、库存、商家接入、风控等执行约束
- 是否说明了人类监督或受控执行边界

## 常见专题模板
- 学术界 vs 工业界双视角
- 支持 vs 矛盾综合
- 数据集 / benchmark 图谱
- 子方向专题深挖
- 主稿成熟化合并

模板使用建议：
- 主题尚不稳定时先写增量稿或专题稿。
- 方向已稳定、章节完整时再合并成熟主稿。
- 需要强对比结论时优先写“支持 vs 矛盾综合”。
- 需要展示落地链路时优先写“学术界 + 工业界结合视角”。

## 常见高风险措辞
- `已经解决`
- `可以稳定线上落地`
- `行业标准已经形成`
- `模拟器等同于真实用户`
- `offline 指标可以直接预测 business lift`

推荐替换为：
- `当前证据支持这是强趋势`
- `已有受控场景落地，但边界仍清晰存在`
- `该 benchmark 说明了能力上限，不等于部署成熟度`
