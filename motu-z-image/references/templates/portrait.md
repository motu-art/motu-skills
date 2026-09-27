# 真人肖像 — portrait

**何时用**：企业头像、LinkedIn/职业照、商务人像、模特片、ID 照、高端人物摄影 ——
一切「真实存在感的人」的半身/特写肖像。Z-Image 官方默认示例就是一张美妆人像，
本意图可用字段组最全。

## 填充清单

| 字段 | 必答 |
|---|---|
| 身份 | 年龄段、性别、外貌特征、职业身份、族裔 |
| 面部 | 真实皮肤纹理、自然毛孔/眼睛/发丝；不磨皮不美颜不改五官 |
| 表情 | 自然微笑/自信/亲和；视线看镜头 |
| 姿势 | 正面或 3/4 侧；肩自然、头微倾 |
| 服装 | 西装/衬衫/商务休闲；颜色、材质、剪裁 |
| 背景 | 摄影棚纯色/办公室/城市虚化；主体背景分离 |
| 灯光 | 大柔光主光 + 补光 + 轮廓光；`ratio:` 控制对比 |
| 相机 | 85mm 人像镜头、浅景深、平视、中特写 |
| 禁止 | 塑料皮肤、过度修图、AI 脸、畸变五官、不对称、多指 |

## Z-Image 骨架

```text
title: [一句话人设], A professional portrait of [身份] in [场景].,
[4-6 氛围词: confident, approachable, executive, editorial …],
[环境: modern office interior / seamless gray studio backdrop],
[背景元素: softly blurred bookshelves and glass wall],
[配色: charcoal, crisp white, warm skin tones],
human, [gender], age range: [N-N], [ethnicity], [features/build/气质 3-4 项],
[pose: seated, shoulders relaxed, slight head tilt, turned three-quarter to camera],
[face: oval face, defined jawline / round face, soft features],
[expression: natural confident smile, direct to camera, engaging],
[lips/beard 等细部: neatly trimmed beard / softly parted lips],
[hair: short, neatly combed, color: dark brown / medium-long, sleek and straight, tucked behind ears],
[skin/makeup: natural skin texture with visible pores, minimal retouching / clean natural makeup],
[outfit: tailored navy suit, crisp white shirt, no tie / white silk blouse],
full_frame, 85mm, prime, f/2.0, ISO 100, shutter speed: 1/160, white balance: 5200,
[景别] medium close-up portrait, [画幅] vertical, eye-level, subject centered with slight headroom, eyes (nearest eye sharp),
shallow, softly blurred background,
Large Softbox Key Light, [光源+柔光], position: camera left, 45 degrees, intensity: soft and even,
white bounce card, ratio: 2:1, position: camera right, subtle hair light for separation,
natural, soft, professional,
premium corporate photography, realistic photography,
neutral, contrast: medium, soft transitions, saturation: moderate, natural skin tones,
authentic and composed, quietly confident,
[叙事句] He projects calm authority and quiet competence.,
[情绪词] trust and professionalism, approachable authority,
realistic skin texture, no plastic skin, no over-retouched face, no ai-looking face,
no deformed eyes, no asymmetrical face, no extra fingers
```

## 填写要点

- 「真实感」靠三件事锁：`natural skin texture with visible pores`、负面里的
  `no plastic skin / no ai-looking face`、以及克制的调色（`saturation: moderate,
  natural skin tones`）。
- 灯光用 `ratio:` 控制对比：1:2 平柔（美妆/亲和），2:1 有型（高管/杂志），
  4:1 戏剧化（慎用）。
- ID/证件类需求 → 纯色背景 + 正面 + 平光（`ratio: 1:1`）+ 不笑。
- 与官方默认示例（美妆人像）结构完全同构，可直接参考 `prompting.md` 字段组表。

## 示例（完整可直接提交）

```text
title: Confident Founder Portrait, A professional corporate portrait of a startup founder in a modern office., confident, approachable, executive, editorial, natural, modern office interior with warm wood accents, softly blurred bookshelves and glass wall in background, charcoal gray, crisp white, warm skin tones, human, male, age range: 30-35, East Asian, refined features, athletic build, poised, seated on an office chair, shoulders relaxed, slight head tilt, turned three-quarter to camera, oval face, defined jawline, natural confident smile, direct to camera, engaging, neatly trimmed short beard, short neat side-parted hair, color: black, natural skin texture with visible pores, minimal retouching, tailored charcoal suit, crisp white shirt, no tie, full_frame, 85mm, prime, f/2.0, ISO 100, shutter speed: 1/160, white balance: 5200, medium close-up portrait, vertical, eye-level, subject centered with slight headroom, eyes (nearest eye sharp), shallow, softly blurred background, Large Softbox Key Light, diffused studio strobe through large softbox, position: camera left, 45 degrees, intensity: soft and even, white bounce card, ratio: 2:1, position: camera right, subtle hair light for separation, natural, soft, professional, premium corporate photography, realistic photography, neutral with slight warm bias, contrast: medium, soft transitions, saturation: moderate, natural skin tones, authentic and composed, quietly confident, He projects calm authority and quiet competence., trust and professionalism, approachable authority, realistic skin texture, no plastic skin, no over-retouched face, no ai-looking face, no deformed eyes, no asymmetrical face, no extra fingers
```
