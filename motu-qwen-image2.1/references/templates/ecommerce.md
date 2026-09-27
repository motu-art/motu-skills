# 电商主图 — ecommerce

**何时用**：电商平台主图、白底图、详情页首图、上架合规图。要求纯白背景 +
产品完整 + 平台友好。有场景感的生活方式图用 [product.md](product.md)。

## 填充清单

| 字段 | 设计要点 |
|---|---|
| 产品 | 是什么；关键部件逐个列 |
| 占比 | 主体占画面 70–85%，视觉中心明确 |
| 背景 | 纯白、干净、无纹理无装饰 |
| 真实性 | 真实比例、边缘清晰、材质真实、结构准确 |
| 光线 | 均匀商业摄影光、柔和自然阴影 |
| 视角 | 正面或轻微 3/4；产品不裁切 |
| 禁止 | 人物、额外产品、复杂背景、道具、文字、水印、Logo 变形 |

## Qwen 散文骨架

```text
Commercial e-commerce hero product photograph of [product], the single subject fully visible and uncropped from [a straight-on / slight three-quarter] view.
The structure must be accurate: [key parts listed one by one].
The product is centered in the frame and fills about [75] percent of the image with a clear single visual focus, its edges crisp against the background.
The background is pure clean white with no texture, no props and no decoration.
Materials and proportions read true and realistic: [material sentence].
Lighting is even commercial studio light from the front with soft natural contact shadows grounding the product.
Commercial e-commerce product photography, sharp product edges, accurate geometry, high detail.
Absolutely no people, no additional products, no complex background, no props, no text, no watermark, no distorted logo.
```

## 填写要点

- 白底主图的「干净」要显式写三次：背景句、负面句、`no props`——任何一次省略
  都可能漂出杂物。
- 阴影只留 `soft natural contact shadows`（贴地接触影）；地面投影一重就显得脏。
- 有些平台禁 AI 感过强的锐化——保持 `natural` 类词，避免堆 `ultra sharp`。
- 需要多角度主图 → 逐张生成（每张只换视角句），参考 [series.md](series.md)。

## 示例（完整可直接提交）

```text
Commercial e-commerce hero product photograph of a minimalist white ceramic pour-over coffee dripper with its matching cup, the single subject fully visible and uncropped from a straight-on slight three-quarter view. The structure must be accurate: a cone-shaped ribbed dripper body, a small rectangular spout on the rim, a matching round saucer base, and a smooth matte glaze throughout. The dripper set is centered in the frame and fills about seventy-five percent of the image with a clear single visual focus, its edges crisp against the background. The background is pure clean white with no texture, no props and no decoration. Materials and proportions read true and realistic: warm white stoneware with a soft matte glaze and gently speckled clay visible at the rim. Lighting is even commercial studio light from the front with soft natural contact shadows grounding the set. Commercial e-commerce product photography, sharp product edges, accurate geometry, high detail. Absolutely no people, no additional products, no complex background, no props, no text, no watermark, no distorted logo.
```
