# 竖屏渲染：怎么做、缺什么

## 目标

把 `film.js` / film HTML 按竖屏 1080×1920 逐帧渲染成视频片段，
再用 `scripts/stitch_ffmpeg.py` 拼合。

## 原仓库的做法（本仓库不含）

原仓库复用另一个 skill（ai-teardown）的 cine 引擎：
浏览器逐帧截图 + `record.py` / `stills.py` / `finish.py`，
另需 Python（numpy / scipy / pillow / playwright）、ffmpeg、swiftc（OCR）。
本仓库**不含 cine 引擎**，也没有复制它的代码。

## 本仓库现在的状态（2026-11-24）

- 有：竖屏骨架 `skills/vibe-knowledge/templates/film_skeleton_vertical.html`
  （1080×1920，自己写的）、组件库 `skills/vibe-knowledge/kit/know.js`
  （已改编，去掉了付费相关注释）、前置检查 `scripts/render_vertical.py`。
- 缺：Playwright（Python 包）和 Chromium / Chrome（浏览器）。
  本机检查结果：`python3 -c "import playwright"` 报错 ModuleNotFoundError，
  `which chromium chromium-browser google-chrome` 什么都没找到。
  所以 `scripts/render_vertical.py` 现在会直接报错说渲染跑不通，
  不会假装出片。

## 接下来二选一（等 Peter 定）

1. **装 Playwright + Chromium**：在本机装好后，用浏览器打开 film HTML，
   按时间逐帧截图，再用 FFmpeg 合成视频。这是原仓库的路线，
   改动最小，但要装浏览器。
2. **改用 HyperFrames / Remotion**：Peter 已经试过这两条，
   HTML / React 代码渲染成 MP4，和 vibe 的“代码成片”是同一类做法，
   而且和小号已定的浅色步骤卡模板更贴。改动稍大，但不用再装 cine 引擎。

在定下来之前，不要承诺渲染能跑通。
