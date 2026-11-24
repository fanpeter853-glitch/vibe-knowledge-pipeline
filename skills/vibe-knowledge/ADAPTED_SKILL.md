# Vibe 代码动画路线 — 改编版（andyhuo520/vibe-knowledge，只取核心）

> 2026-11-24 v0.2.0 改动（Peter 确认）：配音板块已删、改为配乐板块（默认 Scott Buckley《Undertow》，CC-BY 4.0，须署名）；渲染改为 HyperFrames / Remotion，黑色系默认，脚本 render/build_beats_v3.py；不装 Playwright / Chromium。本文件其余“自己配音 / Playwright 待验证”说法是首次改编时的历史记录，以 v0.2.0 和 pipeline_dag.json 0.2.0 为准。

> 状态：**改编文档已写好，原仓库代码文件未复制、未运行、未安装。**
>
> 原因：2026-11-24 在处理 `/tmp/vibe-compare/andyhuo520_vibe-knowledge` 时，系统执行风险检查未通过。
> 那批克隆内容在处理时可能运行代码。按安全规则，不能直接运行、复制、安装它，
> 也不能把它放进工作流、配置或 PATH。
> Peter 在 2026-11-24 16:51 已确认“装 andyhuo520，只取核心，去掉 Renoise 和 MiMo”，
> 但那次确认是在风险提示之前给的，不能当作“已知风险后仍同意复制代码”的确认。
> **下一步需要 Peter 在看到这条风险说明后，再用一句话明确确认是否继续复制代码。**
> 在那之前，本目录只放我自己写的改编说明，不放原仓库的任何代码、脚本、模板文件。

## 来源

- 仓库：`andyhuo520/vibe-knowledge`
- 地址：https://github.com/andyhuo520/vibe-knowledge
- 协议：MIT，Copyright (c) 2026 Berryxia (andyhuo520)，已只读核对 LICENSE 全文。
- 原定位：一个知识点 → 一条有旁白、每句有出处的精品知识短片，Claude Code skill。
- 原流程（只读核对 README / SKILL.md）：选题 → 查证 → 写稿 → 配音 → 代码成片 → 1080p60 → 质检 → 发布包。
- 本目录改编日期：2026-11-24。改编者：Muse（按 Peter 的工作流约束改写，非原作者）。

## 原仓库里有什么（只读清单，不代表已复制）

- `skills/vibe-knowledge/SKILL.md`：主 skill 说明，默认 16:9 1080p60，时长由用户定。
- `skills/vibe-knowledge/references/`：14 份规范，包括 01 六种母版、02 精品标准、04 Renoise、08 两档制作、09 风格工作室、13 时长、14 踩坑等。
- `skills/vibe-knowledge/styles/`：44 套风格，8 个家族，另有 `catalog.json` 和 `INDEX.md`。
- `skills/vibe-knowledge/kit/know.js`：知识片组件库。
- `skills/vibe-knowledge/tools/`：new_film.py、recommend.py、qa.py、fit_bgm.py、cover_first.py、duration.py 等，另有 `ocr.swift`、`vision_layers.swift`。
- `skills/vibe-knowledge/templates/`：`facts.md`、`assets.json`、`film.skeleton.js`、`narration/A–F.json`。
- `skills/vibe-knowledge/assets/`：默认 BGM `vibe-bgm.m4a`、默认配音示例。
- `skills/ai-teardown/`：cine 渲染引擎，另需 Python（numpy / scipy / pillow / playwright）、ffmpeg、swiftc（OCR）。
- `docs/`：封面、风格墙、试听音频；样片在 Release v1.0.0，不在工作流里。

完整只读清单见本目录 `SOURCE_INVENTORY.md`。

## 改编：去掉了什么

以下全部去掉或明确禁用，不进入工作流：

1. **Renoise 增强档全部去掉。** 原仓库的增强档用 Renoise 生成配图和动态镜头，
   涉及 Midjourney / GPT Image / Wan 3.0 / Seedance 2.5 / Kling / Grok Video / Lyria / ElevenLabs 音效，
   按积分收费（原 README 举例：轻约 25–40，标准约 250–300，旗舰约 600–700 积分；
   商鞅立木增强版用了 246 积分）。Peter 的工作流是 100% 免费，付费档不进。
   凡是提到 Renoise、积分、增强档、`ENH = true`、Wan / Seedance 动态镜头的部分，
   在改编版里一律视为禁用。
2. **MiMo 默认配音全部去掉。** 原默认配音是小米 MiMo 克隆音色，默认音色是仓库自带的
   AI 声音“科技博主沉稳男声”，不是真人，语速 5.5–6 字/秒；密钥放 `MIMO_API_KEY`。
   改编版不设 MiMo，不存密钥，不用默认 AI 音色代替 Peter 自己配音。
3. **强制默认 BGM 去掉。** 原仓库强制每条视频都用同一首 `vibe-bgm.m4a`（112.9 BPM，160 秒），
   混音时没放 BGM 会自动补上。改编版不强制，BGM 由 Peter 在剪映里自己定，可无 BGM。
4. **示例视频 / 大体积样片不搬。** 原仓库约 141M，大部分是样片、风格图和 docs，
   不复制进工作流。
5. **横屏默认改掉。** 原默认 16:9 1080p60，改编版默认竖屏 1080×1920，见 `VERTICAL_1080x1920.md`。

## 改编：保留了什么

1. **选题三问：** 3 秒内能不能让人先猜 / 先选？有没有贯穿全片的道具？有没有反转？
2. **查证 facts.md：** 旁白和画面上的每一个数字、人名、年份、引文都要有一行出处；
   没有出处的不上屏；来源分级 T1 原始文献 / 官方 / 论文、T2 权威二手、T3 社区只能当线索；
   有分歧两说并列。这是原仓库最值得保留的部分，也和 Peter“不编数字”一致。
3. **六种母版，全部保留，小号先用两种：**
   - A 猜谜概念片：一个抽象概念，先给直觉题，再点题，再用量化小游戏、两个例子、亲身体验、尺度拉大、回环收尾。
   - B 两难选择片：历史事件 / 博弈 / 心理实验，先讲离奇事实，再问“换你怎么办”，再讲前情、经过、等待、揭晓、反转、对照、回问。
   - C 痛点原理片：日常困扰 × 冷门原理，一个贯穿道具，代入观众，3 秒能做的解法，治愈收尾。
   - D 一条主线片：多个碎片其实有一条线，依次穿过 5–7 个节点，收成网 / 树。
   - E 闯关片：考试题型 / 方法论，冒险地图，每关题干、陷阱、正解、秘籍卡，最后总表。
   - F 六面轮转片：一个问题六种答案，每种人名、书名、年份加一句原话，45–60 秒。
   - 小号第一期先用 A 或 C，其他四种以后再试。
4. **母版共用规则：** 前 3 秒让观众参与，不先上标题、不先自我介绍；标题延后；
   一个主道具贯穿全片；画面字只放关键词（≤8 字）、数字、出处，整句交给旁白和字幕；
   每章一句金句收尾；结尾回扣开头，把问题交回观众。
5. **对抗审查：** 写完旁白后逐条自查钩子、出处、字数，改完再往下走。
   原仓库的做法是子 agent 对抗审查；改编版在 Muse 这里就是人工逐条对 facts.md 核对。
6. **三个确认点：** 确认 1 选题 / 母版 / 时长 / 风格；确认 2 看旁白稿加分镜，同意后才生成；
   确认 3 看成片，再出发布包。确认 2 之前不生成，确认 3 之前不发布。

## 改编：改了什么（适配 Peter 的工作流）

- **画幅：** 16:9 1080p60 → 竖屏 1080×1920 优先，横屏只当备选。
- **配音：** MiMo 克隆音色 → Peter 自己配音优先。旁白稿按分段录音单拆，
  录好后用工作流 Node 4 的 `tts_muse.py --probe-only` 或 VoiceStudio 本地克隆
  生成 `durations.json`，时间线以真实录音时长为准。没有录音时不默认用 AI 音色顶替。
- **时长：** 原仓库一期 45 秒–5 分钟，按复杂度给四档。改编版小号先按 60 秒左右、
  约 250–330 字起步（原 2 分钟工作流是 400–500 字，vibe 第一期先短一点跑通），
  跑通后再决定是否拉长到 2 分钟。
- **画面：** 原仓库是代码逐帧渲染（cine / know.js）。改编版分两条路，
  不要混用：
  - 路线 1（现有）：Muse 自带生成真人 B-roll，单场景连续，尾帧当下一段首帧，
    讲个人经历 / 口播。
  - 路线 2（本 skill）：代码动画讲能画出来的知识点，画面是 SVG / 粒子 / 数据组件，
    不用真人出镜，不用 B-roll 连续性那套。
  - 第一期 vibe 只走路线 2，不要把两条路拼在同一条视频里。
- **风格：** 原 44 套全搬 → 改编版先只留适合竖屏、中文、浅色 / 深色数学 / 暗金线描这类
  能讲干货的少量风格，具体选哪套等第一期知识点定了再定，不要一次全搬。
  增强档风格（敦煌、青花、木刻、半调拼贴、长卷、铜版博物）一律不选，因为它们要生图。
- **渲染：** 原仓库要装 ai-teardown 的 cine 引擎、Playwright / Chromium、swiftc。
  本机目前未确认已装 Playwright / Chromium（上一轮汇报说未装），
  所以本改编版目前只做到“选题 → 查证 → 写稿 → 分镜”这四步能跑，
  代码成片渲染那步是待验证的，不要谎称已跑通。

## 使用步骤（Node 8，附录路线）

1. 定知识点加一句话角度（Peter 定，例如“一个能画出来的外贸 / AI 概念”）。
2. 建 `facts.md`：每句事实一行出处，分级 T1 / T2 / T3，分歧两说并列，示意画面标注。
3. 选母版（先 A 或 C），按母版骨架写旁白稿，字数按目标秒数 × 5.5 字/秒估算，
   再按 Peter 自己配音的实际语速校准，不要编数字。
4. 出分镜：每拍画面只写关键词 / 数字 / 出处，整句交给旁白。
5. Peter 看旁白稿加分镜，确认后才往下走。
6. 代码成片（v0.2.0：HyperFrames / Remotion，黑色系默认，render/build_beats_v3.py）。
7. 配乐（v0.2.0：不用配音，音乐版即成片），FFmpeg 拼合画面 + 配乐，验帧，检查烧录文字、字幕、数字、图表。
8. 确认后才发布，发布时勾选 / 标注 AI 生成。

## 还缺什么（截至 2026-11-24，未跑通的部分）

- 原仓库代码文件未复制：`SKILL.md` 原文、`references/`、`styles/`、`kit/know.js`、
  `tools/*.py`、`templates/film.skeleton.js`、`assets/` 均未进工作流。
- 本机 Playwright / Chromium 是否已装：上一轮汇报说未装，本轮未再用 exec 验证，
  渲染跑不通是已知缺口，不要强行安装浏览器或绕过。
- cine 引擎（ai-teardown）未装，未验证。
- 小号第一期 vibe 的知识点加一句话角度：Peter 还没定。
- 实际复制代码的最终确认：需要 Peter 在看到执行风险说明后，再明确一句话确认。

## 许可与署名

- 原代码 MIT，Copyright (c) 2026 Berryxia (andyhuo520)。
- 本改编文档是我方原创改写，引用来源已注明；如后续复制原代码文件，
  须保留原 LICENSE 和版权声明。
- 原仓库的示例视频、AI 生成配图、默认 BGM 与默认音色的说明见原仓库 `NOTICE.md`；
  第三方组件见 `THIRD_PARTY.md`。
