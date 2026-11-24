# 重新找 skill（2026-11-24，Peter 确认改工作流时重找）

范围：只找贴合新工作流（HyperFrames 渲染、Remotion 批量模板、免费配乐选曲/混音）
的三类。优先免费开源、能竖屏 1080×1920、不要付费 API、不要 AI 配音。
星数和协议是 2026-11-24 用 GitHub API 当天核实的，不是照抄旧数字。

## 对比（5 个候选）

| # | 候选 | 星数（2026-11-24） | 协议 | 能不能直接用 | 结论 |
|---|---|---|---|---|---|
| 1 | heygen-com/hyperframes（HyperFrames 官方 skill） | 89,298 | Apache-2.0 | 能。HTML/CSS/GSAP 写画面，逐帧渲染成 MP4；Node 22+、FFmpeg；本地免费，无按次收费 | **已装进工作流**：`skills/hyperframes/SKILL.md`（核心）+ `media-use-SKILL.md`（配乐/混音），`render/package.json` 里 `hyperframes ^0.9.88`，v3 就是用它渲的 |
| 2 | remotion-dev/remotion | 75,367 | NOASSERTION（源代码公开，Remotion License：个人 / ≤3 人免费，4 人以上要公司许可） | 能，但重。React 写模板，批量换文案很合适；本仓库目前没有 Remotion 模板，装了也用不上 | **备选，不装**。只在 DAG Node 5 里留了分工，要写批量模板时再装 `remotion-dev/skills` |
| 3 | remotion-dev/skills（Remotion 官方 agent skill） | 7,924 | 无（None） | 能，配合上条用 | **不装**，同上，写 Remotion 模板时再装 |
| 4 | Scott Buckley 音乐库（配乐来源，不是 skill） | —（音乐库） | CC-BY 4.0 | 能。免费、可商用、可改编，条件是必须署名 | **已用**：默认曲《Undertow》，见 `examples/01-placeholder/music.md`；换曲要重新核实授权 |
| 5 | Pixabay Music / Free Music Archive 等免费音乐库（配乐来源，不是 skill） | — | 每首曲子协议不同，要逐首核实 | 不能直接当 skill 用 | **不装**。只作选曲时的来源，逐首核实；已弃用的两首（Pixabay《Deep in Memory》PRS/Content ID、Otomusu《Remembrance at Dusk》疑似 AI 生成）见 music.md |

## 本地 skill 库里没有的

用 `muse.skill_search` 在 Muse 自带 skill 库里找过 HyperFrames / Remotion /
免费配乐，没有贴合的 skill（只返回了 ai_long_video_workflow、music_discovery
等不相关的）。所以上面 1、2、3 都是 GitHub 官方 skill，不是本地库里的。

## 装了什么，没装什么

- 装了：HyperFrames 官方 skill 核心两份，原文从
  `https://github.com/heygen-com/hyperframes`（main 分支，2026-11-24）取回，
  未改内容，来源见 `skills/hyperframes/SOURCE.md`。
  - `skills/hyperframes/SKILL.md`（7,722 字节）：渲染合同和工作流，先读这份。
  - `skills/hyperframes/media-use-SKILL.md`（5,491 字节）：配乐、音效、混音。
  - 注意：skill 原文里写着首次使用前要发一次 usage note（`npx hyperframes events`），
    本仓库没有跑这条，也没有登录 HeyGen 账号，只用本地渲染，不发 telemetry。
  - `npx skills add heygen-com/hyperframes` 官方安装命令在本机跑了 120 秒没完成
    （交互提示未走完），所以改成直接从 GitHub raw 取回上面两份 SKILL.md；
    渲染本身用的就是本地已装的 `hyperframes ^0.9.88`，不受影响。
- 没装：Remotion（本体 + skill）、Renoise / MiMo / 任何付费档、任何 AI 配音。
  Remotion 只在 DAG 里留了分工，不装、不写模板、不假装已有。

## 下次换 skill 怎么走

1. 先按上面这张表比星数、协议、能不能竖屏、要不要付费 API、要不要 AI 配音。
2. 选中的才取回 SKILL.md 原文放进 `skills/<名字>/`，加 `SOURCE.md` 写清来源、
   星数、协议、取回日期、改了什么。
3. 不合适的不要全装进来；装完要在 `pipeline_dag.json` 里写清它负责哪个 Node。
