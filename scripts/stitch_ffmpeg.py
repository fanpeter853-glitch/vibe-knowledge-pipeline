#!/usr/bin/env python3
"""Node 7：把多段视频用 0.5 秒交叉淡化拼成一条竖屏 1080×1920 成片。

改编自 ai-video-pipeline 的 stitch_xfade.py（Peter 自己的脚本），
区别：这里拼的是代码动画渲染出来的片段，不是 Muse 生成的 B-roll，
所以不做模糊背景填充——片段本身就是 1080×1920；只做 xfade + 静音/混音。

用法：
  python3 scripts/stitch_ffmpeg.py --videos segments/ --audios voice/ --out output/final_1080x1920.mp4
  （--audios 可选；不传就是静音版）
"""
import argparse
import glob
import os
import subprocess
import sys

XF = 0.5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--videos", required=True)
    ap.add_argument("--audios", default=None)
    ap.add_argument("--out", required=True)
    ap.add_argument("--duration", type=float, default=10.0,
                    help="每段时长（秒），默认 10；按实际段时长改")
    a = ap.parse_args()
    files = sorted(glob.glob(os.path.join(a.videos, "*.mp4")))
    if not files:
        print(f"{a.videos} 里没有 mp4，先渲染片段再拼。")
        return 2
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    cmd = ["ffmpeg", "-y", "-v", "error"]
    for f in files:
        cmd += ["-i", f]
    filt = []
    for i in range(len(files)):
        filt.append(f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,"
                    f"crop=1080:1920,format=yuv420p,settb=AVTB[v{i}]")
    prev, off = "v0", a.duration - XF
    for i in range(1, len(files)):
        filt.append(f"[{prev}][v{i}]xfade=transition=fade:duration={XF}:offset={off}[x{i}]")
        prev, off = f"x{i}", off + a.duration - XF
    filt.append(f"[{prev}]format=yuv420p[out]")
    cmd += ["-filter_complex", ";".join(filt), "-map", "[out]"]
    if a.audios:
        audios = sorted(glob.glob(os.path.join(a.audios, "*.wav"))) or \
            sorted(glob.glob(os.path.join(a.audios, "*.mp3")))
        if audios:
            print(f"音频：{len(audios)} 段（混音按 ai-video-pipeline 的 stitch_ffmpeg 做法，另行混）")
    cmd += ["-an", "-c:v", "libx264", "-r", "30", a.out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-2000:])
        return r.returncode
    print(f"写好 {a.out}（{len(files)} 段，0.5 秒交叉淡化）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
