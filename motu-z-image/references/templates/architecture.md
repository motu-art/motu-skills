# 建筑 / 室内设计 — architecture

**何时用**：客厅/办公室/酒店/餐厅/展厅/会议室等空间效果图、建筑外观、家装方案图。

## 填充清单

| 字段 | 必答 |
|---|---|
| 空间类型 | 客厅/办公室/酒店/餐厅/展厅… |
| 设计目标 | 高级/现代/温暖/未来/极简 |
| 结构 | 空间比例；墙面/地面/天花材料 |
| 家具 | 沙发/桌/椅/灯具/装饰，逐件 |
| 材质 | 木材/石材/玻璃/金属；纹理真实、材质间视觉区别明显 |
| 色彩 | 主色/辅色/点缀色 |
| 灯光 | 自然光从哪侧窗进入 + 吊灯/壁灯/灯带；柔和 |
| 空间关系 | 入口/主要家具/窗户/视觉焦点各在哪 |
| 相机 | 建筑摄影、广角、平视、垂直线笔直、平衡构图 |
| 禁止 | 透视错误、弯曲墙壁、重复家具、漂浮家具、不合理结构 |

## Z-Image 骨架

```text
title: [空间一句话], An architectural interior photograph of [空间类型] in [风格].,
[4-6 氛围词: modern, serene, luminous, refined …],
[空间: 开放式布局 + 尺寸比例感受],
[前景: 具体元素], [中景: 主体家具], [背景: 窗户/墙面/尽头],
[配色: 主色, 辅色, 点缀色],
interior, [空间类型], [设计语言: warm minimalism / contemporary …],
[结构组: 墙面材质, 地面材质, 天花材质],
[家具组: 逐件 —— boucle sofa in oatmeal, low walnut coffee table, arc floor lamp, ceramic vase],
[材质组: white oak flooring with subtle grain, honed travertine wall, brushed brass details],
[spatial: entry on the left, sofa centered against the far wall, full-height windows on the right, focal fireplace on the far wall],
full_frame, 24mm, tilt-shift, f/8.0, ISO 200, shutter speed: 1/60,
two-point interior view, horizontal, eye-level, straight vertical lines, balanced one-point perspective,
deep, sharp throughout,
Natural Window Light, daylight through full-height windows, position: camera right, intensity: soft and even,
warm pendant glow, ratio: 2:1, position: above seating area, gentle warmth in the evening zone,
airy, soft, layered,
architectural photography, realistic materials, editorial interiors,
neutral warm, contrast: low-medium, soft transitions, saturation: moderate, true material colors,
calm and spacious, quietly luxurious,
[叙事句],
[情绪词],
correct perspective with straight verticals, no bent walls, no repeated furniture,
no floating furniture, no impossible structures, no text, no watermark
```

## 填写要点

- `straight vertical lines` + `tilt-shift` 是建筑摄影不变形的钥匙，构图组必写。
- 材质**分区描述**（墙/地/顶/家具各一句），材质间要拉开视觉区别。
- 家具逐件列出并给位置 —— 负面 `no repeated furniture` 挡复制粘贴怪。
- 室外建筑外观：换成 three-quarter exterior view + `facade` 结构组，其余同构。

## 示例（完整可直接提交）

```text
title: Travertine Living Room, An architectural interior photograph of a modern living room in warm minimal style., modern, serene, luminous, refined, warm minimalism, open-plan living room with double-height ceiling and generous proportions, foreground of low travertine coffee table with ceramic bowl and stacked art books, midground of boucle sofa with linen throw, background of full-height windows with sheer curtains and a planted courtyard beyond, oatmeal, warm travertine beige, muted olive accent, interior, living room, warm minimalism, micro-cement walls, white oak herringbone flooring, smooth white plaster ceiling with recessed linear lighting, boucle sofa in oatmeal, low travertine coffee table, arc floor lamp in aged brass, large ceramic vase with dried branches, entry hallway on the left, sofa centered against the far wall, full-height windows on the right, black steel fireplace as focal point on the far wall, white oak with subtle grain, honed travertine surfaces, brushed brass details, soft boucle texture, full_frame, 24mm, tilt-shift, f/8.0, ISO 200, shutter speed: 1/60, two-point interior view, horizontal, eye-level, straight vertical lines, balanced one-point perspective, deep, sharp throughout, Natural Window Light, daylight through full-height windows, position: camera right, intensity: soft and even, warm pendant glow, ratio: 2:1, position: above seating area, gentle warmth in the evening zone, airy, soft, layered, architectural photography, realistic materials, editorial interiors, neutral warm, contrast: low-medium, soft transitions, saturation: moderate, true material colors, calm and spacious, quietly luxurious, Late afternoon light rakes across the travertine and everything slows down., calm permanence, understated warmth, correct perspective with straight verticals, no bent walls, no repeated furniture, no floating furniture, no impossible structures, no text, no watermark
```
