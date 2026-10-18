import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'skills/report-html-publisher-zh/scripts/publish_report.py'


class PublisherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.source = self.base / 'source'
        self.source.mkdir()
        self.out = self.base / 'site'

    def put(self, name, text):
        p = self.source / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding='utf-8')
        return p

    def run_site(self, *args, ok=True):
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.source / 'report.md'), '--output', str(self.out), *args], capture_output=True, text=True)
        if ok:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout)
        return result

    def html(self):
        return (self.out / 'index.html').read_text(encoding='utf-8')

    def test_end_to_end_chinese_table_code_and_source_integrity(self):
        text = '# 中文研究\n\n正文 **忠实** 与引用 [1]。\n\n| 项目 | 数值 |\n| --- | --- |\n| 样本 | 42 |\n\n> 引用原文\n\n```python\nprint("[1] <script>")\n```\n'
        src = self.put('report.md', text)
        self.run_site('--title', '测试标题')
        html = self.html()
        for expected in ('<title>测试标题</title>', '<table>', '中文研究', '正文 <strong>忠实</strong>', '<blockquote>', 'print(&quot;[1] &lt;script&gt;&quot;)'):
            self.assertIn(expected, html)
        self.assertEqual(src.read_text(), text)
        manifest = json.loads((self.out / 'manifest.json').read_text())
        self.assertEqual(manifest['pages'][0]['source_sha256'], hashlib.sha256(text.encode()).hexdigest())
        self.assertTrue(manifest['local_only'])
        self.assertNotIn(str(self.base), json.dumps(manifest))
        self.assertFalse(list(self.out.rglob('*.md')))

    def test_closed_math_delimiters_preserve_literal_tex(self):
        from html import escape
        samples = [
            r'\(x\) and $\{x\}$',
            r'\[\{x\} + x_1 * y_2\]',
            r'$$\{x\} + x_1 * y_2$$',
            '$$\n' + r'\{x\} + \frac{1}{2}' + '\n$$',
            '\\[\n' + r'\{x\} + \frac{1}{2}' + '\n\\]',
            r'$a + \$b$ and \(a + \\) + b\)',
            r'$<script>alert(1)</script> & [1] *x*$',
            r'\([fake](missing.md)\)',
        ]
        code = r'\(x\) $\{x\}$ [1]'
        self.put('report.md', '# Report\n\n' + '\n\n'.join(samples)
                 + '\n\n`' + code + '`\n\n```tex\n' + code
                 + '\n```\n\n    ' + code
                 + '\n\n## Sources\n\n[1] https://example.org/paper\n')
        self.run_site()
        h = self.html()
        for sample in samples:
            with self.subTest(sample=sample):
                self.assertIn(escape(sample), h)
        self.assertIn('<code>' + escape(code) + '</code>', h)
        self.assertIn('<code class="language-tex">' + escape(code) + '\n</code>', h)
        self.assertIn('<pre><code>' + escape(code) + '\n</code></pre>', h)
        self.assertNotIn('<script>alert(1)</script>', h)
        self.assertNotIn('<script src=', h)

    def test_math_does_not_swallow_inline_code(self):
        code = r'\{x\} $'
        self.put('report.md', '# Report\n\n$unclosed `' + code + '` after\n\n'
                 + r'\(unclosed `\{x\} \)` after')
        self.run_site()
        self.assertIn('<code>' + code + '</code>', self.html())
        self.assertIn(r'<code>\{x\} \)</code>', self.html())

    def test_math_heading_keeps_literal_label_in_toc(self):
        self.put('report.md', r'# Formula \(\{x\}\)')
        self.run_site()
        from html.parser import HTMLParser

        class TOC(HTMLParser):
            def __init__(self):
                super().__init__()
                self.in_nav, self.labels = False, []

            def handle_starttag(self, tag, attrs):
                if tag == 'nav':
                    self.in_nav = True

            def handle_endtag(self, tag):
                if tag == 'nav':
                    self.in_nav = False

            def handle_data(self, data):
                if self.in_nav:
                    self.labels.append(data)

        parsed = TOC()
        parsed.feed(self.html())
        self.assertEqual(''.join(parsed.labels), r'Formula \(\{x\}\)')
        self.assert_local_fragments_resolve()

    def test_default_omits_local_material_and_records_reason(self):
        self.put('report.md', '# Report\n\n[Private notes](notes.md) ![plot](plot.png)')
        self.put('notes.md', 'secret')
        self.put('plot.png', 'image')
        self.run_site()
        self.assertIn('Private notes', self.html())
        self.assertIn('plot', self.html())
        self.assertNotIn('href="notes.md"', self.html())
        self.assertNotIn('src="plot.png"', self.html())
        manifest = json.loads((self.out / 'manifest.json').read_text())
        self.assertEqual(len(manifest['omitted_links']), 2)
        self.assertEqual(set(p.name for p in self.out.iterdir()), {'index.html', 'manifest.json'})

    def test_recursive_pages_attachments_and_unique_anchors(self):
        self.put('report.md', '# Intro\n\n[one](a/notes.md#重复-2) [two](b/notes.md#重复) [self](#intro) [pdf](file.pdf)')
        self.put('a/notes.md', '# 重复\n\n## 重复\n\n[back](../report.md#intro) [other](../b/notes.md#重复)')
        self.put('b/notes.md', '# 重复\n\n[back](../report.md#intro)')
        self.put('file.pdf', '%PDF fixture')
        self.run_site('--include-linked', '--copy-attachments')
        manifest = json.loads((self.out / 'manifest.json').read_text())
        self.assertEqual(len(manifest['pages']), 3)
        paths = {p['source']: p['output'] for p in manifest['pages']}
        self.assertNotEqual(paths['a/notes.md'], paths['b/notes.md'])
        self.assertIn('id="重复-2"', (self.out / paths['a/notes.md']).read_text())
        from html.parser import HTMLParser
        from urllib.parse import unquote, urlsplit
        class Links(HTMLParser):
            def __init__(self):
                super().__init__(); self.links = []; self.ids = set()
            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if 'id' in attrs: self.ids.add(attrs['id'])
                if tag in ('a', 'img'): self.links.append(attrs.get('href', attrs.get('src', '')))
        for item in manifest['pages']:
            page = self.out / item['output']
            parsed = Links(); parsed.feed(page.read_text())
            for url in parsed.links:
                u = urlsplit(url)
                if u.scheme: continue
                target = (page.parent / unquote(u.path)).resolve() if u.path else page
                self.assertTrue(target.is_file(), url)
                if u.fragment:
                    dest = Links(); dest.feed(target.read_text())
                    self.assertIn(unquote(u.fragment), dest.ids)
        self.assertEqual((self.out / 'attachments/file.pdf').read_text(), '%PDF fixture')

    def test_source_boundaries_and_missing_links_are_errors(self):
        outside = self.base / 'outside.md'; outside.write_text('# Secret')
        (self.source / 'escape.md').symlink_to(outside)
        for url in ('missing.md', '../outside.md', '%2e%2e/outside.md', 'escape.md', 'file:///etc/passwd', '/etc/passwd', '%252e%252e/outside.md', 'report.md#absent'):
            with self.subTest(url=url):
                self.put('report.md', '# Report\n\n[link](' + url + ')')
                result = self.run_site('--include-linked', '--copy-attachments', ok=False)
                self.assertIn('Error:', result.stderr)
                self.assertFalse(self.out.exists())

    def test_output_ownership_overwrite_and_symlinks(self):
        src = self.put('report.md', '# Original')
        self.out.mkdir(); (self.out / 'stranger.txt').write_text('keep')
        self.run_site(ok=False)
        self.run_site('--overwrite', ok=False)
        self.assertEqual((self.out / 'stranger.txt').read_text(), 'keep')
        (self.out / 'stranger.txt').unlink()
        self.run_site()
        (self.out / 'stranger.txt').write_text('keep')
        src.write_text('# Updated')
        self.run_site('--overwrite')
        self.assertIn('Updated', self.html())
        self.assertEqual((self.out / 'stranger.txt').read_text(), 'keep')
        (self.out / 'trap').symlink_to(self.source, target_is_directory=True)
        self.run_site('--overwrite', ok=False)
        self.assertEqual(src.read_text(), '# Updated')
        for bad in (self.source, self.base):
            self.run_site('--output', str(bad), '--overwrite', ok=False)
        self.assertEqual(src.read_text(), '# Updated')

    def assert_local_fragments_resolve(self):
        from html.parser import HTMLParser
        from urllib.parse import unquote, urlsplit

        class Links(HTMLParser):
            def __init__(self):
                super().__init__()
                self.ids, self.links = [], []

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if 'id' in attrs:
                    self.ids.append(attrs['id'])
                if tag == 'a' and 'href' in attrs:
                    self.links.append(attrs['href'])

        pages = {}
        for path in self.out.rglob('*.html'):
            parsed = Links()
            parsed.feed(path.read_text(encoding='utf-8'))
            self.assertEqual(len(parsed.ids), len(set(parsed.ids)), str(path))
            pages[path.resolve()] = parsed
        for path, parsed in pages.items():
            for url in parsed.links:
                parts = urlsplit(url)
                if parts.scheme or parts.netloc or not parts.fragment:
                    continue
                target = (path.parent / unquote(parts.path)).resolve() if parts.path else path
                self.assertIn(target, pages, url)
                self.assertIn(unquote(parts.fragment), pages[target].ids, url)

    def test_reference_link_source_does_not_create_phantom_citation(self):
        self.put('report.md', '# Report\n\nClaim \\[1].\n\n## Sources\n\n'
                 '[1] https://example.org/paper\n\n[1]: https://other.example/\n')
        self.run_site()
        self.assert_local_fragments_resolve()
        self.assertIn('<p>Claim [1].</p>', self.html())
        self.assertIn('<a href="https://other.example/">1</a>', self.html())

    def test_explicit_fragment_cannot_use_unemitted_source_id(self):
        self.put('report.md', '# Report\n\n[Source](#source-1)\n\n## Sources\n\n'
                 '[1] https://example.org/paper\n\n[1]: https://other.example/\n')
        result = self.run_site(ok=False)
        self.assertIn('Missing heading: #source-1', result.stderr)
        self.assertFalse(self.out.exists())

    def test_source_ids_stay_unique_with_headings_and_duplicate_sources(self):
        self.put('report.md', '# source-1\n\n## source-1-2\n\nClaim [1] and \\[2]. '
                 '`[1]` [existing [1]](https://example.org/existing)\n\n'
                 '```text\n[1]\n```\n\n[Notes](notes.md#source-3)\n\n## Sources\n\n'
                 '[1] https://example.org/first\n\n[1] https://example.org/duplicate\n\n'
                 '[2] https://example.org/second\n\n[2]: https://other.example/\n')
        self.put('notes.md', '# Notes\n\nClaim [3]. [Back](report.md#source-1-3)\n\n'
                 '## Sources\n\n[3] https://example.org/third\n')
        self.run_site('--include-linked')
        self.assert_local_fragments_resolve()
        h = self.html()
        self.assertIn('href="index.html#source-1-3"', h)
        self.assertIn('<code>[1]</code>', h)
        self.assertIn('<a href="https://example.org/existing">existing [1]</a>', h)
        self.assertIn('<code class="language-text">[1]\n</code>', h)
        self.assertNotIn('id="source-2"', h)

    def test_consecutive_sources_have_distinct_visual_lines(self):
        self.put('report.md', '# Report\n\nClaim [1] and [2].\n\nBody line one\n'
                 'body line two.\n\n## Sources\n\n'
                 '[1] https://example.org/first — First `code`\n'
                 '[2] https://example.org/second — Second [details](https://example.org/details)\n')
        self.run_site()
        self.assert_local_fragments_resolve()
        from html.parser import HTMLParser

        class SourceLines(HTMLParser):
            def __init__(self):
                super().__init__()
                self.line, self.source_lines, self.urls = 0, {}, []

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if tag in ('br', 'p', 'li', 'div'):
                    self.line += 1
                if (attrs.get('id') or '').startswith('source-'):
                    self.source_lines[attrs['id']] = self.line
                if tag == 'a':
                    self.urls.append(attrs.get('href'))

        parsed = SourceLines()
        parsed.feed(self.html())
        self.assertEqual(set(parsed.source_lines), {'source-1', 'source-2'})
        self.assertNotEqual(parsed.source_lines['source-1'], parsed.source_lines['source-2'])
        for number, name in ((1, 'first'), (2, 'second')):
            self.assertIn(f'index.html#source-{number}', parsed.urls)
            self.assertIn(f'https://example.org/{name}', parsed.urls)
        self.assertIn('<p>Body line one\nbody line two.</p>', self.html())
        self.assertIn('First <code>code</code>', self.html())
        self.assertIn('Second <a href="https://example.org/details">details</a>', self.html())

    def test_source_citations_are_clickable_without_rewriting_code_links(self):
        self.put('report.md', '# Report\n\n结论 [1] 与 `代码[1]` 和 [已有[1]](https://example.org/other)。\n\n```text\n[1]\n```\n\n## Sources\n\n[1] https://example.org/paper — 标题\n')
        self.run_site()
        h = self.html()
        self.assertIn('href="index.html#source-1"', h)
        self.assertIn('id="source-1"', h)
        self.assertIn('<code>代码[1]</code>', h)
        self.assertIn('<a href="https://example.org/other">已有[1]</a>', h)
        self.assertIn('<code class="language-text">[1]\n</code>', h)
        self.assertIn('https://example.org/paper</a> — 标题', h)

    def test_no_active_raw_html_or_remote_images(self):
        self.put('report.md', '# Report\n\n<script>alert(1)</script>\n\n![远程图](https://example.org/track.png)\n\n[外链](https://example.org/)\n\n<iframe src="https://evil.example"></iframe>')
        self.run_site()
        h = self.html()
        self.assertNotIn('<script>alert(1)', h)
        self.assertNotIn('<iframe', h)
        self.assertNotIn('<img src="https://', h)
        self.assertIn('远程图', h)
        self.assertIn('href="https://example.org/"', h)
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;', h)
        for url in ('javascript:alert(1)', 'data:text/html;base64,PHNjcmlwdD4=', 'vbscript:msgbox(1)', 'jav%61script:alert(1)'):
            self.put('report.md', '# Unsafe\n\n[link](' + url + ')')
            self.run_site('--overwrite', ok=False)
            self.assertEqual(self.html(), h)

    def test_attachments_exclude_credentials_executables_and_active_formats(self):
        names = ('safe.txt', 'credentials.json', 'secret.txt', 'config/token.json', 'auth.json', 'evil.html', 'evil.js', 'evil.svg', 'run.txt', 'key.txt', 'settings.json')
        self.put('report.md', '# Report\n\n' + ' '.join(f'[{n}]({n})' for n in names))
        for name in names:
            self.put(name, 'fixture')
        (self.source / 'run.txt').chmod(0o755)
        (self.source / 'key.txt').write_text('-----BEGIN PRIVATE KEY-----\nprivate')
        (self.source / 'settings.json').write_text('{"token":"secret value"}')
        self.run_site('--copy-attachments')
        copied = {p.relative_to(self.out).as_posix() for p in self.out.rglob('*') if p.is_file()}
        self.assertEqual(copied, {'index.html', 'manifest.json', 'attachments/safe.txt'})
        manifest = json.loads((self.out / 'manifest.json').read_text())
        self.assertEqual(len(manifest['omitted_links']), len(names) - 1)

    def test_offline_reading_shell_with_responsive_toc_and_print(self):
        self.put('report.md', '# Report\n\n## 第二节\n\n正文')
        self.run_site()
        h = self.html()
        for marker in ('Hermes Research', 'id="reading-progress"', 'id="toc"', 'aria-controls="toc"', 'name="viewport"', '@media print', '@media (max-width:', '<style>', '<script>', 'addEventListener', 'href="#第二节"'):
            self.assertIn(marker, h)
        self.assertIn('Content-Security-Policy', h)
        self.assertNotIn('<script src=', h)
        self.assertNotIn('<link ', h)

    def test_heading_ids_do_not_collide_with_reading_shell(self):
        self.put('report.md', '# toc\n\n# report-content\n\n# reading-progress\n\n# toc\n\n# toc-2')
        self.run_site()
        from html.parser import HTMLParser
        class IDs(HTMLParser):
            def __init__(self): super().__init__(); self.ids = []
            def handle_starttag(self, tag, attrs):
                if 'id' in dict(attrs): self.ids.append(dict(attrs)['id'])
        parser = IDs(); parser.feed(self.html())
        self.assertEqual(len(parser.ids), len(set(parser.ids)))

    def test_encoded_filenames_resolve_without_changing_url_semantics(self):
        self.put('report.md', '# Report\n\n[encoded](notes%23one.md#章节) [space](my%20notes.md)')
        self.put('notes#one.md', '# 章节')
        self.put('my notes.md', '# Other')
        self.run_site('--include-linked')
        self.assertIn('href="pages/notes%23one.md.html#%E7%AB%A0%E8%8A%82"', self.html())
        self.assertTrue((self.out / 'pages/notes#one.md.html').is_file())
        self.assertTrue((self.out / 'pages/my notes.md.html').is_file())

    def test_unsupported_image_and_attachment_fragments_fail(self):
        self.put('notes.md', '# Notes')
        self.put('data.txt', 'data')
        for link in ('![not an image](notes.md)', '[bad fragment](data.txt#missing)'):
            with self.subTest(link=link):
                self.put('report.md', '# Report\n\n' + link)
                self.run_site('--include-linked', '--copy-attachments', ok=False)
                self.assertFalse(self.out.exists())

    def test_overwrite_refuses_hardlinked_owned_files(self):
        src = self.put('report.md', '# Report')
        self.run_site()
        original = self.html()
        linked = self.put('saved.txt', original)
        (self.out / 'index.html').unlink()
        os.link(linked, self.out / 'index.html')
        src.write_text('# Changed')
        self.run_site('--overwrite', ok=False)
        self.assertEqual(linked.read_text(), original)


if __name__ == '__main__':
    unittest.main()
