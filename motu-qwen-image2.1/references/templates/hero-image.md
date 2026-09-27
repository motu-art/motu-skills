# 网站 Hero Image — hero-image

**何时用**：SaaS/AI 产品官网首屏图、落地页头图、产品宣传视觉。核心约束是
**大留白给网站标题**，主体偏侧。适合 16:9 横幅。

## 填充清单

| 字段 | 设计要点 |
|---|---|
| 用途 | Website hero image（决定 16:9 + 留白） |
| 产品 | 什么产品；一句话价值（视觉要隐喻它） |
| 核心概念 | 用什么视觉隐喻表达产品价值 |
| 主体 | 人物/产品/UI 截图感/抽象物体 |
| 场景 | 什么环境/背景 |
| 构图 | 主体位于右侧；**左侧 ≥40% 干净留白**给网站标题 |
| 视觉动线 | 背景 → 产品 → 核心主体 |
| 风格 | premium SaaS / AI-native / futuristic / minimal / editorial |
| 光线 | 柔和电影感光、微妙辉光、可控对比 |
| 背景 | 简洁、不抢主体 |
| 禁止 | 文字（标题是网站叠上去的！）、水印、复杂背景 |

## Qwen 散文骨架

```text
[Task statement]. A website hero image for [product], expressing [one-line product value] through [visual metaphor].
[Core subject: what it is, rendered how, with what materials and detail].
The subject sits in the right half of the frame, while the left forty percent stays clean and uncluttered, reserved for a website headline to be overlaid later.
[Scene around it: environment, depth, supporting elements kept minimal].
The visual flow leads the eye from the calm background through [supporting element] to the subject.
Soft cinematic lighting with a subtle glow around the subject and controlled contrast keeps the composition airy.
[Palette: primary, secondary, accent], premium SaaS aesthetic with AI-native futuristic minimalism and editorial polish.
High-end technology advertising art direction in a 16:9 website hero composition with large negative space.
Absolutely no text, no typography, no letters, no words, no numbers, no logos, no watermark, no busy background, no people unless specified.
```

## 填写要点

- **默认无文字**：hero 图的文字是网站 HTML 叠加的，prompt 里出现任何文字要求
  都是错的——负面句必须排全部 text。
- 「左侧 40% 留白」是本模板的命门句，漏写则主体居中、网站标题没地方放。
- 抽象隐喻（数据流、神经网络光丝、几何云）比产品截图拼贴更稳、更高档。
- 请求 2048×1152（banner preset）获得 16:9 且细节充足。

## 示例（完整可直接提交）

```text
A website hero image for an AI knowledge-base product, expressing the idea of scattered documents converging into one clear insight. A luminous sphere of thin flowing light-threads hovers in the right half of the frame, hundreds of delicate strands sweeping in from the edges and weaving into its coherent glowing core, rendered with fine glass-like refraction and soft particle depth. The subject sits in the right half of the frame, while the left forty percent stays clean and uncluttered, reserved for a website headline to be overlaid later. Around it, a deep midnight-blue gradient environment falls softly out of focus, with only a few faint floating sheets of light suggesting documents dissolving into the stream. The visual flow leads the eye from the calm background through the converging strands to the sphere. Soft cinematic lighting with a subtle glow around the subject and controlled contrast keeps the composition airy. The palette holds deep indigo and soft cyan with a warm white accent at the sphere's core, premium SaaS aesthetic with AI-native futuristic minimalism and editorial polish. High-end technology advertising art direction in a 16:9 website hero composition with large negative space. Absolutely no text, no typography, no letters, no words, no numbers, no logos, no watermark, no busy background, no people.
```
