#!/usr/bin/env python3
"""Node 5：竖屏渲染前置检查（只检查，不渲染）。

用法：
  python3 scripts/render_vertical.py --film skills/vibe-knowledge/templates/film_skeleton_vertical.html

检查：
- film HTML 存在，且画幅是 1080×1920；
- 本机有没有 Playwright / Chromium（渲染逐帧截图要用）。
缺 Playwright / Chromium 时直接报错退出，不会假装出片。
真正的逐帧渲染等渲染路线定了再接（见 docs/vertical-render.md）。
"""
import argparse
import re
import shutil
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--film", required=True)
    a = ap.parse_args()
    try:
        html = open(a.film, encoding="utf-8").read()
    except FileNotFoundError:
        print(f"找不到 film 文件：{a.film}")
        return 2
    if "1080" not in html or "1920" not in html:
        print("film 里没写 1080×1920，先把竖屏画幅写进骨架再渲染。")
        return 2
    print("film 检查通过：竖屏 1080×1920。")
    missing = []
    if shutil.which("chromium") is None and shutil.which("chromium-browser") is None \
            and shutil.which("google-chrome") is None:
        missing.append("Chromium/Chrome（浏览器）")
    try:
        import playwright  # noqa: F401
    except ImportError:
        missing.append("Playwright（Python 包）")
    if missing:
        print("渲染跑不通，缺：" + "、".join(missing) + "。")
        print("先装好再渲染，不要强行安装，也不要谎称已出片。")
        return 2
    print("渲染环境齐了（Playwright + Chromium），可以接逐帧渲染。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
