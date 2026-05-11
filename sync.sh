#!/bin/bash
# 同步新饭笔记到 GitHub Pages 并发布

VAULT="/Users/benniyan/Documents/Obsidian Vault/Resources/新饭笔记"
REPO="/Users/benniyan/Documents/GitHub/byneanea.github.io"

# ── 1. 同步文件 ────────────────────────────────────────────
echo "同步文章..."

# 同步2026年（可按同样格式添加更多年份）
for folder in 2026/01 2026/02; do
  src="$VAULT/$folder"
  dst="$REPO/新饭笔记2026/$(basename $folder)"
  [ -d "$src" ] || continue
  mkdir -p "$dst"
  find "$src" -name "*.md" ! -name "*副本*" -exec cp -u {} "$dst/" \;
done

# ── 2. 重建 index.md ───────────────────────────────────────
python3 "$REPO/build_index.py"

# ── 3. Commit & Push ──────────────────────────────────────
cd "$REPO"
git add -A

if git diff --cached --quiet; then
  echo "没有新内容，无需更新。"
  exit 0
fi

COUNT=$(git diff --cached --name-only | grep "新饭笔记" | wc -l | tr -d ' ')
git commit -m "更新笔记（新增/修改 ${COUNT} 篇）"
git push origin main
echo "✓ 发布完成！访问 https://byneanea.github.io"
