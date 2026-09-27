# 角色 / IP 形象设计 — character

**何时用**：游戏角色、IP 吉祥物、卡通形象、品牌人设、3D 虚拟形象、儿童绘本
角色。要求「真实存在感的人」时用 [portrait.md](portrait.md)。

## 填充清单

| 字段 | 设计要点 |
|---|---|
| 用途 | 游戏/IP/品牌/教育/广告/产品，决定设计语言 |
| 身份 | 年龄感、性别/物种、角色身份（魔法师/教师/吉祥物…） |
| 外观 | 脸型、发型发色、眼睛、身材比例、皮肤/毛发质感 |
| 服装 | 上装/下装/鞋/配饰，逐件写颜色材质 |
| 标志性元素 | 必须跨图保留的视觉识别（帽子/徽章/道具）—— IP 角色必填 |
| 动作情绪 | 在做什么、身体姿态、双手、视线、可读的表情 |
| 造型语言 | 可爱/高级/神秘/未来/专业；剪影识别度优先，避免过度装饰 |
| 画面 | 全身、头身手脚完整、居中、正面或 3/4 侧、纯色背景 |
| 风格 | 3D cartoon / 2D illustration / anime / Pixar-like 3D，材质造型颜色统一 |
| 光线 | 均匀柔光 + 轻微轮廓光，主体与背景分离 |

## Qwen 散文骨架

```text
[Design statement]. [Full-body character design sheet of a] [age/gender/species] [identity], created for [game/IP/brand use].
[Appearance: face shape, hairstyle and color, eyes, build, skin or fur texture].
[Outfit: each piece with color and material]. [Signature element] that must stay recognizable in every pose and angle.
[Action: what the character is doing, body posture, hands, head direction, gaze direction], with [readable emotion] expression.
The overall design language is [cute/premium/mysterious/futuristic/professional], with a clean readable silhouette and restrained detail.
The character stands centered in full body with head, torso, hands and feet all visible, in [front/three-quarter] view against [a plain solid color background].
Rendered in [3D cartoon / 2D illustration / anime / Pixar-like 3D] style with consistent materials and unified color.
Lit by soft even studio lighting with a subtle rim light separating the character from the background.
Absolutely no extra characters, no extra arms, no extra fingers, no deformed hands or feet, no cropped body, no complex background, no text, no watermark.
```

## 填写要点

- 「剪影识别度」靠标志性元素：一个独特轮廓物（尖帽、天线耳、大尾巴）比十个
  小装饰有效 —— 写进 prompt 并注明 recognizable in every pose。
- 表情写「可读」：`a bright readable smile`；情绪是这个模板的核心交付物。
- IP 角色把标志性元素单独成句并要求一致，为后续套图（[series.md](series.md)）
  留出 MASTER 块。
- 吉祥物/低龄向 → 3D cartoon + 圆润比例；品牌高级感 → editorial illustration +
  克制配色。

## 示例（完整可直接提交）

```text
Full-body character design sheet of a young fox mascot for a children's science education brand. The character is a friendly anthropomorphic fox around eight years old in energy, with a rounded face, large amber eyes, a fluffy cream-tipped tail, and warm orange fur with a white muzzle and belly. He wears a small teal lab coat over a mustard-yellow t-shirt, round dark-rimmed glasses, and a tiny brass compass pendant as his signature element that must stay recognizable in every pose and angle. He is standing with one hand raised in an enthusiastic wave and the other holding a rolled-up star chart, head tilted slightly, gaze toward the viewer, with a bright readable smile full of curiosity. The overall design language is cute, clever and approachable, with a clean readable silhouette and restrained detail. The character stands centered in full body with head, torso, hands and feet all visible, in three-quarter view against a plain light warm-gray background. Rendered in Pixar-like 3D cartoon style with consistent soft fur materials and a unified orange-teal-cream palette. Lit by soft even studio lighting with a subtle rim light separating the character from the background. Absolutely no extra characters, no extra arms, no extra fingers, no deformed hands or feet, no cropped body, no complex background, no text, no watermark.
```
