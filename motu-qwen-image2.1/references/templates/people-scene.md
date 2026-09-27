# 人物 + 场景组合 — people-scene

**何时用**：人物在具体环境里做事——实际项目里最常见的出图需求：生活方式图、
品牌故事片、纪实感画面、教程配图、广告情景。纯环境无人用
[scene.md](scene.md)，棚拍肖像用 [portrait.md](portrait.md)。

## 填充清单

| 字段 | 设计要点 |
|---|---|
| 人物身份 | 谁：年龄/性别/族裔/职业/气质 |
| 外观 | 脸型、发型发色、肤色、体态 |
| 服装 | 逐件 + 颜色材质；与环境是否呼应 |
| 动作 | 在做什么（可观察的行为，不写心理） |
| 表情视线 | 什么情绪、看向哪里 |
| 道具 | 与动作相关的关键物品 |
| 环境 | 在哪里、什么时间、什么天气 |
| 空间关系 | 人物距前景/背景的关系、在画面哪个位置 |
| 视觉分层 | 第一重点（人物）→ 第二（道具）→ 第三（环境） |
| 光线 | 主光源 + 方向 + 色温 + 阴影性质 |
| 构图 | 景别、视角、镜头、主体位置 |
| 一致性 | 跨图时脸/发型/服装/道具必须稳定 |

## Qwen 散文骨架

```text
[Medium statement]. [A lifestyle photograph of] a [identity] [doing what] in [environment] at [time].
[Appearance: face, hair, build] and [outfit: pieces, colors, materials that suit the scene].
[Action detail: hands, posture] with [expression and gaze direction], holding [key prop].
The setting is [specific place with foreground, midground and background elements], [weather or air quality].
[The person is positioned in the frame, spatial relation to fore/background, visual hierarchy: the figure first, the prop second, the environment third].
Light comes from [source and direction] at [color temperature], producing [shadow character] on [what it touches].
Shot from [shot size and camera angle] on a [lens] with [depth of field], focusing on [what].
[Style statement: visual language, palette of primary, secondary and accent colors, mood].
Absolutely no [unwanted elements for this scene], no text, no watermark.
```

## 填写要点

- 动作写「可观察的行为」：`pouring hot water in a slow spiral over coffee grounds`，
  不写 `专注地冲咖啡`（心理词画面落实不了，落到表情上）。
- 空间关系是这个模板的脊柱：人物在画面哪一侧、前景是什么、背景怎么虚，三句
  各答一次。
- 视觉分层倒着检查：先看环境会不会抢人物（背景太亮/太密 → 加 `quiet
  background` 类描述），再看道具是否可读。
- 跨图一致 → 把身份/外观/服装句提出来做 MASTER 块，见 [series.md](series.md)。

## 示例（完整可直接提交）

```text
A lifestyle photograph of a young ceramicist shaping a clay vase on a potter's wheel in her sunlit studio on a slow spring morning. She is a woman in her late twenties, East Asian, with an oval face, dark brown hair tied back loosely with a few strands escaping, light olive skin on slender arms dusted with pale clay, wearing a clay-stained oatmeal linen apron over a rolled-sleeve dark green shirt. She leans forward with both hands cupping the wet clay as the wheel spins, her gaze fixed on the rising wall of the vessel, with a quietly focused expression. The studio around her holds shelves of unglazed pots in the midground and a rain-flecked window with trailing plants in the background, the air soft with drifting dust in the light. She sits in the left third of the frame with the wheel before her, the figure reading first, the spinning vase second, and the warm cluttered studio third, the foreground anchored by a tray of throwing tools slightly out of focus. Light comes from the large window camera right at a cool morning temperature, producing long soft shadows across the workbench and a gentle glow along her arms. Shot as a medium shot from a slightly high three-quarter angle on a 50mm lens with shallow depth of field, focusing on her hands and the clay. Warm documentary lifestyle photography with a palette of oatmeal, clay gray and deep green, unhurried and tactile in mood. Absolutely no other people, no text, no watermark.
```
