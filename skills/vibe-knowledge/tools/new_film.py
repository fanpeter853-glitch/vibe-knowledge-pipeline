#!/usr/bin/env python3
"""新建一期知识短片（建在 ai-teardown 的 cine 引擎上）。

用法：
  python3 ~/.claude/skills/vibe-knowledge/tools/new_film.py <期号> --template A --title "本福特定律" [--ws ~/Desktop/vibe-knowledge] [--series vk]
         [--voice-ref <你的 10–30 秒录音.wav>] [--ratio 16:9]

做的事：
1. 工作区 / 系列不存在就调用 ai-teardown 的 new_series.py --style cine 建好（引擎、字体、渲染工具）。
2. 把 kit/know.js 装进 <系列>/cine/engine/，给 cine/tools/record.py、stills.py 打补丁：每次 seek 之后 await window.__vk.wait()（等配图、视频帧解码完再截图）。
3. 音色参照：不设默认 AI 音色；--voice-ref 传 Peter 自己 10–30 秒录音才拷，否则跳过。
4. lessons/<期号>/：narration.json（母版旁白骨架）、film.js（画面骨架）、facts.md（事实清单）、assets.json（代码资产清单）、assets/{img,clips,audio}/。
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
AT = Path.home() / ".claude/skills/ai-teardown"
DEFAULT_REF = None  # 改编版：不设默认 AI 音色；--voice-ref 传 Peter 自己 10–30 秒录音才拷，否则跳过

SEEK = 'pg.evaluate("(t) => window.__film.seek(t)", t)'
PATCHED = SEEK + '; pg.evaluate("() => window.__vk ? window.__vk.wait() : null")'


def patch_tools(sd: Path):
    for name in ("record.py", "stills.py"):
        p = sd / "cine/tools" / name
        s = p.read_text(encoding="utf-8")
        if "__vk" in s:
            continue
        if SEEK not in s:
            sys.exit(f"{p} 里找不到 seek 调用，cine 引擎改过了，补丁要重写")
        p.write_text(s.replace(SEEK, PATCHED), encoding="utf-8")
        print(f"✓ 补丁：{p.relative_to(sd)}")


FIN_OLD = '"-i", str(m["src"]),'
FIN_NEW = '"-i", str(m["src"] if Path(m["src"]).is_absolute() else ROOT / m["src"]),'


def patch_finish(sd: Path):
    p = sd / "cine/tools/finish.py"
    s = p.read_text(encoding="utf-8")
    if FIN_NEW in s:
        return
    if FIN_OLD not in s:
        sys.exit(f"{p} 里找不到 music src 的写法，cine 引擎改过了，补丁要重写")
    p.write_text(s.replace(FIN_OLD, FIN_NEW), encoding="utf-8")
    print(f"✓ 补丁：{p.relative_to(sd)}（music 的 src 可写相对系列目录的路径）")




def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    ap.add_argument("--template", required=True, choices=list("ABCDEF"))
    ap.add_argument("--title", required=True)
    ap.add_argument("--ws", default=str(Path.home() / "Desktop/vibe-knowledge"))
    ap.add_argument("--series", default="vk")
    ap.add_argument("--voice-ref", default=None)
    a = ap.parse_args()

    ws = Path(a.ws).expanduser().resolve()
    sd = ws / "examples" / a.series
    if not AT.exists():
        sys.exit("cine 引擎（ai-teardown）未装，本仓库不含 cine 引擎；见 docs/vertical-render.md，先定渲染路线再建片。")
    if not (sd / "cine/engine/core.js").exists():
        subprocess.run([sys.executable, str(AT / "engine/scripts/new_series.py"), str(ws), a.series, "--style", "cine", "--title", "Vibe知识大赏"], check=True)
        shutil.copytree(AT / "templates/series-cine/tools", sd / "tools", dirs_exist_ok=True)
    shutil.copy(SKILL / "kit/know.js", sd / "cine/engine/know.js")
    patch_tools(sd)
    patch_finish(sd)
    sys.path.insert(0, str(SKILL / "tools")); import patch_earshot; patch_earshot.patch(sd)   # earshot 代码音效

    if a.voice_ref:
        ref = sd / "voice/host-ref.wav"
        src = Path(a.voice_ref).expanduser()
        if not src.exists():
            sys.exit(f"找不到音色参照：{src}")
        ref.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src, ref)
        print(f"✓ 音色参照（Peter 自己录音）：{src} → {ref.relative_to(ws)}")
    else:
        print("音色参照：未传 --voice-ref，不拷默认音色（本仓库不用 AI 默认音色）")

    L = sd / "lessons" / a.id
    if L.exists():
        sys.exit(f"这一期已存在：{L}")
    for d in ("assets/img", "assets/clips", "assets/audio", "build", "stills"):
        (L / d).mkdir(parents=True)
    T = SKILL / "templates"
    narr = (T / f"narration/{a.template}.json").read_text(encoding="utf-8")
    (L / "narration.json").write_text(narr, encoding="utf-8")
    film = (T / "film.skeleton.js").read_text(encoding="utf-8").replace("__TITLE__", a.title).replace("__ID__", a.id).replace("__TPL__", a.template)
    (L / "film.js").write_text(film, encoding="utf-8")
    shutil.copy(T / "facts.md", L / "facts.md")
    (L / "assets.json").write_text(json.dumps({"_how": "代码资产清单（本仓库改编版）：只列代码画的资产，不列付费生成资产；status: plan / done", "items": []}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"✓ 新一期：{L}\n  母版 {a.template} · {a.title}\n  下一步：写 facts.md → narration.json → assets.json（代码资产清单，无报价）→ 配音 → film.js")


if __name__ == "__main__":
    main()
