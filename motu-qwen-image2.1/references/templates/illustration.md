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

## Qwen 散文骨架

```text
[Medium statement]. [An editorial illustration of] [subject/story one-liner], conveying [theme] through [visual metaphor].
[Main subject: what it is, what it does, rendered with what degree of stylization].
[Supporting elements: symbolic objects and their placement, how the eye travels through the composition].
The composition places [subject position] with [negative space where], leading the eye from [entry] toward [focal point].
Painted in [watercolor / gouache / ink linework / flat vector / textured brushwork] in the spirit of [style anchors], with [paper grain / visible brushstrokes / screen-tone texture].
The palette holds [primary], [secondary] and [accent], the mood [warm / wistful / bright / quiet].
Absolutely no photorealism, no 3D rendering, no text, no watermark.
```

## 填写要点

- 隐喻句是插画与照片描写的分水岭：先把主题翻译成一个可画的意象，再写画面。
- 媒介 + 纹理两句锁定「手感」：`visible paper grain and soft bleed edges` 比
  「水彩风」有效得多。
- 扁平/矢量风 → 明确 `flat shapes, no gradients or minimal gradients`，否则模型
  自作主张加 3D 光泽。
- 需要留白给标题的插画（文章头图）→ 写明留白方位，文字留给排版。

## 示例（完整可直接提交）

```text
An editorial illustration of a young woman planting a tiny tree that grows into a swirling network of glowing paper cranes, conveying the theme of small consistent efforts compounding into something beautiful. The woman kneels at the lower left in simple silhouette-like form, pressing soil around the sapling with both hands, while the trunk rises in a gentle S-curve and blossoms into a spiral flock of cranes filling the upper right. Supporting elements scatter along the curve — scattered seeds, a watering can, a clock dissolving into leaves — guiding the eye from the girl's hands up along the trunk to the birds. The composition places the human figure small in the lower left with generous warm negative space around the crane spiral, leading the eye from her hands toward the brightest crane at the top. Painted in soft gouache with visible paper grain and delicate ink outlines, in the spirit of Japanese picture-book illustration mixed with mid-century editorial warmth. The palette holds muted terracotta, sage green and cream with a single coral accent on the brightest crane, the mood hopeful and unhurried. Absolutely no photorealism, no 3D rendering, no text, no watermark.
```
