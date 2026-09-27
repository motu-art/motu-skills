# Hero Image / 产品宣传场景 — hero-image

**何时用**：SaaS / AI 产品官网 hero 大图、落地页头图、产品宣传横幅 —— 需要**大留白
给网页标题**的图。非常适合与前端配合：图归模型，字由 HTML 叠加。

## 填充清单

| 字段 | 设计要点 |
|---|---|
| 用途 | Website Hero Image（横幅 16:9 为主） |
| 产品 | 什么产品 |
| 核心概念 | 一句话产品价值，用视觉表现它 |
| 主体 | 人物/产品/UI/抽象物体 |
| 场景 | 具体环境 |
| 构图 | **主体偏右（或左），另一侧保留 ≥40% 干净空间**给网站标题 |
| 视觉动线 | 背景 → 产品 → 核心主体 |
| 风格 | premium SaaS / AI-native / futuristic / minimal / editorial |
| 光线 | 柔和电影光、微光 glow、受控对比 |
| 禁止 | 背景复杂抢主体、文字（网页字由 HTML 叠加，图内不要文字） |

## Z-Image 骨架

```text
title: [产品] Hero, A premium website hero image for [产品/品牌].,
premium, ai-native, futuristic, minimal, editorial,
[场景: 具体 —— soft gradient tech environment / abstract studio space],
[背景元素: subtle grid lines, floating glass panels …],
[配色: 深底主色, 辅色, 发光强调色],
[核心主体组: [抽象物体/产品/UI 卡片] 的具体描述],
[spatial: subject positioned on the right half, left half kept clean with at least 40 percent negative space for website headline],
[视觉动线组: reading path from background glow to product to key subject],
full_frame, [35/50]mm, f/4.0, ISO 100, shutter speed: 1/125,
horizontal hero composition (16:9), eye-level, balanced asymmetry,
[景深: medium with soft depth falloff],
Soft Cinematic Lighting, [光源], position: behind and above subject, intensity: soft with subtle glow,
bounce fill, ratio: 2:1, position: camera left, gentle lift on negative space,
soft, glowing, controlled,
premium saas advertising, high-end technology art direction,
[调色: 冷暖, contrast: medium, saturation: moderate, 关键发光色],
[调子词],
[叙事句],
[情绪词],
clean uncluttered background, background does not compete with subject,
no embedded text, no headlines, no logos, no watermark
```

## 填写要点

- **图内不渲染文字** —— 标题由网页 HTML 叠加，所以负面必须 `no embedded text,
  no headlines`，留白侧保持干净（`left half kept clean`）。
- 留白方向和网页布局对齐：标题在左 → 主体在右；标题在右则镜像。
- 加 `subtle glow / gradient background` 一类词给叠加文字提供低对比区域。
- 输出用 `banner` preset（1024×576 → 2048×1152 成图）正对网页 hero。

## 示例（完整可直接提交）

```text
title: Data Platform Hero, A premium website hero image for an ai data analytics platform., premium, ai-native, futuristic, minimal, editorial, abstract dark tech environment with soft depth gradient, faint grid lines receding into darkness, floating translucent glass panels with soft data visualizations, deep navy, slate blue, luminous cyan accent, subject, a levitating cluster of translucent glass panels forming an abstract data constellation, panels catching light along their edges, thin light threads connecting nodes, one brighter focal node at center, subject positioned on the right half, left half kept clean with at least 40 percent negative space for website headline, reading path from background glow through light threads to the central node, full_frame, 50mm, f/4.0, ISO 100, shutter speed: 1/125, horizontal hero composition (16:9), eye-level, balanced asymmetry, medium with soft depth falloff, Soft Cinematic Lighting, large diffused source from behind and above subject, position: behind and camera right, intensity: soft with subtle glow, dark bounce fill, ratio: 2:1, position: camera left, gentle lift across negative space, soft, glowing, controlled, premium saas advertising, high-end technology art direction, cool bias, contrast: medium, smooth transitions, saturation: moderate, luminous cyan highlights restrained, calm and futuristic, quietly powerful, Data becomes architecture, quietly lighting the way forward., clarity and momentum, engineered calm, clean uncluttered background, background does not compete with subject, no embedded text, no headlines, no logos, no watermark
```
