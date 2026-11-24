#!/usr/bin/env python3
"""Build the 8 beat compositions for vibe EP01 — v2 (richer visuals).

EP01: 人为什么会对某段回忆念念不忘（母版 A 猜谜概念片，小号）
Style: paper （浅色暖纸、点阵、墨 + 朱砂点缀），竖屏 1080x1920。
贯穿道具：一颗金色小光点，每想一次就亮一点（示意动画，不是真实大脑照片）。
无真人出镜、无照片、无实拍。纯代码动画（HTML/CSS/GSAP + HyperFrames）。

v2 相对 v1 的改动（Peter：画面太单调）：
- 每拍都有一个全程在动的可视化，不再是“亮一下就静止”：
  B01 光点 + 5 颗轨迹小点依次亮起；B02 光点连线成网；B03 涟漪三连扩
  + 绕转小点；B04a 标签盖章 + 情绪强度条注满；B04b 碎片拼合→散开→再拼合
  （循环两次）；B04c 缺口圆环旋转 + 虚线弧画出又收回；B05 记忆曲线画出，
  光点沿曲线走；B06 两颗光点 + 投票条轻轻起伏。
- 背景每拍有细微变化（点阵密度/透明度、暖色晕位置与色调、角落图形），
  但保持同一浅色系、不换场景。
- 全片加了 8 颗缓慢漂移的环境小点 + 暖色晕缓慢呼吸，任何一帧都不静止。
- 版式用满竖屏：舞台区、关键词、副标题、说明行/芯片、脚注、进度条分层排布，
  不再上下大片留白。
- 拍号芯片（01/08）放右上角；每拍说明行/芯片每组 ≤8 字；示意画面标「画面为示意」。
GSAP 本地打包（render/gsap.min.js），渲染不依赖 CDN。
所有动效都用绝对时间写在一条 paused timeline 上，HyperFrames 可逐帧 seek。

Usage:
  python3 render/build_beats_v2.py
  -> writes render/project/b01.html ... b06.html
"""
import json
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RENDER = os.path.join(ROOT, "render")
PROJECT = os.path.join(RENDER, "project")

BEATS = [
    dict(id="b01", dur=6.7, num="01", kicker="想一想", keyword="那段回忆",
         sub="像昨天一样", detail="过去很久了", chips=[],
         foot="", note="", viz="trail",
         tint="#d9a441", tint2="#f3ead8", grid="48px", gop="0.10"),
    dict(id="b02", dur=4.4, num="02", kicker="点题", keyword="念念不忘",
         sub="为什么？", detail="反差背后有原因", chips=[],
         foot="", note="", viz="net",
         tint="#c96a3b", tint2="#f6e8d5", grid="40px", gop="0.08"),
    dict(id="b03", dur=8.4, num="03", kicker="痛点", keyword="越想越牢",
         sub="越讲越记得牢", detail="", chips=["越想忘", "越忘不掉"],
         foot="来源：Roediger & Karpicke 2006", note="画面为示意", viz="ripples",
         tint="#b23a2e", tint2="#f3e2d2", grid="56px", gop="0.12"),
    dict(id="b04a", dur=8.2, num="04", kicker="第一", keyword="情绪贴标签",
         sub="越强 存得越牢", detail="", chips=["情绪越强", "存得越牢"],
         foot="来源：Cahill & McGaugh 1998", note="画面为示意", viz="tag",
         tint="#b23a2e", tint2="#f5e6cf", grid="44px", gop="0.09"),
    dict(id="b04b", dur=10.2, num="05", kicker="第二", keyword="每次重写",
         sub="清晰≠准确", detail="", chips=["细节会变", "感觉留下"],
         foot="来源：Talarico & Rubin 2003", note="画面为示意", viz="fragments",
         tint="#8a6d3b", tint2="#f3ead8", grid="52px", gop="0.11"),
    dict(id="b04c", dur=9.1, num="06", kicker="第三", keyword="没说完的事",
         sub="不一定都成立", detail="", chips=["没做完", "更容易记住"],
         foot="来源：Zeigarnik 1927；2025 系统综述", note="画面为示意", viz="openring",
         tint="#7a7a5a", tint2="#f2ecd8", grid="48px", gop="0.10"),
    dict(id="b05", dur=7.1, num="07", kicker="金句", keyword="忘不掉的是情绪",
         sub="和一次次想起的你", detail="不是那件事本身", chips=[],
         foot="", note="画面为示意", viz="curve",
         tint="#d9a441", tint2="#f6e3c2", grid="44px", gop="0.08"),
    dict(id="b06", dur=6.5, num="08", kicker="回问", keyword="打1还是打2",
         sub="开心多 / 难过多", detail="", chips=["1 开心多", "2 难过多"],
         foot="", note="", viz="two",
         tint="#d9a441", tint2="#f3ead8", grid="48px", gop="0.10"),
]

CSS = """
:root { --paper1:#fbf7ee; --ink:#2a2420; --muted:#7d7266;
        --cinnabar:#b23a2e; --gold:#d9a441; }
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:1080px; height:1920px; overflow:hidden; background:#fbf7ee; }
#root { width:1080px; height:1920px; position:relative; overflow:hidden;
  background:linear-gradient(180deg, #fbf7ee 0%, var(--tint2) 100%);
  font-family:"Noto Sans CJK SC",sans-serif; color:var(--ink); }
#root::before { content:""; position:absolute; inset:0;
  background-image:radial-gradient(rgba(42,36,32,var(--gop)) 1.5px, transparent 1.5px);
  background-size:var(--grid) var(--grid); }
.wash { position:absolute; width:980px; height:980px; border-radius:50%;
  background:radial-gradient(circle, var(--tint) 0%, rgba(217,164,65,0) 65%);
  opacity:.20; left:50px; top:330px; }
.wash2 { position:absolute; width:620px; height:620px; border-radius:50%;
  background:radial-gradient(circle, rgba(178,58,46,0.16) 0%, rgba(178,58,46,0) 65%);
  left:560px; top:1180px; }
.orn { position:absolute; border:3px solid rgba(42,36,32,0.22); }
.orn.c { width:64px; height:64px; border-radius:50%; left:880px; top:210px; }
.orn.s { width:54px; height:54px; left:110px; top:1520px; transform:rotate(12deg); }
.orn.t { width:0; height:0; border-left:34px solid transparent; border-right:34px solid transparent;
  border-bottom:58px solid rgba(42,36,32,0.20); border-top:0; left:930px; top:1500px; }
.kicker { position:absolute; left:90px; top:120px; font-size:42px; letter-spacing:14px;
  color:var(--cinnabar); font-weight:700; }
.beatnum { position:absolute; right:90px; top:120px; font-size:36px; letter-spacing:4px;
  color:var(--muted); font-weight:700; }
.beatnum b { color:var(--cinnabar); }
.stage { position:absolute; left:0; top:250px; width:1080px; height:760px; }
.dot { width:150px; height:150px; border-radius:50%; position:absolute;
  background:radial-gradient(circle at 38% 35%, #ffe9a8 0%, var(--gold) 45%, #b97f1e 100%);
  box-shadow:0 0 60px 30px rgba(217,164,65,0.55), 0 0 160px 80px rgba(217,164,65,0.25); }
.dot.small { width:44px; height:44px; box-shadow:0 0 24px 10px rgba(217,164,65,0.45); }
.dot.grey { background:radial-gradient(circle at 38% 35%, #e8e2d8 0%, #8a8175 55%, #5c554b 100%);
  box-shadow:0 0 40px 16px rgba(90,80,70,0.30); }
.ring { position:absolute; border:3px solid rgba(178,58,46,0.55); border-radius:50%; }
.frag { position:absolute; width:64px; height:64px; border-radius:50%;
  background:radial-gradient(circle at 38% 35%, #ffe9a8 0%, var(--gold) 60%, #b97f1e 100%);
  box-shadow:0 0 24px 8px rgba(217,164,65,0.45); }
.tag { position:absolute; background:var(--cinnabar); color:#fff;
  font-size:38px; font-weight:700; padding:12px 26px; border-radius:12px; }
.chip { display:inline-block; border:2px solid rgba(42,36,32,0.35); border-radius:999px;
  font-size:40px; padding:10px 28px; margin:0 12px; color:var(--ink); background:rgba(255,255,255,0.45); }
.chip.hot { background:var(--cinnabar); border-color:var(--cinnabar); color:#fff; }
.gauge { position:absolute; left:190px; top:640px; width:700px; height:26px; border-radius:13px;
  background:rgba(42,36,32,0.15); overflow:hidden; }
.gauge i { display:block; height:100%; width:0%; border-radius:13px;
  background:linear-gradient(90deg, var(--gold), var(--cinnabar)); }
.gaugelabel { position:absolute; left:190px; top:590px; font-size:36px; color:var(--muted); }
.votebar { position:absolute; left:190px; width:700px; height:30px; border-radius:15px;
  background:rgba(42,36,32,0.12); overflow:hidden; }
.votebar i { display:block; height:100%; border-radius:15px; }
.votebar.gold i { background:linear-gradient(90deg, #f0c268, var(--gold)); }
.votebar.grey i { background:linear-gradient(90deg, #b0a894, #8a8175); }
.votelabel { position:absolute; left:190px; font-size:40px; font-weight:700; }
.openring { width:260px; height:260px; border-radius:50%; position:absolute;
  border:12px solid var(--gold); border-top-color:transparent;
  box-shadow:0 0 40px rgba(217,164,65,0.35); }
.qmark { position:absolute; font-size:120px; font-weight:800; color:var(--cinnabar); }
.keyword { position:absolute; left:0; top:1050px; width:1080px; text-align:center;
  font-family:"Noto Serif CJK SC",serif; font-weight:800;
  font-size:112px; line-height:1.25; color:var(--ink); }
.sub { position:absolute; left:0; top:1270px; width:1080px; text-align:center;
  font-size:52px; color:var(--muted); letter-spacing:6px; }
.detail { position:absolute; left:0; top:1400px; width:1080px; text-align:center;
  font-size:46px; color:var(--ink); letter-spacing:4px; }
.chips { position:absolute; left:0; top:1400px; width:1080px; text-align:center; }
.foot { position:absolute; left:90px; bottom:150px; font-size:30px; color:var(--muted); }
.note { position:absolute; right:90px; bottom:150px; font-size:30px; color:var(--muted); }
.progress { position:absolute; left:90px; bottom:80px; display:flex; gap:18px; }
.progress i { width:34px; height:10px; border-radius:5px; background:rgba(42,36,32,0.18); }
.progress i.on { background:var(--cinnabar); }
.amb { position:absolute; width:18px; height:18px; border-radius:50%;
  background:radial-gradient(circle, rgba(217,164,65,0.85), rgba(217,164,65,0.15)); }
"""

# 环境小点：固定位置，缓慢漂移（每拍 8 颗）
AMB = [(120, 420), (950, 380), (180, 900), (920, 860), (90, 1150), (990, 1180), (300, 300), (760, 280)]

VIZ_HTML = {
    # B01：主光点居中，5 颗轨迹小点从左向右依次亮起
    "trail": (
        '<div class="dot" id="dot" style="left:465px;top:300px"></div>'
        + "".join(
            f'<div class="dot small" id="tr{i}" style="left:{150 + i * 170}px;top:560px;opacity:0"></div>'
            for i in range(5))
    ),
    # B02：中心光点 + 4 颗卫星点，SVG 连线画出
    "net": (
        '<svg width="1080" height="760" viewBox="0 0 1080 760" style="position:absolute;left:0;top:0">'
        '<line id="ln1" x1="540" y1="380" x2="240" y2="180" stroke="#b23a2e" stroke-width="5" stroke-dasharray="1000" pathLength="1000"/>'
        '<line id="ln2" x1="540" y1="380" x2="840" y2="180" stroke="#b23a2e" stroke-width="5" stroke-dasharray="1000" pathLength="1000"/>'
        '<line id="ln3" x1="540" y1="380" x2="240" y2="580" stroke="#d9a441" stroke-width="5" stroke-dasharray="1000" pathLength="1000"/>'
        '<line id="ln4" x1="540" y1="380" x2="840" y2="580" stroke="#d9a441" stroke-width="5" stroke-dasharray="1000" pathLength="1000"/>'
        '</svg>'
        '<div class="dot" id="dot" style="left:465px;top:305px"></div>'
        '<div class="dot small" id="sat1" style="left:218px;top:158px;opacity:0"></div>'
        '<div class="dot small" id="sat2" style="left:818px;top:158px;opacity:0"></div>'
        '<div class="dot small" id="sat3" style="left:218px;top:558px;opacity:0"></div>'
        '<div class="dot small" id="sat4" style="left:818px;top:558px;opacity:0"></div>'
    ),
    # B03：三重涟漪依次扩散 + 一颗绕转小点
    "ripples": (
        '<div class="ring" id="ring1" style="width:260px;height:260px;left:410px;top:250px;opacity:0"></div>'
        '<div class="ring" id="ring2" style="width:260px;height:260px;left:410px;top:250px;opacity:0"></div>'
        '<div class="ring" id="ring3" style="width:260px;height:260px;left:410px;top:250px;opacity:0"></div>'
        '<div class="dot" id="dot" style="left:465px;top:305px"></div>'
        '<div id="orbit" style="position:absolute;left:540px;top:380px;width:0;height:0">'
        '<div class="dot small" id="orb" style="left:190px;top:-22px"></div></div>'
    ),
    # B04a：标签盖章 + 情绪强度条注满，光点随之变亮变大
    "tag": (
        '<div class="dot" id="dot" style="left:465px;top:220px"></div>'
        '<div class="tag" id="tag" style="left:660px;top:300px;opacity:0">情绪</div>'
        '<div class="gaugelabel" id="glabel">情绪强度</div>'
        '<div class="gauge"><i id="gfill"></i></div>'
        '<div class="dot small" id="gdot1" style="left:190px;top:700px;opacity:0"></div>'
        '<div class="dot small" id="gdot2" style="left:480px;top:700px;opacity:0"></div>'
        '<div class="dot small" id="gdot3" style="left:770px;top:700px;opacity:0"></div>'
    ),
    # B04b：三块碎片拼合→成光点→散开→再拼合（循环两次）
    "fragments": (
        '<div class="frag" id="frag1" style="left:270px;top:200px"></div>'
        '<div class="frag" id="frag2" style="left:750px;top:200px"></div>'
        '<div class="frag" id="frag3" style="left:510px;top:560px"></div>'
        '<div class="dot" id="dot" style="left:465px;top:305px;opacity:0"></div>'
        '<div class="qmark" id="qm" style="left:700px;top:180px;opacity:0">？</div>'
    ),
    # B04c：缺口圆环旋转 + 虚线弧画出又收回 + 问号呼吸
    "openring": (
        '<div class="openring" id="openring" style="left:410px;top:250px"></div>'
        '<svg width="1080" height="760" viewBox="0 0 1080 760" style="position:absolute;left:0;top:0">'
        '<circle id="arc" cx="540" cy="380" r="180" fill="none" stroke="#b23a2e" stroke-width="6" '
        'stroke-dasharray="300 1000" pathLength="1300" stroke-linecap="round" transform="rotate(-90 540 380)"/>'
        '</svg>'
        '<div class="dot" id="dot" style="left:485px;top:325px;width:110px;height:110px"></div>'
        '<div class="qmark" id="qm" style="left:700px;top:180px;opacity:0">？</div>'
    ),
    # B05：记忆曲线画出，光点沿曲线走三段
    "curve": (
        '<svg width="1080" height="760" viewBox="0 0 1080 760" style="position:absolute;left:0;top:0">'
        '<path id="curve" d="M 120 600 C 320 200, 520 620, 700 300 S 920 260, 960 180" fill="none" '
        'stroke="#d9a441" stroke-width="7" stroke-linecap="round" stroke-dasharray="1000" pathLength="1000"/>'
        '</svg>'
        '<div class="dot" id="dot" style="left:45px;top:525px"></div>'
        '<div class="dot small" id="cd1" style="left:98px;top:578px;opacity:0"></div>'
        '<div class="dot small" id="cd2" style="left:678px;top:278px;opacity:0"></div>'
    ),
    # B06：两颗光点 + 两条投票条起伏
    "two": (
        '<div class="dot" id="dot" style="left:300px;top:220px"></div>'
        '<div class="dot grey" id="dot2" style="left:630px;top:220px"></div>'
        '<div class="votelabel" id="vl1" style="top:470px">1 开心多</div>'
        '<div class="votebar gold" style="top:530px"><i id="vb1" style="width:30%"></i></div>'
        '<div class="votelabel" id="vl2" style="top:600px">2 难过多</div>'
        '<div class="votebar grey" style="top:660px"><i id="vb2" style="width:30%"></i></div>'
    ),
}

# 每拍动效：绝对时间，paused timeline 可 seek；环境小点全程缓慢漂移。
TL = {
    "trail": (
        'tl.fromTo("#dot",{scale:.4,opacity:0},{scale:1,opacity:1,duration:1.0,ease:"power2.out"},0);'
        'tl.to("#dot",{scale:1.15,duration:2.2,ease:"sine.inOut",yoyo:true,repeat:1},1.2);'
        + "".join(
            f'tl.fromTo("#tr{i}",{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.5,ease:"back.out(2)"}},{1.0 + i * 0.7});'
            for i in range(5))
        + 'tl.to("#dot",{boxShadow:"0 0 110px 55px rgba(217,164,65,0.75)",duration:1.5},4.6);'
    ),
    "net": (
        'tl.fromTo("#dot",{scale:.5,opacity:0},{scale:1,opacity:1,duration:.7,ease:"back.out(1.6)"},0);'
        + "".join(
            f'tl.fromTo("#ln{i}",{{strokeDashoffset:1000}},{{strokeDashoffset:0,duration:.6,ease:"power2.out"}},{0.6 + (i - 1) * 0.35});'
            f'tl.fromTo("#sat{i}",{{opacity:0,scale:.3}},{{opacity:1,scale:1,duration:.5,ease:"back.out(2)"}},{0.9 + (i - 1) * 0.35});'
            for i in range(1, 5))
        + 'tl.to("#dot",{scale:1.12,duration:1.0,ease:"sine.inOut",yoyo:true,repeat:1},2.2);'
    ),
    "ripples": (
        'tl.fromTo("#dot",{scale:.6,opacity:0},{scale:1,opacity:1,duration:.7,ease:"power2.out"},0);'
        + "".join(
            f'tl.fromTo("#ring{i}",{{scale:.55,opacity:.9}},{{scale:1.9,opacity:0,duration:2.0,ease:"power1.out"}},{0.8 + (i - 1) * 2.2});'
            for i in range(1, 4))
        + 'tl.fromTo("#orbit",{rotation:0},{rotation:300,duration:7.2,ease:"none"},0.6);'
        + 'tl.to("#dot",{scale:1.1,duration:1.8,ease:"sine.inOut",yoyo:true,repeat:2},1.0);'
    ),
    "tag": (
        'tl.fromTo("#dot",{scale:.6,opacity:0},{scale:1,opacity:1,duration:.7,ease:"power2.out"},0);'
        'tl.fromTo("#tag",{opacity:0,y:24,rotate:-8,scale:.7},{opacity:1,y:0,rotate:0,scale:1,duration:.55,ease:"back.out(1.8)"},.8);'
        'tl.fromTo("#gfill",{width:"0%"},{width:"92%",duration:3.4,ease:"power1.inOut"},1.6);'
        'tl.fromTo("#gdot1",{opacity:0,scale:.4},{opacity:1,scale:1,duration:.4},2.2);'
        'tl.fromTo("#gdot2",{opacity:0,scale:.4},{opacity:1,scale:1,duration:.4},3.4);'
        'tl.fromTo("#gdot3",{opacity:0,scale:.4},{opacity:1,scale:1,duration:.4},4.6);'
        'tl.to("#dot",{scale:1.25,boxShadow:"0 0 110px 55px rgba(217,164,65,0.75)",duration:2.0,ease:"sine.inOut"},4.8);'
    ),
    "fragments": (
        # 第一轮拼合 0–3.2s：碎片聚到中心，成光点
        'tl.fromTo("#frag1",{x:0,y:0},{x:225,y:140,duration:1.1,ease:"power2.inOut"},0);'
        'tl.fromTo("#frag2",{x:0,y:0},{x:-225,y:140,duration:1.1,ease:"power2.inOut"},.15);'
        'tl.fromTo("#frag3",{x:0,y:0},{x:0,y:-220,duration:1.1,ease:"power2.inOut"},.3);'
        'tl.to(["#frag1","#frag2","#frag3"],{opacity:0,scale:.3,duration:.4},1.6);'
        'tl.to("#dot",{opacity:1,scale:1,duration:.7,ease:"back.out(1.6)"},1.9);'
        # 散开 3.4–5.2s：光点变淡，碎片回到原位
        'tl.to("#dot",{opacity:0,scale:.6,duration:.5},3.4);'
        'tl.to(["#frag1","#frag2","#frag3"],{opacity:1,scale:1,x:0,y:0,duration:.9,ease:"power2.inOut"},3.9);'
        'tl.fromTo("#qm",{opacity:0},{opacity:1,duration:.5},4.4);'
        # 第二轮拼合 5.4–8s：碎片再聚，光点再亮（每次重写）
        'tl.to("#frag1",{x:225,y:140,duration:1.1,ease:"power2.inOut"},5.4);'
        'tl.to("#frag2",{x:-225,y:140,duration:1.1,ease:"power2.inOut"},5.55);'
        'tl.to("#frag3",{x:0,y:-220,duration:1.1,ease:"power2.inOut"},5.7);'
        'tl.to(["#frag1","#frag2","#frag3"],{opacity:0,scale:.3,duration:.4},7.0);'
        'tl.to("#dot",{opacity:1,scale:1,duration:.7,ease:"back.out(1.6)"},7.3);'
        'tl.to("#qm",{opacity:0,duration:.5},7.6);'
    ),
    "openring": (
        'tl.fromTo("#openring",{rotate:220,opacity:0},{rotate:40,opacity:1,duration:1.3,ease:"power2.out"},0);'
        'tl.fromTo("#dot",{scale:.4,opacity:0},{scale:1,opacity:1,duration:.8,ease:"back.out(1.6)"},.9);'
        'tl.to("#openring",{rotation:"+=100",duration:3.4,ease:"sine.inOut"},1.8);'
        'tl.fromTo("#arc",{strokeDashoffset:1300},{strokeDashoffset:300,duration:2.6,ease:"power1.inOut"},2.0);'
        'tl.to("#arc",{strokeDashoffset:1300,duration:2.2,ease:"power1.inOut"},5.2);'
        'tl.fromTo("#qm",{opacity:0},{opacity:.9,duration:.6},2.4);'
        'tl.to("#qm",{opacity:.25,duration:1.2,yoyo:true,repeat:1},3.2);'
    ),
    "curve": (
        'tl.fromTo("#curve",{strokeDashoffset:1000},{strokeDashoffset:0,duration:3.6,ease:"power1.inOut"},0);'
        'tl.fromTo("#dot",{scale:.5,opacity:0},{scale:1,opacity:1,duration:.7,ease:"back.out(1.6)"},.4);'
        'tl.to("#dot",{x:210,y:-220,duration:1.4,ease:"power1.inOut"},.8);'
        'tl.to("#dot",{x:580,y:-300,duration:1.4,ease:"power1.inOut"},2.2);'
        'tl.to("#dot",{x:840,y:-420,duration:1.4,ease:"power1.inOut"},3.6);'
        'tl.fromTo("#cd1",{opacity:0,scale:.4},{opacity:1,scale:1,duration:.5},1.0);'
        'tl.fromTo("#cd2",{opacity:0,scale:.4},{opacity:1,scale:1,duration:.5},2.6);'
        'tl.to("#dot",{scale:1.15,duration:1.2,ease:"sine.inOut",yoyo:true,repeat:1},5.0);'
    ),
    "two": (
        'tl.fromTo("#dot",{scale:.4,opacity:0},{scale:1,opacity:1,duration:.7,ease:"back.out(1.6)"},0);'
        'tl.fromTo("#dot2",{scale:.4,opacity:0},{scale:1,opacity:1,duration:.7,ease:"back.out(1.6)"},.5);'
        'tl.fromTo("#vb1",{width:"30%"},{width:"68%",duration:2.0,ease:"power1.inOut"},1.0);'
        'tl.fromTo("#vb2",{width:"30%"},{width:"46%",duration:2.0,ease:"power1.inOut"},1.3);'
        'tl.to("#vb1",{width:"62%",duration:1.4,ease:"sine.inOut",yoyo:true,repeat:1},3.2);'
        'tl.to("#vb2",{width:"52%",duration:1.4,ease:"sine.inOut",yoyo:true,repeat:1},3.4);'
        'tl.to(["#dot","#dot2"],{scale:1.1,duration:1.2,ease:"sine.inOut",yoyo:true,repeat:1},3.0);'
    ),
}


def ambient_html(beat):
    return "".join(
        f'<div class="amb" id="amb{i}" style="left:{x}px;top:{y}px"></div>'
        for i, (x, y) in enumerate(AMB))


def ambient_tl(beat):
    parts = []
    for i, (x, y) in enumerate(AMB):
        dx = 30 if i % 2 == 0 else -30
        dy = -40 if i % 3 == 0 else 35
        parts.append(
            f'tl.fromTo("#amb{i}",{{x:0,y:0,opacity:.35}},'
            f'{{x:{dx},y:{dy},opacity:.7,duration:{beat["dur"]:.1f},ease:"sine.inOut"}},0);')
    parts.append(
        f'tl.fromTo(".wash",{{scale:1,opacity:.20}},'
        f'{{scale:1.07,opacity:.28,duration:{beat["dur"]:.1f},ease:"sine.inOut"}},0);')
    return "".join(parts)


def build(beat, idx):
    dots = "".join(
        '<i class="on"></i>' if i == idx else "<i></i>" for i in range(len(BEATS)))
    foot = f'<div class="foot">{beat["foot"]}</div>' if beat["foot"] else ""
    note = f'<div class="note">{beat["note"]}</div>' if beat["note"] else ""
    if beat["chips"]:
        chips_html = '<div class="chips" id="chips">' + "".join(
            f'<span class="chip{" hot" if j == 0 else ""}">{c}</span>'
            for j, c in enumerate(beat["chips"])) + "</div>"
    elif beat["detail"]:
        chips_html = f'<div class="detail" id="detail">{beat["detail"]}</div>'
    else:
        chips_html = ""
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
     data-duration="{beat["dur"]}" data-width="1080" data-height="1920"
     style="--tint:{beat["tint"]};--tint2:{beat["tint2"]};--grid:{beat["grid"]};--gop:{beat["gop"]}">
  <div class="wash" id="wash"></div>
  <div class="wash2"></div>
  <div class="orn c"></div><div class="orn s"></div><div class="orn t"></div>
  {ambient_html(beat)}
  <div class="kicker" id="kicker">{beat["kicker"]}</div>
  <div class="beatnum" id="beatnum"><b>{beat["num"]}</b> / 08</div>
  <div class="stage" id="stage">{VIZ_HTML[beat["viz"]]}</div>
  <div class="keyword" id="keyword">{beat["keyword"]}</div>
  <div class="sub" id="sub">{beat["sub"]}</div>
  {chips_html}
  {foot}{note}
  <div class="progress">{dots}</div>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
tl.fromTo("#kicker", {{opacity:0, y:-16}}, {{opacity:1, y:0, duration:.6, ease:"power2.out"}}, 0);
tl.fromTo("#beatnum", {{opacity:0}}, {{opacity:1, duration:.6}}, .2);
{ambient_tl(beat)}
{TL[beat["viz"]]}
tl.fromTo("#keyword", {{opacity:0, filter:"blur(10px)"}}, {{opacity:1, filter:"blur(0px)", duration:.7, ease:"power4.out"}}, .5);
tl.fromTo("#sub", {{opacity:0, y:18}}, {{opacity:1, y:0, duration:.6, ease:"power2.out"}}, 1.1);
tl.fromTo("#chips, #detail", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:.6, ease:"power2.out"}}, 1.5);
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
    shutil.copy(os.path.join(RENDER, "gsap.min.js"), os.path.join(PROJECT, "gsap.min.js"))
    with open(os.path.join(PROJECT, "hyperframes.json"), "w", encoding="utf-8") as f:
        json.dump({"$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
                   "paths": {"blocks": "compositions", "components": "compositions/components",
                             "assets": "assets"}}, f, indent=2)
    for i, b in enumerate(BEATS):
        p = os.path.join(PROJECT, f"{b['id']}.html")
        with open(p, "w", encoding="utf-8") as f:
            f.write(build(b, i))
        print(f"wrote {p}  ({b['dur']}s, viz={b['viz']}, keyword={b['keyword']!r})")
    print("done: 8 beats v2")


if __name__ == "__main__":
    main()
