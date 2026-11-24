#!/usr/bin/env python3
"""Node 3：按钩子/痛点/方法/金句/互动五个关键点，拼一版旁白草稿。

用法：
  python3 scripts/vibe_write_script.py --topic "题目" --hook "钩子" --pain "痛点" \\
    --method "方法" --key-line "金句" --interaction "互动" --out narration.md [--template A]

只做结构拼接和字数校验，不编数字和经历；没给的内容留 [待填]。
60–90 秒目标约 330–500 字（约 5.5 字/秒）；写完读一遍改口语，再跑 Node 4。
"""
import argparse
import json
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", required=True)
    ap.add_argument("--hook", default="[待填]")
    ap.add_argument("--pain", default="[待填]")
    ap.add_argument("--method", default="[待填]")
    ap.add_argument("--key-line", default="[待填]")
    ap.add_argument("--interaction", default="[待填]")
    ap.add_argument("--template", default="A", choices=list("ABCDEF"))
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    beats = [
        ("B01 冷开场", a.hook),
        ("B02 点题", f"这个反差背后，就是{a.topic}。"),
        ("B03 痛点", a.pain),
        ("B04 方法", a.method),
        ("B05 金句", a.key_line),
        ("B06 回问", a.interaction),
    ]
    lines = [f"# {a.topic}（母版 {a.template}，草稿）", ""]
    total = 0
    for name, text in beats:
        lines.append(f"## {name}")
        lines.append(text)
        lines.append("")
        total += len(text.replace("[待填]", ""))
    body = "\n".join(lines)
    words = len(body.replace(" ", "").replace("\n", ""))
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(body)
    print(f"写好 {a.out}：约 {words} 字（60–90 秒目标 330–500 字）")
    if "[待填]" in body:
        print("提醒：还有 [待填]，补齐再往下走，不要编。")
    if words < 330 or words > 500:
        print(f"提醒：字数 {words} 不在 330–500 目标内，按时长再裁或再补。")
    data = {"topic": a.topic, "template": a.template,
            "beats": [{"id": n.split()[0], "name": n, "narration": t} for n, t in beats]}
    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    return 0


if __name__ == "__main__":
    main()
