# 海报 / 广告设计 — poster

**何时用**：品牌/产品商业海报、活动宣传页、电影海报、促销视觉。
这是**最容易因 prompt 不严谨而失败**的类型 —— 画面文字、层级、留白都要显式约束。
需要大量准确文字时评估改用 HTML/SVG 排版 + AI 素材（见 [infographic.md](infographic.md) 同款建议）。

## 填充清单

| 字段 | 设计要点 |
|---|---|
| 任务 | 什么品牌/产品的什么海报 |
| 核心主体 | 产品/人物 —— 第一视觉 |
| 视觉主题 | 未来科技/高级奢华/自然/年轻/专业 |
| 构图 | 中心/对角线/三分法；主体位置；**30% 左右留白给文字** |
| 视觉层级 | 第一视觉 → 第二（背景元素）→ 第三（装饰） |
| 背景 | 具体背景 |
| 色彩 | 主色/辅色/强调色 |
| 文字 | 主标题/副标题/按钮 —— **逐字引号**；位置；字体气质 |
| 排版 | 标题、副标题、按钮各在哪 |
| 禁止 | 乱码、错拼、额外文字、重复文字、Logo 变形、元素拥挤 |

## Z-Image 骨架

```text
title: [海报名], A commercial advertising poster for [品牌/产品/活动].,
[4-6 氛围词: bold, premium, energetic …],
[背景: 具体背景 + 渐变方向],
[装饰元素: 几何形状/光斑/纹理],
[配色: 主色, 辅色, 强调色],
[核心主体组: [产品/人物描述]],
[spatial: subject positioned [left/center/right], top third reserved clean for headline],
[文字组: headline text "[逐字]" across the top in [字体气质], subheadline text "[逐字]" below in lighter weight, small button text "[逐字]" at bottom center],
[排版组: strong visual hierarchy, headline largest, generous letter spacing, aligned to grid],
full_frame, [35/50]mm, f/[5.6-8], ISO 100, shutter speed: 1/125,
vertical poster composition, [中心/对角线/三分法构图], about 30 percent clean negative space for typography,
[景深],
[主光 + position: + intensity:],
[辅光 + ratio:],
[光感词],
premium advertising design, strong art direction,
[调色: 色温, contrast:, saturation:],
[调子词],
[叙事句],
[情绪词],
exact spelling as quoted, no extra text, no repeated words, no garbled characters,
no distorted logo, no crowded elements, no watermark
```

## 填写要点

- **画面文字逐字放双引号**，并声明 `exact spelling as quoted`；每类文字不超过
  3–5 个词，海报文字越少越不容易翻车。
- 文字位置 = 留白位置，二者必须写一致（headline 在顶部 → 构图写 top 留白）。
- 字体写气质类别（bold condensed sans-serif / elegant high-contrast serif），
  不写具体品牌字体名。
- 中文文字也可以渲染，但同样要短（「春日上新」四字比一整句稳得多）。

## 示例（完整可直接提交）

```text
title: Spring Launch Poster, A commercial advertising poster for a floral tea brand spring launch., fresh, elegant, minimal, botanical, premium, soft gradient background from pale blush to warm ivory, scattered delicate sakura petals drifting diagonally, thin gold line accents, blush pink, warm ivory, deep green accent, a glass teacup with blooming flower tea centered in lower half, petals suspended in golden liquor, visible steam curl, subject positioned in lower half center, top third kept clean for headline, headline text "SPRING BLOOM" across the top in elegant high-contrast serif with generous letter spacing, subheadline text "New Flower Tea Collection" below in light sans-serif, small text "LIMITED EDITION" at bottom center in wide-tracked small caps, strong visual hierarchy, headline largest, aligned to central grid, full_frame, 50mm, f/8.0, ISO 100, shutter speed: 1/125, vertical poster composition, centered symmetrical layout, about 30 percent clean negative space for typography, medium depth with softly blurred petals in background, Soft Diffused Studio Light, large softbox from front above, position: camera front, 45 degrees, intensity: soft and even, gold reflector, ratio: 2:1, position: camera right, warm glint on glass rim, airy, luminous, polished, premium advertising design, strong art direction, botanical editorial, warm bias, contrast: low-medium, soft transitions, saturation: moderate with vivid petal tones, fresh and elegant, quietly luxurious, A single cup holds the whole season., renewal and indulgence, springtime calm, exact spelling as quoted, no extra text, no repeated words, no garbled characters, no distorted logo, no crowded elements, no watermark
```
