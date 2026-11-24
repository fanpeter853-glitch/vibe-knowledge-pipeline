#!/usr/bin/env python3
"""检查本仓库的技能代码和模板里有没有付费残留。

用法：
  python3 scripts/check_no_paid.py

查的范围：skills/vibe-knowledge/ 下的 SKILL.md、references/、templates/、
kit/、tools/、styles/（.md/.py/.js/.json/.swift）。
查的词：付费增强档、默认 AI 配音、API key 值、付费模型名。
注意：ADAPTED_SKILL.md / SOURCE_INVENTORY.md / VERTICAL_1080x1920.md /
facts-template.md / README.md / SOURCE.md 是改编说明文档，
里面会写明“去掉了什么”，所以不在这次检查的范围内——
它们是文档，不是会执行的代码和模板。
发现残留时退出码 1，并逐条列出来。
"""
import re
import sys
from pathlib import Path

ROOT = Path.home() / "workspace/vibe-knowledge-pipeline/skills/vibe-knowledge"
PAT = re.compile(r"renoise|mimo|elevenlabs|midjourney|seedance|wan 3|lyria|"
                 r"vibe-bgm|fit_bgm|bgm_force|api[_-]?key\s*[:=]\s*\S|sk-[A-Za-z0-9]{8,}", re.I)
SKIP = {"ADAPTED_SKILL.md", "SOURCE_INVENTORY.md", "VERTICAL_1080x1920.md", "facts-template.md"}
hits = []
for p in sorted(ROOT.rglob("*")):
    if not p.is_file() or p.suffix not in {".md", ".py", ".js", ".json", ".swift"}:
        continue
    if p.name in SKIP:
        continue
    for i, ln in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
        if PAT.search(ln):
            hits.append(f"{p.relative_to(ROOT)}:{i}: {ln.strip()[:120]}")
if hits:
    print(f"发现 {len(hits)} 处付费残留：")
    for h in hits:
        print(f"  - {h}")
    sys.exit(1)
print("检查通过：技能代码和模板里没有付费残留。")
