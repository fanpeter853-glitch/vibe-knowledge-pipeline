# 竖屏渲染：HyperFrames / Remotion 路线（2026-11-24，Peter 已定；2026-11-24 v0.2.0 写回工作流）

## 决定

渲染用 HyperFrames / Remotion，不用配音，音乐版即成片。
不装 Playwright / Chromium，不装 cine 引擎。

## 分工

| 画面 | 用哪个 | 怎么做 |
|---|---|---|
| 标题卡、步骤卡、关键概念卡（静态卡 + 简单动效） | HyperFrames（默认，已实装） | 写 HTML / CSS（GSAP 动效），照竖屏骨架 `skills/vibe-knowledge/templates/film_skeleton_vertical.html`（1080×1920）做一页，渲染成 MP4 片段。实装脚本：`render/build_beats_v3.py`（v3 黑色版，默认）、`render/build_beats_v2.py`（v2 浅色版，备选） |
| 需要批量换文案、需要动态模板（比如同一套卡换多条、进度条、计数器） | Remotion（备选，未实装） | 用 React 写一个模板，只换文案和数字，渲染成 MP4 片段。本仓库目前还没有 Remotion 模板，要用时再按 `remotion-dev/skills` 写，不要假装已有 |
| 拼合 | FFmpeg | `scripts/stitch_ffmpeg.py`，0.5 秒交叉淡化，1080×1920 |
| 声音 | 配乐，不用配音 | 默认 Scott Buckley《Undertow》（CC-BY 4.0，须署名），见 Node 6 / `examples/<期>/music.md` |

## 黑色系默认模板（v3，第一期已验证）

- 底：深黑 / 炭黑 `#0a0b10 → #12141f` 渐变，不纯黑死黑，加微弱金色 / 青色光晕。
- 主色：金色 `#f5c04e`、白色正文 `#f7f3e8`、青色点缀 `#63d8d2`、朱砂 `#e0705f` 少量。
- 三层同时动：底层 36 颗星点漂移闪烁 + 两团星云光晕呼吸 + 点阵底纹；
  中层主可视化连续生长（连线、涟漪、碎片拼合、圆环、曲线、投票条）；
  上层大字逐字出现、小字逐行淡入、拍号 / 进度条同步动。
- 版式每拍换一种排布，舞台占满竖屏。
- 浅色版（暖纸）只作备选，见 `render/build_beats_v2.py`。

## 转场限制（说实话）

HyperFrames 是按拍分别渲染再拼合，**不是**单画布连续变形。
拍与拍的连续只能靠主光点起止位置衔接 + 0.5 秒交叉淡化近似，
做不到单画布像素级连续变形；淡化中间 0.5 秒两拍文字会叠影，属正常转场。

## 本仓库现在的状态（2026-11-24，实测）

- 有：竖屏骨架、组件库 `skills/vibe-knowledge/kit/know.js`、前置检查
  `scripts/render_vertical.py`（HyperFrames / Remotion 路线，不再要求 Playwright）。
- 有：Node v24.22.1、FFmpeg、HyperFrames 本机已装（`render/package.json`，
  `hyperframes ^0.9.88`，`gsap ^3.13.0`），v3 已渲出：
  `render/build_beats_v3.py` → `render/out_v3/v3_*.mp4` → 拼合后
  `examples/01-placeholder/final_v3_black_with_music_1080x1920.mp4`（57.1 秒）。
- 缺：Remotion 模板未实装（只有分工和 skill 来源，见 `docs/skills.md`）。
- 不装：Playwright（Python 包）、Chromium / Chrome、cine 引擎。
  原仓库的浏览器逐帧截图路线已废弃，不要再按那条走。

## 下一步怎么做（每期）

1. 按分镜表，把每一拍写成一页 HyperFrames HTML（关键词 ≤8 字一组，
   同屏最多两组，脚注写出处，示意画面标“为示意”），黑色系默认。
2. 需要批量 / 动态的拍，改成 Remotion 模板，只换文案。
3. 每页渲染成 MP4 片段，再用 `scripts/stitch_ffmpeg.py` 拼合（0.5 秒交叉淡化）。
4. 加配乐（Node 6），全片抽帧验烧录文字、数字和图表，再听一遍配乐音量。
