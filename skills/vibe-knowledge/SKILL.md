> 强制默认 BGM 相关内容；默认改成竖屏 1080×1920、Peter 自己配音。
> 原文见上游 andyhuo520/vibe-knowledge（MIT）。

---
name: vibe-knowledge
---

# Vibe知识大赏 · 精品知识短片工作室

一期 = 一个知识点 → 一条有旁白的精品短片（默认 16:9 1080p60）。**时长由用户定**：先按复杂度给四档建议（速览 / 精讲 / 标准 / 深挖），每档写清能讲多细、要砍什么（references/13-duration.md）。


**两档制作**（references/08-tiers.md）：
- 同一份 film.js 两档通用（`ENH` 开关：plate/vclip ↔ layers）。

## BGM（强制，2026-10-28 起，两档通用）



```bash
# 同时输出 bgm.beats.json（成片里每一拍 / 每一小节的秒数），film.js 想卡点就读它
```

film.js 里：`music.push({ src: P("audio/bgm.wav"), from: 0, at: 0, dur: END + TAIL, gain_curve: [[0, -11], [END, -11], [END + TAIL, -8]], fade_in: 0.3, fade_out: 1.8 })`（旁白段 finish.py 会自动再压低）。

## 首次使用与风格推荐（先做这一步）

- **首次使用**（`~/.vibe-knowledge/welcomed` 不存在）：先跑 `python3 ~/.claude/skills/vibe-knowledge/tools/welcome.py`，生成并打开本地「风格图鉴」（`~/Desktop/vibe-knowledge/风格图鉴/index.html`：风格快闪片、样片集、按家族分组的风格卡、三种开口方式、两档、流程），然后在对话里用 5–6 句话介绍：母版 × 风格 × 档位、8 个家族各举一两套、三种开口方式，最后问「想先做哪个选题？」。风格库更新后用 `--force` 重新生成。
- 风格目录的唯一来源是 `styles/catalog.json`（推荐、图鉴、快闪片都读它）；加新风格时同步 catalog.json、STYLE.md、still.jpg。

## 核心主张（不能丢）

2. **没出处不上屏**：数字、人名、年份、引文全部进 facts.md；示意画面标明；分歧两说并列。
3. **旁白讲故事，画面给关键词**：画面字 ≤8 字一组、同屏最多两组；整句交给旁白和自动字幕。
4. **先猜后讲、标题延后、一个主道具贯穿、结尾回问**（母版共用规则，references/01-templates.md）。
6. **旁白对位硬规则**：没念到不露面、计数在念到时落定、强调有预算、最长静止 ≤3 秒（references/11-absorbed.md 第一节）。

## 工作区

```bash
python3 ~/.claude/skills/vibe-knowledge/tools/new_film.py <期号> --template A --title "本福特定律"
#   默认工作区 ~/Desktop/vibe-knowledge、系列 vk；第一次会自动建 cine 系列、装 know.js、给录制工具打补丁、放用户克隆音色
S=~/Desktop/vibe-knowledge/examples/vk; L=$S/lessons/<期号>
```


## 流水线（三个确认点）

| 段 | 做什么 | 产出 |
|---|---|---|
| ① 选题 | 三问：能不能让人 3 秒内先猜 / 先选？有没有贯穿道具？有没有反转？给用户 3–5 个候选 + 推荐母版 | 选题 |
| **确认 1** | 用户选题、母版、**时长**（先跑 `duration.py` 按复杂度给四档，推荐档排第一；用户选的档跟复杂度差两级以上要提醒）、**风格**（库里的 / 我的 / 改一套 / 从空白，见 09-style-studio.md；推荐项排第一附风格图）、**做哪一档**（基础 / 增强轻 / 标准 / 旗舰） | |
| ② 查 | 事实清单（T1/T2/T3 分级、原文摘录、用在哪拍） | `facts.md` |
| ③ 写 | 按母版骨架写旁白（字数上限见骨架 `_guide`）→ 子 agent 对抗审查（钩子、出处、字数）→ 改 | `narration.json` |
| **确认 2** | 用户看旁白稿 + 分镜（+ 增强镜头清单和报价），明确同意后才生成 | |
| ⑦ 编 | film.js（know.js 组件）→ stills.py 接触表逐张看（含动画中途帧） | `stills/` |
| ⑧ 渲 | queue.sh（record → finish → deliver） | 成片 |
| ⑨ 质检 | `qa.py` 接触表 + OCR 回读对照 facts.md + 响度；接触表里整段画面不变 = 录制出事，重录 | `qa/` |
| **确认 3** | 用户看成片；改完出发布包，封面用 `cover_first.py` 接成开头帧 | `post.txt`、封面 |

## 常用命令

```bash
cd ~/Desktop/vibe-knowledge; S=examples/vk; L=$S/lessons/<期号>
python3 scripts/speed.py $L 1.1                                        # 需要时整体提速，目标 5.5–6 字/秒
(cd $S && python3 tools/check_timings.py <期号>)                       # 对齐有没有断
cd $S && $CINE_PY cine/tools/stills.py <期号> lessons/<期号>/stills/sheet.png 1 B01+1 B02.title B05.count+0.5 …
echo "<期号>|<片名>|<封面秒>" >> cine/queue.txt   # 只能追加！queue.txt 多会话共用
pgrep -f cine/tools/queue.sh || CINE_PY=$CINE_PY cine/tools/queue.sh   # 已有队列在跑就别再起第二个，否则两路录制写坏同一个 picture.mp4
python3 ~/.claude/skills/vibe-knowledge/tools/qa.py lessons/<期号>/build/lesson<期号>.mp4
python3 ~/.claude/skills/vibe-knowledge/tools/cover_first.py <成片.mp4> cover_16x9.jpg <交付.mp4>   # 封面接成开头帧（0.5 秒），每期交付必做
```

voice.log 里回读 <95% 的拍删掉 `build/audio/<拍>.*` 重配；专名用 lexicon 写读音。

## 参考文件

| 文件 | 内容 |
|---|---|
| references/01-templates.md | 6 种母版（有旁白版）：每拍做什么、画面、对标作品 |
| references/02-premium.md | 精品标准：画面、声音、内容、交付规格（交付前逐条过） |
| references/05-publish.md | 发布包：活动标题规则、话题、封面、简介、交付文件夹 |
| references/06-benchmarks.md | 对标作品数据与共性 |
| references/07-kit.md | know.js 组件 API |
| references/09-style-studio.md | 风格工作室：四个入口、一题一问（推荐排第一 / 你定 / 自由对话）、三分法、汇总 → 风格图 → demo → 固化到 ~/vibe-knowledge-styles/ |
| styles/INDEX.md | 风格库目录：44 套按 8 个家族分组（每套 STYLE.md + still.jpg，样片源码 styles/_samples/） |
| references/13-duration.md | 时长与拆解细腻度：五项复杂度打分、四档时长（字数 / 拍数 / 细腻度 / 能讲到 / 要砍掉）、推荐规则、不匹配提醒、封面停留时长 |
| references/14-pitfalls.md | 制作踩坑清单（按环节）：渲染队列共用、AI 器物图结构错、配音对齐断、Wan 下载失败、CSS 清底色、AAC 峰值… |
| references/11-absorbed.md | 吸星大法：14 个开源同类项目的旁白对位规则、9 种解说语法、结构与发布技巧、质检流程、12 个新风格候选、Vox 纸拼贴做法、许可证边界 |
| templates/narration/A–F.json | 6 个母版的旁白骨架（每拍字数上限、[[cue]]） |
| templates/film.skeleton.js | film.js 骨架（配乐、音效、冷开场、尾卡写法） |

cine 引擎本身的契约、组件、渲染队列、坑：`~/.claude/skills/ai-teardown/references/10-cine.md`（改引擎前必读）。
