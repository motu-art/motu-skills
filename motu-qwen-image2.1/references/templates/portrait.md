# 真人肖像 — portrait

**何时用**：企业头像、LinkedIn/职业照、商务人像、模特片、ID 照、高端人物摄影 ——
一切「真实存在感的人」的半身/特写肖像。官方默认示例就是一张时尚编辑人像，
本意图与 Qwen 散文格式同构度最高。卡通/3D 角色用 [character.md](character.md)。

## 填充清单

| 字段 | 设计要点 |
|---|---|
| 身份 | 年龄段、性别、外貌特征、职业身份、族裔 |
| 面部 | 真实皮肤纹理、自然毛孔/眼睛/发丝；不磨皮不美颜不改五官 |
| 表情 | 自然微笑/自信/亲和；视线看镜头 |
| 姿势 | 正面或 3/4 侧；肩自然、头微倾 |
| 服装 | 西装/衬衫/商务休闲；颜色、材质、剪裁 |
| 背景 | 摄影棚纯色/办公室/城市虚化；主体背景分离 |
| 灯光 | 大柔光主光 + 补光 + 轮廓光；明暗比控制对比 |
| 相机 | 85mm 人像镜头、浅景深、平视、中特写 |
| 禁止 | 塑料皮肤、过度修图、AI 脸、畸变五官、不对称、多指 |

## Qwen 散文骨架

```text
[Medium statement]. A professional portrait of a [identity] in [setting], captured with [lighting character].
[Appearance: age range, gender, ethnicity, features, build, presence].
[Expression and gaze: natural confident smile, eyes direct to camera].
[Pose: seated or standing, shoulders relaxed, slight head tilt, turned three-quarter to camera].
[Face and hair details: face shape, skin texture with visible pores, hairstyle and color, makeup or beard].
[Outfit: each piece with color, fabric, tailoring].
[Background: elements and their blur, subject separation].
Light comes from [a large softbox at 45 degrees camera left], with [a white bounce fill from the right and a subtle hair light for separation], creating [soft natural skin highlights and gentle shadows].
Shot on an 85mm portrait lens at eye level, medium close-up framing with slight headroom, the nearest eye in sharp focus against a softly blurred background.
Premium corporate photography, realistic materials, natural skin tones, authentic human presence.
Absolutely no plastic skin, no over-retouched face, no AI-looking face, no deformed eyes, no asymmetrical face, no unnatural teeth, no extra fingers, no watermark.
```

## 填写要点

- 「真实感」靠三件事锁：`natural skin texture with visible pores`、负面里的
  `no plastic skin / no AI-looking face`、以及克制的调色（`natural skin tones`）。
- 光比控制对比：平柔（美妆/亲和）→ `soft and even, gentle shadows`；有型
  （高管/杂志）→ `razor-sharp key light and deep shadows`（官方默认示例即后者）。
- ID/证件类 → 纯色背景 + 正面 + 平光 + 不笑。
- 本模板与官方默认示例结构完全同构，可参考 `../api.md` 的默认示例。

## 示例（完整可直接提交）

```text
A professional corporate portrait of a startup founder in a modern office, captured with soft directional studio lighting. She is a woman in her early thirties, East Asian, with refined features, a slim build, and a poised, composed presence. She wears a natural confident smile with her eyes direct to camera. She is seated with shoulders relaxed and a slight head tilt, turned three-quarter to the camera. She has an oval face with defined cheekbones, natural skin texture with visible pores and minimal retouching, shoulder-length straight black hair neatly tucked behind one ear, and clean natural makeup. She wears a tailored charcoal blazer over a crisp white shirt with no tie, the fabrics draping with realistic weight. The background is a softly blurred modern office interior with warm wood shelving and a glass wall, keeping clear separation between subject and background. Light comes from a large softbox at 45 degrees camera left, with a white bounce fill from the right and a subtle hair light for separation, creating soft natural skin highlights and gentle shadows. Shot on an 85mm portrait lens at eye level, medium close-up framing with slight headroom, the nearest eye in sharp focus against a softly blurred background. Premium corporate photography, realistic materials, natural skin tones, authentic human presence. Absolutely no plastic skin, no over-retouched face, no AI-looking face, no deformed eyes, no asymmetrical face, no unnatural teeth, no extra fingers, no watermark.
```
