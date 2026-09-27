# 信息图 / 流程图 — infographic

**何时用**：流程说明图、步骤图、概念示意图。
**重要**：这是唯一一个「结构准确性要求超过画面美感」的类型 —— 生图模型不擅长
严格几何 + 精确文字。**生产环境推荐：AI 生成视觉素材（图标/插画/背景），HTML/SVG
负责结构和文字**，不要让生图同时管两者。
仍要用生图时，按本模板把结构和文字约束到最严。

## 填充清单

| 字段 | 必答 |
|---|---|
| 主题 | 什么主题 |
| 结构 | 从左到右 STEP 1 → 2 → 3 → 4（方向显式） |
| 节点 | 每步：标题 + 说明 + 图标 |
| 连接关系 | 清晰箭头、**从左向右**、节点间不交叉 |
| 视觉 | professional infographic、clean vector illustration、统一图标风格 |
| 文字 | 严格按提供文本；不改顺序、不加节点、不删节点 |

## Z-Image 骨架

```text
title: [主题] Infographic, A professional vector infographic explaining [主题] in [N] steps.,
clean, professional, instructional, flat, modern,
plain very light background with generous margins,
[配色: 主色, 辅色, 交替节点色],
[结构组: horizontal flow from left to right, exactly [N] steps connected by clean arrows pointing right, no crossing connectors],
[节点组: step 1 titled "[逐字]" with [图标] icon, step 2 titled "[逐字]" with [图标] icon, …],
[图标组: consistent flat line icon style, uniform stroke weight, same size in every step],
[层级组: numbered badges above titles, one short caption line below each title],
horizontal layout, all steps fully visible with equal spacing, centered,
flat vector illustration, Even Flat Lighting, no shadows, intensity: uniform,
none, flat graphic only,
clean, flat, orderly,
professional infographic, clean vector illustration, consistent icon style,
[调色: 高对比文字, contrast: high, saturation: restrained],
clear and orderly,
[叙事句],
[情绪词],
exactly [N] steps in the quoted order, arrows strictly left to right,
no crossing lines, no added or missing steps, no misspelled words,
no garbled text, no watermark
```

## 填写要点

- 步骤数和顺序显式写死（`exactly 4 steps in the quoted order`），负面双保险。
- 每步文字极短（标题 2–3 词 + 一行说明），越短越不容易乱码。
- 图标风格统一是观感关键：`consistent flat line icon style, uniform stroke weight`。
- 步骤超过 4 步或文字较长 → 放弃生图，改 HTML/SVG 制作。

## 示例（完整可直接提交）

```text
title: Coffee Brewing Infographic, A professional vector infographic explaining pour-over coffee brewing in 4 steps., clean, professional, instructional, flat, modern, plain very light warm background with generous margins, cream, walnut brown, sage green accent, horizontal flow from left to right, exactly 4 steps connected by clean arrows pointing right, no crossing connectors, step 1 titled "GRIND" with coffee grinder icon, step 2 titled "BLOOM" with water drip icon, step 3 titled "POUR" with spiral pour icon, step 4 titled "ENJOY" with cup icon, each step with one short caption line below the title, numbered badges above titles, consistent flat line icon style, uniform stroke weight, same size in every step, horizontal layout, all steps fully visible with equal spacing, centered, flat vector illustration, Even Flat Lighting, no shadows, intensity: uniform, none, flat graphic only, clean, flat, orderly, professional infographic, clean vector illustration, consistent icon style, warm neutral, contrast: high, saturation: restrained, clear and orderly, Four small steps between beans and a good cup., simplicity and craft, morning clarity, exactly 4 steps in the quoted order, arrows strictly left to right, no crossing lines, no added or missing steps, no misspelled words, no garbled text, no watermark
```
