#!/usr/bin/env python3
"""Build the 8 beat compositions for vibe EP01 — v3 (black, richer).

EP01: 人为什么会对某段回忆念念不忘（母版 A 猜谜概念片，小号）
Style: BLACK — 深黑/炭黑底 + 微弱渐变 + 星点粒子底纹；金色主色，
白色正文，青色点缀。配色方向借鉴 Jensen《挚友往往相识于少年》的
黑底金字思路，但画面、文案、图表全部是本期自己的，不照搬那条。
贯穿道具：一颗发光金色小光点，带光晕和拖尾，每想一次就亮一点（示意）。
无真人出镜、无照片、无实拍。纯代码动画（HTML/CSS/GSAP + HyperFrames）。

v3 相对 v2 的改动（Peter：v2 还是太单调，改黑色系）：
v2 抽帧诊断（逐秒抽帧看过 final_with_music_1080x1920.mp4）：
  1. 每拍同一版式：kicker 左上、拍号右上、光点居中、关键词同一 y 值，
     8 拍看下来像同一张卡片换了几个字。
  2. 舞台区 250-1010px 只有一颗光点，中间大片空白，上下留白大。
  3. 动画播完就停：光点 2 秒后静止，涟漪/连线播一轮就没了，画面后半段
     几乎不动；0.5 秒交叉淡化那帧发虚、发白。
  4. 浅色底对比弱，大字不够醒目。
v3 做法：
  - 黑色系：#0a0b10 → #12141f 渐变 + 微光晕，绝不纯黑死黑。
  - 三层同时动：底层星点/粒子漂移 + 光晕呼吸 + 背景微光流动；
    中层主可视化连续生长（涟漪一圈接一圈、连线越连越多、碎片拼合散开
    再拼合循环、曲线边画边走、圆环一直转、投票条起伏）；上层大字逐字
    出现、小字逐行淡入、拍号/进度条/学科标签同步动。
  - 版式每拍换一种排布（居中 / 左对齐 / 上下分层 / 双栏），舞台占满竖屏。
  - 转场：除 0.5 秒交叉淡化外，主光点在每拍的起止位置刻意衔接
    （同一颗光点、同一身份），用 xfade 承接。诚实说明：HyperFrames 是
    按拍分别渲染再拼合，不是同一块画布连续生长，所以拍与拍之间的
    “变形带到下一拍”只能靠光点位置衔接 + 淡化近似，做不到单画布
    像素级连续变形；本脚本不假装这一点。
GSAP 本地打包（render/gsap.min.js），渲染不依赖 CDN。
所有动效都用绝对时间写在一条 paused timeline 上，HyperFrames 可逐帧 seek。
星点位置用 Python 确定性伪随机生成，JS 里没有 Math.random / Date.now。

Usage:
  python3 render/build_beats_v3.py
  -> writes render/project_v3/b01.html ... b06.html
  -> then render each: cd render && TMPDIR=$PWD/.tmp-render \
       HYPERFRAMES_EXTRACT_CACHE_DIR=$PWD/.tmp-render \
       npx hyperframes render project_v3 -c b01.html -o out_v3/v3_b01.mp4
"""
import json
import os
import random
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RENDER = os.path.join(ROOT, "render")
PROJECT = os.path.join(RENDER, "project_v3")

BEATS = [
    dict(id="b01", dur=6.7, num="01", kicker="想一想", disc="记忆 · 开场",
         keyword="那段回忆", sub="像昨天一样", detail="过去很久了",
         chips=[], foot="", note="", viz="trail",
         accent="#f5c04e", accent2="#63d8d2", glow="rgba(245,192,78,0.30)",
         kw_top=1180, sub_top=1420, chips_top=1560, stage_top=210, stage_h=900,
         kw_align="center"),
    dict(id="b02", dur=4.4, num="02", kicker="点题", disc="记忆 · 概念",
         keyword="念念不忘", sub="为什么？", detail="反差背后有原因",
         chips=[], foot="", note="", viz="net",
         accent="#63d8d2", accent2="#f5c04e", glow="rgba(99,216,210,0.25)",
         kw_top=300, sub_top=520, chips_top=640, stage_top=700, stage_h=1150,
         kw_align="left"),
    dict(id="b03", dur=8.4, num="03", kicker="痛点", disc="记忆 · 提取练习",
         keyword="越想越牢", sub="越讲越记得牢", detail="",
         chips=["越想忘", "越忘不掉"], foot="来源：Roediger & Karpicke 2006",
         note="画面为示意", viz="ripples",
         accent="#e0705f", accent2="#f5c04e", glow="rgba(224,112,95,0.28)",
         kw_top=1250, sub_top=1470, chips_top=1600, stage_top=260, stage_h=950,
         kw_align="center"),
    dict(id="b04a", dur=8.2, num="04", kicker="第一", disc="脑科学 · 情绪",
         keyword="情绪贴标签", sub="越强 存得越牢", detail="",
         chips=["情绪越强", "存得越牢"], foot="来源：Cahill & McGaugh 1998",
         note="画面为示意", viz="tag",
         accent="#f5c04e", accent2="#e0705f", glow="rgba(245,192,78,0.30)",
         kw_top=280, sub_top=500, chips_top=1620, stage_top=640, stage_h=900,
         kw_align="left"),
    dict(id="b04b", dur=10.2, num="05", kicker="第二", disc="记忆 · 重构",
         keyword="每次重写", sub="清晰≠准确", detail="",
         chips=["细节会变", "感觉留下"], foot="来源：Talarico & Rubin 2003",
         note="画面为示意", viz="fragments",
         accent="#63d8d2", accent2="#f5c04e", glow="rgba(99,216,210,0.25)",
         kw_top=260, sub_top=480, chips_top=1640, stage_top=600, stage_h=980,
         kw_align="center"),
    dict(id="b04c", dur=9.1, num="06", kicker="第三", disc="心理学 · 未完成",
         keyword="没说完的事", sub="不一定都成立", detail="",
         chips=["没做完", "更容易记住"], foot="来源：Zeigarnik 1927；2025 系统综述",
         note="画面为示意", viz="openring",
         accent="#63d8d2", accent2="#f5c04e", glow="rgba(99,216,210,0.28)",
         kw_top=1260, sub_top=1480, chips_top=1610, stage_top=240, stage_h=980,
         kw_align="center"),
    dict(id="b05", dur=7.1, num="07", kicker="金句", disc="记忆 · 金句",
         keyword="忘不掉的是情绪", sub="和一次次想起的你", detail="不是那件事本身",
         chips=[], foot="", note="画面为示意", viz="curve",
         accent="#f5c04e", accent2="#63d8d2", glow="rgba(245,192,78,0.30)",
         kw_top=280, sub_top=500, chips_top=620, stage_top=680, stage_h=1150,
         kw_align="left"),
    dict(id="b06", dur=6.5, num="08", kicker="回问", disc="互动 · 二选一",
         keyword="打1还是打2", sub="开心多 / 难过多", detail="",
         chips=["1 开心多", "2 难过多"], foot="", note="", viz="two",
         accent="#f5c04e", accent2="#63d8d2", glow="rgba(245,192,78,0.30)",
         kw_top=280, sub_top=500, chips_top=1620, stage_top=640, stage_h=900,
         kw_align="center"),
]

CSS = """
:root { --gold:#f5c04e; --gold2:#ffd97a; --ink:#f7f3e8; --muted:#a8aebf;
        --cyan:#63d8d2; --rose:#e0705f; }
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:1080px; height:1920px; overflow:hidden; background:#0a0b10; }
#root { width:1080px; height:1920px; position:relative; overflow:hidden;
  background:linear-gradient(180deg, #0a0b10 0%, #12141f 45%, #0b0d16 100%);
  font-family:"Noto Sans CJK SC",sans-serif; color:var(--ink); }
#root::before { content:""; position:absolute; inset:0;
  background-image:radial-gradient(rgba(245,192,78,0.35) 1.2px, transparent 1.2px);
  background-size:56px 56px; opacity:.35; }
#root::after { content:""; position:absolute; inset:0;
  background:radial-gradient(ellipse 90% 60% at 50% 0%, rgba(245,192,78,0.07) 0%, transparent 60%),
             radial-gradient(ellipse 80% 50% at 50% 110%, rgba(99,216,210,0.06) 0%, transparent 60%);
  pointer-events:none; }
.neb { position:absolute; border-radius:50%; filter:blur(2px); }
.neb1 { width:900px; height:900px; left:-180px; top:180px;
  background:radial-gradient(circle, var(--glow) 0%, transparent 65%); }
.neb2 { width:700px; height:700px; right:-220px; bottom:120px;
  background:radial-gradient(circle, rgba(99,216,210,0.14) 0%, transparent 65%); }
.streak { position:absolute; height:3px; width:420px; border-radius:2px;
  background:linear-gradient(90deg, transparent, var(--gold), transparent);
  box-shadow:0 0 24px 6px rgba(245,192,78,0.45); opacity:.8; }
.star { position:absolute; border-radius:50%; background:#fff8dd;
  box-shadow:0 0 10px 2px rgba(245,192,78,0.55); }
.star.c { background:#c9f5f2; box-shadow:0 0 10px 2px rgba(99,216,210,0.55); }
.kicker { position:absolute; left:80px; top:96px; font-size:44px; letter-spacing:16px;
  color:var(--gold); font-weight:700; }
.disc { position:absolute; left:80px; top:168px; font-size:34px; letter-spacing:8px;
  color:var(--muted); font-weight:700; }
.beatnum { position:absolute; right:80px; top:96px; font-size:38px; letter-spacing:4px;
  color:var(--muted); font-weight:700; }
.beatnum b { color:var(--gold); font-size:48px; }
.stage { position:absolute; left:0; width:1080px; }
.dot { position:absolute; border-radius:50%;
  background:radial-gradient(circle at 38% 35%, #fff3c4 0%, var(--gold) 45%, #c98f1b 100%);
  box-shadow:0 0 50px 22px rgba(245,192,78,0.55), 0 0 140px 70px rgba(245,192,78,0.28); }
.dot.trail { width:34px; height:34px;
  box-shadow:0 0 22px 8px rgba(245,192,78,0.5); }
.dot.small { width:46px; height:46px;
  box-shadow:0 0 26px 10px rgba(245,192,78,0.5); }
.dot.cyan { background:radial-gradient(circle at 38% 35%, #d8fffb 0%, var(--cyan) 55%, #2f8f8a 100%);
  box-shadow:0 0 40px 16px rgba(99,216,210,0.5); }
.ring { position:absolute; border:3px solid var(--rose); border-radius:50%; }
.ring.gold { border-color:rgba(245,192,78,0.75); }
.ring.cyan { border-color:rgba(99,216,210,0.7); }
.frag { position:absolute; border-radius:14px;
  background:linear-gradient(135deg, #ffe9a8, var(--gold));
  box-shadow:0 0 26px 8px rgba(245,192,78,0.4); }
.frag.c { background:linear-gradient(135deg, #c9f5f2, var(--cyan));
  box-shadow:0 0 26px 8px rgba(99,216,210,0.35); }
.tag { position:absolute; color:#0a0b10; background:var(--gold);
  font-size:44px; font-weight:800; padding:14px 30px; border-radius:14px;
  box-shadow:0 0 34px rgba(245,192,78,0.45); }
.tag.rose { background:var(--rose); color:#fff; }
.tag.ghost { background:transparent; color:var(--cyan); border:3px solid var(--cyan);
  box-shadow:none; }
.chip { display:inline-block; border:2px solid rgba(247,243,232,0.4); border-radius:999px;
  font-size:42px; padding:12px 30px; margin:0 12px; color:var(--ink);
  background:rgba(247,243,232,0.08); }
.chip.hot { background:var(--gold); border-color:var(--gold); color:#0a0b10; font-weight:700; }
.gauge { position:absolute; left:80px; width:920px; height:30px; border-radius:15px;
  background:rgba(247,243,232,0.14); overflow:hidden; }
.gauge i { display:block; height:100%; width:0%; border-radius:15px;
  background:linear-gradient(90deg, var(--gold), var(--rose)); }
.gaugelabel { position:absolute; left:80px; font-size:38px; color:var(--muted); }
.votebar { position:absolute; left:80px; width:920px; height:34px; border-radius:17px;
  background:rgba(247,243,232,0.12); overflow:hidden; }
.votebar i { display:block; height:100%; border-radius:17px; }
.votebar.gold i { background:linear-gradient(90deg, #ffd97a, var(--gold)); }
.votebar.cyan i { background:linear-gradient(90deg, #8fe8e2, var(--cyan)); }
.votelabel { position:absolute; left:80px; font-size:44px; font-weight:700; }
.openring { position:absolute; border-radius:50%;
  border:14px solid var(--gold); border-top-color:transparent;
  box-shadow:0 0 50px rgba(245,192,78,0.4); }
.qmark { position:absolute; font-size:130px; font-weight:800; color:var(--gold);
  text-shadow:0 0 40px rgba(245,192,78,0.6); }
.keyword { position:absolute; width:1080px;
  font-family:"Noto Serif CJK SC",serif; font-weight:800;
  font-size:118px; line-height:1.2; color:var(--ink);
  text-shadow:0 0 34px rgba(245,192,78,0.25); }
.keyword.center { text-align:center; left:0; }
.keyword.left { text-align:left; left:80px; width:920px; }
.kwc { display:inline-block; }
.sub { position:absolute; width:1080px; text-align:center;
  font-size:54px; color:#d8d3c4; letter-spacing:6px; }
.sub.left { text-align:left; left:80px; width:920px; }
.detail { position:absolute; left:0; width:1080px; text-align:center;
  font-size:48px; color:var(--ink); letter-spacing:4px; }
.detail.left { text-align:left; left:80px; width:920px; }
.chips { position:absolute; left:0; width:1080px; text-align:center; }
.chips.left { text-align:left; left:80px; width:920px; }
.foot { position:absolute; left:80px; bottom:120px; font-size:30px; color:var(--muted); }
.note { position:absolute; right:80px; bottom:120px; font-size:30px; color:var(--muted); }
.progress { position:absolute; left:80px; bottom:64px; width:920px; height:8px;
  border-radius:4px; background:rgba(247,243,232,0.15); overflow:hidden; }
.progress i { display:block; height:100%; width:0%; border-radius:4px;
  background:linear-gradient(90deg, var(--gold), var(--cyan)); }
.pdots { position:absolute; left:80px; bottom:96px; display:flex; gap:16px; }
.pdots i { width:26px; height:8px; border-radius:4px; background:rgba(247,243,232,0.22); }
.pdots i.on { background:var(--gold); }
"""

# Deterministic star field: 36 stars per beat, seeded.
def stars_html(beat_idx):
    rng = random.Random(1000 + beat_idx * 7)
    out = []
    for i in range(36):
        x = rng.randint(30, 1020)
        y = rng.randint(120, 1780)
        s = rng.choice([5, 6, 7, 9])
        cls = "star c" if rng.random() < 0.3 else "star"
        out.append(f'<div class="{cls}" id="st{i}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;opacity:.5"></div>')
    return "".join(out)


def stars_tl(dur):
    parts = []
    for i in range(36):
        reps = max(1, int(dur // 1.4))
        parts.append(
            f'tl.fromTo("#st{i}",{{opacity:.25}},'
            f'{{opacity:.9,duration:.7,ease:"sine.inOut",yoyo:true,repeat:{reps}}},{(i % 12) * 0.12});')
        dx = 24 if i % 2 == 0 else -24
        parts.append(
            f'tl.fromTo("#st{i}",{{x:0,y:0}},{{x:{dx},y:{-18 if i % 3 == 0 else 18},'
            f'duration:{dur:.1f},ease:"sine.inOut"}},0);')
    return "".join(parts)


VIZ_HTML = {
    "trail": (
        '<svg width="1080" height="900" viewBox="0 0 1080 900" style="position:absolute;left:0;top:0">'
        '<path id="path1" d="M 120 700 C 350 300, 700 760, 960 320" fill="none" stroke="#f5c04e" '
        'stroke-width="5" stroke-linecap="round" stroke-dasharray="1000" pathLength="1000" opacity="0.85"/>'
        '<path id="path2" d="M 120 700 C 350 300, 700 760, 960 320" fill="none" stroke="#63d8d2" '
        'stroke-width="3" stroke-linecap="round" stroke-dasharray="1000" pathLength="1000" opacity="0.5"/>'
        '</svg>'
        '<div class="ring gold" id="ring1" style="width:240px;height:240px;left:420px;top:330px;opacity:0"></div>'
        '<div class="ring cyan" id="ring2" style="width:240px;height:240px;left:420px;top:330px;opacity:0"></div>'
        '<div class="ring gold" id="ring3" style="width:240px;height:240px;left:420px;top:330px;opacity:0"></div>'
        '<div class="dot" id="dot" style="left:45px;top:625px;width:150px;height:150px"></div>'
        '<div class="dot trail" id="tr0" style="left:120px;top:660px;opacity:0"></div>'
        '<div class="dot trail" id="tr1" style="left:300px;top:560px;opacity:0"></div>'
        '<div class="dot trail" id="tr2" style="left:520px;top:560px;opacity:0"></div>'
        '<div class="dot trail" id="tr3" style="left:720px;top:480px;opacity:0"></div>'
        '<div class="dot trail" id="tr4" style="left:900px;top:300px;opacity:0"></div>'
    ),
    "net": (
        '<svg width="1080" height="1150" viewBox="0 0 1080 1150" style="position:absolute;left:0;top:0">'
        '<line id="ln1" x1="540" y1="500" x2="180" y2="180" stroke="#f5c04e" stroke-width="5" stroke-dasharray="1000" pathLength="1000"/>'
        '<line id="ln2" x1="540" y1="500" x2="900" y2="180" stroke="#63d8d2" stroke-width="5" stroke-dasharray="1000" pathLength="1000"/>'
        '<line id="ln3" x1="540" y1="500" x2="180" y2="820" stroke="#63d8d2" stroke-width="5" stroke-dasharray="1000" pathLength="1000"/>'
        '<line id="ln4" x1="540" y1="500" x2="900" y2="820" stroke="#f5c04e" stroke-width="5" stroke-dasharray="1000" pathLength="1000"/>'
        '<line id="ln5" x1="180" y1="180" x2="900" y2="180" stroke="#f5c04e" stroke-width="3" stroke-dasharray="1000" pathLength="1000" opacity="0.6"/>'
        '<line id="ln6" x1="180" y1="820" x2="900" y2="820" stroke="#63d8d2" stroke-width="3" stroke-dasharray="1000" pathLength="1000" opacity="0.6"/>'
        '</svg>'
        '<div class="dot" id="dot" style="left:465px;top:425px;width:150px;height:150px"></div>'
        '<div class="dot small" id="sat1" style="left:157px;top:157px;opacity:0"></div>'
        '<div class="dot small cyan" id="sat2" style="left:877px;top:157px;opacity:0"></div>'
        '<div class="dot small cyan" id="sat3" style="left:157px;top:797px;opacity:0"></div>'
        '<div class="dot small" id="sat4" style="left:877px;top:797px;opacity:0"></div>'
        '<div class="dot small" id="sat5" style="left:517px;top:80px;opacity:0"></div>'
        '<div class="dot small cyan" id="sat6" style="left:517px;top:920px;opacity:0"></div>'
    ),
    "ripples": (
        '<div class="ring" id="ring1" style="width:300px;height:300px;left:390px;top:325px;opacity:0"></div>'
        '<div class="ring gold" id="ring2" style="width:300px;height:300px;left:390px;top:325px;opacity:0"></div>'
        '<div class="ring cyan" id="ring3" style="width:300px;height:300px;left:390px;top:325px;opacity:0"></div>'
        '<div class="ring" id="ring4" style="width:300px;height:300px;left:390px;top:325px;opacity:0"></div>'
        '<div class="ring gold" id="ring5" style="width:300px;height:300px;left:390px;top:325px;opacity:0"></div>'
        '<div class="dot" id="dot" style="left:465px;top:400px;width:150px;height:150px"></div>'
        '<div id="orbit" style="position:absolute;left:540px;top:475px;width:0;height:0">'
        '<div class="dot small" id="orb" style="left:230px;top:-23px"></div></div>'
        '<div id="orbit2" style="position:absolute;left:540px;top:475px;width:0;height:0">'
        '<div class="dot small cyan" id="orb2" style="left:-270px;top:-23px"></div></div>'
    ),
    "tag": (
        '<div class="dot" id="dot" style="left:80px;top:80px;width:170px;height:170px"></div>'
        '<div class="tag" id="tag1" style="left:330px;top:110px;opacity:0">情绪</div>'
        '<div class="tag rose" id="tag2" style="left:560px;top:240px;opacity:0">杏仁核</div>'
        '<div class="tag ghost" id="tag3" style="left:330px;top:380px;opacity:0">海马体</div>'
        '<svg width="1080" height="900" viewBox="0 0 1080 900" style="position:absolute;left:0;top:0">'
        '<path id="arrow" d="M 700 300 C 780 380, 640 420, 560 430" fill="none" stroke="#63d8d2" '
        'stroke-width="5" stroke-linecap="round" stroke-dasharray="1000" pathLength="1000"/>'
        '</svg>'
        '<div class="gaugelabel" id="glabel" style="top:560px">情绪强度</div>'
        '<div class="gauge" style="top:620px"><i id="gfill"></i></div>'
        '<div class="dot small" id="gdot1" style="left:80px;top:700px;opacity:0"></div>'
        '<div class="dot small" id="gdot2" style="left:500px;top:700px;opacity:0"></div>'
        '<div class="dot small" id="gdot3" style="left:900px;top:700px;opacity:0"></div>'
    ),
    "fragments": (
        '<div class="frag" id="frag1" style="left:180px;top:120px;width:110px;height:110px"></div>'
        '<div class="frag c" id="frag2" style="left:790px;top:120px;width:90px;height:90px;border-radius:50%"></div>'
        '<div class="frag" id="frag3" style="left:120px;top:560px;width:90px;height:90px;border-radius:50%"></div>'
        '<div class="frag c" id="frag4" style="left:830px;top:560px;width:110px;height:110px"></div>'
        '<div class="frag" id="frag5" style="left:500px;top:760px;width:80px;height:80px"></div>'
        '<div class="dot" id="dot" style="left:465px;top:400px;width:150px;height:150px;opacity:0"></div>'
        '<div class="tag" id="rewrite" style="left:420px;top:330px;opacity:0">重写</div>'
    ),
    "openring": (
        '<div class="openring" id="openring" style="left:390px;top:290px;width:300px;height:300px"></div>'
        '<svg width="1080" height="980" viewBox="0 0 1080 980" style="position:absolute;left:0;top:0">'
        '<circle id="arc" cx="540" cy="440" r="210" fill="none" stroke="#e0705f" stroke-width="7" '
        'stroke-dasharray="300 1100" pathLength="1400" stroke-linecap="round" transform="rotate(-90 540 440)"/>'
        '<circle id="arc2" cx="540" cy="440" r="270" fill="none" stroke="#63d8d2" stroke-width="4" '
        'stroke-dasharray="200 1500" pathLength="1700" stroke-linecap="round" transform="rotate(90 540 440)" opacity="0.7"/>'
        '</svg>'
        '<div class="dot" id="dot" style="left:490px;top:390px;width:100px;height:100px"></div>'
        '<div id="orbit" style="position:absolute;left:540px;top:440px;width:0;height:0">'
        '<div class="dot small" id="orb" style="left:200px;top:-23px"></div></div>'
        '<div class="qmark" id="qm" style="left:760px;top:180px;opacity:0">？</div>'
        '<div class="tag rose" id="unfin" style="left:340px;top:720px;opacity:0">没做完</div>'
    ),
    "curve": (
        '<svg width="1080" height="1150" viewBox="0 0 1080 1150" style="position:absolute;left:0;top:0">'
        '<path id="curve2" d="M 80 900 C 300 500, 500 950, 700 450 S 950 350, 1000 200" fill="none" '
        'stroke="#63d8d2" stroke-width="4" stroke-linecap="round" stroke-dasharray="1000" pathLength="1000" opacity="0.45"/>'
        '<path id="curve" d="M 80 980 C 300 560, 520 1000, 720 520 S 960 420, 1010 260" fill="none" '
        'stroke="#f5c04e" stroke-width="8" stroke-linecap="round" stroke-dasharray="1000" pathLength="1000"/>'
        '</svg>'
        '<div class="dot" id="dot" style="left:5px;top:905px;width:150px;height:150px"></div>'
        '<div class="dot trail" id="cd1" style="left:60px;top:930px;opacity:0"></div>'
        '<div class="dot trail" id="cd2" style="left:420px;top:760px;opacity:0"></div>'
        '<div class="dot trail" id="cd3" style="left:700px;top:480px;opacity:0"></div>'
        '<div class="dot small cyan" id="cd4" style="left:880px;top:360px;opacity:0"></div>'
    ),
    "two": (
        '<div class="dot" id="dot" style="left:180px;top:60px;width:160px;height:160px"></div>'
        '<div class="dot cyan" id="dot2" style="left:740px;top:60px;width:160px;height:160px"></div>'
        '<div class="votelabel" id="vl1" style="top:300px;color:#f5c04e">1 开心多</div>'
        '<div class="votebar gold" style="top:370px"><i id="vb1" style="width:30%"></i></div>'
        '<div class="votelabel" id="vl2" style="top:470px;color:#63d8d2">2 难过多</div>'
        '<div class="votebar cyan" style="top:540px"><i id="vb2" style="width:30%"></i></div>'
        '<div class="tag" id="vs" style="left:480px;top:640px;opacity:0">选一个</div>'
    ),
}

TL = {
    "trail": (
        'tl.fromTo("#dot",{scale:.4,opacity:0},{scale:1,opacity:1,duration:.8,ease:"power2.out"},0);'
        'tl.fromTo("#path1",{strokeDashoffset:1000},{strokeDashoffset:0,duration:3.2,ease:"power1.inOut"},.4);'
        'tl.fromTo("#path2",{strokeDashoffset:1000},{strokeDashoffset:0,duration:3.2,ease:"power1.inOut"},.9);'
        'tl.to("#dot",{x:200,y:-180,duration:1.6,ease:"power1.inOut"},.8);'
        'tl.to("#dot",{x:460,y:-120,duration:1.6,ease:"power1.inOut"},2.4);'
        'tl.to("#dot",{x:700,y:-260,duration:1.6,ease:"power1.inOut"},4.0);'
        'tl.to("#dot",{scale:1.2,duration:1.0,ease:"sine.inOut",yoyo:true,repeat:1},5.2);'
        + "".join(
            f'tl.fromTo("#tr{i}",{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.5,ease:"back.out(2)"}},{1.2 + i * 0.9});'
            for i in range(5))
        + "".join(
            f'tl.fromTo("#ring{i}",{{scale:.5,opacity:.9}},{{scale:1.8,opacity:0,duration:1.8,ease:"power1.out"}},{1.0 + (i - 1) * 1.7});'
            for i in range(1, 4))
    ),
    "net": (
        'tl.fromTo("#dot",{scale:.5,opacity:0},{scale:1,opacity:1,duration:.6,ease:"back.out(1.6)"},0);'
        + "".join(
            f'tl.fromTo("#ln{i}",{{strokeDashoffset:1000}},{{strokeDashoffset:0,duration:.55,ease:"power2.out"}},{0.5 + (i - 1) * 0.28});'
            for i in range(1, 7))
        + "".join(
            f'tl.fromTo("#sat{i}",{{opacity:0,scale:.3}},{{opacity:1,scale:1,duration:.45,ease:"back.out(2)"}},{0.8 + (i - 1) * 0.28});'
            for i in range(1, 7))
        + 'tl.to("#dot",{scale:1.15,duration:.9,ease:"sine.inOut",yoyo:true,repeat:3},1.8);'
        + 'tl.to(["#ln1","#ln3","#ln5"],{opacity:.35,duration:.6,ease:"sine.inOut",yoyo:true,repeat:3},2.0);'
        + 'tl.to(["#ln2","#ln4","#ln6"],{opacity:.35,duration:.6,ease:"sine.inOut",yoyo:true,repeat:3},2.3);'
    ),
    "ripples": (
        'tl.fromTo("#dot",{scale:.6,opacity:0},{scale:1,opacity:1,duration:.7,ease:"power2.out"},0);'
        + "".join(
            f'tl.fromTo("#ring{i}",{{scale:.55,opacity:.95}},{{scale:2.1,opacity:0,duration:2.2,ease:"power1.out"}},{0.7 + (i - 1) * 1.45});'
            for i in range(1, 6))
        + 'tl.fromTo("#orbit",{rotation:0},{rotation:420,duration:7.6,ease:"none"},.6);'
        + 'tl.fromTo("#orbit2",{rotation:180},{rotation:-240,duration:7.6,ease:"none"},.6);'
        + 'tl.to("#dot",{scale:1.12,duration:1.4,ease:"sine.inOut",yoyo:true,repeat:4},1.0);'
    ),
    "tag": (
        'tl.fromTo("#dot",{scale:.6,opacity:0},{scale:1,opacity:1,duration:.7,ease:"power2.out"},0);'
        'tl.fromTo("#tag1",{opacity:0,y:24,rotate:-8,scale:.7},{opacity:1,y:0,rotate:0,scale:1,duration:.5,ease:"back.out(1.8)"},.8);'
        'tl.fromTo("#tag2",{opacity:0,y:24,rotate:6,scale:.7},{opacity:1,y:0,rotate:0,scale:1,duration:.5,ease:"back.out(1.8)"},2.0);'
        'tl.fromTo("#arrow",{strokeDashoffset:1000},{strokeDashoffset:0,duration:1.2,ease:"power1.inOut"},2.6);'
        'tl.fromTo("#tag3",{opacity:0,y:24,scale:.7},{opacity:1,y:0,scale:1,duration:.5,ease:"back.out(1.8)"},3.8);'
        'tl.fromTo("#gfill",{width:"0%"},{width:"92%",duration:3.2,ease:"power1.inOut"},1.6);'
        'tl.to("#gfill",{width:"78%",duration:1.0,ease:"sine.inOut",yoyo:true,repeat:1},5.2);'
        'tl.fromTo("#gdot1",{opacity:0,scale:.4},{opacity:1,scale:1,duration:.4},2.2);'
        'tl.fromTo("#gdot2",{opacity:0,scale:.4},{opacity:1,scale:1,duration:.4},3.4);'
        'tl.fromTo("#gdot3",{opacity:0,scale:.4},{opacity:1,scale:1,duration:.4},4.6);'
        'tl.to("#dot",{scale:1.3,boxShadow:"0 0 110px 55px rgba(245,192,78,0.8)",duration:1.8,ease:"sine.inOut"},5.0);'
    ),
    "fragments": (
        'tl.fromTo("#frag1",{x:0,y:0},{x:330,y:340,duration:1.2,ease:"power2.inOut"},0);'
        'tl.fromTo("#frag2",{x:0,y:0},{x:-330,y:340,duration:1.2,ease:"power2.inOut"},.15);'
        'tl.fromTo("#frag3",{x:0,y:0},{x:360,y:-140,duration:1.2,ease:"power2.inOut"},.3);'
        'tl.fromTo("#frag4",{x:0,y:0},{x:-360,y:-140,duration:1.2,ease:"power2.inOut"},.45);'
        'tl.fromTo("#frag5",{x:0,y:0},{x:0,y:-340,duration:1.2,ease:"power2.inOut"},.6);'
        'tl.to(["#frag1","#frag2","#frag3","#frag4","#frag5"],{opacity:0,scale:.3,duration:.4},1.9);'
        'tl.to("#dot",{opacity:1,scale:1,duration:.7,ease:"back.out(1.6)"},2.2);'
        'tl.fromTo("#rewrite",{opacity:0,scale:.7},{opacity:1,scale:1,duration:.5,ease:"back.out(1.8)"},2.9);'
        'tl.to("#dot",{opacity:0,scale:.6,duration:.5},3.9);'
        'tl.to("#rewrite",{opacity:0,duration:.4},4.0);'
        'tl.to(["#frag1","#frag2","#frag3","#frag4","#frag5"],{opacity:1,scale:1,x:0,y:0,duration:.9,ease:"power2.inOut",rotation:0},4.4);'
        'tl.to("#frag1",{x:330,y:340,rotation:45,duration:1.1,ease:"power2.inOut"},5.6);'
        'tl.to("#frag2",{x:-330,y:340,rotation:-40,duration:1.1,ease:"power2.inOut"},5.75);'
        'tl.to("#frag3",{x:360,y:-140,rotation:30,duration:1.1,ease:"power2.inOut"},5.9);'
        'tl.to("#frag4",{x:-360,y:-140,rotation:-30,duration:1.1,ease:"power2.inOut"},6.05);'
        'tl.to("#frag5",{x:0,y:-340,rotation:90,duration:1.1,ease:"power2.inOut"},6.2);'
        'tl.to(["#frag1","#frag2","#frag3","#frag4","#frag5"],{opacity:0,scale:.3,duration:.4},7.6);'
        'tl.fromTo("#rewrite",{opacity:0,scale:.7},{opacity:1,scale:1,duration:.5,ease:"back.out(1.8)"},8.0);'
        'tl.to("#dot",{opacity:1,scale:1,duration:.7,ease:"back.out(1.6)"},8.3);'
        'tl.to("#dot",{scale:1.15,duration:1.0,ease:"sine.inOut",yoyo:true,repeat:1},9.0);'
    ),
    "openring": (
        'tl.fromTo("#openring",{rotate:220,opacity:0},{rotate:40,opacity:1,duration:1.2,ease:"power2.out"},0);'
        'tl.fromTo("#dot",{scale:.4,opacity:0},{scale:1,opacity:1,duration:.8,ease:"back.out(1.6)"},.9);'
        'tl.to("#openring",{rotation:"+=300",duration:7.0,ease:"none"},1.6);'
        'tl.fromTo("#arc",{strokeDashoffset:1400},{strokeDashoffset:300,duration:2.4,ease:"power1.inOut"},1.8);'
        'tl.to("#arc",{strokeDashoffset:1400,duration:2.2,ease:"power1.inOut"},4.6);'
        'tl.fromTo("#arc",{strokeDashoffset:1400},{strokeDashoffset:300,duration:1.8,ease:"power1.inOut"},7.0);'
        'tl.fromTo("#arc2",{strokeDashoffset:1700},{strokeDashoffset:200,duration:3.0,ease:"power1.inOut"},2.0);'
        'tl.fromTo("#orbit",{rotation:0},{rotation:360,duration:7.4,ease:"none"},1.0);'
        'tl.fromTo("#qm",{opacity:0},{opacity:.95,duration:.6},2.2);'
        'tl.to("#qm",{opacity:.3,duration:1.1,ease:"sine.inOut",yoyo:true,repeat:3},3.0);'
        'tl.fromTo("#unfin",{opacity:0,y:20},{opacity:1,y:0,duration:.6,ease:"back.out(1.8)"},3.4);'
        'tl.to("#unfin",{scale:1.06,duration:.9,ease:"sine.inOut",yoyo:true,repeat:2},4.4);'
    ),
    "curve": (
        'tl.fromTo("#curve2",{strokeDashoffset:1000},{strokeDashoffset:0,duration:3.0,ease:"power1.inOut"},0);'
        'tl.fromTo("#curve",{strokeDashoffset:1000},{strokeDashoffset:0,duration:3.6,ease:"power1.inOut"},.3);'
        'tl.fromTo("#dot",{scale:.5,opacity:0},{scale:1,opacity:1,duration:.7,ease:"back.out(1.6)"},.4);'
        'tl.to("#dot",{x:260,y:-260,duration:1.5,ease:"power1.inOut"},.8);'
        'tl.to("#dot",{x:560,y:-360,duration:1.5,ease:"power1.inOut"},2.3);'
        'tl.to("#dot",{x:860,y:-620,duration:1.5,ease:"power1.inOut"},3.8);'
        'tl.fromTo("#cd1",{opacity:0,scale:.4},{opacity:1,scale:1,duration:.5},1.0);'
        'tl.fromTo("#cd2",{opacity:0,scale:.4},{opacity:1,scale:1,duration:.5},2.4);'
        'tl.fromTo("#cd3",{opacity:0,scale:.4},{opacity:1,scale:1,duration:.5},3.9);'
        'tl.fromTo("#cd4",{opacity:0,scale:.4},{opacity:1,scale:1,duration:.5},5.2);'
        'tl.to("#dot",{scale:1.18,duration:1.1,ease:"sine.inOut",yoyo:true,repeat:1},5.4);'
    ),
    "two": (
        'tl.fromTo("#dot",{scale:.4,opacity:0},{scale:1,opacity:1,duration:.7,ease:"back.out(1.6)"},0);'
        'tl.fromTo("#dot2",{scale:.4,opacity:0},{scale:1,opacity:1,duration:.7,ease:"back.out(1.6)"},.5);'
        'tl.fromTo("#vb1",{width:"30%"},{width:"72%",duration:1.8,ease:"power1.inOut"},1.0);'
        'tl.fromTo("#vb2",{width:"30%"},{width:"44%",duration:1.8,ease:"power1.inOut"},1.3);'
        'tl.to("#vb1",{width:"58%",duration:1.2,ease:"sine.inOut",yoyo:true,repeat:1},3.0);'
        'tl.to("#vb2",{width:"56%",duration:1.2,ease:"sine.inOut",yoyo:true,repeat:1},3.2);'
        'tl.to("#vb1",{width:"70%",duration:1.2,ease:"sine.inOut"},4.6);'
        'tl.to("#vb2",{width:"48%",duration:1.2,ease:"sine.inOut"},4.8);'
        'tl.to(["#dot","#dot2"],{scale:1.12,duration:1.1,ease:"sine.inOut",yoyo:true,repeat:2},2.8);'
        'tl.fromTo("#vs",{opacity:0,scale:.7},{opacity:1,scale:1,duration:.5,ease:"back.out(1.8)"},3.6);'
        'tl.to("#vs",{scale:1.08,duration:.9,ease:"sine.inOut",yoyo:true,repeat:1},4.6);'
    ),
}


def build(beat, idx):
    kw_chars = "".join(f'<span class="kwc">{c}</span>' for c in beat["keyword"])
    align = beat["kw_align"]
    kw_cls = f"keyword {align}"
    sub_cls = f"sub{' left' if align == 'left' else ''}"
    chips_cls = f"chips{' left' if align == 'left' else ''}"
    detail_cls = f"detail{' left' if align == 'left' else ''}"
    dots = "".join(
        '<i class="on"></i>' if i == idx else "<i></i>" for i in range(len(BEATS)))
    foot = f'<div class="foot">{beat["foot"]}</div>' if beat["foot"] else ""
    note = f'<div class="note">{beat["note"]}</div>' if beat["note"] else ""
    if beat["chips"]:
        chips_html = '<div class="' + chips_cls + '" id="chips" style="top:0">' + "".join(
            f'<span class="chip{" hot" if j == 0 else ""}">{c}</span>'
            for j, c in enumerate(beat["chips"])) + "</div>"
    elif beat["detail"]:
        chips_html = f'<div class="{detail_cls}" id="detail" style="top:0">{beat["detail"]}</div>'
    else:
        chips_html = ""
    fonts_css = open(os.path.join(RENDER, "project", "fonts.css"), encoding="utf-8").read()
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
     data-duration="{beat["dur"]}" data-width="1080" data-height="1920"
     style="--glow:{beat["glow"]}">
  <div class="neb neb1" id="neb1"></div>
  <div class="neb neb2" id="neb2"></div>
  {stars_html(idx)}
  <div class="kicker" id="kicker">{beat["kicker"]}</div>
  <div class="disc" id="disc">{beat["disc"]}</div>
  <div class="beatnum" id="beatnum"><b>{beat["num"]}</b> / 08</div>
  <div class="stage" id="stage" style="top:{beat["stage_top"]}px;height:{beat["stage_h"]}px">{VIZ_HTML[beat["viz"]]}</div>
  <div class="{kw_cls}" id="keyword" style="top:{beat["kw_top"]}px">{kw_chars}</div>
  <div class="{sub_cls}" id="sub" style="top:{beat["sub_top"]}px">{beat["sub"]}</div>
  <div id="chipswrap" style="position:absolute;left:0;top:{beat["chips_top"]}px;width:1080px">{chips_html}</div>
  {foot}{note}
  <div class="pdots">{dots}</div>
  <div class="progress"><i id="pfill"></i></div>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
tl.fromTo("#kicker", {{opacity:0, y:-16}}, {{opacity:1, y:0, duration:.6, ease:"power2.out"}}, 0);
tl.fromTo("#disc", {{opacity:0}}, {{opacity:1, duration:.6}}, .3);
tl.fromTo("#beatnum", {{opacity:0}}, {{opacity:1, duration:.6}}, .2);
tl.fromTo(".kwc", {{opacity:0, filter:"blur(12px)", y:26}},
  {{opacity:1, filter:"blur(0px)", y:0, duration:.55, ease:"power4.out", stagger:.07}}, .5);
tl.fromTo("#sub", {{opacity:0, y:18}}, {{opacity:1, y:0, duration:.6, ease:"power2.out"}}, 1.2);
tl.fromTo("#chipswrap", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:.6, ease:"power2.out"}}, 1.6);
tl.fromTo(".foot, .note", {{opacity:0}}, {{opacity:1, duration:.6}}, 1.8);
tl.fromTo(".pdots", {{opacity:0}}, {{opacity:1, duration:.6}}, 1.9);
tl.fromTo("#pfill", {{width:"0%"}}, {{width:"100%", duration:{beat["dur"]:.1f}, ease:"none"}}, 0);
tl.fromTo("#neb1", {{scale:1, opacity:.85}}, {{scale:1.12, opacity:1, duration:{beat["dur"]:.1f}, ease:"sine.inOut"}}, 0);
tl.fromTo("#neb2", {{scale:1.05, opacity:.8}}, {{scale:.95, opacity:1, duration:{beat["dur"]:.1f}, ease:"sine.inOut"}}, 0);
{stars_tl(beat["dur"])}
{TL[beat["viz"]]}
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body>
</html>
"""


def main():
    os.makedirs(PROJECT, exist_ok=True)
    shutil.copy(os.path.join(RENDER, "gsap.min.js"), os.path.join(PROJECT, "gsap.min.js"))
    shutil.copytree(os.path.join(RENDER, "project", "assets"),
                    os.path.join(PROJECT, "assets"), dirs_exist_ok=True)
    with open(os.path.join(PROJECT, "hyperframes.json"), "w", encoding="utf-8") as f:
        json.dump({"$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
                   "paths": {"blocks": "compositions", "components": "compositions/components",
                             "assets": "assets"}}, f, indent=2)
    for i, b in enumerate(BEATS):
        p = os.path.join(PROJECT, f"{b['id']}.html")
        with open(p, "w", encoding="utf-8") as f:
            f.write(build(b, i))
        print(f"wrote {p}  ({b['dur']}s, viz={b['viz']}, keyword={b['keyword']!r})")
    print("done: 8 beats v3 (black)")


if __name__ == "__main__":
    main()
