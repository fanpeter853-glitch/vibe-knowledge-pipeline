#!/usr/bin/env python3
"""Node 5：竖屏渲染前置检查（只检查，不渲染）。

渲染路线（2026-11-24，Peter 已定；v0.2.0 写回工作流）：HyperFrames / Remotion，
黑色系默认，脚本 render/build_beats_v3.py；不装 Playwright / Chromium，不用 cine 引擎。
不用配音，音乐版即成片。

用法：
  python3 scripts/render_vertical.py --film skills/vibe-knowledge/templates/film_skeleton_vertical.html

检查：
- film HTML 存在，且画幅是 1080×1920；
- 打印 HyperFrames / Remotion 的下一步，不再把缺 Playwright 当成失败。

真正的渲染由 HyperFrames（标题卡、步骤卡、关键概念卡，HTML/CSS 转 MP4）
或 Remotion（批量 / 动态模板）做，再用 scripts/stitch_ffmpeg.py 拼合。
HyperFrames 本机已装（render/package.json，hyperframes ^0.9.88），v3 已渲出；
Remotion 模板未实装，只作批量模板备选。这个脚本只做前置检查。
"""
import argparse
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
    print("渲染路线：HyperFrames / Remotion（2026-11-24 已定，不装 Playwright/Chromium）。")
    print("下一步：HyperFrames 做标题卡/步骤卡/关键概念卡（HTML/CSS 转 MP4）；")
    print("需要批量/动态的拍改用 Remotion 模板；再用 scripts/stitch_ffmpeg.py 拼合。")
    print("注意：HyperFrames 本机已装，v3 已按 render/build_beats_v3.py 渲出；")
    print("Remotion 模板未实装，只作备选，不要谎称已有。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
