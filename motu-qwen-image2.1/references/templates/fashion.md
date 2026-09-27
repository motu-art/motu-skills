# 时尚编辑大片 — fashion

**何时用**：服装品牌 lookbook、杂志编辑大片、造型展示、时尚街拍。**服装与造型
是主角，人是衣架**——这是与 [portrait.md](portrait.md)（人本身是主角）的分界。
全身、姿势感、场景叙事。

## 填充清单

| 字段 | 设计要点 |
|---|---|
| 服装 | 逐件：品类 + 面料 + 廓形 + 颜色（oversized 廓形是关键信息） |
| 造型 | 妆容 + 发型（湿发/高马尾/羊毛卷）+ 配饰 |
| 模特气质 | 年龄段、身形、族裔、台风（清冷/张扬/慵懒） |
| 姿势 | editorial pose：靠墙/行进中转身/坐姿伸展——写关节角度 |
| 表情视线 | 直视镜头/侧脸望远/闭眼仰头 |
| 场景 | 秀场后台/街头/极简影棚/废弃工厂/海边 |
| 相机 | 80mm 中画幅感、全身、平视或低机位拉比例 |
| 灯光 | 硬闪（时尚感）/大柔光（高级感）/自然光（街拍） |
| 色彩 | 服装色 × 环境色的关系（撞色/同色系） |
| 禁止 | 畸形手/多指、假人感塑料皮肤、文字、水印 |

## Qwen 散文骨架

```text
[Medium statement]. [A fashion editorial photograph of] a [model temperament] model in [outfit headline], shot in [setting].
The outfit is the story: [piece by piece with fabric, silhouette and color].
[Styling: hair, makeup, accessories, nails — the details that sell the look].
She/He poses [editorial pose with joint angles], [expression and gaze direction].
The setting is [specific environment and how it frames the outfit].
Light comes from [hard flash / large softbox / natural source and direction], producing [crisp shadows on the wall / luminous skin / moody falloff].
Shot on a medium-format look with an 80mm lens, full-body framing at [eye level / a slightly low angle lengthening the figure], the outfit sharp against [background treatment].
The palette sets [garment colors] against [environment colors], the mood [editorial attitude].
Absolutely no deformed hands, no extra fingers, no plastic skin, no text, no watermark.
```

## 填写要点

- 服装句「面料 + 廓形 + 颜色」三件缺一不可：`an oversized raw-denim jacket with
  dropped shoulders` 里的廓形词决定整张图的时尚度。
- 姿势写关节不写氛围：`leaning against the wall with one knee bent and chin
  lifted`，比 `很酷的姿势` 可执行一万倍。
- 硬闪 + 影子 = 时尚感（`hard flash casting a crisp shadow on the colored wall`）；
  高级感 = 大柔光 + 低饱和；街拍 = 自然光 + 环境。
- 低机位（`a slightly low angle lengthening the figure`）是编辑大片常用比例技巧。

## 示例（完整可直接提交）

```text
A fashion editorial photograph of a statuesque model in a sculptural autumn look, shot against a raw concrete wall in an empty parking structure. The outfit is the story: an oversized cognac leather trench coat with a dropped shoulder line and belt cinched tight, over a fine-knit chocolate turtleneck and wide-leg charcoal wool trousers, with square-toe black boots. Her styling is a sleek wet-look slicked-back bun, clean skin with a bronze glossy lip, small gold hoop earrings, and bare minimal jewelry letting the coat lead. She strides mid-step toward the camera with one hand deep in her pocket and the other pulling the coat collar, chin slightly down with a level, unbothered gaze into the lens. The setting is bare painted concrete pillars and a yellow parking-line floor under diffused skylight, framing the warm leather against cool gray. Light comes from a hard flash camera left, producing a crisp full-length shadow on the wall behind her and clean specular highlights on the leather. Shot on a medium-format look with an 80mm lens, full-body framing at a slightly low angle lengthening the figure, the outfit sharp against the softly receding concrete. The palette sets cognac and chocolate against concrete gray with a yellow line accent, the mood quiet-luxury and assertive. Absolutely no deformed hands, no extra fingers, no plastic skin, no text, no watermark.
```
