# 艺术插画 — illustration

**何时用**：编辑插画（文章/博客配图）、书籍插图、概念艺术、绘本画面、品牌
叙事插画。以**画面隐喻与叙事**为主；商业排版文字为主的海报用
[poster.md](poster.md)，封面用 [bookcover.md](bookcover.md)。

## 填充清单

| 字段 | 设计要点 |
|---|---|
| 主题故事 | 画什么、讲什么一句话故事 |
| 视觉隐喻 | 用什么符号/意象承载主题（生长=植物、连接=桥/线） |
| 媒介 | 水彩/水粉/墨线/版画/扁平矢量/厚涂/铅笔淡彩/剪纸拼贴 |
| 画风锚点 | 2–3 个风格参照（mid-century editorial / 北欧扁平 / 日式绘本） |
| 主体 | 主体是什么、在做什么 |
| 构图动线 | 视线怎么走（左下→右上）；主体位置；留白 |
| 色调 | 主色/辅色/强调色 + 整体调性（温暖/忧郁/明快） |
| 纹理 | 纸纹/笔触/网点/颗粒——插画的「手感」来源 |
| 禁止 | 照片感、3D 渲染感、乱码文字、水印 |

## Z-Image 骨架

```text
title: [插画名], An editorial illustration of [主体与一句话故事].,
[4-6 氛围词: hopeful, wistful, playful …],
[视觉隐喻: the growing plant as compounding effort, …],
[主体: what it is doing, stylization 程度],
[辅助元素: symbolic object 1, symbolic object 2, 沿动线摆放],
[构图: subject lower-left, generous negative space upper-right, eye path from X to Y],
[媒介: soft gouache / ink linework / flat vector shapes],
[画风锚点: japanese picture-book, mid-century editorial],
[纹理: visible paper grain, delicate ink outlines, screen-tone dots],
[配色: 主色, 辅色, 强调色],
[调子词: warm / wistful / bright],
editorial illustration, hand-painted texture, clean shapes,
flat lighting with soft painted shadows,
no photorealism, no 3d render, no text, no watermark
```

## 填写要点

- 隐喻组是插画与照片描写的分水岭：先把主题翻译成一个可画的意象，再写画面。
- 媒介 + 纹理两组锁定「手感」：`visible paper grain, soft bleed edges` 比
  「水彩风」有效得多。
- 扁平/矢量风 → 明确 `flat shapes, no gradients`，否则模型自作主张加 3D 光泽。
- 需要留白给标题的插画（文章头图）→ 构图组写明留白方位，文字留给排版。

## 示例（完整可直接提交）

```text
title: The Patience Garden, An editorial illustration of a young woman planting a tiny tree that grows into a spiral of paper cranes., hopeful, quiet, wistful, warm, hand-tended effort blooming into something greater, a kneeling girl pressing soil around a sapling, the trunk rising in an S-curve into a spiral flock of cranes, scattered seeds and a dissolving clock along the curve as symbols of time and small steps, subject small at lower-left, generous warm negative space upper-right, eye path rising from her hands along the trunk to the brightest crane, soft gouache with ink linework, japanese picture-book warmth, mid-century editorial shapes, visible paper grain, delicate ink outlines, muted terracotta, sage green, cream, single coral accent on the brightest crane, warm and unhurried, editorial illustration, hand-painted texture, clean shapes, flat lighting with soft painted shadows, no photorealism, no 3d render, no text, no watermark
```
