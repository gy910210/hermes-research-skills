# HTML Publication Output Contract

## `html_publication_packet`（由代理交付）

- `source_report`：原始Markdown与版本；避免在公开页面泄露个人绝对路径。
- `entry_html`：真实存在的入口；本地交付时提供用户可打开的绝对路径。
- `output_dir`：完整静态包目录，不把父级研究目录当作部署目录。
- `included_pages[]`：实际导出的主稿和附页。
- `included_attachments[]`：显式批准、实际复制的附件。
- `omitted_links[]`：因未选择导出范围而省略的本地资源及原因。
- `source_unchanged`：是否验证源稿未修改。
- `checks`：正文保真、表格、代码、引用、页内/跨页链接、手机/桌面、控制台、打印；每项写清passed/not_run及原因。
- `deployment_status`：`local_only` 或 `published_verified`，不能把“准备部署”写为已上线。
- `public_url`：仅在线上真实回读验证后填写；本地生成时留空。
- `deployment_checks`：若部署，记录检查的入口与至少一个附页/资源；否则not_run。

## 生成目录

- `index.html`：入口主文。
- 其他HTML：只有选择 `--include-linked` 时才生成附页；保留或映射目录结构，不能因同名覆盖。
- 附件：只有选择 `--copy-attachments` 时导出，并且必须在允许类型内。
- `manifest.json`：生成器写入的机器可读清单，记录来源hash、页面、资源、省略项与local-only状态；以脚本输出字段为准，不手写伪造。

manifest描述本地构建；不会自动宣称线上部署。代理填写的publication packet不能覆盖或篡改构建事实。

## 保真要求

HTML可调整标题层级的视觉样式、将引用编号变成锚点、给宽表格加横向滚动容器，但不得增删论点、数字、限定条件和来源。副标题、空格折行、来源区域展示形式可以改变，原文含义必须保留。

Markdown原始HTML不作为受信任可执行内容；脚本应转义或拒绝，不以忠实复制为由执行script、iframe或事件属性。TeX/Mermaid不启用渲染，不生成看似正确的替代结果，也不加载CDN或数学渲染依赖。

数学文本支持边界：

- 同一Markdown行内块（如段落、标题、列表项或单个表格单元格）内，非空且明确闭合的 `\(...\)`、`\[...\]`、`$...$`、`$$...$$` 原样保留定界符与内部TeX字符；输出HTML仅做安全转义。可跨该块内部的普通软换行，但浏览器仍按普通文本排版，不承诺数学布局或逐字节空白排版。
- 从开定界符匹配到首个未被反斜杠转义的同型闭定界符；不解析嵌套数学环境。`$` / `$$` 必须是精确长度的美元符号串，不识别 `$$$`；要表达非数学美元符号请使用Markdown转义或代码。
- 不跨空行、Markdown块结构、表格单元格或反引号代码边界；链接目标与图片alt不属于数学文本支持范围。这些复杂输入请放入代码块，不能假设普通Markdown会保留TeX反斜杠。
- 裸TeX与未闭合定界符按普通Markdown处理，不承诺TeX转换/保真；使用inline code或代码块可明确保留。代码块及inline code不经过数学转换；支持范围内的数学文本不再解释Markdown链接、强调或引用编号，内部HTML也只能作为文本显示。

## 更新

默认创建新输出目录。仅当已有目录被manifest识别为本工具生成且用户同意时使用 `--overwrite`；不得覆盖陌生文件、通过symlink改写外部文件或修改源Markdown。改稿仍以Markdown为唯一事实源。
