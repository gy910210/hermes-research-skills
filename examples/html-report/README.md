# 可运行的 HTML 示例

这组文件是转换测试夹具：研究内容和数字明确标为演示，不冒充真实实验。

从仓库根目录执行：

```sh
python -m pip install -r skills/report-html-publisher-zh/requirements.txt
python skills/report-html-publisher-zh/scripts/publish_report.py examples/html-report/report.md --output build/html-example --include-linked
python -m unittest discover -s tests/skills -p 'test_report_html*.py' -v
```

打开 `build/html-example/index.html`，应能看到：

- 中文长文排版与目录；
- 一个表格，保留“虚构测试数据”说明；
- 正文编号跳转到来源，但代码中的 `[1]` 保持原样；
- 指向“复核范围”的附页链接，以及附页返回主稿的链接；
- 打印样式和窄屏布局。

重复生成到相同目录时，确认其为本工具管理的输出后才追加 `--overwrite`；也可换一个新输出目录。`build/` 为本地产物，不提交到仓库。本地示例不代表已经部署公网。
