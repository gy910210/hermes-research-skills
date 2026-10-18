---
name: report-html-publisher-zh
description: "将研究报告 Markdown 转为保留正文、表格和引用的响应式 HTML 阅读页."
version: 0.1.0
author: gy910210, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, markdown, html, publishing, citations, Chinese]
    related_skills: [research-orchestrator-zh, report-maintainer-zh, doc-diagram-orchestrator-zh]
---

# Research Report HTML Publisher（中文）

把已有研究稿转换为可直接在浏览器打开的静态阅读页。保留事实、限定条件和引用，不重新总结论文、不补造图表、不替用户公开资料。默认只生成本地页面；公网部署是需要另行授权并验证的后续动作。

## 何时使用

- 用户要求“把这篇 Markdown 报告生成 HTML / 网页 / 阅读版”。
- 需要把稳定主稿、精读笔记或专题稿做成带目录、引用跳转和打印样式的页面。
- 需要研究主稿与经批准的附页组成一个可移植静态目录。
- 不用于：改写论点、从 PDF 直接猜排版、制作营销落地页或自动开通公网托管。应先完成文本提取/研究成稿。

## 前提

- Python 3.10+；依赖清单为 [requirements.txt](requirements.txt)，使用 `markdown-it-py`，不需要账号/API key。
- 用 `skill_view` 返回的 skill 目录定位脚本；仓库内路径示例见下，安装后替换成实际 skill 目录，不硬编码个人目录。
- 若缺依赖，通过 `terminal` 在当前项目虚拟环境安装 requirements；不要为了转换一份报告修改 Hermes 全局配置。

## 输入 / 输出

输入：`report_path`、`output_dir`，以及显式选择的 `include_linked`、`copy_attachments`、`overwrite`、可选 `title`。

输出：`index.html`、可选附页/附件、`manifest.json`；代理另交付 `html_publication_packet`，记录页面入口、导出范围、验证结果及是否真正部署。详见 [output-contract.md](references/output-contract.md)。

## How to Run

通过 `terminal` 执行，下面以仓库目录为工作目录。路径有空格时按实际shell安全引用。

```python
terminal(command="python -m pip install -r skills/report-html-publisher-zh/requirements.txt")
terminal(command="python skills/report-html-publisher-zh/scripts/publish_report.py research/report.md --output research/site-v1")
```

默认不递归公开内部笔记，不复制原论文PDF，不提供原Markdown下载。被省略的本地链接保留文字但不提供失效点击入口，详情进入manifest。只有用户同意导出范围后才扩展：

```python
terminal(command="python skills/report-html-publisher-zh/scripts/publish_report.py research/report.md --output research/site-v2 --include-linked --copy-attachments")
```

| 选项 | 行为 |
|---|---|
| `--output DIR` | 独立输出目录；默认拒绝覆盖非空目录 |
| `--include-linked` | 递归导出源稿目录内、实际被链接的Markdown附页 |
| `--copy-attachments` | 复制实际引用的允许类型附件；先检查隐私与再分发许可 |
| `--overwrite` | 只更新本工具管理的既有输出，不能当作清空任意目录的开关 |
| `--title TEXT` | 自定义页面标题；保留原文正文 |

## 工作流

1. 用 `read_file` 读取原稿，检查标题、章节、表格、代码、来源列表与本地链接。若只是转换，保持已存在的证据边界，不重新做研究。
2. 决定公开范围与输出路径：默认单篇、本地、新目录。不得默认打包 `.meta/`、个人路径、凭据或用户未批准的附件；不得直接覆盖Markdown。
3. 使用脚本生成，而不是手工复制全文。验收：输出入口和manifest真实存在，源稿不变，没有联网加载依赖。
4. 用manifest复核实际导出/省略范围；检查引用跳转、页内/跨页锚点和附件。链接不支持或越出源根目录时解决来源问题，不关闭路径保护。
   - 连续来源条目必须逐条显示，不能把Markdown软换行当作浏览器已换行。
   - 用户要求“项目文件链接可打开”时，使用显式附页/附件选项生成完整本地包，并检查每个条目；不得把禁用链接或“未包含”提示当成满足该要求。公开发布仍需另行授权。
5. 用浏览器打开实际生成页；检查桌面与窄屏、目录交互、引用、横向表格、控制台及打印媒体样式。脚本不等于浏览器验证；无法打开时说明静态检查的局限。
6. 若用户明确要公网发布，先按 [publishing-boundary.md](references/publishing-boundary.md) 确认托管目标、账号和公开目录。完成部署后读取真实线上URL复核，不以本地文件或部署日志冒充公网成功。
7. 交付入口路径、导出范围、验证结果和部署状态。保存更新命令，便于下一轮由Markdown重新生成，不直接修改生成HTML形成两份事实源。

## 守护与限制

- 页面采用单列长文、桌面目录、移动目录、来源跳转、阅读进度与打印样式；CSS/JS内联，无CDN。
- 引用格式支持来源区中的 `[1] https://... — 标题`；没有对应来源的编号不能凭空补造。代码或已有链接里的编号不是新引用。
- 原始HTML不执行；危险URL、越界路径和symlink逃逸不作为网页资源导出。这是导出边界，不是对研究内容正确性的证明。
- 协议相对URL、本地查询参数、附件片段和双重URL编码不支持，会明确报错；不要删掉路径保护来绕过错误。凭据过滤是保守的文件名/内容规则，不是完整秘密检测或恶意附件扫描。
- `--overwrite` 会核对受管文件hash，拒绝已被手工修改的输出及symlink/hardlink；保留陌生文件，仅清理不再需要的受管文件。
- 不自动渲染TeX/Mermaid：同一Markdown行内块中明确闭合、非空的 `\(...\)`、`\[...\]`、`$...$`、`$$...$$` 保留定界符与TeX文本（HTML安全转义），可跨普通软换行，不解释其中的Markdown/引用。数学范围不能跨空行、块结构、表格单元格或包含反引号；不处理链接目标/图片alt中的数学。裸TeX、未闭合范围按普通Markdown处理，不承诺TeX保真；这类输入需放入inline code或代码块，代码内容不改写。详见输出契约。如需数学排版或图示，先确认离线渲染方案，不能暗中引入在线脚本。
- 图片/PDF等附件复制需要显式选项；仅生成HTML不等于用户允许公开原论文全文。
- 不因网站排版删掉“待验证”“仅开发集”“非因果”等限定条件；不把研究判断变成营销文案。
- 不把单一机器上成功打开等同于所有浏览器/打印机都兼容；记录实测范围。

## 验证 / 停止条件

仓库测试通过 `terminal` 执行：

```python
terminal(command="python -m unittest discover -s tests/skills -p test_report_html_publisher.py -v")
```

实际任务必须检查：源稿未变；正文/表格/代码/引用未丢失；选中的链接与锚点有效；省略内容在manifest可解释；桌面/手机可读；目录/打印可用。只在这些完成后报告本地HTML交付。公网交付还需要真实URL回读通过。

## 资源

- 生成脚本：[scripts/publish_report.py](scripts/publish_report.py)
- 样式：[assets/report.css](assets/report.css)
- 交互：[assets/report.js](assets/report.js)
- 依赖：[requirements.txt](requirements.txt)
- 输出契约：[references/output-contract.md](references/output-contract.md)
- 发布边界：[references/publishing-boundary.md](references/publishing-boundary.md)
