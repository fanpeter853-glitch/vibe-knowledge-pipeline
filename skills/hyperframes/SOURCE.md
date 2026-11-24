# HyperFrames 官方 skill — 来源说明

- 来源仓库：`heygen-com/hyperframes`
- 地址：https://github.com/heygen-com/hyperframes
- 协议：Apache-2.0
- 星数：89,298（2026-11-24，GitHub API 当天核实）
- 创建：2026-03-10；最后推送：2026-11-24
- 取回日期：2026-11-24，直接从 main 分支 raw 取回，未改内容。
- 本目录文件：
  - `SKILL.md`（7,722 字节）：核心 skill，渲染合同和工作流，先读这份。
  - `media-use-SKILL.md`（5,491 字节）：配乐、音效、混音（`skills/media-use/SKILL.md` 原文）。
- 本仓库的渲染实装：`render/package.json`（`hyperframes ^0.9.88`，`gsap ^3.13.0`），
  构建脚本 `render/build_beats_v3.py`（v3 黑色版，默认）、`render/build_beats_v2.py`（浅色备选）。
- 注意：skill 原文里写着首次使用前要发一次 usage note（`npx hyperframes events`），
  本仓库没有跑这条，也没有登录 HeyGen 账号，只用本地渲染。
- `npx skills add heygen-com/hyperframes` 官方安装命令在本机跑了 120 秒没完成，
  所以改成直接取回上面两份 SKILL.md；渲染本身用的就是本地已装的 HyperFrames，不受影响。
- Remotion 没有装进本目录，只作批量模板备选，见 `docs/skills.md`。
