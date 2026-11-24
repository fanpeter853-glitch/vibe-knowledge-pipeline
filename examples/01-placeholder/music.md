# 配乐说明 — vibe 第一期《人为什么会对某段回忆念念不忘》

## 采用的曲目

- 曲名：Undertow
- 作者：Scott Buckley（真人作曲家，澳大利亚）
- 来源页面：https://www.scottbuckley.com.au/library/undertow/
- 音频文件：`music_undertow.mp3`（与本文件同目录，320 kbps MP3，4 分 10 秒，10.0 MB）
- 下载地址：https://www.scottbuckley.com.au/library/wp-content/uploads/2019/12/sb_undertow.mp3
- 作者原话描述：A sombre, ebbing piano/string/synth track.（忧郁、起伏的钢琴/弦乐/合成器）
- 情绪：温柔偏钢琴 + 弦乐，忧郁但不沉重，贴合“回忆、念念不忘”。
- 授权：Creative Commons Attribution 4.0 International（CC-BY 4.0）
  - 免费，可商用，可改编（剪短、淡入淡出、压低音量都属于改编，允许）。
  - 条件：必须署名。发布时视频简介里必须写：
    `'Undertow' by Scott Buckley - released under CC-BY 4.0. www.scottbuckley.com.au`
  - 抖音发布时把这行署名放进视频描述，不要只放评论区。
  - 不能把音乐单独拿去卖、不能声称是自己写的。

## 混音参数（带音乐版 final_with_music_1080x1920.mp4）

- 取原曲开头 0–57.1 秒（对齐画面总时长 57.1 秒，不循环、不拼接）。
- 音量：volume=0.35，实测混后整条音乐平均 -29.7 dB、峰值 -10.9 dB（原曲开头偏静），
  音乐版即成片，不用配音。
- 淡入：开头 1 秒 afade=t=in:st=0:d=1；淡出：最后 2 秒 afade=t=out:st=55.1:d=2。
- 不用配音：音乐保持 volume 0.35，不再压低；音乐版即成片。

## 备选 / 未采用（都核实过，不用）

1. Pixabay《Deep in Memory》— SergePavkinMusic（pixabay.com/music/id-239371）
   未采用：作者注明隶属英国 PRS（表演权协会），且有 YouTube Content ID 登记提示，
   发抖音虽不在 YouTube 体系内，但版权链路不如 CC-BY 干净，弃用。
2. Otomusu《Remembrance at Dusk》（夕暮れの追憶，2:59，钢琴，怀旧）
   未采用：来源页面写明“生成時のスタイル指定”（生成时指定风格），疑似 AI 生成曲目；
   任务要求不用 AI 生成音乐充数，故弃用。文件未保留在本仓库。
3. Pixabay《Dreamy Piano》— The_Mountain
   未采用：页面明确标注 AI generated，弃用。

## 核实

- 2026-11-24 实测下载：文件真实存在，ffprobe 读到 249.93 秒、320 kbps、44.1 kHz；
  volumedetect 平均 -16.5 dB、峰值 -1.1 dB，是真实音乐，不是静音/噪声。
- 不是 Jensen 那条视频的原音乐，没有用流行歌，没有付费音乐，没有 AI 生成音乐。
