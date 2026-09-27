# 样机 Mockup — mockup

**何时用**：把设计「落」到实物上：T 恤/卫衣印花上身、包装盒落地、海报上墙、
手机/笔记本屏幕界面、名片、手提袋、杯身。验证设计真实效果的标准工具。

## 填充清单

| 字段 | 设计要点 |
|---|---|
| 载体 | 什么物品（T恤/纸盒/马克杯/屏幕/墙面） |
| 设计内容 | 印花/界面/海报画面——引号逐字（若有文字）+ 视觉描述 |
| 载体材质 | 棉布纹理/牛皮纸/哑光陶瓷/玻璃屏反光 |
| 状态 | 平铺/悬挂/手持/置于场景中/模特上身 |
| 场景 | 简洁桌面/影棚/生活场景（不得抢载体） |
| 透视 | 贴合载体曲面/褶皱的透视变形要真实（这是样机的命门） |
| 光线 | 柔光 + 载体造型光；屏幕需要环境反光 |
| 相机 | 50mm、平视或微俯、载体占画面 60%+ |
| 禁止 | 贴图悬浮感（不随曲面变形）、乱码、错误文字、水印 |

## Z-Image 骨架

```text
title: [样机名], A product mockup photograph showing [设计内容] applied to [载体].,
[4-6 氛围词: clean, artisanal, tactile, honest …],
[载体: heavyweight cream cotton tee, folded once, slightly rumpled],
[设计: single-line mountain and sun mark, hand-width, centered on chest, word "北岭" beneath in clean sans-serif],
[透视: printed area following the fabric's soft folds faithfully, no floating sticker look],
[场景: pale oak tabletop, linen cloth and eucalyptus sprig far out of focus],
[配色: cream, pale oak, ink black],
[材质: heavyweight cotton with visible weave and soft folds],
full_frame, 50mm, f/4.0, ISO 100, shutter speed: 1/160,
slight top-down angle, [画幅], carrier filling seventy percent of the frame, crisp edges,
medium, fabric folds softly rendered,
Soft Window Light, large window, position: camera left, intensity: soft and even,
white bounce card, ratio: 2:1, gentle fill across the folds,
clean, tactile, honest,
product mockup photography, realistic material response,
[调色: warm neutrals, contrast: soft, saturation: moderate],
[调子词: clean, artisanal],
no floating sticker effect, no warped typography, no garbled text,
no misspelling, no watermark, no cluttered scene
```

## 填写要点

- 样机命门一组：`printed area following the fabric's folds and the box's
  perspective faithfully, no floating sticker look`——贴图不随载体变形是最大
  破绽。
- 上身效果（模特穿）→ 载体组改成模特 + 服装，姿势简单（`standing relaxed,
  arms at sides`），焦点在印花。
- 屏幕样机 → 写 `interface glowing softly with realistic ambient reflection on
  the glass`，屏幕内容引号逐字。
- 印花文字 ≤ 6 词最稳；长文案上载体必错字；中文长文字 → motu-qwen-image2-1。

## 示例（完整可直接提交）

```text
title: North Ridge Tee, A product mockup photograph showing a minimal line-art mountain logo applied to a heavyweight cream cotton t-shirt., clean, artisanal, tactile, honest, quiet, heavyweight cream cotton tee folded once and slightly rumpled, single-line mountain and sun mark about hand-width centered on the chest with the small word "北岭" beneath it in clean sans-serif, printed area following the fabric's soft folds faithfully with no floating sticker look, pale oak tabletop with a linen cloth and a sprig of eucalyptus far out of focus, cream, pale oak, ink black, heavyweight cotton with visible weave and soft folds, full_frame, 50mm, f/4.0, ISO 100, shutter speed: 1/160, slight top-down angle, vertical, carrier filling seventy percent of the frame, crisp edges, medium, fabric folds softly rendered, Soft Window Light, large window, position: camera left, intensity: soft and even, white bounce card, ratio: 2:1, gentle fill across the folds, clean, tactile, honest, product mockup photography, realistic material response, warm neutrals, contrast: soft, saturation: moderate, clean, artisanal, no floating sticker effect, no warped typography, no garbled text, no misspelling, no watermark, no cluttered scene
```
