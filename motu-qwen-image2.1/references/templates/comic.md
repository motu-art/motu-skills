# 漫画 / 分镜 — comic

**何时用**：四格漫画、连环画、storyboard、故事板、绘本分镜。核心是**多格 +
角色跨格一致 + 景别变化**。单张不分级格的插画按内容选其它模板。

## 填充清单

| 字段 | 设计要点 |
|---|---|
| 故事 | 一句话故事 |
| 角色 | 角色 A/B 外观（进 MASTER 块，跨格一致） |
| 分镜 | 每格：景别（远/中/近）、角色、动作、表情、镜头 |
| 格数 | 4 格最稳（2×2）；逐格编号 |
| 连续性 | 所有格中外观/服装/发型/道具/场景一致 |
| 画风 | manga / western comic / storybook / storyboard sketch |
| 对白 | 每格 ≤ 1 句气泡对白，逐字引用（可选） |
| 视觉 | cinematic storyboard、clear visual storytelling |

## Qwen 散文骨架

```text
[Medium statement]. A [N]-panel comic page (2 by 2 grid, panels numbered left to right) telling this story: [one-line story].
The recurring character is [full appearance locked in every panel: age, face, hair, outfit, prop].
Panel one, a [wide / medium / close] shot: [character] [action], [expression]. Panel two, a [shot] shot: [action], [expression]. Panel three, a [shot] shot: [action], [expression]. Panel four, a [shot] shot: [action], [expression].
[Optional: short speech bubble in panel N reading "[EXACT TEXT]"].
The character's face, hairstyle, clothing and props stay identical across all panels, and the setting stays consistent.
Drawn in [manga style with ink linework and screentone / clean western comic style / soft storybook illustration], cinematic storyboard composition with clear visual storytelling.
Absolutely no inconsistent character design, no changing outfits between panels, no garbled text, no misspelling, no extra panels, no watermark.
```

## 填写要点

- 角色外观句写一次、声明「in every panel」——四格里三次复述外观是浪费字符，
  一次锁死 + 负面兜底 `no inconsistent character design` 更有效。
- 每格景别必须变化（远→中→近→特写）——四格全是中景是最常见失败模式，
  模板里直接写成阶梯。
- 对白 ≤ 1 句/格且逐字引用；无对白漫画最稳（`silent comic`）。
- 需要多页 → 每页一张图，MASTER 角色句原样复制，参考 [series.md](series.md)。

## 示例（完整可直接提交）

```text
A four-panel comic page in a 2 by 2 grid, panels numbered left to right, top to bottom, telling this story: a night-shift baker's cat steals a bun and gets gently forgiven. The recurring character is a round gray tabby cat with a torn left ear and a small red collar, identical in every panel. Panel one, a wide shot: the cat slips through the dark bakery doorway past cooling racks of buns, alert. Panel two, a close shot: the cat grips one golden bun in its mouth mid-tiptoe, guilty-eyed. Panel three, a medium shot: the elderly baker in a flour-dusted apron looks down at the cat with a tired warm smile, hand on hip. Panel four, a close shot: the cat sits on the counter happily nibbling the bun while the baker lights the first oven of the morning behind. The character's face, markings and red collar stay identical across all panels, and the bakery setting stays consistent. Drawn in soft storybook illustration with warm ink linework, cinematic storyboard composition with clear visual storytelling. Absolutely no inconsistent character design, no changing collar between panels, no text, no watermark.
```
