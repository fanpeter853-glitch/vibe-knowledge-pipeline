#!/usr/bin/env python3
"""Node 4：把旁白按拍拆成分镜，估算每拍时长（约 5.5 字/秒）。

用法：
  python3 scripts/split_storyboard.py --narration narration.md --out storyboard.json

输入是 vibe_write_script.py 生成的 narration.md（## 拍名 + 正文），
或同名 .json。输出 storyboard.json，每拍有 id、name、narration、
duration_sec（按字数估算）、visual（画面关键词，默认 [待填]）。
画面只给关键词/数字/出处，每拍画面字 ≤ 8 字一组，写分镜时再填。
"""
import argparse
import json
import math
import re
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--narration", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    if a.narration.endswith(".json"):
        data = json.load(open(a.narration, encoding="utf-8"))
        beats = [(b["id"], b["name"], b["narration"]) for b in data["beats"]]
        topic = data.get("topic", "[待填]")
    else:
        text = open(a.narration, encoding="utf-8").read()
        topic = text.splitlines()[0].lstrip("# ").split("（")[0] if text else "[待填]"
        beats = []
        for m in re.finditer(r"## (.+)\n([^\n#]+)", text):
            beats.append((m.group(1).split()[0], m.group(1), m.group(2).strip()))
    shots = []
    total = 0.0
    for bid, name, narr in beats:
        words = len(re.sub(r"\[待填\]", "", narr))
        dur = max(3.0, round(words / 5.5, 1))
        total += dur
        shots.append({"shot_id": bid, "name": name, "narration": narr,
                      "duration_sec": dur, "visual": "[待填：画面关键词，≤8 字一组]",
                      "source": "[待填：出处，见 facts.md]"})
    out = {"topic": topic, "total_sec": round(total, 1), "shots": shots}
    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"写好 {a.out}：{len(shots)} 拍，合计约 {total:.1f} 秒")
    return 0


if __name__ == "__main__":
    main()
