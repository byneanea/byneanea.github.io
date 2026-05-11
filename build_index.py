#!/usr/bin/env python3
"""重建 index.html，扫描所有 notes XXXX 目录"""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

def display(filename):
    name = filename[:-3]
    name = re.sub(r'^\d{8}_', '', name)
    return name

def month_key(filename):
    m = re.match(r'^(\d{4})(\d{2})\d{2}', filename)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    m = re.match(r'^(\d+)月', filename)
    if m:
        return (2026, int(m.group(1)))
    m = re.match(r'^(\d{4})-(\d{2})', filename)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    return (9999, 99)

def month_label(key):
    if key == (9999, 99):
        return "专题文章"
    return f"{key[0]}年{key[1]}月"

# 收集所有文章
articles = {}

for entry in sorted(os.listdir(BASE)):
    if not re.match(r'^notes\d{4}$', entry):
        continue
    year_dir = os.path.join(BASE, entry)
    for sub in sorted(os.listdir(year_dir)):
        sub_dir = os.path.join(year_dir, sub)
        if not os.path.isdir(sub_dir):
            continue
        for f in sorted(os.listdir(sub_dir)):
            if not f.endswith('.md') or '副本' in f:
                continue
            key = month_key(f)
            rel = f"{entry}/{sub}/{f}"
            articles.setdefault(key, []).append((rel, f))

sorted_months = sorted(articles.keys())
total = sum(len(v) for v in articles.values())

# Build HTML
items_html = ""
for key in sorted_months:
    files = articles[key]
    label = month_label(key)
    items_html += f'<h2>{label}（{len(files)} 篇）</h2>\n<ul>\n'
    for rel, fname in files:
        title = display(fname)
        items_html += f'  <li><a href="article.html?file={rel}">{title}</a></li>\n'
    items_html += '</ul>\n'

html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>新饭笔记</title>
<style>
  body {{ max-width: 760px; margin: 40px auto; padding: 0 20px; font-family: -apple-system, "PingFang SC", sans-serif; line-height: 1.8; color: #222; }}
  h1 {{ font-size: 1.8em; margin-bottom: 4px; }}
  .meta {{ color: #888; font-size: 14px; margin-bottom: 32px; }}
  h2 {{ font-size: 1.1em; margin-top: 2em; margin-bottom: 8px; color: #444; border-bottom: 1px solid #eee; padding-bottom: 4px; }}
  ul {{ margin: 0; padding-left: 20px; }}
  li {{ margin: 4px 0; }}
  a {{ color: #0066cc; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  hr {{ border: none; border-top: 1px solid #eee; margin: 32px 0; }}
</style>
</head>
<body>
<h1>新饭笔记 2026</h1>
<p class="meta">共 {total} 篇文章</p>
<hr>
{items_html}
<hr>
<h2>其他</h2>
<ul>
  <li><a href="article.html?file=李国飞最新分享-价值投资三种底层的思维框架.md">李国飞最新分享 · 价值投资三种底层思维框架</a></li>
</ul>
</body>
</html>
"""

with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)

print(f"index.html 已生成，共 {total} 篇文章")
