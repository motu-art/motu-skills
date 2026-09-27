# Logo / 品牌视觉 — logo

**何时用**：品牌 Logo、icon、标志、品牌字标。要求几何极简、小尺寸可用。
**双语 wordmark（品牌名含中文）是本 skill 的优势场景**；纯拉丁字母的字形
打磨 motu-ideogram4 更专。

## 填充清单

| 字段 | 设计要点 |
|---|---|
| 品牌 | 品牌名称（wordmark 文字，逐字） |
| 行业 | AI/科技/汽车/教育/金融/医疗 |
| 品牌属性 | 专业/可信/创新/未来/简单/高端 |
| 核心概念 | A + B 的结合（如 AI + Document） |
| 图形 | 简洁几何、强识别度、小尺寸可辨 |
| 结构 | 图形 Logo + Wordmark；图形左、名称右 |
| 颜色 | 主色/辅色（≤2 色 + 底色） |
| 应用 | 网站/App icon/favicon/名片——决定必须极简 |
| 禁止 | 复杂插画、3D、过度渐变、阴影、照片质感、多余装饰 |

## Qwen 散文骨架

```text
[Task statement]. A minimal vector-style logo design for [brand name], a [industry] brand with [brand attributes] character.
The mark combines [concept A] with [concept B] in [one simple geometric idea], drawn with clean strokes that stay recognizable at favicon size.
The structure pairs the symbol on the left with the wordmark "[EXACT BRAND NAME]" on the right in [font style], spelled exactly as written.
The logo sits centered on [a plain white / deep navy] background with generous clear space.
The palette uses [primary color] with [secondary color], flat and restrained.
Minimal, geometric, modern, professional and scalable logo design.
Absolutely no 3D effects, no heavy gradients, no drop shadows, no photorealistic texture, no complex illustration, no extra decoration, no other text, no watermark.
```

## 填写要点

- 核心概念句决定创意质量：写「A 与 B 结合成什么几何形」，不写「要一个高级的
  Logo」。例：`combines a bear paw with a location pin into one rounded triangular mark`。
- Wordmark 逐字引用（中文品牌名也行），负面排 `no other text`——Logo 图里
  出现第二行字就废了。
- 平面化是硬约束：负面四连 `no 3D effects, no heavy gradients, no drop shadows,
  no photorealistic texture`。
- 生成的是位图；要真矢量需后期描摹。多方案 → 逐张换概念句生成后挑选。

## 示例（完整可直接提交）

```text
A minimal vector-style logo design for "云弧 CloudArc", a cloud computing brand with a professional and forward-looking character. The mark combines a rising arc with a stylized cloud silhouette in one continuous open curve suggesting momentum, drawn with clean uniform strokes that stay recognizable at favicon size. The structure pairs the symbol on the left with the wordmark "云弧 CloudArc" on the right in a modern geometric sans-serif with slightly wide spacing, spelled exactly as written. The logo sits centered on a plain white background with generous clear space around it. The palette uses deep indigo blue with a single teal accent stroke, flat and restrained. Minimal, geometric, modern, professional and scalable logo design. Absolutely no 3D effects, no heavy gradients, no drop shadows, no photorealistic texture, no complex illustration, no extra decoration, no other text, no watermark.
```
