# Contributing

感谢你愿意为 Hermes Research Skills 贡献内容。

这个仓库当前以中文 research workflow 为主，目标不是堆很多 prompt，而是持续维护一条稳定、可复用、可组合的研究工作流。

## 贡献方向

欢迎这些类型的贡献：

- 新增 research skill
- 改进已有 skill 的结构、说明或执行协议
- 补充 `references/` 资料
- 补充 `scripts/` 工具脚本
- 修正 README、示例、发布文案
- 修复引用路径、依赖缺失、文档不一致问题
- 增强 Hermes 原生适配

## 仓库结构

```text
skills/
  <skill-name>/
    SKILL.md
    references/
    scripts/
README.md
CHANGELOG.md
PUBLISHING.md
CONTRIBUTING.md
.github/
```

每个 skill 应尽量自包含：
- `SKILL.md` 说明它做什么、何时使用、输入输出、工作流
- `references/` 放约束、模板、说明文档
- `scripts/` 放辅助脚本

## 新增一个 skill 的建议规范

### 1. 目录命名

请使用稳定、清晰、可搜索的名字：
- 推荐：`research-orchestrator-zh`
- 推荐：`paper-reader-zh`
- 避免：`reader2`
- 避免：`new-skill-final-v3`

如果是中文首发 skill，建议继续保留 `-zh` 后缀。

### 2. SKILL.md 最小结构

建议至少包含：

- `name`
- `description`
- 何时使用
- 输入
- 输出
- 工作流
- 守护/限制
- 资源

### 3. 优先 Hermes 原生工具

新增或修改 skill 时，请优先按 Hermes 原生工具链来设计：

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

不要把 Claude 专属 agent 配置当成前提。

### 4. 强执行优先

我们更偏好“执行型 skill”，而不是只描述方法论的 skill。

好的 skill 应该尽量回答这些问题：
- 先做什么
- 后做什么
- 需要产出什么工件
- 什么时候停止
- 什么时候升级到并行/监测/维护链路

## 推荐写法

### 好例子

- 先读取已有材料，再联网
- 搜索结果必须聚类和去重
- 精读必须形成 `paper_notes`
- 综合写作必须区分：
  - 直接证据支持的结论
  - 综合判断
  - open question / hypothesis

### 不推荐写法

- “你可以考虑先搜一下”
- “如果有需要，也许可以做精读”
- “最后写个总结即可”

我们更希望 skill 像工作流协议，而不是松散建议。

## 修改已有 skill 时请注意

### 1. 不要破坏相对路径

如果 `SKILL.md` 中引用了：
- `references/...`
- `scripts/...`
- `../other-skill/references/...`

请确保对应文件真实存在。

### 2. 尽量保持兼容

如果你要重写一个 skill：
- 可以增强执行协议
- 可以补充结构
- 可以去掉本地环境痕迹
- 但尽量不要无理由删除已有输入/输出约定

### 3. 保持中文首发定位

当前仓库主版本是中文首发版。
新增内容可以包含英文说明，但不要把主叙述风格全部切成英文。

## references 与 scripts 的原则

### references/
适合放：
- artifact contracts
- evidence discipline
- report types
- source tiering
- diagram selection
- monitoring runbook

### scripts/
适合放：
- 扫描文稿候选图位
- 创建版本快照
- 更新 manifest
- 扫描交叉文档一致性

脚本应尽量：
- 可读
- 小而明确
- 不依赖个人本机路径
- 不依赖私有环境变量（除非在文档里明确说明）

## 提交规范

推荐 commit message：

- `feat: add new research skill for ...`
- `docs: improve README and examples`
- `fix: repair broken reference paths`
- `refactor: strengthen Hermes execution protocol`
- `chore: reorganize skill assets`

## Pull Request 建议

PR 最好回答这几个问题：

1. 你改了哪个 skill / 哪些文件？
2. 这次改动解决了什么问题？
3. 是否影响已有调用链？
4. 是否新增了 references/scripts？
5. 使用者能得到什么更好的结果？

## 发布相关

发布流程见：
- `PUBLISHING.md`

变更记录见：
- `CHANGELOG.md`

如果你的改动值得进入 release，请在 PR 描述里附一段可直接进入 changelog 的摘要。

## 最后

这个仓库最欢迎的，不是“多一个 prompt”，而是：
- 更清晰的研究流程
- 更稳定的产物契约
- 更强的 Hermes 适配
- 更好维护的 skill 体系

如果你的贡献能让别人更容易把 Hermes 用成长期研究搭子，那就是很好的贡献。