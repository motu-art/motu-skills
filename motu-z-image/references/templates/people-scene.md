# 人物 + 场景组合 — people-scene

**何时用**：实际项目里最常见的出图需求 —— 一个具体的人在具体的环境里做具体的
事。广告 lifestyle、品牌宣传片截帧、文章配图、封面、电商场景图。
没有更专属模板时，**默认从这里起步**。

## 填充清单（8 组）

| 字段 | 必答 |
|---|---|
| 人物身份 | 谁：年龄/性别/气质/身份 |
| 人物外观 | 脸型发型、肤色体态 —— 需跨图一致时逐项固定 |
| 服装配饰 | 具体到颜色材质 |
| 动作 | 在做什么（可观察的小动作，不是抽象状态） |
| 表情视线 | 看哪里、什么情绪 |
| 道具 | 手里/身边的物件 |
| 环境 + 空间关系 | 在哪里；人物离前景多远、与背景什么关系、位于画面哪个区域 |
| 时间天气 | 清晨/黄昏/夜；晴/雨/雾 |
| 构图 | 景别、视角、焦段、主体位置 |
| 视觉分层 | 第一重点（人物）→ 第二（道具）→ 第三（环境） |
| 光线 | 主光源、方向、色温、阴影性质 |
| 色彩 | 主色/辅色/强调色 |
| 一致性 | 跨图必须稳定的部分（脸、发型、服装、比例、道具、场景结构） |

## Z-Image 骨架

```text
title: [一句话画面], A [媒介] image of [人物身份] [做什么] in [哪里].,
[4-6 氛围词],
[环境: 具体地点 + 空间特征],
[前景元素], [中景元素], [背景元素],
[时间天气: early morning, thin mist …],
[配色: 主色, 辅色, 强调色],
human, [性别], age range: [N-N], [族裔], [外观: 发型发色/脸型/体态/肤色],
[outfit: 具体服装配饰颜色材质],
[action: 正在做的可观察动作，1-2 个],
[expression: 表情 + 视线朝向],
[props: 手中/身边道具],
[spatial: 距前景关系 + 画面位置 + 与背景关系],
full_frame, [35/50/85]mm, prime, f/[1.8-4], ISO [100-800], shutter speed: [1/125-1/500],
[景别: wide/medium/close-up], [画幅], [机位: eye-level/low angle], subject positioned [thirds/center],
[景深: shallow with blurred background / deep focus],
[主光: 光源名 + 性质 + position: + intensity:],
[辅光: bounce/rim + ratio: + 作用],
[光感词],
[风格定位一句],
[调色: 色温, contrast:, saturation:, 关键色调],
[调子词],
[叙事句],
[情绪词],
[一致性要求(套图时): same face, hairstyle, outfit and color palette across the series],
[负面约束: no extra people, no distorted hands, no text, no watermark]
```

## 填写要点

- 动作写成**可观察的小步骤**（「右手端起陶杯凑近唇边」），不写抽象状态
  （「享受生活」）。
- 空间关系三件套必写：距前景、画面位置、与背景关系 —— 这是「人在场景里」
  而不是「人贴在背景上」的关键。
- 光线方向与时间一致：清晨 = 低角度暖光 camera 侧，别配正午顶光。
- 留白方向跟用途走：要叠字就写 `generous negative space on the [left/top]`。

## 示例（完整可直接提交）

```text
title: Rainy Bookshop Afternoon, A cinematic lifestyle image of a young woman browsing books in a cozy independent bookshop on a rainy afternoon., warm, intimate, nostalgic, editorial, cinematic, cozy independent bookshop interior with tall wooden shelves and warm pendant lamps, foreground of stacked books on a low table, midground of narrow aisle between shelves, background of rain-streaked window with blurred street lights, late afternoon, steady rain outside, warm amber, deep walnut brown, muted teal accent, human, female, age range: 22-27, East Asian, oval face, soft features, medium build, shoulder-length black hair loosely tucked behind left ear, wearing an oversized cream knit sweater, dark straight-leg jeans, thin gold necklace, holding an open paperback in both hands, absorbed, gaze lowered to the page, subtle contented smile, standing in the aisle, medium distance from foreground books, positioned on the right third of frame, bookshelves receding behind her, full_frame, 50mm, prime, f/2.0, ISO 400, shutter speed: 1/125, medium shot, vertical, eye-level, subject on right third with generous negative space on the left, shallow, softly blurred background, Warm Tungsten Mix, pendant lamp glow through paper shades, position: above and camera left, intensity: warm and soft, window bounce fill, ratio: 2:1, position: camera right, cool rim from window light for separation, warm, diffused, gently contrasty, intimate editorial lifestyle photography, warm bias, contrast: medium, soft transitions, saturation: moderate, natural skin tones under warm light, nostalgic and warm, quietly romantic, She is completely absorbed in her book while the rain paints the window behind her., quiet comfort, absorbed tranquility, no extra people, no distorted hands, no text, no watermark
```
