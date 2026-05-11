#!/usr/bin/env python3
"""重建 index.md，扫描所有 新饭笔记XXXX 目录"""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

def display(filename):
    name = filename[:-3]
    name = re.sub(r'^\d{8}_', '', name)
    return name

def month_key(filename):
    """返回用于排序/分组的月份标签"""
    m = re.match(r'^(\d{4})(\d{2})\d{2}', filename)
    if m:
        return f"{m.group(1)}年{int(m.group(2))}月"
    m = re.match(r'^(\d+)月', filename)
    if m:
        return f"2026年{int(m.group(1))}月"
    m = re.match(r'^(\d{4})-(\d{2})', filename)
    if m:
        return f"{m.group(1)}年{int(m.group(2))}月"
    return "其他"

# 收集所有文章
articles = {}  # month -> [(rel_path, filename)]

for entry in sorted(os.listdir(BASE)):
    if not re.match(r'^新饭笔记\d{4}$', entry):
        continue
    year_dir = os.path.join(BASE, entry)
    for sub in sorted(os.listdir(year_dir)):
        sub_dir = os.path.join(year_dir, sub)
        if not os.path.isdir(sub_dir):
            continue
        for f in sorted(os.listdir(sub_dir)):
            if not f.endswith('.md') or '副本' in f:
                continue
            month = month_key(f)
            rel = f"{entry}/{sub}/{f}"
            articles.setdefault(month, []).append((rel, f))

# 月份排序
def sort_month(m):
    match = re.match(r'(\d+)年(\d+)月', m)
    return (int(match.group(1)), int(match.group(2))) if match else (9999, 99)

sorted_months = sorted(articles.keys(), key=sort_month)
total = sum(len(v) for v in articles.values())

lines = [
    "---",
    "title: 新饭笔记",
    "---",
    "",
    "# 新饭笔记",
    "",
    f"> 共 {total} 篇文章",
    "",
    "---",
    "",
]

for month in sorted_months:
    files = articles[month]
    label = "专题文章" if month == "其他" else month
    lines.append(f"## {label}（{len(files)} 篇）")
    lines.append("")
    for rel, fname in files:
        lines.append(f"- [{display(fname)}]({rel})")
    lines.append("")

lines += [
    "---",
    "",
    "## 其他",
    "",
    "- [李国飞最新分享 · 价值投资三种底层思维框架](李国飞最新分享-价值投资三种底层的思维框架.md)",
    "",
]

with open(os.path.join(BASE, "index.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"index.md 已更新，共 {total} 篇文章")
