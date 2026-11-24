#!/usr/bin/env python3
"""Node 2：校验 facts.md——每一行事实都要有出处，没有出处的不上屏。

用法：
  python3 scripts/check_facts.py --facts examples/01-placeholder/facts.md

规则：
- 表格里每一行事实，出处列不能为空，也不能是 [待填]；
- [待填] 的行会逐条列出来，退出码 1（表示这期还没法开拍）；
- 没有 [待填] 且每行都有出处时，退出码 0。
"""
import argparse
import re
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--facts", required=True)
    a = ap.parse_args()
    text = open(a.facts, encoding="utf-8").read()
    rows = [ln for ln in text.splitlines() if ln.strip().startswith("|") and "---" not in ln and "编号" not in ln and "事实" not in ln]
    problems = []
    for ln in rows:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        fact, source = cells[1], cells[2]
        if not fact or fact == "[待填]":
            problems.append(f"事实未填：{ln.strip()}")
        elif not source or source == "[待填]":
            problems.append(f"无出处：{fact}")
    if problems:
        print(f"facts.md 未通过：{len(problems)} 条问题")
        for p in problems:
            print(f"  - {p}")
        print("先把出处补齐再写稿，不要编数字。")
        sys.exit(1)
    print(f"facts.md 通过：{len(rows)} 行事实都有出处。")
    return 0


if __name__ == "__main__":
    main()
