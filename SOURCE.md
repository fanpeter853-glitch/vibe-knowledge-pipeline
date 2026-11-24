> 2026-11-24 v0.2.0 改动（Peter 确认）：配音板块已删、改为配乐板块；渲染改为 HyperFrames / Remotion，黑色系默认。本文件里旧的“自己配音”说法是 2026-11-24 首次改编时的历史记录，以 v0.2.0 为准。

# 来源与改编说明

## 来源

- 仓库：`andyhuo520/vibe-knowledge`
- 地址：https://github.com/andyhuo520/vibe-knowledge
- 协议：MIT，Copyright (c) 2026 Berryxia (andyhuo520)
- 原定位：一个知识点 → 一条有旁白、每句有出处的精品知识短片（抖音 #Vibe知识大赏）。
  原流程：选题 → 查证 → 写稿 → 配音 → 代码成片 → 1080p60 → 质检 → 发布包。
- 核对方式：只读核对了原仓库的 README / SKILL.md / LICENSE，
  以及 `/tmp/vibe-compare/andyhuo520_vibe-knowledge` 里 skills 目录的清单。
  没有运行原仓库的任何脚本。

## 本仓库改了什么

1. **Renoise 增强档全部去掉。** 原仓库的增强档用 Renoise 生成配图和动态镜头，
   涉及 Midjourney / GPT Image / Wan / Seedance / Kling / ElevenLabs 音效，
   按积分收费。Peter 的工作流是 100% 免费，付费档不进。
2. **MiMo 默认配音全部去掉。** 原默认配音是小米 MiMo 克隆 AI 音色，
   本仓库不设 MiMo，不存密钥，不用 AI 音色代替 Peter 自己配音。
3. **强制默认 BGM 去掉。** 原仓库强制每条视频都用同一首 BGM，
   本仓库不强制，BGM 由 Peter 在剪映里自己定，可无 BGM。
4. **横屏默认改掉。** 原默认 16:9 1080p60，改成本仓库默认竖屏 1080×1920。
5. **时长改短。** 原仓库一期 45 秒～5 分钟，本仓库小号先做 60–90 秒，
   约 330–500 字。
6. **渲染引擎依赖去掉。** 原仓库复用另一个 skill（ai-teardown）的 cine 引擎，
   另需 Python（numpy / scipy / pillow / playwright）、MiMo 密钥、Renoise MCP、
   ffmpeg、swiftc（OCR）。本仓库不依赖 cine，不依赖 MiMo / Renoise，
   渲染只要求浏览器逐帧截图 + FFmpeg（见 docs/vertical-render.md）。
7. **示例视频 / 大体积样片不搬。** 原仓库约 141M，大部分是样片、风格图和 docs，
   不复制进本仓库。

## 本仓库搬了什么（2026-11-24，Peter 16:55 看到风险说明后确认继续）

确认后才复制，只进本仓库，不进主工作流。复制清单见 README.md 的“复制清单”一节。
复制后逐个文件做了改编（删付费相关行、改竖屏、改自己配音），
`scripts/check_no_paid.py` 检查通过。

明确没搬的：
- `tools/` 里的 bgm_force.py、fit_bgm.py、clip2frames.py、voice_post.py、
  welcome.py、recommend.py、style_reel.py、vision_layers.swift
- `references/` 里的 03、04、06、08、09、11、12
- `styles/` 其余 40 套、`assets/`（默认 BGM 和默认配音示例）、
  `docs/`、示例视频和大体积样片、`skills/ai-teardown/`（cine 引擎）
- 本仓库不含 cine 引擎和 macOS OCR（swiftc），渲染路线待定，
  见 `docs/vertical-render.md`。

## 和 ai-video-pipeline 的关系

- `ai-video-pipeline`：真人 B-roll 口播长视频工作流（主号 A+B）。
- 本仓库：vibe 代码动画工作流（小号 AI 干货里讲知识点的那一期）。
- 两个仓库独立成套，互不覆盖。共用的只有同一套硬约束：
  100% 免费、自己配音、竖屏 1080×1920、不编数字、不擅自发布。
