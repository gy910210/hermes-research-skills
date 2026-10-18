#!/usr/bin/env python3
"""Render research Markdown into an offline, opt-in static reading bundle."""
import argparse
import hashlib
import html
import json
import os
import re
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

from markdown_it import MarkdownIt
from markdown_it.token import Token

PUBLISHER = 'hermes-report-html-v1'
SAFE_ATTACHMENTS = {'.pdf', '.png', '.jpg', '.jpeg', '.webp', '.gif', '.json', '.csv', '.txt'}


def math_literal(state, silent):
    """Protect closed TeX delimiters within one Markdown inline block."""
    start, maximum = state.pos, state.posMax
    source = state.src
    opener = next((s for s in (r'\(', r'\[', '$$', '$')
                   if source.startswith(s, start)), None)
    if opener is None:
        return False
    closer = {r'\(': r'\)', r'\[': r'\]', '$$': '$$', '$': '$'}[opener]
    # Dollar delimiters must be exact runs, not part of $$$ or longer.
    if opener.startswith('$') and (source[start - 1:start] == '$'
                                   or source.startswith('$', start + len(opener))):
        return False
    end = start + len(opener)
    while True:
        end = source.find(closer, end, maximum)
        if end < 0:
            return False
        preceding = end
        while preceding > 0 and source[preceding - 1] == '\\':
            preceding -= 1
        escaped = (end - preceding) % 2
        dollar_run = closer.startswith('$') and (source[end - 1:end] == '$'
                                                or source.startswith('$', end + len(closer)))
        if not escaped and not dollar_run:
            break
        end += len(closer)
    content = source[start + len(opener):end]
    # Never consume an inline code boundary while looking for a math closer.
    if not content.strip() or '`' in content:
        return False
    end += len(closer)
    if not silent:
        token = state.push('math_literal', '', 0)
        token.content = source[start:end]
    state.pos = end
    return True


def heading_ids(tokens):
    used = {'toc', 'toc-toggle', 'reading-progress', 'report-content'}
    headings = []
    for i, token in enumerate(tokens):
        if token.type != 'heading_open':
            continue
        label = ''.join(t.content for t in tokens[i + 1].children or [] if t.type in ('text', 'code_inline', 'image', 'math_literal'))
        base = re.sub(r'[^\w\-\s]', '', label.lower()).strip()
        base = re.sub(r'\s+', '-', base) or 'section'
        ident, count = base, 1
        while ident in used:
            count += 1
            ident = f'{base}-{count}'
        used.add(ident)
        token.attrSet('id', ident)
        headings.append((ident, label))
    return used, headings


def citations(tokens, used_ids):
    """Link numeric citations only in plain inline text, never code or links."""
    refs, source_blocks, entry_blocks = {}, set(), set()
    in_sources = False
    section_level = 0
    for i, block in enumerate(tokens):
        if block.type == 'heading_open':
            label = tokens[i + 1].content.strip().lower()
            level = int(block.tag[1:])
            if label in ('sources', '参考来源', '参考文献', 'references'):
                in_sources, section_level = True, level
            elif level <= section_level:
                in_sources = False
        if in_sources and block.type == 'inline':
            source_blocks.add(i)
            for match in re.finditer(r'(?:^|\n)\[(\d+)\]\s+(https?://[^\s<>]+)', block.content):
                refs[match[1]] = match[2]
                entry_blocks.add(i)
    targets = {}
    # Emit source anchors first. Only actual anchors may become link targets or
    # valid IDs; a raw [1] may already have parsed as a Markdown reference link.
    for i in sorted(range(len(tokens)), key=lambda index: index not in source_blocks):
        block = tokens[i]
        if not block.children:
            continue
        result, depth = [], 0
        for token in block.children:
            if token.type == 'link_open':
                depth += 1
            if token.type == 'link_close':
                depth -= 1
            # Keep source-entry paragraphs line-oriented without changing prose,
            # inline code, math literals or softbreaks inside existing links.
            if i in entry_blocks and token.type == 'softbreak' and not depth:
                token.type, token.tag = 'hardbreak', 'br'
            if token.type != 'text' or depth:
                result.append(token)
                continue
            pattern = r'\[(\d+)\]|https?://[^\s<>]+' if i in source_blocks else r'\[(\d+)\]'
            cursor = 0
            for match in re.finditer(pattern, token.content):
                url = refs.get(match[1]) if match[1] else match[0]
                if not url or (i not in source_blocks and match[1] not in targets):
                    continue
                before = Token('text', '', 0); before.content = token.content[cursor:match.start()]
                if i in source_blocks and match[1]:
                    opening = Token('span_open', 'span', 1)
                    if match[1] not in targets:
                        base = f'source-{match[1]}'
                        ident, count = base, 1
                        while ident in used_ids:
                            count += 1
                            ident = f'{base}-{count}'
                        opening.attrSet('id', ident)
                        used_ids.add(ident)
                        targets[match[1]] = ident
                    closing = Token('span_close', 'span', -1)
                else:
                    opening = Token('link_open', 'a', 1)
                    opening.attrSet('href', '#' + targets[match[1]] if match[1] else url)
                    closing = Token('link_close', 'a', -1)
                label = Token('text', '', 0); label.content = match[0]
                result.extend((before, opening, label, closing))
                cursor = match.end()
            tail = Token('text', '', 0); tail.content = token.content[cursor:]
            result.append(tail)
        block.children = result


def safe_attachment(path, root):
    """Conservative deny rules; not a substitute for reviewing publication data."""
    if path.suffix.lower() not in SAFE_ATTACHMENTS:
        return False
    if any(part.startswith('.') or re.search(r'(credential|secret|password|token|id_rsa|id_ed25519|private.?key|^auth(?:[._-]|$))', part, re.I)
           for part in path.relative_to(root).parts):
        return False
    if not path.is_file():
        raise ValueError(f'Missing attachment: {path.relative_to(root)}')
    if path.stat().st_mode & 0o111:
        return False
    data = path.read_bytes()
    if re.search(rb'-----BEGIN [A-Z ]*PRIVATE KEY-----|["\'](?:api[_-]?key|(?:access[_-]?|refresh[_-]?)?token|password|client[_-]?secret)["\']\s*:', data, re.I):
        return False
    return True


def reading_shell(title, body, headings):
    assets = Path(__file__).resolve().parents[1] / 'assets'
    css = (assets / 'report.css').read_text(encoding='utf-8')
    js = (assets / 'report.js').read_text(encoding='utf-8')
    toc = ''.join('<li><a href="#' + html.escape(ident, quote=True) + '">' + html.escape(label) + '</a></li>' for ident, label in headings)
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self' file:; style-src 'unsafe-inline'; script-src 'unsafe-inline'; base-uri 'none'; form-action 'none'; connect-src 'none'">
<meta name="referrer" content="no-referrer"><title>{html.escape(title)}</title>
<style>{css}</style></head><body>
<a class="skip" href="#report-content">跳到正文</a>
<progress id="reading-progress" max="100" value="0" aria-label="阅读进度"></progress>
<div class="layout"><aside class="rail"><div class="brand">Hermes Research</div><small>RESEARCH NOTES · LOCAL EDITION</small>
<nav id="toc" aria-label="文章目录"><ol>{toc}</ol></nav></aside>
<main id="report-content"><div class="toolbar"><span>研究报告 · 离线阅读</span>
<button id="toc-toggle" aria-controls="toc" aria-expanded="false">目录</button><button data-print>打印 / PDF</button></div>
<article>{body}</article><footer>Hermes Research · Static reading edition · Review before sharing</footer></main></div>
<script>{js}</script></body></html>'''


def publish(args):
    source = Path(args.input).absolute()
    if source.is_symlink():
        raise ValueError('Input Markdown must not be a symlink')
    source = source.resolve()
    root = source.parent
    requested_output = Path(args.output).absolute()
    if any(p.is_symlink() for p in (requested_output, *requested_output.parents)):
        raise ValueError('Output path contains a symlink')
    output = requested_output.resolve()
    if root == output or root.is_relative_to(output):
        raise ValueError('Output must not equal or contain source root')
    owned = {}
    if output.exists():
        if not output.is_dir() or any(p.is_symlink() or (p.is_file() and p.stat().st_nlink > 1) for p in output.rglob('*')):
            raise ValueError('Output must be a directory without symlinks or hardlinks')
        if any(output.iterdir()):
            if not args.overwrite:
                raise ValueError('Output is nonempty; use --overwrite only for owned output')
            marker = output / 'manifest.json'
            if not marker.is_file():
                raise ValueError('Output has no publisher manifest')
            old = json.loads(marker.read_text(encoding='utf-8'))
            if old.get('publisher') != PUBLISHER or not isinstance(old.get('files'), dict):
                raise ValueError('Output has no valid publisher manifest')
            owned = old['files']
            for name, digest in owned.items():
                candidate = output / name
                if Path(name).is_absolute() or '..' in Path(name).parts or not candidate.is_file():
                    raise ValueError('Invalid or missing owned output file')
                if hashlib.sha256(candidate.read_bytes()).hexdigest() != digest:
                    raise ValueError('Owned output was edited; refusing overwrite')
    md = MarkdownIt('commonmark', {'html': False}).enable('table')
    md.inline.ruler.before('escape', 'math_literal', math_literal)
    md.add_render_rule('math_literal', lambda renderer, tokens, idx, options, env: html.escape(tokens[idx].content))
    # Parse all destinations so rejected schemes cannot silently become text.
    md.validateLink = lambda url: True
    pages, attachments, omitted = {}, {}, []

    def output_name(path):
        return 'index.html' if path == source else 'pages/' + path.relative_to(root).as_posix() + '.html'

    def load(path):
        if path in pages:
            return
        raw = path.read_bytes()
        tokens = md.parse(raw.decode('utf-8'))
        ids, headings = heading_ids(tokens)
        citations(tokens, ids)
        pages[path] = {'tokens': tokens, 'ids': ids, 'headings': headings, 'raw': raw}
        for block in tokens:
            stack = []
            for token in block.children or []:
                if token.type not in ('link_open', 'image', 'link_close'):
                    continue
                if token.type == 'link_close':
                    if stack.pop():
                        token.tag = 'span'
                    continue
                image = token.type == 'image'
                attr = 'src' if image else 'href'
                url = str(token.attrGet(attr) or '')
                decoded = unquote(url)
                if re.search(r'%[0-9a-fA-F]{2}', decoded) or '\\' in decoded or any(ord(c) < 32 for c in decoded):
                    raise ValueError(f'Unsupported encoded/control path: {url}')
                parts = urlsplit(url)
                if urlsplit(decoded).scheme.lower() not in ('', 'http', 'https', 'mailto'):
                    raise ValueError(f'Unsafe encoded URL scheme: {url}')
                if parts.scheme and parts.scheme.lower() not in ('http', 'https', 'mailto'):
                    raise ValueError(f'Unsafe URL scheme: {url}')
                if parts.netloc and not parts.scheme:
                    raise ValueError(f'Protocol-relative URL unsupported: {url}')
                omit = False
                if not parts.scheme and not parts.netloc:
                    local_path = unquote(parts.path)
                    if parts.query or local_path.startswith('/'):
                        raise ValueError(f'Absolute paths and local queries unsupported: {url}')
                    target = (path.parent / local_path).resolve() if local_path else path
                    if not target.is_relative_to(root):
                        raise ValueError(f'Local link escapes source root: {url}')
                    is_page = target.suffix.lower() == '.md'
                    included = (target == path or args.include_linked) if is_page else args.copy_attachments and safe_attachment(target, root)
                    if included:
                        if image and target.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.webp', '.gif'}:
                            raise ValueError(f'Unsupported local image type: {url}')
                        if not is_page and parts.fragment:
                            raise ValueError(f'Attachment fragments are unsupported: {url}')
                        if is_page:
                            load(target)
                            if parts.fragment and unquote(parts.fragment) not in pages[target]['ids']:
                                raise ValueError(f'Missing heading: {url}')
                            dest = output_name(target)
                        else:
                            dest = 'attachments/' + target.relative_to(root).as_posix()
                            attachments[dest] = target.read_bytes()
                        relative = os.path.relpath(dest, str(Path(output_name(path)).parent)).replace(os.sep, '/')
                        token.attrSet(attr, quote(relative, safe='/') + ('#' + quote(unquote(parts.fragment)) if parts.fragment else ''))
                    else:
                        omit = True
                        omitted.append({'page': path.relative_to(root).as_posix(), 'target': url, 'reason': 'not opted in or unsupported attachment'})
                        token.type = 'text' if image else 'span_open'
                        token.tag = '' if image else 'span'
                        token.attrs = {} if image else {'class': 'omitted-link', 'title': 'Local material not included'}
                if image and parts.scheme:
                    omitted.append({'page': path.relative_to(root).as_posix(), 'target': url, 'reason': 'remote image disabled'})
                    token.type, token.tag, token.attrs = 'text', '', {}
                    token.content = token.content + ' [remote image not loaded: ' + url + ']'
                if not image:
                    stack.append(omit)

    load(source)
    files = dict(attachments)
    entries = []
    for path, page in pages.items():
        body = md.renderer.render(page['tokens'], md.options, {})
        title = args.title if path == source and args.title else (page['headings'][0][1] if page['headings'] else path.stem)
        files[output_name(path)] = reading_shell(title, body, page['headings']).encode()
        entries.append({'source': path.relative_to(root).as_posix(), 'output': output_name(path), 'source_sha256': hashlib.sha256(page['raw']).hexdigest()})
    manifest = {'publisher': PUBLISHER, 'local_only': True, 'pages': entries, 'omitted_links': omitted,
                'files': {name: hashlib.sha256(data).hexdigest() for name, data in files.items()}}
    files['manifest.json'] = json.dumps(manifest, ensure_ascii=False, indent=2).encode()
    for name in files:
        dest = output / name
        if dest.exists() and name != 'manifest.json' and name not in owned:
            raise ValueError(f'Refusing to replace unowned file: {name}')
        if any(p.exists() and not p.is_dir() for p in dest.parents if p != output):
            raise ValueError('Output parent is not a directory')
    output.mkdir(parents=True, exist_ok=True)
    for name in owned.keys() - files.keys():
        (output / name).unlink()
    for name, content in files.items():
        dest = output / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(content)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    parser.add_argument('--output', required=True)
    parser.add_argument('--title')
    parser.add_argument('--include-linked', action='store_true')
    parser.add_argument('--copy-attachments', action='store_true')
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    try:
        publish(args)
    except (ValueError, OSError) as exc:
        parser.exit(1, f'Error: {exc}\n')


if __name__ == '__main__':
    main()
