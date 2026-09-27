# 产品摄影 — product

**何时用**：消费电子、工业品、SaaS 虚拟产品宣传、包装设计、家具器物。要求
结构准确 + 商业影棚光。白底电商主图用 [ecommerce.md](ecommerce.md)，汽车
零部件/机械用 [automotive.md](automotive.md)。

## 填充清单

| 字段 | 设计要点 |
|---|---|
| 产品 | 是什么、名称/型号 |
| 结构 | 逐个列出必须准确保留的部件/按钮/接口/Logo 位 |
| 状态 | 静止/使用中/悬浮/展开 |
| 摆放 | 放在什么上；主体占画面比例（~60%） |
| 视角 | 正面/45 度/侧面/俯视；产品完整可见 |
| 背景 | 纯白/浅灰/深色/品牌色；极简无异物 |
| 光线 | 柔光箱 + 可控影棚光；柔和反射、干净高光、真实阴影 |
| 材质 | 金属/玻璃/塑料/皮革/木材；真实反射与纹理 |
| 构图 | 视觉中心；留出哪一侧空白给广告文案 |
| 相机 | 商业产品摄影、50/85mm、锐利对焦、高动态范围 |
| 禁止 | 变形、错误结构、多余零件、漂浮阴影、错误 Logo、乱码 |

## Qwen 散文骨架

```text
[Medium statement]. Commercial product photograph of [product], presented [state: floating at a slight angle / resting on ...].
The product's structure must be rendered accurately: [structure 1], [structure 2], [button], [port], [logo position], [distinctive shape].
It rests on [surface] against [background color and quality, minimal, free of unrelated objects], the product filling about [60] percent of the frame and fully visible from [front/45-degree/side/top] view.
Materials read true: [matte aluminum body with ...], [glass ...], with realistic reflections and fine surface texture.
Light comes from [a large softbox above left] with [a controlled fill from the right and a subtle gradient on the background], producing [soft reflections, clean highlights and a realistic grounded shadow].
The composition centers the product in the visual middle, leaving [the left third / generous space above] clean for advertising copy.
Commercial product photography on a 50mm lens with sharp focus and high dynamic range, premium advertising quality with precise geometry.
Absolutely no distorted structure, no extra parts, no floating shadows, no incorrect logo, no garbled text, no duplicate products, no cluttered background, no watermark.
```

## 填写要点

- 结构句是这个模板的命脉：把必须保留的部件逐个写进一句（`a circular brushed
  dial on top, two physical buttons on the right edge, a USB-C port at the bottom`）。
  写了才保得住，漏了模型自由发挥。
- 「留白给文案」要写明方向和比例——这是设计交付物时最常被漏掉的一句。
- 悬浮展示 → `floating at a slight three-quarter angle with a soft shadow beneath`，
  并在负面里排除 `floating shadows` 之外的多余影子。
- 材质反射各写一句金属/玻璃；塑料感是最大翻车点，负面加 `no plasticky metal`。

## 示例（完整可直接提交）

```text
Commercial product photograph of over-ear wireless headphones in deep graphite, presented resting at a slight angle on a pale travertine pedestal. The product's structure must be rendered accurately: two oval ear cups with quilted leather pads, a single curved aluminum headband with engraved brand mark on the left hinge, a small multifunction button on the right ear cup, and a subtle LED dot at its base. It rests on the stone pedestal against a warm light-gray seamless studio background free of unrelated objects, the headphones filling about sixty percent of the frame and fully visible from a three-quarter front view. Materials read true: anodized aluminum with soft satin reflections on the headband, fine-stitched leather with visible grain on the ear pads, and a matte polymer body with a gentle sheen. Light comes from a large softbox above left with a controlled fill from the right and a subtle gradient across the background, producing soft reflections, clean highlights and a realistic grounded shadow beneath the pedestal. The composition centers the headphones in the visual middle, leaving the upper third clean for advertising copy. Commercial product photography on a 50mm lens with sharp focus and high dynamic range, premium advertising quality with precise geometry. Absolutely no distorted structure, no extra parts, no floating shadows, no incorrect logo, no garbled text, no duplicate products, no cluttered background, no watermark.
```
