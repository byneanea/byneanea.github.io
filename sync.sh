#!/bin/bash
# 同步新饭笔记到 GitHub Pages 并发布

VAULT="/Users/benniyan/Documents/Obsidian Vault/Resources/新饭笔记"
REPO="/Users/benniyan/Documents/GitHub/byneanea.github.io"

# ── 1. 同步文件 ────────────────────────────────────────────
echo "同步文章..."

# 同步各年份笔记
for year in 2024 2025 2026; do
  for sub in "$VAULT/$year"/*/; do
    [ -d "$sub" ] || continue
    folder=$(basename "$sub")
    dst="$REPO/notes${year}/${folder}"
    mkdir -p "$dst"
    rsync -a --exclude="*副本*" --include="*.md" --exclude="*" "$sub" "$dst/"
  done
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
