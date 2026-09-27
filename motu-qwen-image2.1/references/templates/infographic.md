# 信息图 / 流程图 — infographic

**何时用**：流程图、步骤图、概念科普图、Slide 配图。**先读警告**：结构准确性
要求高的图（精确节点连线、大量数据标签）不应完全依赖生图——推荐「AI 生成视觉
素材 + HTML/SVG 生成结构」组合。仍用生图时，本模板 + Qwen 文字渲染能把步骤
标题/短说明写对。

## 填充清单

| 字段 | 设计要点 |
|---|---|
| 主题 | 什么流程/概念 |
| 结构 | 从左到右 STEP 1 → 2 → 3 → 4（固定节点数，勿多） |
| 节点内容 | 每步：标题 + 一句说明 + 图标——逐字引用 |
| 连接关系 | 清晰箭头、从左向右、节点间不交叉 |
| 视觉 | professional infographic、clean vector illustration、统一图标风格 |
| 层级 | clear hierarchy、minimal background |
| 文字 | 严格按提供文本；不改序、不加节点、不删节点 |
| 禁止 | 乱码、错字、额外节点、箭头交叉、装饰干扰 |

## Qwen 散文骨架

```text
[Medium statement]. A professional infographic showing [topic] as a left-to-right process of exactly [N] steps.
Step one, titled "[EXACT TEXT]", shows [meaning] with an icon of [icon]; step two, titled "[EXACT TEXT]", shows [meaning] with an icon of [icon]; step three, titled "[EXACT TEXT]", shows [meaning]; step four, titled "[EXACT TEXT]", shows [meaning].
Clean directional arrows connect the steps from left to right with no crossing lines, each node a rounded card with its short description line rendered exactly as written: "[EXACT TEXT]".
The visual style is clean flat vector illustration with a consistent icon family, clear typographic hierarchy and a minimal background.
The palette uses [primary], [secondary] and one [accent] for the arrows.
Absolutely no extra steps, no missing steps, no reordered text, no garbled characters, no misspelling, no crossing connectors, no decorative clutter, no watermark.
```

## 填写要点

- **节点数 ≤ 4–5**：每多一个节点，文字与连线错误率显著上升。更多步骤 → 拆两
  张图或改用 HTML/SVG。
- 每步标题逐字引用；说明行短（≤ 10 字中文 / ≤ 6 词英文）。数字步骤用
  `step one/two` 写死顺序，负面排 `no reordered text`。
- 箭头方向显式声明 `from left to right with no crossing lines`。
- 交付要求像素级结构（真实流程图、数据图）→ 果断转 HTML/SVG；生图版当草稿。

## 示例（完整可直接提交）

```text
A professional infographic showing the cold brew coffee process as a left-to-right process of exactly four steps. Step one, titled "研磨", shows coarse-ground beans with an icon of a grinder; step two, titled "冷水浸泡", shows a jar steeping in water with a clock icon; step three, titled "过滤", shows a fine mesh strainer with a filter icon; step four, titled "加冰享用", shows a tall glass with ice. Clean directional arrows connect the four steps from left to right with no crossing lines, each node a rounded card with its short description line rendered exactly as written: "粗研磨 · 12 小时". The visual style is clean flat vector illustration with a consistent line-icon family, clear typographic hierarchy and a minimal warm-white background. The palette uses soft brown, cream and one amber accent for the arrows. Absolutely no extra steps, no missing steps, no reordered text, no garbled characters, no misspelling, no crossing connectors, no decorative clutter, no watermark.
```
