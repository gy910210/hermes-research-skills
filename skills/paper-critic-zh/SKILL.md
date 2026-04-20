---
name: paper-critic-zh
description: "证据审校器：基于 paper_notes 或来源包审查直接证据、综合判断、过度推理、benchmark/release/private data/license 风险，并生成中文 evidence_audit。需要把研究内容从“能写”提升到“写得稳”时调用。"
---

## Hermes 适配说明
- 本 skill 现面向 Hermes 使用，优先依赖 Hermes 原生工具：`search_files`、`read_file`、`write_file`、`patch`、`session_search`、`delegate_task`、`cronjob`、`browser`、`web/search`、`vision`。
- 若正文提到 `references/...` 或 `scripts/...`，优先读取当前 skill 目录下对应文件，不再依赖 Claude 专属目录结构。
- 原始 Claude `agents/openai.yaml` 不作为执行前提；需要并行研究、分工精读或角色评审时，改用 Hermes 的 `delegate_task`。
- 保留原有研究方法论与产物契约，但执行层统一按 Hermes 工具体系落地。

# Paper Critic（中文）

## 输入
- `paper_notes`（推荐）
- `evidence_map`（可选）
- `existing_claims` 或拟写结论（可选）

## 输出
- `evidence_audit`
  - 字段契约见 `../research-orchestrator-zh/references/artifact-contracts.md`

## 步骤
1. 对每条拟写结论判断它属于 `直接证据`、`邻近证据` 还是 `综合判断`。
2. 检查是否存在常见过度推理：
   - 从 offline 指标推出 online gain
   - 从模拟器推出真实用户迁移
   - 从 demo 推出可部署
   - 从行业报道或产品观察推出平台内部结论
   - 从单个入口形态推出底层技术路线已经成立
3. 对 benchmark、release、私有数据、license、未披露规模等信息做事实性审校。
4. 若来源包含行业报道、采访、产品观察或二手传闻，补充一层 `publicly_verifiable / industry_observation / rumor_or_unverified` 标注。
5. 对每个子方向产出：
   - `strongest_support`
   - `strongest_contradiction`
   - `still-missing evidence`
   - `risky wording to avoid`
6. 给出可直接用于改写主稿的 `rewrite_suggestions`。

## 守护
- 所有审校意见都要能回指到原始来源。
- 审校器不是为了“挑刺”，而是为了把结论写稳。
- 不能确认的事实应降级为 `未披露` 或 `待验证`。
- 对产业侧信息，优先区分“官方页面可确认”“高质量报道可观察”“内部说法不可证实”三层。
