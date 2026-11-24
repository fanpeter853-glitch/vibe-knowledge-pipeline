#!/usr/bin/env python3
"""Build the 8 beat compositions for vibe EP01 as HyperFrames HTML files.

EP01: 人为什么会对某段回忆念念不忘（母版 A 猜谜概念片，小号）
Style: paper （水墨纸本，浅色暖纸、点阵、墨 + 朱砂点缀），竖屏 1080x1920。
贯穿道具：一颗小光点，每想一次就亮一点（示意动画，不是真实大脑照片）。
On-screen text rule: 每组 ≤8 字，同屏最多两组（大字关键词 + 一行小字），
脚注写出处，示意画面标「画面为示意」。无英文旁白、无假数字、无 AI 配音。
GSAP is bundled locally (render/gsap.min.js) so render does not depend on a CDN.

Usage:
  python3 render/build_beats.py
  -> writes render/project/b01.html ... b06.html (+ hyperframes.json, gsap.min.js)
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RENDER = os.path.join(ROOT, "render")
PROJECT = os.path.join(RENDER, "project")

BEATS = [
    dict(id="b01", dur=6.7, kicker="想一想", keyword="那段回忆", sub="像昨天一样",
         foot="", dot="dim", note=""),
    dict(id="b02", dur=4.4, kicker="点题", keyword="念念不忘", sub="为什么？",
         foot="", dot="bright", note=""),
    dict(id="b03", dur=8.4, kicker="痛点", keyword="越想越牢", sub="越讲越记得牢",
         foot="来源：Roediger & Karpicke 2006", dot="rings", note="画面为示意"),
    dict(id="b04a", dur=8.2, kicker="第一", keyword="情绪贴标签", sub="越强 存得越牢",
         foot="来源：Cahill & McGaugh 1998", dot="tag", note="画面为示意"),
    dict(id="b04b", dur=10.2, kicker="第二", keyword="每次重写", sub="清晰≠准确",
         foot="来源：Talarico & Rubin 2003", dot="fragments", note="画面为示意"),
    dict(id="b04c", dur=9.1, kicker="第三", keyword="没说完的事", sub="不一定都成立",
         foot="来源：Zeigarnik 1927；2025 系统综述", dot="openring", note="画面为示意"),
    dict(id="b05", dur=7.1, kicker="金句", keyword="忘不掉的是情绪", sub="和一次次想起的你",
         foot="", dot="big", note="画面为示意"),
    dict(id="b06", dur=6.5, kicker="回问", keyword="打1还是打2", sub="开心多 / 难过多",
         foot="", dot="two", note=""),
]

CSS = """
:root { --paper1:#fbf7ee; --paper2:#f3ead8; --ink:#2a2420; --muted:#7d7266;
        --cinnabar:#b23a2e; --gold:#d9a441; }
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:1080px; height:1920px; overflow:hidden; background:var(--paper1); }
#root { width:1080px; height:1920px; position:relative; overflow:hidden;
  background:linear-gradient(180deg, var(--paper1) 0%, var(--paper2) 100%);
  font-family:"Noto Sans CJK SC",sans-serif; color:var(--ink); }
#root::before { content:""; position:absolute; inset:0;
  background-image:radial-gradient(rgba(42,36,32,0.10) 1.5px, transparent 1.5px);
  background-size:48px 48px; }
.wash { position:absolute; width:900px; height:900px; border-radius:50%;
  background:radial-gradient(circle, rgba(217,164,65,0.18) 0%, rgba(217,164,65,0) 65%);
  left:90px; top:380px; }
.kicker { position:absolute; left:90px; top:150px; font-size:40px; letter-spacing:14px;
  color:var(--cinnabar); font-weight:700; }
.dotwrap { position:absolute; left:0; top:520px; width:1080px; height:420px;
  display:flex; align-items:center; justify-content:center; }
.dot { width:150px; height:150px; border-radius:50%;
  background:radial-gradient(circle at 38% 35%, #ffe9a8 0%, var(--gold) 45%, #b97f1e 100%);
  box-shadow:0 0 60px 30px rgba(217,164,65,0.55), 0 0 160px 80px rgba(217,164,65,0.25); }
.dot.dim { width:90px; height:90px; box-shadow:0 0 30px 12px rgba(217,164,65,0.35); }
.dot.big { width:220px; height:220px; box-shadow:0 0 90px 45px rgba(217,164,65,0.65), 0 0 220px 110px rgba(217,164,65,0.30); }
.ring { position:absolute; border:3px solid rgba(178,58,46,0.55); border-radius:50%; }
.frag { position:absolute; width:56px; height:56px; border-radius:50%;
  background:radial-gradient(circle at 38% 35%, #ffe9a8 0%, var(--gold) 60%, #b97f1e 100%);
  box-shadow:0 0 24px 8px rgba(217,164,65,0.45); }
.tag { position:absolute; left:640px; top:560px; background:var(--cinnabar); color:#fff;
  font-size:36px; font-weight:700; padding:10px 22px; border-radius:12px; }
.openring { width:230px; height:230px; border-radius:50%;
  border:10px solid var(--gold); border-top-color:transparent;
  transform:rotate(40deg); box-shadow:0 0 40px rgba(217,164,65,0.35); }
.twin { display:flex; gap:120px; align-items:center; }
.twin .d { text-align:center; }
.twin .d .dot { width:130px; height:130px; }
.twin .d .n { font-size:56px; font-weight:800; margin-top:24px; }
.twin .d.two .dot { background:radial-gradient(circle at 38% 35%, #e8e2d8 0%, #8a8175 55%, #5c554b 100%);
  box-shadow:0 0 40px 16px rgba(90,80,70,0.30); }
.keyword { position:absolute; left:0; top:1010px; width:1080px; text-align:center;
  font-family:"Noto Serif CJK SC",serif; font-weight:800;
  font-size:118px; line-height:1.25; color:var(--ink); }
.sub { position:absolute; left:0; top:1240px; width:1080px; text-align:center;
  font-size:52px; color:var(--muted); letter-spacing:6px; }
.foot { position:absolute; left:90px; bottom:150px; font-size:30px; color:var(--muted); }
.note { position:absolute; right:90px; bottom:150px; font-size:30px; color:var(--muted); }
.progress { position:absolute; left:90px; bottom:80px; display:flex; gap:18px; }
.progress i { width:34px; height:10px; border-radius:5px; background:rgba(42,36,32,0.18); }
.progress i.on { background:var(--cinnabar); }
"""

DOT_HTML = {
    "dim": '<div class="dot dim" id="dot"></div>',
    "bright": '<div class="dot" id="dot"></div>',
    "rings": ('<div class="ring" id="ring1" style="width:260px;height:260px"></div>'
              '<div class="ring" id="ring2" style="width:380px;height:380px;opacity:.6"></div>'
              '<div class="dot" id="dot"></div>'),
    "tag": '<div class="dot" id="dot"></div><div class="tag" id="tag">标签</div>',
    "fragments": ('<div class="frag" id="frag1"></div><div class="frag" id="frag2"></div>'
                  '<div class="frag" id="frag3"></div><div class="dot" id="dot" style="opacity:0"></div>'),
    "openring": '<div class="openring" id="openring"></div><div class="dot" id="dot" style="width:110px;height:110px"></div>',
    "big": '<div class="dot big" id="dot"></div>',
    "two": ('<div class="twin"><div class="d"><div class="dot" id="dot"></div><div class="n">1</div></div>'
            '<div class="d two"><div class="dot" id="dot2"></div><div class="n">2</div></div></div>'),
}

# GSAP choreography per dot type: all absolute times, paused timeline, seekable.
TL = {
    "dim": 'tl.fromTo("#dot",{scale:.4,opacity:0},{scale:1,opacity:1,duration:1.2,ease:"power2.out"},0);'
           'tl.to("#dot",{scale:1.25,duration:1.6,ease:"sine.inOut",yoyo:true,repeat:1},1.4);',
    "bright": 'tl.fromTo("#dot",{scale:.5,opacity:0},{scale:1,opacity:1,duration:.8,ease:"back.out(1.6)"},0);'
              'tl.to("#dot",{boxShadow:"0 0 90px 45px rgba(217,164,65,0.7)",duration:1.2},.9);',
    "rings": 'tl.fromTo("#dot",{scale:.6,opacity:0},{scale:1,opacity:1,duration:.7,ease:"power2.out"},0);'
             'tl.fromTo("#ring1",{scale:.5,opacity:0},{scale:1,opacity:1,duration:1.4,ease:"power2.out"},.5);'
             'tl.fromTo("#ring2",{scale:.5,opacity:0},{scale:1,opacity:.6,duration:1.4,ease:"power2.out"},.9);'
             'tl.to("#ring1",{scale:1.15,duration:2,ease:"sine.inOut",yoyo:true,repeat:1},2.4);',
    "tag": 'tl.fromTo("#dot",{scale:.6,opacity:0},{scale:1,opacity:1,duration:.7,ease:"power2.out"},0);'
           'tl.fromTo("#tag",{opacity:0,y:20,rotate:-6},{opacity:1,y:0,rotate:0,duration:.6,ease:"back.out(1.8)"},.8);',
    "fragments": 'tl.fromTo("#frag1",{x:-260,y:-90,opacity:0},{x:0,y:0,opacity:1,duration:.8,ease:"power2.out"},0);'
                 'tl.fromTo("#frag2",{x:260,y:-110,opacity:0},{x:0,y:0,opacity:1,duration:.8,ease:"power2.out"},.15);'
                 'tl.fromTo("#frag3",{x:0,y:180,opacity:0},{x:0,y:0,opacity:1,duration:.8,ease:"power2.out"},.3);'
                 'tl.to(["#frag1","#frag2","#frag3"],{opacity:0,scale:.4,duration:.5},2.6);'
                 'tl.to("#dot",{opacity:1,scale:1,duration:.8,ease:"back.out(1.6)"},3.0);',
    "openring": 'tl.fromTo("#openring",{rotate:220,opacity:0},{rotate:40,opacity:1,duration:1.4,ease:"power2.out"},0);'
                'tl.fromTo("#dot",{scale:.4,opacity:0},{scale:1,opacity:1,duration:.8,ease:"back.out(1.6)"},.9);'
                'tl.to("#openring",{rotate:130,duration:2.4,ease:"sine.inOut",yoyo:true,repeat:1},2.0);',
    "big": 'tl.fromTo("#dot",{scale:.5,opacity:0},{scale:1,opacity:1,duration:1.0,ease:"power2.out"},0);'
           'tl.to("#dot",{scale:1.12,duration:1.8,ease:"sine.inOut",yoyo:true,repeat:1},1.2);',
    "two": 'tl.fromTo("#dot",{scale:.4,opacity:0},{scale:1,opacity:1,duration:.7,ease:"back.out(1.6)"},0);'
           'tl.fromTo("#dot2",{scale:.4,opacity:0},{scale:1,opacity:1,duration:.7,ease:"back.out(1.6)"},.5);',
}


def build(beat, idx):
    dots = "".join(
        '<i class="on"></i>' if i == idx else "<i></i>" for i in range(len(BEATS)))
    foot = f'<div class="foot">{beat["foot"]}</div>' if beat["foot"] else ""
    note = f'<div class="note">{beat["note"]}</div>' if beat["note"] else ""
    fonts_css = open(os.path.join(PROJECT, "fonts.css"), encoding="utf-8").read()
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="./gsap.min.js"></script>
<style>{fonts_css}
{CSS}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0"
     data-duration="{beat["dur"]}" data-width="1080" data-height="1920">
  <div class="wash"></div>
  <div class="kicker" id="kicker">{beat["kicker"]}</div>
  <div class="dotwrap" id="dotwrap">{DOT_HTML[beat["dot"]]}</div>
  <div class="keyword" id="keyword">{beat["keyword"]}</div>
  <div class="sub" id="sub">{beat["sub"]}</div>
  {foot}{note}
  <div class="progress">{dots}</div>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
tl.fromTo("#kicker", {{opacity:0, y:-16}}, {{opacity:1, y:0, duration:.6, ease:"power2.out"}}, 0);
{TL[beat["dot"]]}
tl.fromTo("#keyword", {{opacity:0, filter:"blur(10px)"}}, {{opacity:1, filter:"blur(0px)", duration:.7, ease:"power4.out"}}, .5);
tl.fromTo("#sub", {{opacity:0, y:18}}, {{opacity:1, y:0, duration:.6, ease:"power2.out"}}, 1.1);
tl.fromTo(".foot, .note", {{opacity:0}}, {{opacity:1, duration:.6}}, 1.6);
tl.fromTo(".progress", {{opacity:0}}, {{opacity:1, duration:.6}}, 1.8);
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body>
</html>
"""


def main():
    os.makedirs(PROJECT, exist_ok=True)
    import shutil
    shutil.copy(os.path.join(RENDER, "gsap.min.js"), os.path.join(PROJECT, "gsap.min.js"))
    with open(os.path.join(PROJECT, "hyperframes.json"), "w", encoding="utf-8") as f:
        json.dump({"$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
                   "paths": {"blocks": "compositions", "components": "compositions/components",
                             "assets": "assets"}}, f, indent=2)
    for i, b in enumerate(BEATS):
        p = os.path.join(PROJECT, f"{b['id']}.html")
        with open(p, "w", encoding="utf-8") as f:
            f.write(build(b, i))
        print(f"wrote {p}  ({b['dur']}s, keyword={b['keyword']!r})")
    print("done: 8 beats")


if __name__ == "__main__":
    main()
