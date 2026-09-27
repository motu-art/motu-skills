# 汽车 / 工业机械 — automotive

**何时用**：汽车整车、零部件（轴承/轮毂/卡钳）、工业设备、五金工具、精密
机械件。核心是「精密金属质感 + 真实机械结构」。消费电子白底图用
[ecommerce.md](ecommerce.md)。

## 填充清单

| 字段 | 必答 |
|---|---|
| 部件 | 名称；结构逐个列（外圈/内圈/滚珠/密封/法兰/螺栓孔…） |
| 材料 | 高精度金属；机加工表面、精细倒角、真实金属反射 |
| 状态 | 单独展示 / 安装在整车上 / 拆解爆炸图 |
| 场景 | 高级工业影棚、深色工业背景 |
| 构图 | 主体占 60–80%，完整、结构清晰 |
| 光线 | 硬轮廓光 + 柔补光；可控金属反射；戏剧工业光 |
| 相机 | 85mm 微距产品摄影、锐焦、高微观细节 |
| 风格 | premium automotive advertising、工程精密感、工业奢华 |
| 禁止 | 错误机械结构、多余零件、不可能的装配、塑料金属感、变形 |

## Qwen 散文骨架

```text
[Medium statement]. Premium industrial product photograph of [part name], shown [standalone / installed on ... / in exploded view].
The mechanical structure must be accurate and complete: [structure 1], [structure 2], [structure 3], [structure 4], with true assembly relationships.
Machined metal reads true: [high-precision steel], polished [surfaces], fine chamfers, real metallic reflections with no plasticky sheen.
The part occupies [60–80] percent of the frame, fully visible with clear structure, against a dark industrial studio background.
Light comes from [a hard rim light from behind left] balanced by [a soft fill from the front], the reflections controlled along the machined edges, creating dramatic industrial contrast that traces the geometry.
Shot on an 85mm macro product lens, sharp focus with high micro-detail and realistic metal texture.
Premium automotive advertising style with engineering precision and industrial luxury.
Absolutely no incorrect mechanical structure, no extra parts, no impossible assembly, no plasticky metal, no warped geometry, no watermark.
```

## 填写要点

- 机械结构句决定成败：每个部件点名 + 装配关系写明（`the inner race seated
  within the outer race, a single row of steel balls visible between them`）。
  模型不懂「轴承」默认长什么样，全靠这句。
- 金属质感三板斧：`machined surface texture` + `fine chamfers` +
  `controlled reflections`；负面锁 `no plasticky metal`。
- 硬轮廓光（hard rim light）勾勒金属边缘，正面柔补光保留细节——两光各一句。
- 整车外观 → 场景换成展台/公路，加车身漆面句（`deep layered metallic paint`）。

## 示例（完整可直接提交）

```text
Premium industrial product photograph of a precision wheel bearing assembly, shown standalone at a slight three-quarter angle. The mechanical structure must be accurate and complete: an outer race with a flanged edge, the inner race seated within it, a single row of polished steel balls visible between the raceways, a dark rubber seal on both faces, and six evenly spaced bolt holes on the flange, with true assembly relationships. Machined metal reads true: high-precision bearing steel, ground and polished raceways, fine chamfers on every edge, real metallic reflections with no plasticky sheen. The assembly occupies about seventy percent of the frame, fully visible with clear structure, against a dark charcoal industrial studio background with a subtle gradient. Light comes from a hard rim light from behind left balanced by a soft fill from the front, the reflections controlled along the machined edges, creating dramatic industrial contrast that traces the geometry. Shot on an 85mm macro product lens, sharp focus with high micro-detail and realistic metal texture. Premium automotive advertising style with engineering precision and industrial luxury. Absolutely no incorrect mechanical structure, no extra parts, no impossible assembly, no plasticky metal, no warped geometry, no watermark.
```
