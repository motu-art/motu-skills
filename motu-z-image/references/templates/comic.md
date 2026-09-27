# 漫画 / 分镜 / 故事板 — comic

**何时用**：多格漫画、连环画、故事板、分镜概念稿。
多格之间角色一致是最大难点 ——
单格内只画一个场景，跨格一致靠固定描述块（见 [series.md](series.md)）。
一格一图、逐格生成再排版，比一张图里塞四格稳定得多。

## 填充清单

| 字段 | 设计要点 |
|---|---|
| 故事 | 一句话剧情 |
| 角色 | 每个角色的固定外观（跨格一致） |
| 分格 | 每格：景别、角色、动作、表情、镜头 |
| 连续性 | 所有格中角色外观/服装/发型/道具/场景保持一致 |
| 视觉 | 漫画风格锚点（manga / western comic / webtoon / 水彩绘本） |

## Z-Image 骨架（单格）

```text
title: [故事名] Panel [N], A [风格] comic panel of [一句话这格剧情].,
[4-6 氛围词],
[场景: 具体地点 + 时间],
[配色],
[角色固定块（每格原样复制）: [角色A 外观：年龄感/发型发色/服装/标志物] …],
[本格动作组: 正在发生的可观察动作],
[本格表情组: 表情 + 视线],
[本格对白/音效（可选）: speech bubble text "[逐字]" / sound effect text "[拟声词]"],
[spatial: 角色在画面中的位置 + 前后景关系],
full_frame, [景别对应焦段], f/[2.8-5.6], …,
[景别: wide establishing / medium two-shot / close-up reaction], [画幅], [机位角度],
[景深],
[主光 + position: + intensity:],
[辅光 + ratio:],
[光感词],
[风格] comic art, clean line work, expressive characters,
[调色],
[调子词],
[叙事句],
[情绪词],
consistent character design across panels, no extra fingers, no distorted faces,
no garbled speech text, no watermark
```

## 填写要点

- **一格一图**：把 4 格拆成 4 次生成（套用 [series.md](series.md) 的 MASTER 块），
  再由排版工具拼页 —— 比一图 4 格成功率高得多。
- 角色固定块逐字复制进每一格，是跨格一致性的唯一手段。
- 每格换景别（远 → 中 → 近）形成节奏；对白气泡文字 ≤ 6 词。
- 漫画风格锚点要具体到线条感（`clean ink line art with flat cel shading`）。

## 示例（完整可直接提交）

```text
title: Lantern Keeper Panel 2, A warm watercolor comic panel of a young lantern keeper discovering a firefly cave., warm, wondrous, gentle, storybook, quiet dusk, forest path leading to a cave mouth glowing softly, deep teal, warm gold, ink brown accents, character, girl, age around 10, round face, freckles, short black bob with straight bangs, mustard raincoat, red rubber boots, carrying a small brass lantern, taking one cautious step forward while lifting the lantern higher, eyes wide with wonder looking into the cave, mouth slightly open in awe, positioned on the left third walking toward the glow on the right, cave entrance in background with floating fireflies, full_frame, 35mm, f/4.0, ISO 400, shutter speed: 1/125, medium shot, horizontal, eye-level slightly low, shallow with softly blurred fireflies, Soft Dusk Ambient, fading sky light from behind, position: behind and camera right, intensity: soft and dim, lantern key glow, ratio: 1:2, position: camera left, warm pool of light around the girl, warm, dim, magical, watercolor storybook comic art, clean ink line work with soft washes, warm bias, contrast: low-medium, soft transitions, saturation: moderate, golds glowing against teal, hushed and expectant, quietly thrilled, The cave breathes gold and she steps toward it., wonder and courage, small brave steps, consistent character design across panels, no extra fingers, no distorted faces, no garbled speech text, no watermark
```
