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

## Qwen 散文骨架

```text
[Medium statement]. A product mockup photograph showing [design content] applied to [carrier].
The artwork reads exactly as designed: [visual description of the applied design, quoted text if any, spelled exactly].
The [carrier material and state: folded heavyweight cotton tee / matte kraft box standing open], the printed area following the fabric's folds and the box's perspective faithfully — no floating sticker look.
The scene is [simple setting: oak tabletop / concrete studio wall], kept quiet so the carrier leads.
Light comes from [soft window light / studio softbox direction], modeling the [carrier form: fabric folds / box edges] and giving the print realistic material response.
Shot on a 50mm lens from [eye level / a slight top-down angle], the carrier filling about [70] percent of the frame with crisp edges.
[Palette and mood].
Absolutely no floating sticker effect, no warped typography, no garbled text, no misspelling, no watermark, no cluttered scene.
```

## 填写要点

- 样机命门一句：`the printed area following the fabric's folds and the box's
  perspective faithfully — no floating sticker look`——贴图不随载体变形是
  最大破绽。
- 上身效果（模特穿）→ 载体描述改成模特 + 服装，姿势简单（`standing relaxed,
  arms at sides`），焦点在印花。
- 屏幕样机 → 写 `the interface glowing softly with realistic ambient reflection
  on the glass`，屏幕内容引号逐字。
- 印花文字 ≤ 6 词最稳；长文案上载体必错字。

## 示例（完整可直接提交）

```text
A product mockup photograph showing a minimal line-art mountain logo applied to a heavyweight cream cotton t-shirt. The artwork reads exactly as designed: a single-line mountain and sun mark about hand-width wide centered on the chest, with the small word "北岭" beneath it in clean sans-serif, spelled exactly. The folded-once heavyweight cotton tee lies slightly rumpled on a pale oak tabletop, the printed area following the fabric's soft folds faithfully with no floating sticker look. The scene is a quiet corner with a linen cloth and a sprig of eucalyptus far out of focus, kept quiet so the garment leads. Light comes from a large window camera left, modeling the fabric's folds and giving the print a soft matte material response. Shot on a 50mm lens from a slight top-down angle, the tee filling about seventy percent of the frame with crisp edges. The palette holds cream, pale oak and ink black, the mood clean and artisanal. Absolutely no floating sticker effect, no warped typography, no garbled text, no misspelling, no watermark, no cluttered scene.
```
