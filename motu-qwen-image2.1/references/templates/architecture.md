# 建筑 / 室内设计 — architecture

**何时用**：客厅/办公室/酒店/餐厅/展厅/会议室等空间效果图、家装方案、建筑
外观。核心是「透视垂直 + 材质分区 + 空间关系明确」。无人场景概念图用
[scene.md](scene.md)。

## 填充清单

| 字段 | 必答 |
|---|---|
| 空间类型 | 客厅/办公室/酒店/餐厅/展厅/会议室 |
| 设计目标 | 高级/现代/温暖/未来/极简——落到材质与色彩上兑现 |
| 结构 | 空间比例；墙面/地面/天花各什么材料 |
| 家具 | 沙发/桌/椅/灯具/装饰逐个写 |
| 材质 | 木材/石材/玻璃/金属；纹理真实、材质间视觉区分明显 |
| 色彩 | 主色/辅色/点缀色 |
| 灯光 | 自然光从窗户哪个方向进 + 吊灯/壁灯/灯带；柔和 |
| 空间关系 | 入口在哪、主家具在哪、窗在哪、视觉焦点在哪 |
| 相机 | 建筑摄影、广角、平视、垂直线笔直、构图平衡 |
| 禁止 | 透视错误、弯曲墙壁、重复家具、漂浮家具、不合理结构 |

## Qwen 散文骨架

```text
[Medium statement]. Architectural interior photograph of a [space type], designed as a [design goal] space with [spatial proportion statement].
The room is enclosed by [wall material] walls, a [floor material] floor and a [ceiling material] ceiling, the materials distinct in texture and tone.
[Furniture inventory: each piece with placement].
Natural light enters from [window position], joined by [pendant light / floor lamp / linear LED strip] for layered evening warmth.
The entry sits [where], the main furniture anchors [where], the windows run along [which side], and the visual focal point is [feature].
Shot in professional architectural photography style with a wide-angle lens at eye level, straight vertical lines, balanced composition and realistic perspective.
The palette is [primary] with [secondary] and [accent] details, the mood [calm / refined / welcoming].
Absolutely no warped perspective, no bent walls, no duplicated furniture, no floating objects, no impossible structure, no text, no watermark.
```

## 填写要点

- 「设计目标」是形容词（高级/温暖），必须翻译成材质与色彩事实：
  高级 = 石材 + 胡桃木 + 金属细节；温暖 = 原木 + 羊毛织物 + 暖白灯带。
- 空间关系四连（入口/主家具/窗/焦点）各写一次——这是这个模板区别于 scene
  的地方：布局可被读出来。
- 垂直线笔直（`straight vertical lines`）+ 平视（`eye level`）锁住建筑透视；
  负面 `no warped perspective` 兜底。
- 效果图有真人使用场景时按 [people-scene.md](people-scene.md) 加人物句。

## 示例（完整可直接提交）

```text
Architectural interior photograph of a double-height living room, designed as a warm minimalist space with an open plan flowing toward a glass wall. The room is enclosed by warm white limewash walls, a wide-plange oak floor laid in a herringbone pattern and a pale spruce slatted ceiling, the materials distinct in texture and tone. A low boucle sofa in oatmeal anchors the center on a muted terracotta rug, paired with a travertine coffee table, a curved floor lamp with a linen shade in the corner, and a single sculptural armchair near the window. Natural light enters from the full-height glazing on the south side, joined by a warm linear LED strip washing the ceiling for layered evening light. The entry sits behind a slim oak screen on the left, the windows run along the entire right wall, and the visual focal point is a freestanding black steel fireplace set into the far wall. Shot in professional architectural photography style with a wide-angle lens at eye level, straight vertical lines, balanced composition and realistic perspective. The palette is warm white and oak with a terracotta accent, the mood calm, refined and livable. Absolutely no warped perspective, no bent walls, no duplicated furniture, no floating objects, no impossible structure, no text, no watermark.
```
