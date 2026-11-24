# Vibe 知识大赏工作流 — 一个知识点 → 一条代码动画短片

独立仓库，和 `fanpeter853-glitch/ai-video-pipeline` 分开管理。
那个仓库做真人 B-roll 口播长视频，这个仓库只做一件事：**把一个能画出来的知识点，
用 HTML / Canvas 代码逐帧渲染成竖屏动画短片，不用配音，配乐版即成片**。

目标：100% 免费基础档，0 成本；竖屏 1080×1920；中文；60–90 秒；
每句事实都有出处，不编数字；黑色系默认。

## 这是什么，不是什么

- 是：抖音 #Vibe知识大赏 那种做法的改编版——选题 → 查证 → 写稿 → 分镜 →
  代码成片（HyperFrames / Remotion）→ 配乐 → FFmpeg 拼合 → 验帧。
- 不是：剪辑软件，不是 AI 一键成片工具，不是真人出镜口播。
- 不是原仓库的原样复制：来源 `andyhuo520/vibe-knowledge`（MIT），
  但本仓库是**自己写的改编版**，见 `SOURCE.md`。

## 和 ai-video-pipeline 的分工

| 仓库 | 讲什么 | 画面怎么做 | 配音 |
|---|---|---|---|
| ai-video-pipeline | 个人经历、成长创业口播（A+B 路线） | Muse 生成真人 B-roll，单场景连续，尾帧当下一段首帧 | Peter 自己录 |
| vibe-knowledge-pipeline（本仓库） | 一个能画出来的知识点（概念、机制、原理） | HTML / Canvas 代码动画，逐帧渲染 | 不用配音，配乐版即成片 |

两条线不混用：讲经历用 B-roll，讲知识点用代码动画。

## 7 步流程

```
Node 1 选题：3 秒内能不能让人先猜 / 先选？有没有贯穿全片的道具？有没有反转？
Node 2 查证：facts.md，每句事实（数字、人名、年份、引文）都要有一行出处，
             没出处的不上屏，分歧两说并列。脚本：scripts/check_facts.py
Node 3 写稿：按 6 种母版写旁白，优先猜谜概念片 / 痛点原理片；
             60–90 秒约 330–500 字（约 5.5 字/秒），先猜后讲、标题延后、
             一个主道具贯穿、结尾回问。脚本：scripts/vibe_write_script.py
Node 4 分镜：旁白拆成拍（beat），每拍画面只给关键词 / 数字 / 出处，
             每拍画面字 ≤ 8 字一组。脚本：scripts/split_storyboard.py
Node 5 代码成片：HyperFrames 做标题卡 / 步骤卡 / 关键概念卡，
                Remotion 做批量 / 动态模板（未实装，只作备选），
                黑色系默认，脚本 render/build_beats_v3.py。
                不装 Playwright / Chromium。见 docs/vertical-render.md
Node 6 配乐：只用免费、无版权纠纷、能发抖音的音乐，默认
                Scott Buckley《Undertow》（CC-BY 4.0，须署名），
                volume 0.35，1 秒淡入、最后 2 秒淡出；不用配音。
Node 7 拼合 + 验帧：FFmpeg 拼合画面 + 配乐（0.5 秒交叉淡化，
                1080×1920），全片抽帧检查烧录文字、字幕、数字和图表。
                脚本：scripts/stitch_ffmpeg.py
```

每一步都要 Peter 确认才能往下走：选题、旁白稿 + 分镜、成片，三次确认。

## 6 种母版（只留讲法，不搬原仓库的骨架文件）

1. 猜谜概念片：先给一道直觉题，再讲概念（抽象概念首选）
2. 两难选择片：换你选，你怎么选（历史事件、博弈、心理实验）
3. 痛点原理片：先讲一个疼的问题，再拆原理（提效工具、方法类首选）
4. 一条主线片：一个主角 / 一条线讲到底
5. 闯关片：一关一关过
6. 六面轮转片：一个概念六个面轮着讲

小号先用 1 和 3。

## 竖屏预设（默认，不用每次再定）

- 画幅：1080×1920，竖屏
- 风格：黑色系默认——深黑 / 炭黑 #0a0b10→#12141f，金色 #f5c04e、白色、青色点缀，
  三层同时动（底层星点漂移 + 光晕呼吸、中层每拍连续生长可视化、上层大字逐字出现）；
  浅色版（render/build_beats_v2.py）只作备选
- 画面字：每屏关键词 ≤ 8 字一组，同屏最多两组；整句交给屏上文案和字幕
- 配乐：不用配音，音乐版即成片；画面上不烧录英文，不烧录假数据
- 模板见 `skills/vibe-knowledge/VERTICAL_1080x1920.md`，
  骨架见 `skills/vibe-knowledge/templates/film_skeleton_vertical.html`

## 免费限制（硬约束，别绕过）

- 基础档 0 成本：代码画图 + 配乐（CC-BY 免费曲）+ FFmpeg，全部免费；不用配音。
- **Renoise 增强档全部去掉**：原仓库用 Renoise 生成配图和动态镜头，
  按积分收费，不进本仓库。
- **MiMo 默认配音全部去掉**：原默认是小米 MiMo 克隆 AI 音色，
  本仓库不设 MiMo，不存密钥，不用 AI 音色；配音板块已整个删掉，改为配乐板块。
- **强制默认 BGM 去掉**：原仓库强制每条都用同一首 BGM，
  本仓库不强制同一首；当前默认是 Scott Buckley《Undertow》（CC-BY 4.0，
  须署名），换曲要重新核实授权并写进 music.md。
- 示例视频、大体积样片、风格图不搬进仓库。

## 目录

```
pipeline_dag.json                  — 7 个节点的拓扑与数据传递
scripts/check_facts.py             — Node 2：校验 facts.md 有没有无出处事实
scripts/vibe_write_script.py       — Node 3：按钩子/痛点/方法/金句/互动拼旁白草稿
scripts/split_storyboard.py        — Node 4：旁白拆成拍，估算每拍时长
scripts/render_vertical.py         — Node 5：竖屏渲染前置检查（HyperFrames / Remotion 路线，不再要求 Playwright/Chromium）
render/build_beats_v3.py           — Node 5：v3 黑色版构建脚本（默认），HyperFrames 渲染 8 拍
render/build_beats_v2.py           — Node 5：v2 浅色版构建脚本（备选）
docs/skills.md                     — 重新找的 skill 对比：HyperFrames 已装，Remotion 备选，配乐来源说明
scripts/stitch_ffmpeg.py           — Node 7：FFmpeg 拼合，0.5 秒交叉淡化，1080×1920
scripts/check_no_paid.py           — 检查 scripts/ 和 templates/ 里有没有付费残留
skills/vibe-knowledge/ADAPTED_SKILL.md       — 改编版 skill 说明（从主工作流搬过来）
skills/vibe-knowledge/VERTICAL_1080x1920.md  — 竖屏预设（从主工作流搬过来）
skills/vibe-knowledge/SOURCE_INVENTORY.md     — 来源清单（从主工作流搬过来）
skills/vibe-knowledge/facts-template.md       — 事实清单模板（从主工作流搬过来）
skills/vibe-knowledge/SKILL.md                — 原仓库主 skill（已改编，见下）
skills/vibe-knowledge/references/             — 原仓库规范 7 份（已改编）
skills/vibe-knowledge/templates/              — facts / 旁白骨架 A–F / film 骨架（已改编）
skills/vibe-knowledge/kit/know.js             — 知识片组件库（已改编）
skills/vibe-knowledge/tools/                  — duration / cover_first / qa / new_film 等（已改编）
skills/vibe-knowledge/styles/                 — 基础风格 4 套：darkmath、minimal、starfield、paper

## 复制清单（2026-11-24，Peter 在看到风险说明后 16:55 确认继续）

从 `/tmp/vibe-compare/andyhuo520_vibe-knowledge` 复制，只进本仓库，不进主工作流。
复制后逐个文件做了改编，`scripts/check_no_paid.py` 检查通过。

复制了：
- `skills/vibe-knowledge/SKILL.md` 原文（删了 21 行付费相关行，见改编说明）
- `references/` 7 份：01 六种母版、02 精品标准、05 发布包、07 组件库、
  10 代码音效、13 时长、14 踩坑（各删了 1–3 行付费相关行）
- `templates/facts.md`（原文，未改）、`templates/narration/A–F.json`
  （配音引擎改成 Peter 自己录；2026-11-24 v0.2.0：配音板块已删，改为配乐板块）、`templates/film.skeleton.js`
  （删了强制 BGM 那几行）、`templates/assets.json`（改写成代码资产清单）
- `kit/know.js`（459 行，只改了 2 行注释里的付费字样）
- `tools/` 7 个：duration.py、cover_first.py、earshot_render.py、
  patch_earshot.py、qa.py（删了强制 BGM 检查）、ocr.swift、
  new_film.py（删了强制 BGM 补丁和默认 AI 音色，cine 引擎缺失时会明说退出）
- `styles/` 4 套：darkmath、minimal、starfield、paper（各含 STYLE.md + still.jpg）

没复制（明确排除）：
- `tools/` 里的 bgm_force.py、fit_bgm.py、clip2frames.py、voice_post.py、
  welcome.py、recommend.py、style_reel.py、vision_layers.swift
- `references/` 里的 03、04、06、08、09、11、12（付费档、风格工作室等）
- `styles/` 其余 40 套、`assets/`（默认 BGM 和默认配音示例）、
  `docs/`、示例视频和大体积样片、`skills/ai-teardown/`（cine 引擎）
- 注意：`new_film.py` 和 `qa.py` 依赖的 cine 引擎和 macOS OCR（swiftc）
  本仓库不含，见 `docs/vertical-render.md`。

## 待办（2026-11-24）

- [x] 核心文件复制（2026-11-24，Peter 16:55 看到风险说明后确认继续）
- [x] GitHub 推送（2026-11-24，commit 6e364d6446e7d63872c3b04c3c27f1f451b4ac24，已回读核验）
- [x] 小号第一期 vibe 选题已定：人为什么会对某段回忆念念不忘（2026-11-24，稿子待 Peter 批）
- [x] 渲染路线已定：改用 HyperFrames / Remotion，不装 Playwright / Chromium（2026-11-24）
- [x] 渲染已跑通：HyperFrames 本机已装（render/package.json，hyperframes ^0.9.88），
  v3 黑色版已渲出（render/build_beats_v3.py → render/out_v3/v3_*.mp4）。
- [x] 小号第一期 vibe 的旁白稿 + 分镜，Peter 2026-11-24 20:30 已批。
- [x] 渲染板块已改成 HyperFrames / Remotion，配音板块已删、改为配乐板块（2026-11-24，
  Peter 确认），DAG 已升到 0.2.0。
- [ ] Remotion 模板未实装：本仓库目前只有 HyperFrames 实装，Remotion 只作批量模板备选。

## 跑一遍（占位示例）

```bash
cd ~/workspace/vibe-knowledge-pipeline
python3 scripts/check_facts.py --facts examples/01-placeholder/facts.md
python3 scripts/vibe_write_script.py --topic "[待填]" --hook "[待填]" --pain "[待填]" \
  --method "[待填]" --key-line "[待填]" --interaction "[待填]" \
  --out examples/01-placeholder/narration.md
python3 scripts/split_storyboard.py --narration examples/01-placeholder/narration.md \
  --out examples/01-placeholder/storyboard.json
python3 scripts/render_vertical.py --film skills/vibe-knowledge/templates/film_skeleton_vertical.html
python3 scripts/check_no_paid.py
```

`render_vertical.py` 现在只做前置检查：film 在不在、是不是 1080×1920，
再打印 HyperFrames / Remotion 的下一步。HyperFrames 本机已装（render/package.json），
v3 已按 render/build_beats_v3.py 渲出。Playwright / Chromium 不装了。

## 第一期（2026-11-24，稿子已批，v3 黑色带音乐版即成片，不用配音、未发布）

- 选题：人为什么会对某段回忆念念不忘
- 账号：小号，vibe 代码动画路线
- 母版：A 猜谜概念片
- 旁白：293 字（不含标点），约 60.6 秒（按 5.5 字/秒估算），文件在 `examples/01-placeholder/narration.md`
- 事实：`examples/01-placeholder/facts.md`，6 行都有出处，`check_facts.py` 通过；未采用的数字（2–3 倍、63%、90% / 两倍）已列在 facts.md 的“未采用”一节，不进稿子
- 分镜：`examples/01-placeholder/storyboard.json`，8 拍，合计 60.6 秒，画面关键词每组 ≤8 字
- 贯穿道具：一颗小光点，每想一次就亮一点（为示意，不是真实大脑照片）

## GitHub

仓库：`fanpeter853-glitch/vibe-knowledge-pipeline`（Public，main 分支）
https://github.com/fanpeter853-glitch/vibe-knowledge-pipeline

来源：`andyhuo520/vibe-knowledge`（MIT，Copyright (c) 2026 Berryxia），
改编说明见 `SOURCE.md` 和 `LICENSE`。
