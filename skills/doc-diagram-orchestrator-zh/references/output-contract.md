# Output Contract

## `diagram_slots`

为每个候选出图点输出：

- `section_title`
- `line_start`
- `line_end`
- `why_visualize`
- `diagram_type`
- `priority`
- `placement_hint`

## `diagram_specs`

为每张确认要画的图输出最小规格：

- `section_title`
- `diagram_type`
- `goal`
- `source_evidence`
- `nodes`
- `edges`
- `lanes`（仅时序图需要）
- `groups`（仅结构图/矩阵图需要）
- `caption`
- `drawing_prompt`
- `mermaid_fallback`

## 委派给 Drawing Skill 的最小包

只传递足以绘图的最小信息：

- 图类型
- 图目标
- 原文证据摘录
- 必须出现的节点/关系
- 不允许推断的边界
- 风格约束
- 图注

不要把整篇文稿直接交给 drawing skill，否则它容易在版式上做得很完整，但在事实边界上越界。

## Markdown 落位建议

默认把图插在对应二级或三级标题之后，并补一小段过渡语：

````markdown
## 某一节标题

下图先把本节的核心结构/流程压缩成一个总览，便于后文展开。

```mermaid
...
```

图 X. <caption>

随后再回到正文，分别解释图中的关键节点或阶段。
````

## Mermaid 回退要求

- 先保证语义正确，再考虑花哨样式。
- 节点命名使用原文术语，不自行改写成新概念。
- 每张 Mermaid 图只服务一个核心问题。
